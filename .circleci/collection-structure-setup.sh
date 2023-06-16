#!/bin/bash

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

ls -la ansible_collections/datadog/dd/roles/agent/
