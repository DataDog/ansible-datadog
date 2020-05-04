CHANGELOG
=========

# 4.2.1 / 2020-05-04

* [BUGFIX] Fix error when checking custom repository file on debian-based systems. See [#275][].

# 4.2.0 / 2020-04-08

* [FEATURE] Ensure the start mode when starting on Windows. See [#271][]. Thanks to [@DevKyleS][].
  * The Agent service will now always be started on Windows at the end of an Ansible run
  if `datadog_enabled` is set to `true`.
  Previously, if the Agent was already installed, the start mode of the existing Agent
  service was used (which meant a disabled Agent service would remain disabled
  after an Ansible run, even with `datadog_enabled: true`).
  If you manually disabled the Agent service and want it to remain disabled,
  set `datadog_enabled` to `false`.
* [FEATURE] Remove old INI config files from v6/v7 configuration. See [#271][]. Thanks to [@b2jrock][].
* [FEATURE] Register result when Agent install task is run. See [#268][].
* [BUGFIX] Update `datadog_additional_groups` task & doc. See [#267][].
* [BUGFIX] Fix role idempotence on Debian. See [#262][]. Thanks to [@jharley][].
* [DOCS] README update: system-probe installation steps. See [#257][].
* [DOCS] README update: minimum Ansible version & various fixes. See [#264][].
* [DOCS] Documentation (README, CONTRIBUTING) overhaul. See [#270][].

# 4.1.1 / 2020-02-10

* [BUGFIX] Add skip check on sysprobe set_fact tasks. See [#259][]
* [BUGFIX] Only try to stop sysprobe if it is installed. See [#255][]. Thanks to [@dv9io0o][].

# 4.1.0 / 2020-01-20

* [FEATURE] Fail with explicit message if OS is not supported by the role. See [#247][]
* [BUGFIX] Ensure that system-probe is stopped if it is disabled or not installed. See [#249][]
* [BUGFIX] Change default datadog_agent group to dd-agent. See [#248][]
* [DOCS] Update instructions to use datadog.datadog as the role name. See [#246][]
* [DOCS] Add development guidelines & small kitchen dev environment. See [#243][]

# 4.0.1 / 2019-12-23

* [BUGFIX] Fix system-probe.yaml.j2 indent filter. See [#240][]
* [BUGFIX] Fix sysprobe service detection for systemd services. See [#242][]
* [OTHER] Improve ansible-galaxy score by following best practices. See [#236][]
* [OTHER] Include names for `include_tasks`. See [#226][]. Thanks to [@the-real-cphilips][].

# 4.0.0 / 2019-12-18

**This role will install Agent v7 by default.** Datadog Agent v7 runs checks with Python 3, so if you were running any custom checks written in Python, they must be compatible with Python 3. If you were not running any custom checks or if your custom checks are already compatible with Python 3, then it is safe to upgrade to Agent v7.

* [MAJOR] Agent 7 support. See [#220][].
  * Refer to the [role upgrade section](README.md#role-upgrade-from-v3-to-v4) of the docs for the complete list of changes and instructions to upgrade this role from v3 to v4.
* [FEATURE] Infer major version from `datadog_agent_version`. See [#239][].
* [FEATURE] Allow pinned version install on multiple platforms at the same time. See [#235][].

# 3.4.0 / 2019-12-18

* [FEATURE] Reset pinned Windows version. See [#234][].
* [DOCS] Add README instructions for Windows hosts. See [#233][].
* [META] Update list of platforms supported by the role. See [#224][].

# 3.3.0 / 2019-11-18

* [FEATURE] Blacklist installation of 6.14.0 and 6.14.1 on Windows.
* [FEATURE] Run fix + sanity check script before agent install/upgrade on Windows.
* [FEATURE] Adding support for Datadog system-probe (thanks to [@jstoja][]).

# 3.2.0 / 2019-10-02

* [DEPRECATION] Drop support for EOL version of Ansible (2.5)
- [FEATURE] Add the `datadog_integration resource` to easily control installed integrations.

# 3.1.0 / 2019-08-30

- [FEATURE] Trust new RPM key on SUSE. See [#203][].
- [IMPROVEMENT] Windows: Add the ability to specify the 'ddagentuser' name and password in the configuration.
- [FEATURE] Add 'pre_task' and 'post_task' folder for custom user tasks.

# 3.0.0 / 2019-05-17

- [FEATURE] On Linux: you can now add the Agent's user to additionnal groups.
- [DEPRECATION] Bumping this minimum supported Ansible version from 2.2 to 2.5 (version prior from 2.5 are EOL).
- [IMPROVEMENT] Use 'include_tasks' instead of 'include' which bump minimum ansible version to 2.4 (thanks to [@rouge8][]).
- [FIX] Make sure the Live Process agent and APM agent aren't started when datadog_enabled is set to false (thanks to [@pdecat][]).

# 2.6.0 / 2019-03-05

* [FEATURE] Add support for managing Windows hosts.

# 2.5.0 / 2019-02-12

* [IMPROVEMENT] Allow the use of a backup keyserver for apt in case the main one is down.
* [IMPROVEMENT] Fix configuration items order to be the same between playbook runs (thanks to [@jpiron][]).

# 2.4.0 / 2018-10-25

* [FEATURE] Add support for "site" configuration.
* [IMPROVEMENT] Add retry policy when failing to pull GPG key from keyserver.ubuntu.com

# 2.3.1 / 2018-08-24

* [FIX] Disabling repo metadata signature check for SUSE/SLES.

# 2.3.0 / 2018-07-23

* [FEATURE] Add support for SUSE/SLES (thanks to [@enarciso][]).

# 2.2.0 / 2018-06-06

* [DEPRECATION] Drop support for EOL platform
* [IMPROVEMENT] Harmonize tasks names between agent5 and agent6 (thanks [@xp-1000][]).

# 2.1.0 / 2018-05-14

* [FEATURE] Support "--check" Ansible option for dry-run.
* [BUGFIX] Fix downgrade on centos.
* [IMPROVEMENT] Update conf paths to respect agent6 best practice (thanks [@dbr1993][]).
* [IMPROVEMENT] Fix YAML cosmetics: standardize syntax everywhere (thanks [@tomgoren][]).
* [DEPRECATION] Drop support for EOL versions of ansible (<2.2).

# 2.0.3 / 2018-04-13

* [BUGFIX] Removing legacy http apt repos pre-dating usage of HTTPS. See [#116][]

# 2.0.2 / 2018-03-27

* [BUGFIX] Remove empty brackets from datadog.yaml when datadog_config is empty. See [#107][]

# 2.0.1 / 2018-03-05

* [BUGFIX] Remove failing import of expired APT key. See [#105][]

# 1.6.1 / 2018-03-05

* [BUGFIX] Remove failing import of expired APT key. See [#105][]

# 2.0.0 / 2018-02-27

* [RELEASE] Make Agent6 the default version to install.
* [IMPROVEMENT] Defaulting to HTTPS for apt and yum repo.

# 1.6.0 / 2018-01-19

* [IMPROVEMENT] Refresh apt cache every hour. See [#98][]

# 1.5.0 / 2018-01-05

* [FEATURE] Add Agent6 (beta) support on RPM-based distros. See [#90][] (thanks [@brendanlong][])

# 1.4.0 / 2017-10-30

* [FEATURE] Allow specifying custom repo. See [#80][]
* [FEATURE] Add Agent6 (beta) support on debianoids. See [#81][]
* [BUGFIX] Fix incorrect handler name in process task. See [#68][] (thanks [@jeffwidman][])
* [SANITY] Improve agent service task name and handler formatting. See [#62][] and [#67][] (thanks [@jeffwidman][])

# 1.3.0 / 2017-04-04

* [FEATURE] Add support for configuring trace agent. See [#45][] and [#58][] (thanks [@pmbauer][])
* [FEATURE] Allow pinning the version of the Agent. See [#61][]
* [IMPROVEMENT] Pipe `datadog_checks` through list for python3 support. See [#51][] (thanks [@gtrummell][])
* [IMPROVEMENT] Use `ansible-lint` on the role and use names on all tasks. See [#50][] (thanks [@eplanet][])
* [BUGFIX] Fix `ini` format of the `datadog.conf` file. See [#59][]

# 1.2.0 / 2016-12-13

* [FEATURE] Trust new APT and RPM keys. See [#30][]
* [IMPROVEMENT] Change the `state` of `apt-transport-https` from `latest` to `present`. See [#36][]
* [IMPROVEMENT] Convert config file tasks to proper YAML formatting. See [#32][] (thanks [@jeffwidman][])

# 1.1.0 / 2016-06-27

* [FEATURE] Allow APT repo settings to be user-defined. See [#20][] (thanks [@geoffwright][])

# 1.0.0 / 2016-06-08

Initial release, compatible with Ansible v1 & v2

<!--- The following link definition list is generated by PimpMyChangelog --->
[#20]: https://github.com/DataDog/ansible-datadog/issues/20
[#30]: https://github.com/DataDog/ansible-datadog/issues/30
[#32]: https://github.com/DataDog/ansible-datadog/issues/32
[#36]: https://github.com/DataDog/ansible-datadog/issues/36
[#45]: https://github.com/DataDog/ansible-datadog/issues/45
[#50]: https://github.com/DataDog/ansible-datadog/issues/50
[#51]: https://github.com/DataDog/ansible-datadog/issues/51
[#58]: https://github.com/DataDog/ansible-datadog/issues/58
[#59]: https://github.com/DataDog/ansible-datadog/issues/59
[#61]: https://github.com/DataDog/ansible-datadog/issues/61
[#62]: https://github.com/DataDog/ansible-datadog/issues/62
[#67]: https://github.com/DataDog/ansible-datadog/issues/67
[#68]: https://github.com/DataDog/ansible-datadog/issues/68
[#80]: https://github.com/DataDog/ansible-datadog/issues/80
[#81]: https://github.com/DataDog/ansible-datadog/issues/81
[#90]: https://github.com/DataDog/ansible-datadog/issues/90
[#98]: https://github.com/DataDog/ansible-datadog/issues/98
[#105]: https://github.com/DataDog/ansible-datadog/issues/105
[#107]: https://github.com/DataDog/ansible-datadog/issues/107
[#116]: https://github.com/DataDog/ansible-datadog/issues/116
[#203]: https://github.com/DataDog/ansible-datadog/issues/203
[#220]: https://github.com/DataDog/ansible-datadog/issues/220
[#224]: https://github.com/DataDog/ansible-datadog/issues/224
[#226]: https://github.com/DataDog/ansible-datadog/issues/226
[#233]: https://github.com/DataDog/ansible-datadog/issues/233
[#234]: https://github.com/DataDog/ansible-datadog/issues/234
[#235]: https://github.com/DataDog/ansible-datadog/issues/235
[#236]: https://github.com/DataDog/ansible-datadog/issues/236
[#239]: https://github.com/DataDog/ansible-datadog/issues/239
[#240]: https://github.com/DataDog/ansible-datadog/issues/240
[#242]: https://github.com/DataDog/ansible-datadog/issues/242
[#243]: https://github.com/DataDog/ansible-datadog/issues/243
[#246]: https://github.com/DataDog/ansible-datadog/issues/246
[#247]: https://github.com/DataDog/ansible-datadog/issues/247
[#248]: https://github.com/DataDog/ansible-datadog/issues/248
[#249]: https://github.com/DataDog/ansible-datadog/issues/249
[#255]: https://github.com/DataDog/ansible-datadog/issues/255
[#257]: https://github.com/DataDog/ansible-datadog/issues/257
[#259]: https://github.com/DataDog/ansible-datadog/issues/259
[#262]: https://github.com/DataDog/ansible-datadog/issues/262
[#264]: https://github.com/DataDog/ansible-datadog/issues/264
[#267]: https://github.com/DataDog/ansible-datadog/issues/267
[#268]: https://github.com/DataDog/ansible-datadog/issues/268
[#270]: https://github.com/DataDog/ansible-datadog/issues/270
[#271]: https://github.com/DataDog/ansible-datadog/issues/271
[#275]: https://github.com/DataDog/ansible-datadog/issues/275
[@DevKyleS]: https://github.com/DevKyleS
[@b2jrock]: https://github.com/b2jrock
[@brendanlong]: https://github.com/brendanlong
[@dbr1993]: https://github.com/dbr1993
[@dv9io0o]: https://github.com/dv9io0o
[@enarciso]: https://github.com/enarciso
[@eplanet]: https://github.com/eplanet
[@geoffwright]: https://github.com/geoffwright
[@gtrummell]: https://github.com/gtrummell
[@jeffwidman]: https://github.com/jeffwidman
[@jharley]: https://github.com/jharley
[@jpiron]: https://github.com/jpiron
[@jstoja]: https://github.com/jstoja
[@pdecat]: https://github.com/pdecat
[@pmbauer]: https://github.com/pmbauer
[@rouge8]: https://github.com/rouge8
[@the-real-cphilips]: https://github.com/the-real-cphilips
[@tomgoren]: https://github.com/tomgoren
[@xp-1000]: https://github.com/xp-1000