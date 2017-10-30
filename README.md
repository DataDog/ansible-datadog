Ansible Datadog Role
========
[![Ansible Galaxy](http://img.shields.io/badge/galaxy-Datadog.datadog-660198.svg)](https://galaxy.ansible.com/Datadog/datadog/)
[![Build Status](https://travis-ci.org/DataDog/ansible-datadog.svg?branch=master)](https://travis-ci.org/DataDog/ansible-datadog)

Install and configure Datadog base agent & checks.

Supports most Debian and RHEL-based Linux distributions.

Installation
------------

```
ansible-galaxy install Datadog.datadog
```

Role Variables
--------------

- `datadog_api_key` - Your Datadog API key.
- `datadog_agent_version` - The pinned version of the Agent to install (optional, but highly recommended)
  Examples: `1:5.12.3-1` on apt-based platforms, `5.12.3-1` on yum-based platforms
- `datadog_checks` - YAML configuration for agent checks to drop into `/etc/dd-agent/conf.d`.
- `datadog_config` - Settings to place in the `/etc/dd-agent/datadog.conf` INI file that go under the `[Main]` section.
- `datadog_config_ex` - Extra INI sections to go in `/etc/dd-agent/datadog.conf` (optional).
- `datadog_process_checks` - Array of process checks and options (DEPRECATED: use `process` under
`datadog_checks` instead)
- `datadog_apt_repo` - Override default Datadog `apt` repository
- `datadog_apt_key_url` - Override default url to Datadog `apt` key
- `datadog_apt_key_url_new` - Override default url to the new Datadog `apt` key (in the near future the `apt` repo will have to be checked against this new key instead of the current key)
- `datadog_agent_allow_downgrade` - Set to `yes` to allow agent downgrades on apt-based platforms (use with caution, see `defaults/main.yml` for details)

Agent 6 (beta)
--------------

This role includes experimental support of the beta versions of Datadog Agent 6.0 on apt-based platforms.
See below for usage. General information on the Datadog Agent 6 is available in the
[datadog-agent](https://github.com/DataDog/datadog-agent/) repo.

To upgrade or install agent6, you need to:

- set `datadog_agent6` to true
- either set `datadog_agent_version` to an existing agent6 version
  (recommended) or leave it empty to always install the latest version.

To downgrade from agent6 to agent5, you need to:

- set `datadog_agent6` to false
- pin `datadog_agent_version` to an existing agent5 version
- set `datadog_agent_allow_downgrade` to yes

Variables:

- `datadog_agent6` - install an agent6 instead of agent5 (default to `false`)
- `datadog_agent6_apt_repo` - Override default Datadog `apt` repository for agent6

Dependencies
------------
None

Example Playbooks
-------------------------
```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes }  # On Ansible < 1.9, use `sudo: yes` instead of `become: yes`
  vars:
    datadog_api_key: "123456"
    datadog_agent_version: "1:5.12.3-1" # for apt-based platforms, use a `5.12.3-1` format on yum-based platforms
    datadog_config:
      tags: "mytag0, mytag1"
      log_level: INFO
      apm_enabled: "true" # has to be set as a string
    datadog_config_ex:
      trace.config:
        env: dev
      trace.concentrator:
        extra_aggregators: version
    datadog_checks:
      process:
        init_config:
        instances:
          - name: ssh
            search_string: ['ssh', 'sshd' ]
          - name: syslog
            search_string: ['rsyslog' ]
            cpu_check_interval: 0.2
            exact_match: true
            ignore_denied_access: true
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

```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes, datadog_api_key: "mykey" }  # On Ansible < 1.9, use `sudo: yes` instead of `become: yes`
```

Known Issues and Workarounds
----------------------------

On Debian Stretch, the `apt_key` module that the role uses requires an additional system dependency to work correctly.
Unfortunately that dependency (`dirmngr`) is not provided by the module. To work around this, you can add the following
to the playbooks that make use of the present role:

```yml
---
- hosts: all
  pre_tasks:
    - name: Debian Stretch requires dirmngr package to be installed in order to use apt_key
      become: yes  # On Ansible < 1.9, use `sudo: yes` instead of `become: yes`
      apt:
        name: dirmngr
        state: present

  roles:
    - { role: Datadog.datadog, become: yes, datadog_api_key: "mykey" }  # On Ansible < 1.9, use `sudo: yes` instead of `become: yes`
```

License
-------

Apache2

Author Information
------------------

brian@akins.org

dustinjamesbrown@gmail.com --Forked from brian@akins.org

Datadog <info@datadoghq.com> --Forked from dustinjamesbrown@gmail.com
