"""

To test this, run 'sudo -u dd-agent dd-agent check system_ports'

When ready:
- place this file in /etc/dd-agent/checks.d/system_ports.py
- put the config file in /etc/dd-agent/conf.d/system_ports.yaml
- service datadog-agent restart
"""

import psutil

from heapq import nlargest
from operator import itemgetter

from checks import AgentCheck


class SystemPortsCheck(AgentCheck):
    SOURCE_TYPE_NAME = 'system_ports'

    def check(self, instance):
        connections = psutil.net_connections()
        port_counts = {}
        for connection in connections:
            _, _, _, local_dest, remote_dest, status, _ = connection
            local_ip, local_port = local_dest
            if remote_dest:
                remote_ip, remote_port = remote_dest
            port_counts[local_port] = port_counts.get(local_port, 0) + 1
            if remote_dest and (remote_ip == '127.0.0.1' or remote_ip == '::1'):
                port_counts[remote_port] = port_counts.get(remote_port, 0) + 1

        highest_used_ports = nlargest(5, port_counts.items(), key=itemgetter(1))

        for used_port in highest_used_ports:
            self.gauge('system.net.ipv4.ephemeral_ports', used_port[1], tags=('port:%s'%used_port[0],))
