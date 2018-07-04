"""

To test this, run 'sudo -u dd-agent dd-agent check nutcracker'

When ready:
- place this file in /etc/dd-agent/checks.d/nutcracker.py
- put the config file in /etc/dd-agent/conf.d/nutcracker.yaml
- service datadog-agent restart
"""

import hashlib
import json
import md5
import os
import socket
import sys
import time
import uuid

from checks import AgentCheck


class NutcrackerCheck(AgentCheck):
    SOURCE_TYPE_NAME = 'nutcracker'
    SERVICE_CHECK = 'nutcracker.can_connect'

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 11211
    DEFAULT_STATS_PORT = 22222

    # Pool stats.  These descriptions are from 'nutcracker --describe-stats'
    POOL_STATS = [
        ['curr_connections', 'gauge', None],  # Number of current connections
        ['total_connections', 'rate', None],  # Running total connections made
        ['server_ejects', 'rate', None],  # times a backend server was ejected
        ['client_err', 'rate', None],  # errors on client connections
    ]

    # Server stats.  These descriptions are from 'nutcracker --describe-stats'
    SERVER_STATS = [
        ['server_eof', 'rate', None],  # eof on server connections
        ['server_err', 'rate', None],  # errors on server connections
        ['server_timedout', 'rate', 'timedout'],  # timeouts on server connections
        ['server_connections', 'gauge', 'connections'],  # active server connections
        ['requests', 'rate', None],  # requests
        ['request_bytes', 'rate', None],  # total request bytes
        ['responses', 'rate', None],  # responses
        ['response_bytes', 'rate', None],  # total response bytes
        ['in_queue', 'gauge', None],  # requests in incoming queue
        ['in_queue_bytes', 'gauge', None],  # current request bytes in incoming queue
        ['out_queue', 'gauge', None],  # requests in outgoing queue
        ['out_queue_bytes', 'gauge', None],  # current request bytes in outgoing queue
    ]

    def _get_raw_stats(self, host, stats_port):
        # Connect
        self.log.debug("Connecting to %s:%s", host, stats_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, stats_port))

        # Read
        file = s.makefile('r')
        data = file.readline();
        s.close()

        # Load
        return json.loads(data);

    def _send_datadog_stat(self, item, data, tag_map, prefix):
        # Break out the info
        stat_key, stat_type, override_name = item

        # Make sure we have a name
        if not override_name:
            override_name = stat_key

        # Add the prefix if appropriate.
        if prefix:
            override_name = prefix + "_" + override_name

        try:
            # Get the data, make sure it's there.
            stat_data = float(data.get(stat_key))
        except:
            # Hrm, not there.  Let it be zero.
            stat_data = 0

        # Make the datadog metric.
        metric = self.normalize(override_name.lower(), self.SOURCE_TYPE_NAME)

        tags = [k + ":" + v for k, v in tag_map.iteritems()]

        if stat_type == 'gauge':
            self.gauge(metric, stat_data, tags=tags)
            return

        if stat_type == 'rate':
            metric += "_rate"
            self.rate(metric, stat_data, tags=tags)
            return

        if stat_type == 'bool':
            self.gauge(metric, (1 if stat_data else 0), tags=tags)
            return

        raise Exception("Unknown datadog stat type '%s' for key '%s'" % (stat_type, stat_key))

    def _get_metrics(self, host, port, stats_port, tags, aggregation_key):
        try:
            raw_stats = self._get_raw_stats(host, stats_port)
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

        # pprint.pprint(raw_stats)

        # Get all the pool stats
        for pool_key, pool_data in raw_stats.iteritems():
            try:
                # Pools are not separated from the other keys, blarg.
                # Just check if it's a dict with one of the pool keys, if not then skip it.
                pool_data['client_connections']
            except:
                # Not there, it's not a pool.
                self.log.debug(pool_key + ": NOT A POOL");
                continue

            # Start the stat tags.
            tags['nutcracker_pool'] = pool_key

            # It's a pool.  Process all the non-server stats
            for item in self.POOL_STATS:
                self._send_datadog_stat(item, pool_data, tags, "pool")

            # Find all the servers.
            for server_key, server_data in pool_data.iteritems():
                try:
                    # Servers are not separated from the other keys, blarg.
                    # Just check if it's a dict with one of the server keys, if not then skip it.
                    server_data['in_queue_bytes']
                except:
                    # Not there, it's not a server.
                    self.log.debug(server_key + ": NOT A SERVER");
                    continue

                # Set the server in the tags.
                tags['nutcracker_pool_server'] = server_key

                # It's a server.  Send stats.
                for item in self.SERVER_STATS:
                    self._send_datadog_stat(item, server_data, tags, "server")

        # Connection is ok.
        self.service_check(self.SERVICE_CHECK, AgentCheck.OK)

    # Called by datadog as the starting point for this check.
    def check(self, instance):
        host = instance.get('host', self.DEFAULT_HOST)
        port = int(instance.get('port', self.DEFAULT_PORT))
        stats_port = int(instance.get('stats_port', self.DEFAULT_STATS_PORT))

        tags = {}
        for item in instance.get('tags', []):
            k, v = item.split(":", 1)
            tags[k] = v

        tags["host"] = host + ":" + str(port)

        aggregation_key = hashlib.md5(host + ":" + str(port)).hexdigest()

        self._get_metrics(host, port, stats_port, tags, aggregation_key)

