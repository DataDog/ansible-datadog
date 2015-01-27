Ansible Datadog Role
========

Install and configure datadog agent.

Currently only supports:
Base agent
Process checks

Requirements
------------

Ubuntu

Role Variables
--------------

- `datadog_api_key` - your datadog API key
- `datadog_process_checks` - Array of process checks and options

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
    datadog_process_checks:
      - name: ssh
        search_string: ['ssh', 'sshd' ]
      - name: syslog
        search_string: ['rsyslog' ]
        cpu_check_interval: '0.2'
        exact_match: true
        ignore_denied_access: true
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
