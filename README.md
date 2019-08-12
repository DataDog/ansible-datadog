Ansible Datadog Role
========
[![Ansible Galaxy](http://img.shields.io/badge/galaxy-Datadog.datadog-660198.svg)](https://galaxy.ansible.com/Datadog/datadog/)
[![Build Status](https://travis-ci.org/DataDog/ansible-datadog.svg?branch=master)](https://travis-ci.org/DataDog/ansible-datadog)

Install and configure Datadog base agent & checks. Starting with version `2` of
this role version 6 of the agent is installed by default (instead of version
5).

Supports most Debian and RHEL-based Linux distributions, and Windows.

Installation
------------

```
ansible-galaxy install Datadog.datadog
```

Role Variables
--------------

- `datadog_api_key` - Your Datadog API key.
- `datadog_site` - The site of the Datadog intake to send Agent data to.
  Defaults to 'datadoghq.com', set to 'datadoghq.eu' to send data to the EU
  site. This option is only available with agent version >= 6.6.0.
- `datadog_agent_version` - The pinned version of the Agent to install (optional, but highly recommended)
  Examples: `1:6.0.0-1` on apt-based platforms, `6.0.0-1` on yum-based platforms, `6.0.0` on Windows platforms
  + **Note** Downgrades are not supported on Windows platforms.
- `datadog_checks` - YAML configuration for agent checks to drop into:
  + `/etc/datadog-agent/conf.d/<check_name>.d/conf.yaml` for agent6
  + `/etc/dd-agent/conf.d` for agent5.
- `datadog_config` - Settings to place in the main agent configuration file:
  + `/etc/datadog-agent/datadog.yaml` for agent6
  + `/etc/dd-agent/datadog.conf` for agent5 (under the `[Main]` section).
- `datadog_config_ex` - Extra INI sections to go in `/etc/dd-agent/datadog.conf` (optional). Agent5 only.
- `datadog_apt_repo` - Override default Datadog `apt` repository
- `datadog_apt_cache_valid_time` - Override the default apt cache expiration time (default 1 hour)
- `datadog_apt_key_url_new` - Override default url to Datadog `apt` key (key ID `382E94DE` ; the deprecated `datadog_apt_key_url` variable refers to an expired key that's been removed from the role)
- `datadog_yum_repo` - Override default Datadog `yum` repository
- `datadog_yum_gpgkey` - Override default url to Datadog `yum` key used to verify Agent 5 and Agent 6 (up to 6.13) packages (key ID `4172A230`)
- `datadog_yum_gpgkey_e09422b3` - Override default url to Datadog `yum` key used to verify Agent 6 (from 6.14 upwards) packages (key ID `E09422B3`)
- `datadog_yum_gpgkey_e09422b3_sha256sum` - Override default checksum of the `datadog_yum_gpgkey_e09422b3` key
- `datadog_zypper_repo` - Override default Datadog `zypper` repository
- `datadog_zypper_gpgkey` - Override default url to Datadog `zypper` key used to verify Agent 5 and Agent 6 (up to 6.13) packages (key ID `4172A230`)
- `datadog_zypper_gpgkey_sha256sum` - Override default checksum of the `datadog_zypper_gpgkey` key
- `datadog_zypper_gpgkey_e09422b3` - Override default url to Datadog `zypper` key used to verify Agent 6 (from 6.14 upwards) packages (key ID `E09422B3`)
- `datadog_zypper_gpgkey_e09422b3_sha256sum` - Override default checksum of the `datadog_zypper_gpgkey_e09422b3` key
- `datadog_agent_allow_downgrade` - Set to `yes` to allow agent downgrades on apt-based platforms (use with caution, see `defaults/main.yml` for details). **On centos this will only work with ansible 2.4 and up**.
- `use_apt_backup_keyserver` - Set `true` to use the backup keyserver instead of the default one
- `datadog_enabled` - Set to `false` to prevent `datadog-agent` service from starting. Defaults to `true`
- `datadog_additional_groups` - Comma separated list of additional groups for the `datadog_user`. Linux only.
- `datadog_windows_ddagentuser_name` - Name of windows user to create/use, in the format `<domain>\<user>`.  Windows only.
- `datadog_windows_ddagentuser_password` - Password to use to create the user, and/or register the service. Windows only.

Agent 5 (older version)
-----------------------

This role includes support for Datadog Agent version 5 for linux only.

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
- for agent6: `/etc/datadog-agent/conf.d/process.d/conf.yaml`
- for agent5: `/etc/dd-agent/conf.d/process.yaml`

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
- for agent6: `/etc/datadog-agent/conf.d/my_custom_check.d/conf.yaml`
- for agent5: `/etc/dd-agent/conf.d/my_custom_check.yaml`

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

Sending data to Datadog US (default) and configuring a few checks.
```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes }
  vars:
    datadog_api_key: "123456"
    datadog_agent_version: "1:6.0.0-1" # for apt-based platforms, use a `6.0.0-1` format on yum-based platforms
    datadog_config:
      tags: "mytag0, mytag1"
      log_level: INFO
      apm_config:
        enabled: true
        max_traces_per_second: 10
      logs_enabled: true  # log collection is available on agent 6
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

Example for sending data to EU site:
```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes }
  vars:
    datadog_site: "datadoghq.eu"
    datadog_api_key: "123456"
```

APM
---

To enable APM with agent V6:

```yaml
datadog_config:
    apm_config:
        enabled: true
```

To enable APM with agent V5:

```yaml
datadog_config:
    apm_enabled: "true" # has to be a string
```

Process Agent
-------------

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

Additional tasks
----------------

`pre_tasks` and `post_tasks` folders allow to run user defined tasks. `pre_tasks` for tasks to be executed before executing any tasks from the Datadog role and `post_tasks` for those to be executed after.

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
