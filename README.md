Ansible Datadog Role
========
[![Ansible Galaxy](http://img.shields.io/badge/galaxy-Datadog.datadog-660198.svg)](https://galaxy.ansible.com/Datadog/datadog/)
[![Build Status](https://travis-ci.org/DataDog/ansible-datadog.svg?branch=master)](https://travis-ci.org/DataDog/ansible-datadog)

Install and configure Datadog base agent & checks. Starting with version `2` of
this role version 6 of the agent is installed by default (instead of version
5).

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
  Examples: `1:6.0.0-1` on apt-based platforms, `6.0.0-1` on yum-based platforms
- `datadog_checks` - YAML configuration for agent checks to drop into:
  + `/etc/datadog-agent/conf.d/<check_name>/conf.yaml` for agent6
  + `/etc/dd-agent/conf.d` for agent5.
- `datadog_config` - Settings to place in the main agent configuration file:
  + `/etc/datadog-agent/datadog.yaml` for agent6
  + `/etc/dd-agent/datadog.conf` for agent5 (under the `[Main]` section).
- `datadog_config_ex` - Extra INI sections to go in `/etc/dd-agent/datadog.conf` (optional). Agent5 only.
- `datadog_apt_repo` - Override default Datadog `apt` repository
- `datadog_apt_cache_valid_time` - Override the default apt cache expiration time (default 1 hour)
- `datadog_apt_key_url_new` - Override default url to Datadog `apt` key (key ID `382E94DE` ; the deprecated `datadog_apt_key_url` variable refers to an expired key that's been removed from the role)
- `datadog_agent_allow_downgrade` - Set to `yes` to allow agent downgrades on apt-based platforms (use with caution, see `defaults/main.yml` for details). **On centos this will only work with ansible 2.4 and up**.

Agent 5 (older version)
-----------------------

This role includes support for Datadog Agent version 5.

To install agent5, you need to:

- set `datadog_agent5` to true
- either set `datadog_agent_version` to an existing agent5 version
  (recommended) or leave it empty to always install the latest version (`5.*`).

To downgrade from agent6 to agent5, you need to (**on centos this will only work with ansible 2.4 and up**):

- set `datadog_agent5` to true
- pin `datadog_agent_version` to an existing agent5 version
- set `datadog_agent_allow_downgrade` to yes

Variables:

- `datadog_agent5` - install agent5 instead of agent6 (default to `false`)
- `datadog_agent5_apt_repo` - Override default Datadog `apt` repository for agent5

Dependencies
------------
None

Configuring a check
-------------------

To configure a check you need to add an entry to the `datadog_checks` section.
The first level key is the name of the check and the value is the yaml payload
to write the configuration file.

Example:

**Process check**

We define 2 instances for the `process` check.
This will create:
- for agent6: `/etc/datadog-agent/conf.d/process/conf.yaml`
- for agent5: `/etc/datadog-agent/conf.d/process.yaml`

```yml
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
```

**custom check**

We define 1 instance for a custom check.

This will create:
- for agent6: `/etc/datadog-agent/conf.d/my_custom_check/conf.yaml`
- for agent5: `/etc/datadog-agent/conf.d/my_custom_check.yaml`

```yml
    datadog_checks:
      my_custom_check:
        init_config:
        instances:
          - some_data: true
```

**autodiscovery check**

There is no pre-processing nor post-processing on the YAML. This means every
YAML sections will be added to the final configuration file, including
`autodiscovery identifiers`.

This example will configure the PostgeSQL check through **autodiscovery**:

```yml
    datadog_checks:
      postgres:
        ad_identifiers:
          - db-master
          - db-slave
        init_config:
        instances:
          - host: %%host%%
            port: %%port%%
            username: username
            password: password
```


Example Playbooks
-----------------
```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes }  # On Ansible < 1.9, use `sudo: yes` instead of `become: yes`
  vars:
    datadog_api_key: "123456"
    datadog_agent_version: "1:6.0.0-1" # for apt-based platforms, use a `6.0.0-1` format on yum-based platforms
    datadog_config:
      tags: "mytag0, mytag1"
      log_level: INFO
      apm_enabled: "true" # has to be set as a string
      logs_enabled: true  # log collection is available on agent 6
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
        #Log collection is available on agent 6
        logs:
          - type: file
            path: /var/log/access.log
            service: myapp
            source: nginx
            sourcecategory: http_web_access
          - type: file
            path: /var/log/error.log
            service: nginx
            source: nginx
            sourcecategory: http_web_access
```

```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes, datadog_api_key: "mykey" }  # On Ansible < 1.9, use `sudo: yes` instead of `become: yes`
```


Process Agent
-------------------------

To control the behavior of the Process Agent, use the `enabled` variable under the `datadog_config` field.
It has to be set as a string and the possible values are: "true", "false" (for only container collection)
or "disabled" (to disable the Process Agent entirely)

#### Variables

- `scrub_args` - enables the scrubbing of sensitive arguments from a process command line. Default value is true
- `custom_sensitive_words` - expands the default list of sensitive words used by the cmdline scrubber

#### Example of configuration
```yml
datadog_config:
  process_config:
    enabled: "true" # has to be set as a string
    scrub_args: true
    custom_sensitive_words: ['consul_token','dd_api_key']
```

### Agent 5

To enable/disable the Process Agent on Agent 5, you need to set on `datadog_config`:

- `process_agent_enabled` to true/false

Set the available variables inside `process.config` under the `datadog_config_ex`
field to control the Process Agent's features.

#### Example of configuration
```yml
datadog_config:
  process_agent_enabled: true
datadog_config_ex:  
  process.config:
    scrub_args: true
    custom_sensitive_words: "consul_token,dd_api_key"
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
