#!/usr/bin/env bats

@test "the datadog-agent should be running" {
      [ "$(ps aux | grep datadog-agent)" ]
}

@test "datadog redis config is present" {
    [ -f "/etc/dd-agent/conf.d/redisdb.yaml" ]
}

@test "datadog mysql config is present" {
    [ -f "/etc/dd-agent/conf.d/mysql.yaml" ]
}
