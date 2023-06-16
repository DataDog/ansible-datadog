#!/bin/bash

pip install ansible-lint==6.17 galaxy-importer

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
ansible-lint -v --profile=production --exclude=galaxy.yml --exclude=meta/
