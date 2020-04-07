# Ansible Datadog Role

The Ansible Datadog role installs and configures the Datadog Agent and integrations. Version `4` of the role installs the Datadog Agent v7 by default.

## Setup

### Requirements

- Requires Ansible v2.6+.
- Supports most Debian and RHEL-based Linux distributions, and Windows.

### Installation

Install the [Datadog role][1] from Ansible Galaxy on your Ansible server:

```shell
ansible-galaxy install datadog.datadog
```

To deploy the Datadog Agent on hosts, add the Datadog role and your API key to your playbook:

```text
- hosts: servers
  roles:
    - { role: datadog.datadog, become: yes }
  vars:
    datadog_api_key: "<YOUR_DD_API_KEY>"
```

#### Role variables

| Variable                                   | Description                                                                                                                                                                                                                                                                                               |
|--------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `datadog_api_key`                          | Your Datadog API key.                                                                                                                                                                                                                                                                                     |
| `datadog_site`                             | The site of the Datadog intake to send Agent data to. Defaults to `datadoghq.com`, set to `datadoghq.eu` to send data to the EU site. This option is only available with Agent version >= 6.6.0.                                                                                                          |
| `datadog_agent_version`                    | The pinned version of the Agent to install (optional, but recommended), for example: `7.16.0`. Setting `datadog_agent_major_version` is not needed if `datadog_agent_version` is used. **Note**: Downgrades are not supported on Windows platforms.                                                       |
| `datadog_agent_major_version`              | The major version of the Agent to install. The possible values are 5, 6, or 7 (default). If `datadog_agent_version` is set, it takes precedence otherwise the latest version of the specified major is installed. Setting `datadog_agent_major_version` is not needed if `datadog_agent_version` is used. |
| `datadog_checks`                           | YAML configuration for Agent checks to drop into: <br> - `/etc/datadog-agent/conf.d/<check_name>.d/conf.yaml` for Agent v6 and v7, <br> - `/etc/dd-agent/conf.d` for Agent v5.                                                                                                                            |
| `datadog_config`                           | Settings for the main Agent configuration file: <br> - `/etc/datadog-agent/datadog.yaml` for Agent v6 and v7,<br> - `/etc/dd-agent/datadog.conf` for Agent v5 (under the `[Main]` section).                                                                                                               |
| `datadog_config_ex`                        | (Optional) Extra INI sections to go in `/etc/dd-agent/datadog.conf` (Agent v5 only).                                                                                                                                                                                                                      |
| `datadog_apt_repo`                         | Override the default Datadog `apt` repository.                                                                                                                                                                                                                                                            |
| `datadog_apt_cache_valid_time`             | Override the default apt cache expiration time (defaults to 1 hour).                                                                                                                                                                                                                                      |
| `datadog_apt_key_url_new`                  | Override the default URL to Datadog `apt` key (key ID `382E94DE`; the deprecated `datadog_apt_key_url` variable refers to an expired key that's been removed from the role).                                                                                                                             |
| `datadog_yum_repo`                         | Override the default Datadog `yum` repository.                                                                                                                                                                                                                                                            |
| `datadog_yum_gpgkey`                       | Override the default URL to the Datadog `yum` key used to verify Agent v5 and v6 (up to 6.13) packages (key ID `4172A230`).                                                                                                                                                                               |
| `datadog_yum_gpgkey_e09422b3`              | Override the default URL to the Datadog `yum` key used to verify Agent v6.14+ packages (key ID `E09422B3`).                                                                                                                                                                                               |
| `datadog_yum_gpgkey_e09422b3_sha256sum`    | Override the default checksum of the `datadog_yum_gpgkey_e09422b3` key.                                                                                                                                                                                                                                   |
| `datadog_zypper_repo`                      | Override the default Datadog `zypper` repository.                                                                                                                                                                                                                                                         |
| `datadog_zypper_gpgkey`                    | Override the default URL to the Datadog `zypper` key used to verify Agent v5 and v6 (up to 6.13) packages (key ID `4172A230`).                                                                                                                                                                            |
| `datadog_zypper_gpgkey_sha256sum`          | Override the default checksum of the `datadog_zypper_gpgkey` key.                                                                                                                                                                                                                                         |
| `datadog_zypper_gpgkey_e09422b3`           | Override the default URL to the Datadog `zypper` key used to verify Agent v6.14+ packages (key ID `E09422B3`).                                                                                                                                                                                            |
| `datadog_zypper_gpgkey_e09422b3_sha256sum` | Override the default checksum of the `datadog_zypper_gpgkey_e09422b3` key.                                                                                                                                                                                                                                |
| `datadog_agent_allow_downgrade`            | Set to `yes` to allow Agent downgrades on apt-based platforms (use with caution, see `defaults/main.yml` for details). **Note**: On Centos this only works with Ansible 2.4+.                                                                                                                             |
| `use_apt_backup_keyserver`                 | Set to `true` to use the backup keyserver instead of the default one.                                                                                                                                                                                                                                     |
| `datadog_enabled`                          | Set to `false` to prevent `datadog-agent` service from starting (defaults to `true`).                                                                                                                                                                                                                     |
| `datadog_additional_groups`                | Either a list, or a string containing a comma-separated list of additional groups for the `datadog_user` (Linux only).                                                                                                                                                                                    |
| `datadog_windows_ddagentuser_name`         | The name of Windows user to create/use, in the format `<domain>\<user>` (Windows only).                                                                                                                                                                                                                   |
| `datadog_windows_ddagentuser_password`     | The password used to create the user and/or register the service (Windows only).                                                                                                                                                                                                                          |

### Integrations

To configure a Datadog integration (check), add an entry to the `datadog_checks` section. The first level key is the name of the check, and the value is the YAML payload to write the configuration file. Examples are provided below.

#### Process check

To define two instances for the `process` check use the configuration below. This creates the corresponding configuration files:

* Agent v6 & v7: `/etc/datadog-agent/conf.d/process.d/conf.yaml`
* Agent v5: `/etc/dd-agent/conf.d/process.yaml`

```yml
    datadog_checks:
      process:
        init_config:
        instances:
          - name: ssh
            search_string: ['ssh', 'sshd']
          - name: syslog
            search_string: ['rsyslog']
            cpu_check_interval: 0.2
            exact_match: true
            ignore_denied_access: true
```

#### Custom check

To configure a custom check use the configuration below. This creates the corresponding configuration files:

- Agent v6 & v7: `/etc/datadog-agent/conf.d/my_custom_check.d/conf.yaml`
- Agent v5: `/etc/dd-agent/conf.d/my_custom_check.yaml`

```yml
    datadog_checks:
      my_custom_check:
        init_config:
        instances:
          - some_data: true
```

#### Autodiscovery

When using Autodiscovery, there is no pre-processing nor post-processing on the YAML. This means every YAML section is added to the final configuration file, including `autodiscovery identifiers`.

The example below configures the PostgreSQL check through **Autodiscovery**:

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

Learn more about [Autodiscovery in the Datadog documentation][3].

### Tracing

To enable trace collection with Agent v6 or v7 use the following configuration:

```yaml
datadog_config:
  apm_config:
    enabled: true
```

To enable trace collection with Agent v5 use the following configuration:

```yaml
datadog_config:
  apm_enabled: "true" # has to be a string
```

### Live processes

To enable [live process][6] collection with Agent v6 or v7 use the following configuration:

```yml
datadog_config:
  process_config:
    enabled: "true" # type: string
```

The possible values for `enabled` are: `"true"`, `"false"` (only container collection), or `"disabled"` (disable live processes entirely).

#### Variables

The following variables are available for live processes:

* `scrub_args`: Enables the scrubbing of sensitive arguments from a process command line (defaults to `true`).
* `custom_sensitive_words`: Expands the default list of sensitive words used by the command line scrubber.

#### System Probe

The [Network Performance Monitoring][7] (NPM) system probe is configured under the `system_probe_config` variable. Any variables nested underneath are written to the `system-probe.yaml`.

**Note**: The system probe only works on Linux with the Agent v6+.

#### Example configuration

```yml
datadog_config:
  process_config:
    enabled: "true" # type: string
    scrub_args: true
    custom_sensitive_words: ['consul_token','dd_api_key']
system_probe_config:
  enabled: true
  sysprobe_socket: /opt/datadog-agent/run/sysprobe.sock
```

Once modification is complete, follow the steps below:

1. Start the system-probe: `sudo service datadog-agent-sysprobe start` **Note**: If the service wrapper is not available on your system, run this command instead: `sudo initctl start datadog-agent-sysprobe`.
2. [Restart the Agent][8]: `sudo service datadog-agent restart`.
3. Enable the system-probe to start on boot: `sudo service enable datadog-agent-sysprobe`.

For manual setup, refer to the [NPM][9] documentation.

#### Agent v5

To enable [live process][6] collection with Agent v5, use the following configuration:

```yml
datadog_config:
  process_agent_enabled: true
datadog_config_ex:
  process.config:
    scrub_args: true
    custom_sensitive_words: "<FIRST_WORD>,<SECOND_WORD>"
```

### Additional tasks

`pre_tasks` and `post_tasks` folders are available to run user defined tasks. `pre_tasks` run before executing any tasks from the Datadog Ansible role, and `post_tasks` run after execution of the role.

Installation tasks on supported platforms register the variable `datadog_agent_install`, which can be used in `post_tasks` to check the installation task's result. `datadog_agent_install.changed` is set to `true` if the installation task did install something, and `false` otherwise (for instance if the requested version was already installed).

## Versions

By default, the current major version of the Datadog Ansible role installs Agent v7. The variables `datadog_agent_version` and `datadog_agent_major_version` are available to control the Agent version installed.

For v4+ of this role, when `datadog_agent_version` is used to pin a specific Agent version, the role derives per-OS version names to comply with the version naming schemes of the supported operating systems, for example:

- `1:7.16.0-1` for Debian and SUSE based
- `7.16.0-1` for Redhat-based
- `7.16.0` for Windows.

This makes it possible to target hosts running different operating systems in the same Ansible run, for example:

| Provided                            | Installs     | System                |
|-------------------------------------|--------------|-----------------------|
| `datadog_agent_version: 7.16.0`     | `1:7.16.0-1` | Debian and SUSE-based |
| `datadog_agent_version: 7.16.0`     | `7.16.0-1`   | Redhat-based          |
| `datadog_agent_version: 7.16.0`     | `7.16.0`     | Windows               |
| `datadog_agent_version: 1:7.16.0-1` | `1:7.16.0-1` | Debian and SUSE-based |
| `datadog_agent_version: 1:7.16.0-1` | `7.16.0-1`   | Redhat-based          |
| `datadog_agent_version: 1:7.16.0-1` | `7.16.0`     | Windows               |

**Note**: If the version is not provided, the role uses `1` as the epoch and `1` as the release number.

**Agent v5 (older version)**:

The Datadog Ansible role includes support for Datadog Agent v5 for Linux only. To install Agent v5, use `datadog_agent_major_version: 5` to install the latest version of Agent v5 or set `datadog_agent_version` to a specific version of Agent v5. **Note**: The `datadog_agent5` variable is obsolete and has been removed.

### Repositories

#### Linux

When the variables `datadog_apt_repo`, `datadog_yum_repo`, and `datadog_zypper_repo` are not set, the official Datadog repositories for the major version set in `datadog_agent_major_version` are used:

| # | Default apt repository                    | Default yum repository             | Default zypper repository               |
|---|-------------------------------------------|------------------------------------|-----------------------------------------|
| 5 | deb https://apt.datadoghq.com stable main | https://yum.datadoghq.com/rpm      | https://yum.datadoghq.com/suse/rpm      |
| 6 | deb https://apt.datadoghq.com stable 6    | https://yum.datadoghq.com/stable/6 | https://yum.datadoghq.com/suse/stable/6 |
| 7 | deb https://apt.datadoghq.com stable 7    | https://yum.datadoghq.com/stable/7 | https://yum.datadoghq.com/suse/stable/7 |

To override the default behavior, set these variables to something else than an empty string.

If you previously used the Agent v5 variables, use the **new** variables below with `datadog_agent_major_version` set to `5` or `datadog_agent_version` pinned to a specific Agent v5 version.

| Old                          | New                   |
|------------------------------|-----------------------|
| `datadog_agent5_apt_repo`    | `datadog_apt_repo`    |
| `datadog_agent5_yum_repo`    | `datadog_yum_repo`    |
| `datadog_agent5_zypper_repo` | `datadog_zypper_repo` |

#### Windows

When the variable `datadog_windows_download_url` is not set, the official Windows MSI package corresponding to the `datadog_agent_major_version` is used:

| # | Default Windows MSI package URL                                                  |
|---|----------------------------------------------------------------------------------|
| 6 | https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-6-latest.amd64.msi |
| 7 | https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi |

To override the default behavior, set this variable to something else than an empty string.

### Upgrade

To upgrade from Agent v6 to v7, use `datadog_agent_major_version: 7` to install the latest version or set `datadog_agent_version` to a specific version of Agent v7. Use similar logic to upgrade from Agent v5 to v6.

#### Integrations

**Available for Agent v6.8+**

Use the `datadog_integration` resource to install a specific version of a Datadog integration. Keep in mind, the Agent comes with all the integrations already installed. This command is useful for upgrading a specific integration without upgrading the whole Agent. For more details, see [Integration Management][4].

Available actions:

- `install`: Installs a specific version of the integration.
- `remove`: Removes an integration.

##### Syntax

```yml
  datadog_integration:
    <INTEGRATION_NAME>:
      action: <ACTION>
      version: <VERSION_TO_INSTALL>
```

##### Example

This example installs version `1.11.0` of the ElasticSearch integration and removes the `postgres` integration.

```yml
 datadog_integration:
   datadog-elastic:
     action: install
     version: 1.11.0
   datadog-postgres:
     action: remove
```

To see the available versions of Datadog integrations, refer to their `CHANGELOG.md` file in the [integrations-core repository][5].

### Downgrade

To downgrade to a prior version of the Agent:

1. Set `datadog_agent_version` to a specific version, for example: `5.32.5`.
2. Set `datadog_agent_allow_downgrade` to `yes`.

**Notes:**

- Downgrades are not supported for Windows platforms.

## Playbooks

Below are some sample playbooks to assist you with using the Datadog Ansible role.

The following example sends data to Datadog US (default), enables logs, and configures a few checks.

```yml
- hosts: servers
  roles:
    - { role: datadog.datadog, become: yes }
  vars:
    datadog_api_key: "<YOUR_DD_API_KEY>"
    datadog_agent_version: "7.16.0"
    datadog_config:
      tags:
        - "<KEY>:<VALUE>"
        - "<KEY>:<VALUE>"
      log_level: INFO
      apm_config:
        enabled: true
        max_traces_per_second: 10
      logs_enabled: true  # available with Agent v6 and v7
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
            password: <YOUR_PASSWORD>
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
              - "<KEY>:<VALUE>"

        #Log collection is available on Agent 6 and 7
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
    # datadog_integration is available on Agent 6.8+
    datadog_integration:
      datadog-elastic:
        action: install
        version: 1.11.0
      datadog-postgres:
        action: remove
    system_probe_config:
      enabled: true
```

### Agent v6

This example installs the latest Agent v6:

```yml
- hosts: servers
  roles:
    - { role: datadog.datadog, become: yes }
  vars:
    datadog_agent_major_version: 6
    datadog_api_key: "<YOUR_DD_API_KEY>"
```

### EU site

This example sends data to the EU site:

```yml
- hosts: servers
  roles:
    - { role: datadog.datadog, become: yes }
  vars:
    datadog_site: "datadoghq.eu"
    datadog_api_key: "<YOUR_DD_API_KEY>"
```

### Windows

On Windows, the `become: yes` option should be removed because it will make the role fail. Below are two methods to make the example playbooks work with Windows hosts:

#### Inventory file

Using the inventory file is the recommended approach. Set the `ansible_become` option to `no` in the inventory file for each Windows host:

```ini
[servers]
linux1 ansible_host=127.0.0.1
linux2 ansible_host=127.0.0.2
windows1 ansible_host=127.0.0.3 ansible_become=no
windows2 ansible_host=127.0.0.4 ansible_become=no
```

To avoid repeating the same configuration for all Windows hosts, group them and set the variable at the group level:

```ini
[linux]
linux1 ansible_host=127.0.0.1
linux2 ansible_host=127.0.0.2

[windows]
windows1 ansible_host=127.0.0.3
windows2 ansible_host=127.0.0.4

[windows:vars]
ansible_become=no
```

#### Playbook file

Alternatively, if your playbook **only runs on Windows hosts**, use the following in the playbook file:

```yml
- hosts: servers
  roles:
    - { role: datadog.datadog }
  vars:
    ...
```

**Note**: This configuration fails on Linux hosts. Only use it if the playbook is specific to Windows hosts. Otherwise, use the [inventory file method](#inventory-file).

## Troubleshooting

### Debian stretch

On Debian Stretch, the `apt_key` module used by the role requires an additional system dependency to work correctly. The dependency (`dirmngr`) is not provided by the module. Add the following configuration to your playbooks to make use of the present role:

```yml
---
- hosts: all
  pre_tasks:
    - name: Debian Stretch requires the dirmngr package to use apt_key
      become: yes
      apt:
        name: dirmngr
        state: present

  roles:
    - { role: datadog.datadog, become: yes }
  vars:
    datadog_api_key: "<YOUR_DD_API_KEY>"
```

### Windows

Due to a critical bug in Agent versions `6.14.0` and `6.14.1` on Windows, these versions have been blacklisted (starting with version `3.3.0` of this role).

**NOTE:** Ansible fails on Windows if `datadog_agent_version` is set to `6.14.0` or `6.14.1`. Use `6.14.2` or above.

If you are updating from **6.14.0 or 6.14.1 on Windows**, use the following steps:

1. Upgrade the present `datadog.datadog` Ansible role to the latest version (`>=3.3.0`).
2. Set the `datadog_agent_version` to `6.14.2` or above (defaults to latest).

For more details, see [Critical Bug in Uninstaller for Datadog Agent 6.14.0 and 6.14.1 on Windows][10].

[1]: https://galaxy.ansible.com/Datadog/datadog
[2]: https://github.com/DataDog/ansible-datadog
[3]: https://docs.datadoghq.com/agent/autodiscovery
[4]: https://docs.datadoghq.com/agent/guide/integration-management/
[5]: https://github.com/DataDog/integrations-core
[6]: https://docs.datadoghq.com/infrastructure/process/
[7]: https://docs.datadoghq.com/network_performance_monitoring/
[8]: https://docs.datadoghq.com/agent/guide/agent-commands/#restart-the-agent
[9]: https://docs.datadoghq.com/network_performance_monitoring/installation/?tab=agent#setup
[10]: https://app.datadoghq.com/help/agent_fix
