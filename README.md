# Ansible Datadog Role


[![Ansible Galaxy](http://img.shields.io/badge/galaxy-Datadog.datadog-660198.svg)](https://galaxy.ansible.com/Datadog/datadog/)
[![Build Status](https://travis-ci.org/DataDog/ansible-datadog.svg?branch=master)](https://travis-ci.org/DataDog/ansible-datadog)

Install and configure Datadog Agent & checks. Starting with version `2` of this role Datadog Agent version 6 is installed by default (instead of version 5).

Supports most Debian and RHEL-based Linux distributions, and Windows.

- [Installation](#installation)
- [Role Variables](#role-variables)
- [Agent 5 (older version)](#agent-5-older-version)
- [Dependencies](#dependencies)
- [Configuring a check](#configuring-a-check)
  - [Process Check](#process-check)
  - [Custom Check](#custom-check)
  - [Autodiscovery Check](#autodiscovery-check)
- [Upgrading an integration](#upgrading-an-integration)
  - [Example](#example)
- [Example Playbooks](#example-playbooks)
- [APM](#apm)
- [Process Agent](#process-agent)
  - [Variables](#variables)
  - [System Probe](#system-probe)
  - [Example of configuration](#example-of-configuration)
  - [Agent 5](#agent-5)
- [Additional tasks](#additional-tasks)
- [Known Issues and Workarounds](#known-issues-and-workarounds)
- [License](#license)
- [Author Information](#author-information)

## Installation

```
ansible-galaxy install Datadog.datadog
```

## Role Variables

| Variable                                                                                                                                        | Description                                                                                                                                                                                                                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `datadog_api_key`                                                                                                                               | Your Datadog API key.                                                                                                                                                                                                                                    |
| `datadog_site`                                                                                                                                  | The site of the Datadog intake to send Agent data to. Defaults to `datadoghq.com`, set to `datadoghq.eu` to send data to the EU site. This option is only available with agent version >= 6.6.0.                                                         |
| `datadog_agent_version`                                                                                                                         | The pinned version of the Agent to install (optional, but highly recommended). Examples: `1:6.0.0-1` on apt-based platforms, `6.0.0-1` on yum-based platforms, `6.0.0` on Windows platforms. **Note** Downgrades are not supported on Windows platforms. |
| `datadog_checks`                                                                                                                                | YAML configuration for agent checks to drop into: <br> - `/etc/datadog-agent/conf.d/<check_name>.d/conf.yaml` for Agent v6. <br> - `/etc/dd-agent/conf.d` for Agent v5.                                                                                  |
| `datadog_config`                                                                                                                                | Settings to place in the main Agent configuration file: <br> - `/etc/datadog-agent/datadog.yaml` for Agent v6 <br> - `/etc/dd-agent/datadog.conf` for Agent v5 (under the `[Main]` section).                                                               |
| `datadog_config_ex`                                                                                                                             | Extra INI sections to go in `/etc/dd-agent/datadog.conf` (optional). Agent v5 only.                                                                                                                                                                      |
| `datadog_apt_repo`                                                                                                                              | Override default Datadog `apt` repository                                                                                                                                                                                                                |
| `datadog_apt_cache_valid_time`                                                                                                                  | Override the default apt cache expiration time (default 1 hour).                                                                                                                                                                                         |
| `datadog_apt_key_url_new`                                                                                                                       | Override default url to Datadog `apt` key (key ID `382E94DE` ; the deprecated `datadog_apt_key_url` variable refers to an expired key that's been removed from the role).                                                                                |
| `datadog_yum_repo`                                                                                                                              | Override default Datadog `yum` repository.                                                                                                                                                                                                               |
| `datadog_yum_gpgkey` | Override default url to Datadog `yum` key used to verify Agent v5 and Agent v6 (up to 6.13) packages (key ID `4172A230`) |                                                                                                                                                                                                                                                          |
| `datadog_yum_gpgkey_e09422b3`                                                                                                                   | Override default url to Datadog `yum` key used to verify Agent v6 (from 6.14 upwards) packages (key ID `E09422B3`)                                                                                                                                       |
| `datadog_yum_gpgkey_e09422b3_sha256sum`                                                                                                         | Override default checksum of the `datadog_yum_gpgkey_e09422b3` key.                                                                                                                                                                                      |
| `datadog_zypper_repo`                                                                                                                           | Override default Datadog `zypper` repository.                                                                                                                                                                                                            |
| `datadog_zypper_gpgkey`                                                                                                                         | Override default url to Datadog `zypper` key used to verify Agent v5 and Agent v6 (up to 6.13) packages (key ID `4172A230`).                                                                                                                             |
| `datadog_zypper_gpgkey_sha256sum`                                                                                                               | Override default checksum of the `datadog_zypper_gpgkey` key                                                                                                                                                                                             |
| `datadog_zypper_gpgkey_e09422b3`                                                                                                                | Override default url to Datadog `zypper` key used to verify Agent v6 (from 6.14 upwards) packages (key ID `E09422B3`)                                                                                                                                    |
| `datadog_zypper_gpgkey_e09422b3_sha256sum`                                                                                                      | Override default checksum of the `datadog_zypper_gpgkey_e09422b3` key                                                                                                                                                                                    |
| `datadog_agent_allow_downgrade`                                                                                                                 | Set to `yes` to allow Agent downgrades on apt-based platforms (use with caution, see `defaults/main.yml` for details). **On centos this will only work with ansible 2.4 and up**.                                                                        |
| `use_apt_backup_keyserver`                                                                                                                      | Set `true` to use the backup keyserver instead of the default one.                                                                                                                                                                                       |
| `datadog_enabled`                                                                                                                               | Set to `false` to prevent `datadog-agent` service from starting. Defaults to `true`                                                                                                                                                                      |
| `datadog_additional_groups`                                                                                                                     | Comma separated list of additional groups for the `datadog_user`. Linux only.                                                                                                                                                                            |
| `datadog_windows_ddagentuser_name`                                                                                                              | Name of windows user to create/use, in the format `<domain>\<user>`.  Windows only.                                                                                                                                                                      |
| `datadog_windows_ddagentuser_password`                                                                                                          | Password to use to create the user, and/or register the service. Windows only.                                                                                                                                                                           |

## Agent 5 (older version)

This role includes support for Datadog Agent version 5 for linux only. To install Agent 5, you need to:

1. Set `datadog_agent5` parmeter to `true`.
2. Set `datadog_agent_version` to an existing Agent v5 version or leave it empty to always install the latest version (`5.*`).

To downgrade from Agent v6 to Agent v5, you need to (**on centos this will only work with ansible 2.4 and up**):

1. Set `datadog_agent5` to `true`.
2. Pin `datadog_agent_version` to an existing Agent 5 version.
3. Set `datadog_agent_allow_downgrade` to `yes`.

Variables:

* `datadog_agent5` - Installs agent5 instead of Agent v6 (default to `false`)
* `datadog_agent5_apt_repo` - Overrides default Datadog `apt` repository for Agent v5.

## Dependencies

None

## Configuring a check

To configure a check you need to add an entry to the `datadog_checks` section. The first level key is the name of the check and the value is the yaml payload to write the configuration file.

Example:

### Process Check

To define 2 instances for the `process` check use the configuration below:

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

This creates the corresponding configuration files:

* For Agent v6: `/etc/datadog-agent/conf.d/process.d/conf.yaml`
* For Agent v5: `/etc/dd-agent/conf.d/process.yaml`

### Custom Check

To configure a custom check use the configuration below:

```yml
    datadog_checks:
      my_custom_check:
        init_config:
        instances:
          - some_data: true
```

This creates the corresponding configuration files:

* For Agent v6: `/etc/datadog-agent/conf.d/my_custom_check.d/conf.yaml`
* For Agent v5: `/etc/dd-agent/conf.d/my_custom_check.yaml`

### Autodiscovery Check

There is no pre-processing nor post-processing on the YAML. This means every YAML sections is added to the final configuration file, including `autodiscovery identifiers`.

The example below configures the PostgeSQL check through **autodiscovery**:

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

Learn more about [Autodiscovery in the Datadog documentation](https://docs.datadoghq.com/agent/autodiscovery/).

## Upgrading an integration

**Available for Agent v6.8+**

The `datadog_integration` resource helps you to install specific version of a Datadog integration. Keep in mind the Agent comes with all the integrations already installed. So this command is here to allow you to upgrade a specific integration without upgrading the whole Agent. For more usage information consult the [Agent documentation](https://docs.datadoghq.com/agent/guide/integration-management/).

Available actions:

* `install`: Installs a specific version of the integration.
* `remove`: Removes an integration.

Syntax:

```yml
  datadog_integration:
    <INTEGRATION_NAME>:
      action: <ACTION>
      version: <VERSION_TO_INSTALL>
```

### Example

This example installs version `1.11.0` of the ElasticSearch integration and removes the `postgres` integration.


```yml
 datadog_integration:
   datadog-elastic:
     action: install
     version: 1.11.0
   datadog-postgres:
     action: remove
```

In order to get the available versions of the integrations, please refer to their `CHANGELOG.md` file in the [integrations-core repository](https://github.com/DataDog/integrations-core).

## Example Playbooks


Sending data to Datadog US (default) and configuring a few checks.

```yml
- hosts: servers
  roles:
    - { role: Datadog.datadog, become: yes } # remove the "become: yes" on Windows
  vars:
    datadog_api_key: "123456"
    datadog_agent_version: "1:6.13.0-1" # for apt-based platforms, use a `6.13.0-1` format on yum-based platforms and `6.13.0` for Windows
    datadog_config:
      tags:
        - "env:dev"
        - "datacenter:local"
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
              - "source:nginx"
              - "instance:foo"
          - nginx_status_url: http://example2.com:1234/nginx_status/
            tags:
              - "source:nginx"
              - "instance:bar"

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
    # datadog_integration is available on agent 6.8+
    datadog_integration:
      datadog-elastic:
        action: install
        version: 1.11.0
      datadog-postgres:
        action: remove
    system_probe_config:
      enabled: true
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

## APM

To enable APM with Agent v6 use the following configuration:

```yaml
datadog_config:
    apm_config:
        enabled: true
```

To enable APM with agent v5 use the following configuration:

```yaml
datadog_config:
    apm_enabled: "true" # has to be a string
```

## Process Agent

To control the behavior of the Process Agent, use the `enabled` variable under the `datadog_config` field. It has to be set as a string and the possible values are: `true`, `false` (for only container collection) or `disabled` (to disable the Process Agent entirely)

### Variables

The following variables are available for the Process Agent:

* `scrub_args`: Enables the scrubbing of sensitive arguments from a process command line. Default value is `true`.
* `custom_sensitive_words`: Expands the default list of sensitive words used by the cmdline scrubber.

### System Probe

The [network performance monitoring](https://docs.datadoghq.com/network_performance_monitoring/) system probe is configured under the `system_probe_config` variable.  Any variables nested underneath will be written to the `system-probe.yaml`.

Currently, the system probe only works on Linux with the Agent 6 version and beyond.

### Example of configuration
```yml
datadog_config:
  process_config:
    enabled: "true" # has to be set as a string
    scrub_args: true
    custom_sensitive_words: ['consul_token','dd_api_key']
system_probe_config:
  enabled: true
  sysprobe_socket: /opt/datadog-agent/run/sysprobe.sock
```

### Agent 5

To enable/disable the Process Agent on Agent 5, you need to set on `datadog_config` the `process_agent_enabled` parameter to `true`/`false`.

Set the available variables inside `process.config` under the `datadog_config_ex` field to control the Process Agent's features.

#### Example of configuration

```yml
datadog_config:
  process_agent_enabled: true
datadog_config_ex:
  process.config:
    scrub_args: true
    custom_sensitive_words: "consul_token,dd_api_key"
```

## Additional tasks

`pre_tasks` and `post_tasks` folders allow to run user defined tasks. `pre_tasks` for tasks to be executed before executing any tasks from the Datadog role and `post_tasks` for those to be executed after.

## Known Issues and Workarounds

### dirmngr

On Debian Stretch, the `apt_key` module that the role uses requires an additional system dependency to work correctly. Unfortunately that dependency (`dirmngr`) is not provided by the module. To work around this, you can add the following configuration to the playbooks that make use of the present role:

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

### Datadog Agent 6.14 for Windows

Due to a critical bug in Agent versions `6.14.0` and `6.14.1` on Windows, these versions have
been blacklisted (starting with the version `3.3.0` of this role).

**PLEASE NOTE:** ansible will fail on Windows if `datadog_agent_version` is set
to `6.14.0` or `6.14.1`. Please use `6.14.2` instead. If the Agent version is not
pinned, `6.14.2` will be installed by default.

If you are updating from **6.14.0 or 6.14.1 on Windows**, we **strongly** recommend following these steps:

1. Upgrade the present `Datadog.datadog` ansible role to the latest version (`>=3.3.0`)
2. Set the `datadog_agent_version` to `6.14.2`

To learn more about this bug, please read [here](http://dtdg.co/win-614-fix).

## License

Apache2

## Author Information

brian@akins.org

dustinjamesbrown@gmail.com --Forked from brian@akins.org

Datadog <info@datadoghq.com> --Forked from dustinjamesbrown@gmail.com
