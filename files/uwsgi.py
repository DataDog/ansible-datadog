"""

To test this, run 'sudo -u dd-agent dd-agent check uwsgi'

When ready:
- place this file in /etc/dd-agent/checks.d/uwsgi.py
- put the config file in /etc/dd-agent/conf.d/uwsgi.yaml
- service datadog-agent restart
"""

import hashlib
import glob
import json
import os
import socket
from stat import ST_CTIME
import time

from checks import AgentCheck


class UwsgiCheck(AgentCheck):
    SOURCE_TYPE_NAME = 'uwsgi'
    SERVICE_CHECK = 'uwsgi.can_connect'

    def metric_name(self, metric):
        return self.normalize(metric.lower(), self.SOURCE_TYPE_NAME)

    def gauge(self, metric, value, *args, **kwargs):
        metric = self.metric_name(metric)
        return super(UwsgiCheck, self).gauge(
            metric, value, *args, **kwargs
        )

    def histogram(self, metric, value, *args, **kwargs):
        metric = self.metric_name(metric)
        return super(UwsgiCheck, self).histogram(
            metric, value, *args, **kwargs
        )

    def _get_raw_stats(self):
        chosen_socket = None
        latest_ctime = 0
        files = glob.glob('/tmp/uwsgi_stats_*.socket')
        for fname in files:
            stats = os.stat(fname)

            if stats[ST_CTIME] > latest_ctime:
                latest_ctime = stats[ST_CTIME]
                chosen_socket = fname

        if not chosen_socket:
            raise RuntimeError("Cannot find uwsgi stats socket file")

        sock_obj = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock_obj.connect(chosen_socket)

        json_str = ''
        while True:
            data = sock_obj.recv(4096)
            if len(data) < 1:
                break
            json_str += data.decode('utf8')

        return json.loads(json_str)

    def _send_stats(self, data):
        self._send_stats_workers(data)

    def _send_stats_workers(self, data):
        code_dir = data['cwd']
        global_tags = [
            'code_dir:%s' % code_dir,
        ]

        self.gauge('listen_queue', data['listen_queue'], tags=global_tags)
        self.gauge('listen_queue_errors', data['listen_queue_errors'], tags=global_tags)

        for worker in data['workers']:
            worker_tags = [
                'worker_id:%s' % worker['id'],
            ]
            tags = worker_tags + global_tags

            self.gauge('worker.accepting', worker['accepting'], tags=tags)
            self.gauge('worker.status.%s' % worker['status'], 1, tags=tags)
            self.gauge('worker.running_time', worker['running_time'],
                       tags=tags)
            self.gauge('worker.data_transmitted', worker['tx'], tags=tags)
            self.gauge('worker.address_space', worker['vsz'], tags=tags)
            self.gauge('worker.rss_memory', worker['rss'], tags=tags)
            self.gauge('worker.respawn_count', worker['respawn_count'],
                       tags=tags)
            self.gauge('worker.exceptions_count', worker['exceptions'],
                       tags=tags)
            self.gauge('worker.harakiri_count', worker['harakiri_count'],
                       tags=tags)
            self.histogram('worker.avg_response_time_ms',
                           worker['avg_rt']/1000, tags=tags)

    def _get_metrics(self, aggregation_key):
        try:
            raw_stats = self._get_raw_stats()
        except Exception as e:
            self.service_check(self.SERVICE_CHECK, AgentCheck.CRITICAL)
            self.event({
                'timestamp': int(time.time()),
                'event_type': 'get_stats',
                'msg_title': 'Cannot get stats',
                'msg_text': str(e),
                'aggregation_key': aggregation_key
            })

            raise

        self._send_stats(raw_stats)

        # Connection is ok.
        self.service_check(self.SERVICE_CHECK, AgentCheck.OK)

    # Called by datadog as the starting point for this check.
    def check(self, instance):
        aggregation_key = hashlib.md5().hexdigest()
        self._get_metrics(aggregation_key)
