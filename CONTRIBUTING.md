# Contributing

The code is licensed under the Apache License 2.0 (see LICENSE for details).

[![Ansible Galaxy](http://img.shields.io/badge/galaxy-Datadog.datadog-660198.svg)](https://galaxy.ansible.com/Datadog/datadog/)
[![Build Status](https://travis-ci.org/DataDog/ansible-datadog.svg?branch=master)](https://travis-ci.org/DataDog/ansible-datadog)

First of all, thanks for contributing!

This document provides some basic guidelines for contributing to this repository. To propose improvements, feel free to submit a PR.

## Submitting issues

* If you think you've found an issue, search the issue list to see if there's an existing issue.
* Then, if you find nothing, open a Github issue.

## Pull Requests

Have you fixed a bug or written a new feature and want to share it? Many thanks!

In order to ease/speed up our review, here are some items you can check/improve when submitting your PR:

  * Have a proper commit history (we advise you to rebase if needed).
  * Write tests for the code you wrote.
  * Preferably, make sure that all unit tests pass locally and some relevant kitchen tests.
  * Summarize your PR with an explanatory title and a message describing your changes, cross-referencing any related bugs/PRs.
  * Open your PR against the `master` branch.

Your pull request must pass all CI tests before we merge it. If you see an error and don't think it's your fault, it may not be! [Join us on Slack][slack] or send us an email, and together we'll get it sorted out.

### Keep it small, focused

Avoid changing too many things at once. For instance if you're fixing a recipe and at the same time adding some code refactor, it makes reviewing harder and the _time-to-release_ longer.

### Commit messages

Please don't be this person: `git commit -m "Fixed stuff"`. Take a moment to write meaningful commit messages.

The commit message should describe the reason for the change and give extra details that will allow someone later on to understand in 5 seconds the thing you've been working on for a day.

If your commit is only shipping documentation changes or example files, and is a complete no-op for the test suite, add **[skip ci]** in the commit message body to skip the build and give that slot to someone else who does need it.

### Squash your commits

Rebase your changes on `master` and squash your commits whenever possible. This keeps history cleaner and easier to revert things. It also makes developers happier!

## Development

To contribute, follow the contributing guidelines above.

### Manual testing

To test the roles provided by this project, you can follow the instructions in the manual tests [readme.md][tests].

### Integration testing

This project uses [Kitchen][kitchen] as an integration tests engine. To verify integration tests, install [Vagrant][vagrant] on your machine.

Kitchen allows you to test specific recipes described in [kitchen.yml][kitchen_yml]. There is only one basic recipe on ubuntu but that should be enough to develop others or to add features in TDD.

To list available targets, you can use the `list` command:

```bash
bundle exec kitchen list
```

To test a specific target, you can run:

```bash
bundle exec kitchen test <target>
```

So for example, if you want to test the agent installation, you can run:

```bash
bundle exec kitchen test default-ubuntu-1810
```

### Development loop

To develop some fixes or some features, the easiest way is to work on the platform and version of your choice, setting the machine up with the `create` command and applying the recipe with the `converge` command. If you want to explore the machine and try different things, you can also login into the machine with the `login` command.

```bash
# Create the relevant vagrant virtual machine
bundle exec kitchen create default-ubuntu-1810

# Converge to test your recipe
bundle exec kitchen converge default-ubuntu-1810

# Login to your machine to check stuff
bundle exec kitchen login default-ubuntu-1810

# Verify the integration tests for your machine
bundle exec kitchen verify default-ubuntu-1810

# Clean your machine
bundle exec kitchen destroy default-ubuntu-1810
```

It is advised that you work in TDD and that you write tests before making changes so that developing your feature or fix is just making tests pass.

## Author Information

brian@akins.org

dustinjamesbrown@gmail.com --Forked from brian@akins.org

Datadog <info@datadoghq.com> --Forked from dustinjamesbrown@gmail.com


[kitchen]: https://kitchen.ci
[kitchen_yml]: https://github.com/DataDog/ansible-datadog/blob/master/kitchen.yml
[slack]: http://datadoghq.slack.com
[tests]: https://github.com/DataDog/ansible-datadog/blob/master/manual_tests/readme.md
[vagrant]: https://www.vagrantup.com
