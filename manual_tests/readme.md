# Test setup

This is an example setup, based on vagrant + virtualbox, that allows to easily run ansible commands to test the module.

# Requirements

- vagrant > 2.0.0
- virtualbox > 5.1.28

# Setup

in `$WORK_DIR/ansible-datadog/manual_tests`:

- provision VM: `vagrant up`
- connect to the VM to check the configuration: `vagrant ssh`
- destroy VM when needed: `vagrant destroy -f`

in `$WORK_DIR`:

- run ansible-playbook: `ansible-playbook ansible-datadog/manual_tests/test_5_full.yml -i ansible-datadog/manual_tests/inventory`
