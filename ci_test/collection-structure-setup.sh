#!/bin/bash
# galaxy-importer requires ansible-lint https://github.com/ansible/galaxy-importer/blob/master/setup.cfg#L22
pip install -r requirements.txt

# Dry-run of galaxy-importer on legacy-role.
# Requires galaxy-importer > 0.4.10, whereas ansible-galaxy currently uses 0.4.0.post1 https://github.com/ansible/galaxy/blob/devel/requirements/requirements.in#L4
# So we do not use same version in role and collection
repo_dir=$(pwd) # use of importer must be done from parent repository
pushd ..
python3 -m galaxy_importer.main --legacy-role "$repo_dir" --namespace datadog
popd || exit

# lint the ansible-role alone
ansible-lint -v --exclude=galaxy.yml --exclude=meta/ --exclude=ci_test/ --exclude=manual_tests/ --exclude=.circleci/

mkdir ansible_collections
cd ansible_collections || exit

ansible-galaxy collection init datadog.dd

mkdir -p datadog/dd/roles/agent/
cd ..

for file in $(find . -type f -and \( -path '*defaults*' -or -path '*tasks*' -or -path '*templates*' -or -path '*handlers*' -or -name '.gitkeep' -or -path '*meta*' -or -name 'README.md' \));
do
    echo "Create ansible_collections/datadog/dd/roles/agent/${file:2}"
    mkdir -p "$(dirname "ansible_collections/datadog/dd/roles/agent/${file:2}")"
    cp -r "$file" "ansible_collections/datadog/dd/roles/agent/${file:2}"
done

cd ansible_collections/datadog/dd/ || exit

ls -la roles/agent/
ansible-lint -v --exclude=galaxy.yml --exclude=meta/

