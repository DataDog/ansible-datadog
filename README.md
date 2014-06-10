Ansible Datadog Role
========

Install and configure datadog agent. Currently only handles base agent.

May extend to handle some service monitoring in the future.

Requirements
------------

Ubuntu

Role Variables
--------------

- `datadog_api_key` - your datadog API key

Dependencies
------------
None

Example Playbook
-------------------------

    - hosts: servers
      roles:
         - { role: bakins.datadog, datadog_api_key: "mykey" }

License
-------

Apache2

Author Information
------------------

brian@akins.org
