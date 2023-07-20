#!/bin/bash

pip install ansible-lint==6.17 galaxy-importer

# lint the ansible-role alone
ansible-lint -v --exclude=galaxy.yml --exclude=meta/ --exclude=ci_test/ --exclude=manual_tests/ --exclude=.circleci/

mkdir ansible_collections
cd ansible_collections

ansible-galaxy collection init datadog.dd 

mkdir -p datadog/dd/roles/agent/
cd ..

for file in $(find . -type f -and \( -path '*defaults*' -or -path '*tasks*' -or -path '*templates*' -or -path '*handlers*' -or -name '.gitkeep' -or -path '*meta*' -or -name 'README.md' \)); 
do
    echo "Create ansible_collections/datadog/dd/roles/agent/${file:2}"
    mkdir -p $(dirname "ansible_collections/datadog/dd/roles/agent/${file:2}")
    cp -r "$file" "ansible_collections/datadog/dd/roles/agent/${file:2}"
done

cd ansible_collections/datadog/dd/

ls -la roles/agent/
ansible-lint -v --exclude=galaxy.yml --exclude=meta/
