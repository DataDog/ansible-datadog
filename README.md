Ansible Datadog Role
========

Install and configure Datadog agent.

Currently only supports:
Base agent
Process checks

Requirements
------------

Ubuntu

Role Variables
--------------

- `datadog_api_key` - Your Datadog API key.
- `datadog_checks` - YAML configuration for agent checks to drop into `/etc/dd-agent/conf.d`.
- `datadog_config` - Settings to place in `/etc/dd-agent/datadog.conf`.
- `datadog_process_checks` - Array of process checks and options.

Dependencies
------------
None

Example Playbooks
-------------------------
```
- hosts: servers
  roles:
    - dustinbrown.datadog
  vars:
    datadog_api_key: "123456"
    datadog_config:
      api_key: "{{ datadog_api_key }}"
      dd_url: "{{ datadog_url }}"
      use_mount: "{{ datadog_use_mount }}"
      tags: "mytag0, mytag1"
    datadog_process_checks:
      - name: ssh
        search_string: ['ssh', 'sshd' ]
      - name: syslog
        search_string: ['rsyslog' ]
        cpu_check_interval: '0.2'
        exact_match: true
        ignore_denied_access: true
    datadog_checks:
      ssh_check:
        init_config:
        instances:
          - host: localhost
            port: 22
            username: root
            password: changeme
            sftp_check: True
            private_key_file:
            add_missing_keys: True
      nginx:
        init_config:
        instances:
          - nginx_status_url: http://example.com/nginx_status/
            tags:
              - instance:foo
          - nginx_status_url: http://example2.com:1234/nginx_status/
            tags:
              - instance:bar
```

```
- hosts: servers
  roles:
    - { role: dustinbrown.datadog, datadog_api_key: "mykey" }
```

License
-------

Apache2

Author Information
------------------

brian@akins.org

dustinjamesbrown@gmail.com --Forked from brian@akins.org
