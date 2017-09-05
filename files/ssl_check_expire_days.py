# A rewrite of https://workshop.avatarnewyork.com/project/datadog-ssl-expires-check/
# I prefer to test the site itself instead of the ssl cert file

import time
import datetime
import subprocess
import sys
from checks import AgentCheck

class SSLCheckExpireDays(AgentCheck):
    def check(self, instance):
        metric = "ssl.expire_in_days"
        site = instance['site']
        p = subprocess.Popen("echo | openssl s_client -showcerts -servername " + site + " -connect " + site + ":443 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -f 2 -d\= | xargs -0 -I arg date -d arg \"+%s\"",stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output:
            output = output.rstrip("\n")
            d0 = int(time.time())
            d1 = int(output)
            delta = d1 - d0
            days= delta/24/60/60 # convert the timestamp to days
            tag="site:" + site # generate the tags
#            print "metric: " + str(metric) + ", tag: " + str(tag) + ", days: " + str(days)
            self.gauge(metric, int(days), tags=[tag])
        else:
            self.gauge(metric, -1, tags=[site])
