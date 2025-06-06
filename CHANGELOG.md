CHANGELOG
=========
# 5.2.1 / 2025-05-22
* [IMPROVEMENT] Provide bootstrap environment variables to installer only if not empty strings [#655]
* [IMPROVEMENT] Remove community.general.zypper reference [#658]
* [IMPROVEMENT] Only gather facts and services if notd done already [#659] [Thanks @POIFischbacher]
* [IMROVEMENT] [CI] Remove role prefix lint warnings [#660]
* [BUGFIX] [CI] Fix installer tests after 7.66.0 release [#657]

# 5.2.0 / 2025-05-21
* [IMPROVEMENT] Add feature to override the Datadog installer default package version [#652] Thanks [@snowman11784]
* [IMPROVEMENT] Add support to override datadog-apm-inject version [#654]

# 5.1.1 / 2025-05-07
* [DOCS] Remove centos 6/7 from readme [#647]
* [BUGFIX] Fix typo in fix-parse-version-windows.yml [#648] Thanks [@jacob9423]
* [IMPROVEMENT] [CI] Add FQCN checks to ansible-lint [#650]

# 5.1.0 / 2025-04-30
**This role removes support for Ansible Core versions below 2.10.**
* [IMPROVEMENT] Bump ansible-lint to 25.1.2 and fix compatibility issues [#644]
* [IMPROVEMENT] Bump ansible galaxy/lint version [#642]
* [BUGFIX] Fix Windows fqcn error [#645]

# 5.0.0 / 2025-04-21
**This role removes support for Python 2 and Agent 5, and bumps the minimum Ansible version for this role to 2.8** Additionally, it no longer supports older versions of Amazon Linux 2 and CentOS. While version 4 of the role will continue to receive backport updates, Ansible collections corresponding to version 4 of this role (Datadog Ansible Collection v5) will not be updated. We recommend upgrading to the latest version for better support and improvements. 

* [MAJOR] Remove support for Python 2 and Agent 5. [#639]
* [IMPROVEMENT] [CI] Explicitly set use: service to ensure compatibility in CI [#640]
* [IMPROVEMENT] [CI] Fix test_install_downgrade ci failures [#638]
 
# 4.30.0 / 2025-04-08
* [IMPROVEMENT] Add system_probe_other_config as catch all [#634]
* [DOCS] Fix typo [#635]

# 4.29.0 / 2025-03-03
* [IMPROVEMENT] Remove deprecated APM deb/rpms [#624]
* [IMPROVEMENT] [CI] Fix MacOS CI [#630]
* [BUGFIX] Fix Ansible check mode when installer/apm injection is enabled [#619]
* [DOCS] Add information for air-gapped installation [#622]
* [CHORE] Transfer ownership to container-ecosystems [#618]
* [CHORE] Remove agent-delivery as CODEOWNER [#629]

# 4.28.0 / 2024-09-24
* [IMPROVEMENT] Add ansible managed comment to checks.yaml [#602]
* [BUGFIX] Fix default APM setup [#608]
* [BUGFIX] Fix APM injector ownership logic [#604]
* [IMPROVEMENT] Allow pinned version of the agent with the installer [#605]
* [BUGFIX] Fix updated list of APM packages to install [#607]
* [BUGFIX] Fix role crash when pinning the agent version with the installer enabled [#609]
* [BUGFIX] Don't create system-probe config when it is disabled [#611]
* [BUGFIX] Fix distribution version detection on Amazon Linux 2023 [#612]

# 4.27.0 / 2024-08-26
* [BUGFIX] Process apm list again [#600]

# 4.26.0 / 2024-08-19
* [IMPROVEMENT] datadog-installer registry support [#596]
* [BUGFIX] Fix the datadog-installer on openSUSE [#594]

# 4.25.0 / 2024-08-06
* [BUGFIX] Correctly install datadog-installer on RHEL derivatives [#587]
* [BUGFIX] Enable datadog-installer when remote_updates is true [#588]
* [BUGFIX] Fix security-agent.yaml generation [#591]
* [BUGFIX] Don't install datadog-agent when owned by datadog-installer [#589]
* [BUGFIX] Fix APM config when owned by datadog-installer [#590]
* [IMPROVEMENT] Speed up conf.d checks [#584]
* [IMPROVEMENT] Don't sort configuration keys [#577]

# 4.24.0 / 2024-07-18
* [FEATURE] creating install.json file related to apm single step instrumation [#572]
* [FEATURE] add support for datadog-installer [#573]
* [FEATURE] add new future GPG key following 2024 GPG key rotation [#568]
* [BUGFIX] Correctly read install.json on remote computer [#575]
* [BUGFIX] Disable logging of datadog_windows_ddagentuser_password [#563]. Thanks [@a-rhodes]
* [BUGFIX] Use install.datadoghq.com instead of the dd-agent bucket link [#576]
* [BUGFIX] Fix ansible-lint warnings on latest version [#578]
* [DOCS] Update broken Ansible Galaxy URLs [#580] Thanks [@kaveet]
* [DOCS] README: fix broken links to ansible-galaxy [#571]

# 4.23.0 / 2024-06-04
* [FEATURE] Add version pinning and telemetry for APM tracer libraries [#541]
* [FEATURE] Allow using proxy for Windows downloads [#553]
* [IMPROVEMENT] Restrict the Agent version that can be installed on RHEL (and derivatives) < 7 [#556]
* [IMPROVEMENT] Install old RPM GPG key only when needed on Agent <= 7.35 [#561]
* [BUGFIX] Change `mode` to use string parameters [#528], thanks [@janorn]
* [BUGFIX] Allow 160 character long lines before wrapping [#529], thanks [@janorn]
* [BUGFIX] Properly detect when DEB package is installed [#551]
* [BUGFIX] Fix idempotency molecule test on Windows [#560]
* [BUGFIX] Remove `warn` argument that is not supported in newer Ansible versions [#566]
* [DOCS] Fix inter-readme links for integrations [#546], thanks [@valscion]
* [DOCS] Clarify that role variables are set in the `vars` section of the playbook [#550]
* [DOCS] [DOCS-7475] Replace install command for Windows [#559]

# 4.22.0 / 2024-01-25
* [IMPROVEMENT] Use Get-ItemProperty to retrieve Windows Agent version [#536]
* [DOCS] Add a note about required API Key since 4.21 [#538]

# 4.21.0 / 2023-12-04
* [FEATURE] [Windows] [AP-1946] Force reinstall if configuration changed [#509]
* [FEATURE] Adding yum repo configuration options [#517] thanks [@chipselden]
* [IMPROVEMENT] Remove usage of datadog-apm-library-all meta package, to make sure Ansible keeps updating the tracer packages if "all" is used in Ansible configuration [#532]
* [IMPROVEMENT] [CI] add call to importer in the role [#515]
* [IMPROVEMENT] [AP-2380] Hard fail if api_key is not provided [#512], [#505] thanks [@gopivalleru]
* [IMPROVEMENT] Bump XCode version from 13.3.0 to 13.4.1 [#511]
* [BUGFIX] correct syntax when checking for config changes [#523] thanks [@TomFromTA]
* [DOCS] [DOCS-6354] Update descriptions for APM role values [#520]
* [DOCS] [README] Add openSUSE/SLES `community.general` install instruction [#513]

# 4.20.1 / 2023-07-20
* [CI] Add `empty-string-compare` rule to ansible-lint [#506]

# 4.20.0 / 2023-07-18

* [FEATURE] Add support for configuring APM injection. See [#481].
* [FEATURE] Add support for `compliance_config`. See [#488].
* [IMPROVEMENT] Add an option to delete example check configs. See [#459]. Thanks [@rockaut].
* [IMPROVEMENT] Add new APT and RPM signing keys for the 2024 key rotation. See [#485].
* [BUGFIX] Make the `ansible.windows` collection optional again by refactoring integration-related tasks. See [#483].
* [BUGFIX] Modify integration updates task to prevent always changed status. See [#486].
* [DOCS] Clarifications on downgrade and integrations configuration. See [#501].

# 4.19.0 / 2023-05-10

* [IMPROVEMENT] Ensure user selected for macOS systemwide installation actually exists. See [#479].
* [BUGFIX] Refresh Datadog repository cache on Red Hat family systems to ensure DNF properly imports repodata signing keys to its cache. See [#478].

# 4.18.0 / 2023-01-12

* [DEPRECATION] Remove the old RPM GPG key 4172A230 from hosts that still trust it. This also removes the configuration variables `datadog_yum_gpgkey`, `datadog_zypper_gpgkey` and `datadog_zypper_gpgkey_sha256sum`. See [#466].

# 4.17.0 / 2023-01-04

* [FEATURE] Add support for Universal Service Monitoring sysprobe configuration. See [#458]. Thanks [@marcus-crane].
* [IMPROVEMENT] Lock Agent version using `includepkgs` in repofiles on Red Hat compatible platforms. See [#443]. Thanks [@sspans-sbp].
* [IMPROVEMENT] Prettify and fix yaml indentations. See [#448]. Thanks [@denzhel].
* [IMPROVEMENT] Add the possibility to prevent the zypper repository installation. See [#452]. Thanks [@jb-mayer].
* [IMPROVEMENT] Use `ansible_managed` instead of custom hardcoded message in managed files. See [#454]. Thanks [@jlosito].
* [BUGFIX] Fix version comparison tasks when using ansible-core RC version. See [#446].
* [BUGFIX] Fix running role multiple times in a row on SUSE compatible platforms. See [#453].
* [DOCS] Add troubleshooting instructions about `service_facts` breaking Ubuntu 20.04. See [#449].
* [DOCS] Clarify `datadog_config` behavior. See [#451]. Thanks [@hestonhoffman].

# 4.16.0 / 2022-07-11
* [FEATURE] Add macOS support. See [#437]. Thanks [@lc-applause].
* [BUGFIX] Remove temporary directory after APT key import. See [#442]. Thanks [@wisnij].
* [BUGFIX] Prevent security-agent startup if it's not configured. See [#438].

# 4.15.0 / 2022-04-20

* [IMPROVEMENT] Switch Agent start mode to delayed on Windows. See [#422].
* [BUGFIX] Fix installation of a newer pinned version by DNF. See [#429].

# 4.14.0 / 2022-02-08

* [FEATURE] Add tasks for creating custom Python checks. See [#408]. Thanks [@snorlaX-sleeps].
* [FEATURE] Support Rocky Linux and AlmaLinux. See [#418].
* [BUGFIX] Fix provisioning on Python 3 / Amazon Linux 2. See [#412]. Thanks [@moleskin-smile].
* [BUGFIX] Prevent dependency on `ansible.windows` with non-Windows nodes. See [#416].
* [BUGFIX] Don't display content of `DDAGENTUSER_PASSWORD` for Windows nodes. See [#415].
* [BUGFIX] Additional fixes for `jinja2_native = True` setting. See [#414].

# 4.13.0 / 2022-01-21

* [FEATURE] Add datadog_manage_config to disable changing the Agent config files. See [#410].
* [BUGFIX] Fix error: dict object has no attribute 'system'. See [#409]. Thanks [@stegar123].

# 4.12.0 / 2021-11-03

* [FEATURE] Add Cloud Workload Security Agent configuration. See [#375]. Thanks [@alsmola].
* [IMPROVEMENT] Avoid usage of `ansible_lsb` to not depend on `lsb-release` package on Debian. See [#377].
* [IMPROVEMENT] Check that `datadog_checks` is a mapping to avoid misconfiguration. See [#384]. Thanks [@soar].
* [IMPROVEMENT] Enable turning off the Agent 6.14 fix for Windows. See [#399].
* [DOCS] Mention limitations in enabling NPM on Windows. See [#396].
* [BUGFIX] Fix execution with `jinja2_native = True`. See [#383]. Thanks [@soar].

# 4.11.0 / 2021-07-05

* [IMPROVEMENT] Install datadog-signing-keys package on Debian/Ubuntu. See [#372].
* [IMPROVEMENT] Skip install on Linux systems when pinned version is already installed. See [#371].
* [IMPROVEMENT] Update 'http' URLs to 'https' wherever possible. See [#369].Thanks [@rossigee].
* [BUGFIX] Detect existing version in check mode on Windows. See [#364]. Thanks [@camjay].

# 4.10.0 / 2021-05-25

* [IMPROVEMENT] Make Windows package download behavior in check mode consistent with Linux. See [#359]. Thanks [@camjay].
* [BUGFIX] Remove `indentfirst` in system-probe.yaml.j2, making the role compatible with Jinja2 >= 3. See [#361]. Thanks [@tasktop-teho].
* [BUGFIX] Ensure gnupg is installed on Debian/Ubuntu. See [#358].

# 4.9.0 / 2021-05-06

* [IMPROVEMENT] Improvements for APT keys management. See [#351].
  * By default, get keys from keys.datadoghq.com, not the Ubuntu keyserver.
  * Always add the `DATADOG_APT_KEY_CURRENT.public` key (contains key used to sign current repodata).
  * Add `signed-by` option to all sources list lines.
  * On Debian >= 9 and Ubuntu >= 16, only add keys to `/usr/share/keyrings/datadog-archive-keyring.gpg`.
  * On older systems, also add the same keyring to `/etc/apt/trusted.gpg.d`.
* [BUGFIX] Don't set `repo_gpgcheck=1` by default on RHEL/CentOS 8.1 and on custom repos. See [#352].
* [BUGFIX] Change RPM key URLs to non-SNI versions to ensure the role continues to work with Python <= 2.7.9. See [#353].
* [DOCS] Add a note about installing marketplace integrations. See [#354].

# 4.8.2 / 2021-04-21

* [BUGFIX] Another fix for agent not restarting after a configuration change on Windows. See [#349].

# 4.8.1 / 2021-04-19

* [BUGFIX] Fix Agent not restarting after a configuration change on Windows. See [#347].

# 4.8.0 / 2021-04-13

* [FEATURE] Add NPM support for Windows. See [#335].
* [IMPROVEMENT] Split Windows handler into its own file, so we don't include anything from ansible.windows on non-Windows; add a note about the dependency on `ansible.windows`. See [#337].
* [IMPROVEMENT] Turn on `repo_gpgcheck` on RPM repositories by default. See [#341].
* [IMPROVEMENT] Align Windows agent to Linux so that service is disabled when `datadog_enabled` is `false`. See [#338]. Thanks [@erikhjensen].
* [BUGFIX] Fix system-probe enablement conditions. See [#336].
* [CHORE] Fix issues found by linter (fix file permissions, add `role_name` and `namespace` to `galaxy_info`, remove pre/post tasks). See [#340].

# 4.7.1 / 2021-03-23

* [BUGFIX] Revert addition of NPM support for Windows, which introduced multiple issues. See [#333].

# 4.7.0 / 2021-03-23

* [FEATURE] Enable configuring `gpgcheck` option on RPM repofiles. See [#324].
* [FEATURE] Add NPM support for Windows. See [#326].
* [IMPROVEMENT] Implement usage of multiple GPG keys in repofiles, use keys from keys.datadoghq.com. See [#325].
* [BUGFIX] Use the `dnf` task instead of `yum` when we detect that a Python 3 interpreter is used on a target host. See [#301].
* [DOCS] Lint README for Documentation style. See [#327].

# 4.6.0 / 2021-01-11

* [FEATURE] Allow removing checks. See [#151] and [#320]. Thanks [@Jno21].
* [BUGFIX] Make security-agent also affected by datadog_enabled. See [#318].
* [BUGFIX] Change configuration perms on Linux. See [#313]. Thanks [@loliee].
* [CHORE] Do not name the RPM repo file differently depending on the Agent version. See [#311].
* [CHORE] Replace facts from 'ansible_*' to using 'ansible_facts' dictionary. See [#304]. Thanks to [@samasc30].

# 4.5.0 / 2020-11-06

* [FEATURE] (Windows) Adds support for non-default installation and configuration directories.  See [#295][].
* [BUGFIX] Fixes handling of nil vs. defined but empty variables.  See [#303][].
* [BUGFIX] (Windows) Fixes incorrect service name when validating services.  See [#307][].
* [FEATURE] Adds support for the latest package signing keys.  See [#308][].
* [FEATURE] Adds support for the Datadog IOT agent.  See [#309][].

# 4.4.0 / 2020-09-30

* [BUGFIX] (Windows) Fix compatibility with Ansible 2.10. See [#289][].
* [FEATURE] Adds support for 3rd party integrations via the `datadog-agent integration` command. See [#291][].
* [BUGFIX] Updates apt cache prior to attempting install.  See [#297][].

# 4.3.0 / 2020-07-07

* [FEATURE] Record installation information for telemetry and troubleshooting purposes. See [#281][].
* [BUGFIX] Fix error when facts value doesn't exist on Redhat OS family of the arm architecture. See [#283][]. Thanks to [@kanga333][].
* [BUGFIX] (Windows) Fix idempotence when reinstalling same pinned version. See [#269][].

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
* [OTHER] Include names for `include_tasks`. See [#226][]. Thanks to [@the-real-cphillips][].

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
[#151]: https://github.com/DataDog/ansible-datadog/issues/151
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
[#269]: https://github.com/DataDog/ansible-datadog/issues/269
[#270]: https://github.com/DataDog/ansible-datadog/issues/270
[#271]: https://github.com/DataDog/ansible-datadog/issues/271
[#275]: https://github.com/DataDog/ansible-datadog/issues/275
[#281]: https://github.com/DataDog/ansible-datadog/issues/281
[#283]: https://github.com/DataDog/ansible-datadog/issues/283
[#289]: https://github.com/DataDog/ansible-datadog/issues/289
[#291]: https://github.com/DataDog/ansible-datadog/issues/291
[#295]: https://github.com/DataDog/ansible-datadog/issues/295
[#297]: https://github.com/DataDog/ansible-datadog/issues/297
[#301]: https://github.com/DataDog/ansible-datadog/issues/301
[#303]: https://github.com/DataDog/ansible-datadog/issues/303
[#304]: https://github.com/DataDog/ansible-datadog/issues/304
[#307]: https://github.com/DataDog/ansible-datadog/issues/307
[#308]: https://github.com/DataDog/ansible-datadog/issues/308
[#309]: https://github.com/DataDog/ansible-datadog/issues/309
[#311]: https://github.com/DataDog/ansible-datadog/issues/311
[#313]: https://github.com/DataDog/ansible-datadog/issues/313
[#318]: https://github.com/DataDog/ansible-datadog/issues/318
[#320]: https://github.com/DataDog/ansible-datadog/issues/320
[#324]: https://github.com/DataDog/ansible-datadog/issues/324
[#325]: https://github.com/DataDog/ansible-datadog/issues/325
[#326]: https://github.com/DataDog/ansible-datadog/issues/326
[#327]: https://github.com/DataDog/ansible-datadog/issues/327
[#333]: https://github.com/DataDog/ansible-datadog/issues/333
[#335]: https://github.com/DataDog/ansible-datadog/issues/335
[#336]: https://github.com/DataDog/ansible-datadog/issues/336
[#337]: https://github.com/DataDog/ansible-datadog/issues/337
[#338]: https://github.com/DataDog/ansible-datadog/issues/338
[#340]: https://github.com/DataDog/ansible-datadog/issues/340
[#341]: https://github.com/DataDog/ansible-datadog/issues/341
[#347]: https://github.com/DataDog/ansible-datadog/issues/347
[#349]: https://github.com/DataDog/ansible-datadog/issues/349
[#351]: https://github.com/DataDog/ansible-datadog/issues/351
[#352]: https://github.com/DataDog/ansible-datadog/issues/352
[#353]: https://github.com/DataDog/ansible-datadog/issues/353
[#354]: https://github.com/DataDog/ansible-datadog/issues/354
[#358]: https://github.com/DataDog/ansible-datadog/issues/358
[#359]: https://github.com/DataDog/ansible-datadog/issues/359
[#361]: https://github.com/DataDog/ansible-datadog/issues/361
[#362]: https://github.com/DataDog/ansible-datadog/issues/362
[#364]: https://github.com/DataDog/ansible-datadog/issues/364
[#369]: https://github.com/DataDog/ansible-datadog/issues/369
[#371]: https://github.com/DataDog/ansible-datadog/issues/371
[#372]: https://github.com/DataDog/ansible-datadog/issues/372
[#375]: https://github.com/DataDog/ansible-datadog/issues/375
[#377]: https://github.com/DataDog/ansible-datadog/issues/377
[#383]: https://github.com/DataDog/ansible-datadog/issues/383
[#384]: https://github.com/DataDog/ansible-datadog/issues/384
[#396]: https://github.com/DataDog/ansible-datadog/issues/396
[#399]: https://github.com/DataDog/ansible-datadog/issues/399
[#408]: https://github.com/DataDog/ansible-datadog/issues/408
[#409]: https://github.com/DataDog/ansible-datadog/issues/409
[#410]: https://github.com/DataDog/ansible-datadog/issues/410
[#412]: https://github.com/DataDog/ansible-datadog/issues/412
[#414]: https://github.com/DataDog/ansible-datadog/issues/414
[#415]: https://github.com/DataDog/ansible-datadog/issues/415
[#416]: https://github.com/DataDog/ansible-datadog/issues/416
[#418]: https://github.com/DataDog/ansible-datadog/issues/418
[#422]: https://github.com/DataDog/ansible-datadog/issues/422
[#429]: https://github.com/DataDog/ansible-datadog/issues/429
[#437]: https://github.com/DataDog/ansible-datadog/issues/437
[#438]: https://github.com/DataDog/ansible-datadog/issues/438
[#442]: https://github.com/DataDog/ansible-datadog/issues/442
[#443]: https://github.com/DataDog/ansible-datadog/issues/443
[#446]: https://github.com/DataDog/ansible-datadog/issues/446
[#448]: https://github.com/DataDog/ansible-datadog/issues/448
[#449]: https://github.com/DataDog/ansible-datadog/issues/449
[#451]: https://github.com/DataDog/ansible-datadog/issues/451
[#452]: https://github.com/DataDog/ansible-datadog/issues/452
[#453]: https://github.com/DataDog/ansible-datadog/issues/453
[#454]: https://github.com/DataDog/ansible-datadog/issues/454
[#458]: https://github.com/DataDog/ansible-datadog/issues/458
[#459]: https://github.com/DataDog/ansible-datadog/pull/459
[#466]: https://github.com/DataDog/ansible-datadog/issues/466
[#478]: https://github.com/DataDog/ansible-datadog/issues/478
[#479]: https://github.com/DataDog/ansible-datadog/issues/479
[#481]: https://github.com/DataDog/ansible-datadog/pull/481
[#483]: https://github.com/DataDog/ansible-datadog/pull/483
[#485]: https://github.com/DataDog/ansible-datadog/pull/485
[#486]: https://github.com/DataDog/ansible-datadog/pull/486
[#488]: https://github.com/DataDog/ansible-datadog/pull/488
[#501]: https://github.com/DataDog/ansible-datadog/pull/501
[#505]: https://github.com/DataDog/ansible-datadog/pull/505
[#509]: https://github.com/DataDog/ansible-datadog/pull/509
[#511]: https://github.com/DataDog/ansible-datadog/pull/511
[#512]: https://github.com/DataDog/ansible-datadog/pull/512
[#513]: https://github.com/DataDog/ansible-datadog/pull/513
[#515]: https://github.com/DataDog/ansible-datadog/pull/515
[#517]: https://github.com/DataDog/ansible-datadog/pull/517
[#520]: https://github.com/DataDog/ansible-datadog/pull/520
[#523]: https://github.com/DataDog/ansible-datadog/pull/523
[#528]: https://github.com/DataDog/ansible-datadog/pull/528
[#529]: https://github.com/DataDog/ansible-datadog/pull/529
[#532]: https://github.com/DataDog/ansible-datadog/pull/532
[#536]: https://github.com/DataDog/ansible-datadog/issues/536
[#538]: https://github.com/DataDog/ansible-datadog/issues/538
[#541]: https://github.com/DataDog/ansible-datadog/pull/541
[#546]: https://github.com/DataDog/ansible-datadog/pull/546
[#550]: https://github.com/DataDog/ansible-datadog/pull/550
[#551]: https://github.com/DataDog/ansible-datadog/pull/551
[#553]: https://github.com/DataDog/ansible-datadog/pull/553
[#556]: https://github.com/DataDog/ansible-datadog/pull/556
[#559]: https://github.com/DataDog/ansible-datadog/pull/559
[#560]: https://github.com/DataDog/ansible-datadog/pull/560
[#561]: https://github.com/DataDog/ansible-datadog/pull/561
[#563]: https://github.com/DataDog/ansible-datadog/pull/563
[#566]: https://github.com/DataDog/ansible-datadog/pull/566
[#568]: https://github.com/DataDog/ansible-datadog/pull/568
[#571]: https://github.com/DataDog/ansible-datadog/pull/571
[#572]: https://github.com/DataDog/ansible-datadog/pull/572
[#573]: https://github.com/DataDog/ansible-datadog/pull/573
[#575]: https://github.com/DataDog/ansible-datadog/pull/575
[#576]: https://github.com/DataDog/ansible-datadog/pull/576
[#577]: https://github.com/DataDog/ansible-datadog/pull/577
[#578]: https://github.com/DataDog/ansible-datadog/pull/578
[#584]: https://github.com/DataDog/ansible-datadog/pull/584
[#587]: https://github.com/DataDog/ansible-datadog/pull/587
[#588]: https://github.com/DataDog/ansible-datadog/pull/588
[#589]: https://github.com/DataDog/ansible-datadog/pull/589
[#590]: https://github.com/DataDog/ansible-datadog/pull/590
[#591]: https://github.com/DataDog/ansible-datadog/pull/591
[#594]: https://github.com/DataDog/ansible-datadog/pull/594
[#596]: https://github.com/DataDog/ansible-datadog/pull/596
[#600]: https://github.com/DataDog/ansible-datadog/pull/600
[#602]: https://github.com/DataDog/ansible-datadog/pull/602
[#604]: https://github.com/DataDog/ansible-datadog/pull/604
[#605]: https://github.com/DataDog/ansible-datadog/pull/605
[#607]: https://github.com/DataDog/ansible-datadog/pull/607
[#608]: https://github.com/DataDog/ansible-datadog/pull/608
[#609]: https://github.com/DataDog/ansible-datadog/pull/609
[#611]: https://github.com/DataDog/ansible-datadog/pull/611
[#612]: https://github.com/DataDog/ansible-datadog/pull/612
[#618]: https://github.com/DataDog/ansible-datadog/pull/619
[#619]: https://github.com/DataDog/ansible-datadog/pull/619
[#622]: https://github.com/DataDog/ansible-datadog/pull/622
[#624]: https://github.com/DataDog/ansible-datadog/pull/624
[#629]: https://github.com/DataDog/ansible-datadog/pull/629
[#630]: https://github.com/DataDog/ansible-datadog/pull/630
[#634]: https://github.com/DataDog/ansible-datadog/pull/634
[#635]: https://github.com/DataDog/ansible-datadog/pull/635
[#638]: https://github.com/DataDog/ansible-datadog/pull/638
[#639]: https://github.com/DataDog/ansible-datadog/pull/639
[#640]: https://github.com/DataDog/ansible-datadog/pull/640
[#642]: https://github.com/DataDog/ansible-datadog/pull/642
[#644]: https://github.com/DataDog/ansible-datadog/pull/644
[#645]: https://github.com/DataDog/ansible-datadog/pull/645
[#647]: https://github.com/DataDog/ansible-datadog/pull/647
[#648]: https://github.com/DataDog/ansible-datadog/pull/648
[#650]: https://github.com/DataDog/ansible-datadog/pull/650
[#652]: https://github.com/DataDog/ansible-datadog/pull/652
[#654]: https://github.com/DataDog/ansible-datadog/pull/654
[#655]: https://github.com/DataDog/ansible-datadog/pull/655
[#657]: https://github.com/DataDog/ansible-datadog/pull/657
[#658]: https://github.com/DataDog/ansible-datadog/pull/658
[#659]: https://github.com/DataDog/ansible-datadog/pull/659
[#660]: https://github.com/DataDog/ansible-datadog/pull/660
[@DevKyleS]: https://github.com/DevKyleS
[@Jno21]: https://github.com/Jno21
[@alsmola]: https://github.com/alsmola
[@b2jrock]: https://github.com/b2jrock
[@brendanlong]: https://github.com/brendanlong
[@camjay]: https://github.com/camjay
[@dbr1993]: https://github.com/dbr1993
[@denzhel]: https://github.com/denzhel
[@dv9io0o]: https://github.com/dv9io0o
[@enarciso]: https://github.com/enarciso
[@eplanet]: https://github.com/eplanet
[@erikhjensen]: https://github.com/erikhjensen
[@geoffwright]: https://github.com/geoffwright
[@gtrummell]: https://github.com/gtrummell
[@hestonhoffman]: https://github.com/hestonhoffman
[@janorn]: https://github.com/janorn
[@jb-mayer]: https://github.com/jb-mayer
[@jeffwidman]: https://github.com/jeffwidman
[@jharley]: https://github.com/jharley
[@jlosito]: https://github.com/jlosito
[@jpiron]: https://github.com/jpiron
[@jstoja]: https://github.com/jstoja
[@kanga333]: https://github.com/kanga333
[@lc-applause]: https://github.com/lc-applause
[@loliee]: https://github.com/loliee
[@marcus-crane]: https://github.com/marcus-crane
[@moleskin-smile]: https://github.com/moleskin-smile
[@pdecat]: https://github.com/pdecat
[@pmbauer]: https://github.com/pmbauer
[@rockaut]: https://github.com/rockaut
[@rossigee]: https://github.com/rossigee
[@rouge8]: https://github.com/rouge8
[@samasc30]: https://github.com/samasc30
[@snorlaX-sleeps]: https://github.com/snorlaX-sleeps
[@soar]: https://github.com/soar
[@sspans-sbp]: https://github.com/sspans-sbp
[@stegar123]: https://github.com/stegar123
[@tasktop-teho]: https://github.com/tasktop-teho
[@the-real-cphillips]: https://github.com/the-real-cphillips
[@tomgoren]: https://github.com/tomgoren
[@wisnij]: https://github.com/wisnij
[@xp-1000]: https://github.com/xp-1000
[@TomFromTA]: https://github.com/TomFromTA
[@chipselden]: https://github.com/chipselden
[@gopivalleru]: https://github.com/gopivalleru
[@valscion]: https://github.com/valscion
[@a-rhodes]: https://github.com/a-rhodes
[@kaveet]: https://github.com/kaveet
[@jacob9423]: https://github.com/jacob9423
[@snowman11784]: https://github.com/snowman11784
[@POIFischbacher]: https://github.com/POIFischbacher
