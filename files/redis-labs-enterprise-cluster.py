"""
To test this, run:
'sudo -u dd-agent dd-agent check redis-labs-enterprise-cluster'

When ready:
- place this file in /etc/dd-agent/checks.d/redis-labs-enterprise-cluster.py
- put the config in /etc/dd-agent/conf.d/redis-labs-enterprise-cluster.yaml
- service datadog-agent restart
"""

import base64
import json
import ssl
import socket
import time
import urllib2

from checks import AgentCheck

GIG = 1024 * 1024 * 1024


class RedisLabsEnterpriseClusterCheck(AgentCheck):
    SOURCE_TYPE_NAME = 'rlec'
    SERVICE_CHECK = 'rlec.can_connect'

    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 9443

    stats_endpoints = [
        'bdbs',
        'nodes',
        'bdbs/stats/last',
        'shards/stats/last',
        'nodes/stats/last',
        'cluster/stats/last',
        # 'cluster/actions',
    ]

    def metric_name(self, metric):
        return self.normalize(metric.lower(), self.SOURCE_TYPE_NAME)

    def _get_raw_stats(self, host, port, username, password):
        data = {}
        for endpoint in self.stats_endpoints:
            url = 'https://%s:%s/v1/%s' % (host, port, endpoint)

            req = urllib2.Request(url)

            base64string = base64.encodestring('%s:%s' % (username, password))
            base64string = base64string[:-1]
            req.add_header("Authorization", "Basic %s" % base64string)

            context = ssl._create_unverified_context()
            response = urllib2.urlopen(req, context=context)

            data[endpoint] = json.loads(response.read())

        return data

    def gauge(self, metric, value, *args, **kwargs):
        metric = self.metric_name(metric)
        return super(RedisLabsEnterpriseClusterCheck, self).gauge(
            metric, value, *args, **kwargs
        )

    def _get_metrics_dbs(self, raw_stats):
        bdb_stats_map = raw_stats['bdbs/stats/last']
        for item in raw_stats['bdbs']:
            uid = item['uid']
            str_uid = str(uid)
            bdb_stats = bdb_stats_map[str_uid]

            name = item['name']

            tags = [
                'db_name:%s' % name
            ]

            mem_gigs = int(item['memory_size']) / GIG
            used_gigs = int(bdb_stats['used_memory']) / GIG

            self.gauge('db.total_size_in_gigs', mem_gigs, tags=tags)
            self.gauge('db.num_shards', item['shards_count'], tags=tags)
            self.gauge('db.read_hits', bdb_stats['read_hits'], tags=tags)
            self.gauge('db.read_misses', bdb_stats['read_misses'], tags=tags)
            self.gauge('db.write_hits', bdb_stats['write_hits'], tags=tags)
            self.gauge('db.write_misses', bdb_stats['write_misses'], tags=tags)
            self.gauge('db.num_connections', bdb_stats['conns'], tags=tags)
            self.gauge('db.num_keys', bdb_stats['no_of_keys'], tags=tags)
            self.gauge('db.bytes_added', bdb_stats['ingress_bytes'], tags=tags)
            self.gauge('db.bytes_read', bdb_stats['egress_bytes'], tags=tags)
            self.gauge('db.count_evicted', bdb_stats['evicted_objects'],
                       tags=tags)
            self.gauge('db.count_expired', bdb_stats['expired_objects'],
                       tags=tags)
            self.gauge('db.ops_per_sec',
                       bdb_stats['instantaneous_ops_per_sec'], tags=tags)
            self.gauge('db.used_memory_in_gigs', used_gigs, tags=tags)

    def _get_metrics_nodes(self, raw_stats):
        node_stats_map = raw_stats['nodes/stats/last']
        for node in raw_stats['nodes']:
            # Get the node ip.  Don't send these stats if it doesn't match
            # the node we're on.
            ip = node['addr']
            if ip != socket.gethostbyname(socket.gethostname()):
                continue

            uid = node['uid']
            node_stats = node_stats_map[str(uid)]

            tags = [
                'node_ip:%s' % ip,
                'node_uid:%s' % uid
            ]

            is_active = 1 if (node['status'] == 'active') else 0
            ephemeral_gigs = int(node_stats['ephemeral_storage_free']) / GIG
            persistent_gigs = int(node_stats['persistent_storage_free']) / GIG
            memory_gigs = int(node_stats['free_memory']) / GIG

            self.gauge('node.shard_count', node['shard_count'], tags=tags)
            self.gauge('node.active', is_active, tags=tags)
            self.gauge('node.connections', node_stats['conns'], tags=tags)
            self.gauge('node.aof_rewrites', node_stats['cur_aof_rewrites'],
                       tags=tags)
            self.gauge('node.ephemeral_free_space_gigs', ephemeral_gigs,
                       tags=tags)
            self.gauge('node.persistent_free_space_gigs', persistent_gigs,
                       tags=tags)
            self.gauge('node.free_memory_gigs', memory_gigs, tags=tags)
            self.gauge('node.requests', node_stats['total_req'], tags=tags)

    def _get_metrics_shards(self, raw_stats):
        """
        At this time it looks like this isn't useful info

        shards_stats_map = raw_stats['shards/stats/last']
        """

    def _get_metrics_cluster(self, raw_stats):
        stats = raw_stats['cluster/stats/last']

        tags = []

        ephemeral_gigs = int(stats['ephemeral_storage_free']) / GIG
        persistent_gigs = int(stats['persistent_storage_free']) / GIG
        memory_gigs = int(stats['free_memory']) / GIG

        self.gauge('cluster.connections', stats['conns'], tags=tags)
        self.gauge('cluster.ephemeral_free_space_gigs', ephemeral_gigs,
                   tags=tags)
        self.gauge('cluster.persistent_free_space_gigs', persistent_gigs,
                   tags=tags)
        self.gauge('cluster.free_memory_gigs', memory_gigs, tags=tags)
        self.gauge('cluster.requests', stats['total_req'], tags=tags)
        self.gauge('cluster.bytes_added', stats['ingress_bytes'], tags=tags)
        self.gauge('cluster.bytes_read', stats['egress_bytes'], tags=tags)
        self.gauge('cluster.cpu_idle', stats['cpu_idle'], tags=tags)

    def _get_metrics(self, host, port, username, password, tags):
        try:
            raw_stats = self._get_raw_stats(host, port, username, password)
        except Exception:
            self.service_check(self.SERVICE_CHECK, AgentCheck.CRITICAL)
            self.increment(self.metric_name('node.get_stats.failure'), 1, tags = [
                'host:%s' % host,
            ])

            raise

        # Send all stats
        self._get_metrics_dbs(raw_stats)
        self._get_metrics_nodes(raw_stats)
        self._get_metrics_shards(raw_stats)
        self._get_metrics_cluster(raw_stats)

        # Connection is ok.
        self.service_check(self.SERVICE_CHECK, AgentCheck.OK)

    # Called by datadog as the starting point for this check.
    def check(self, instance):
        host = instance.get('host', self.DEFAULT_HOST)
        port = int(instance.get('port', self.DEFAULT_PORT))
        username = instance['username']
        password = instance['password']

        tags = {}
        for item in instance.get('tags', []):
            k, v = item.split(":", 1)
            tags[k] = v

        self._get_metrics(host, port, username, password, tags)

