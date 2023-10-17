#!/bin/bash
# galaxy-importer requires ansible-lint https://github.com/ansible/galaxy-importer/blob/master/setup.cfg#L22
pip install -r requirements.txt

# Dry-run of galaxy-importer on legacy-role.
repo_dir=$(pwd) # use of importer must be done from parent repository
pushd ..
python3 -m galaxy_importer.main --legacy-role "$repo_dir" --namespace datadog > tmp_importer.log 2>&1
# Filter out warnings for roles not found because location differs for macos or manual tests
grep -v "^WARNING:.*the role '.*' was not found in .*" tmp_importer.log > importer.log
if grep -Eqi "(error|warning)" importer.log; then
    cat importer.log
    exit 1
fi
popd || exit

# lint the ansible-role alone
ansible-lint -v --exclude=galaxy.yml --exclude=meta/ --exclude=ci_test/ --exclude=manual_tests/ --exclude=.circleci/

mkdir ansible_collections
cd ansible_collections || exit

ansible-galaxy collection build datadog.dd

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

