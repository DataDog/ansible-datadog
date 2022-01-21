# Linux test setup with Vagrant

This is an example setup, based on vagrant + virtualbox, that allows to easily run ansible commands to test the module.

## Requirements

- vagrant > 2.0.0
- virtualbox > 5.1.28

## Setup

From `ansible-datadog/manual_tests` directory:

- provision VM: `vagrant up ubuntu --provision --provision-with test_7_full.yml`
- when done, destroy VM if needed: `vagrant destroy -f`

To test with different agent versions or configurations, replace
`--provision-with` argument `test_7_full.yml` with any of the other
`test_*.yml` files in this directory.

To test on different operating systems, replace `ubuntu` with `centos` or `amazonlinux`.

If `vagrant up --provision` is used without any other parameters, all the
playbooks are applied one by one on an Ubuntu machine.

# Windows test setup from WSL

## Requirements

- Install Ansible and `pywinrm` inside WSL: `sudo python3 -m pip install  ansible pywinrm`
- From an elevated Powershell terminal (outside WSL), run the following script to setup WinRM so Ansible can connect:
https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1
- Make sure the Administrator account is enabled and you know the password (or use a different account in the `inventory_win` file).

## Setup

- From `ansible-datadog`'s parent directory, run in a WSL console (it will ask for the Administrator password each time):

```shell
ansible-playbook -k ansible-datadog/manual_tests/test_7_full.yml -i ansible-datadog/manual_tests/inventory_win
```

Note: Replace `test_7_full.yml` with any of the other yaml files on this directory.
