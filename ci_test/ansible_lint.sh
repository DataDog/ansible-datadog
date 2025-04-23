#!/bin/bash -e
# galaxy-importer requires ansible-lint https://github.com/ansible/galaxy-importer/blob/master/setup.cfg#L22
pip install -r requirements.txt

# Dry-run of galaxy-importer on legacy-role.
repo_dir=$(pwd) # use of importer must be done from parent repository
pushd ..
python3 -m galaxy_importer.main --legacy-role "$repo_dir" --namespace datadog 2>&1 | tee tmp_importer.log
# Filter out warnings for roles not found because location differs for macos or manual tests
grep -vq "^WARNING:.*the role '.*' was not found in .*" tmp_importer.log > importer.log
if grep -Eqi "(error|warning)" importer.log; then
    exit 1
fi
popd || exit

rm -rf ansible_collections
mkdir -p ansible_collections/datadog/dd/roles/agent/

for file in $(find . -type f -and \( -path '*defaults*' -or -path '*tasks*' -or -path '*templates*' -or -path '*handlers*' -or -name '.gitkeep' -or -path '*meta*' -or -name 'README.md' \));
do
    echo "Create ansible_collections/datadog/roles/agent/${file:2}"
    mkdir -p "$(dirname "ansible_collections/datadog/roles/agent/${file:2}")"
    cp -r "$file" "ansible_collections/datadog/roles/agent/${file:2}"
done
cat << EOF > ansible_collections/datadog/galaxy.yml
namespace: datadog
name: dd
version: 1.2.3
readme: README.md
authors:
  - Datadog
EOF
cat << EOF > ansible_collections/datadog/.ansible-lint-ignore
roles/agent/defaults/main.yml var-naming[no-role-prefix]
EOF

pushd ansible_collections/datadog/
ansible-galaxy collection build
popd

# explicitly install the ansible-lint version we need, despite what ansible-galaxy
# installed as its dependency
pip install -r requirements-ansible-lint.txt

# lint the ansible-role alone
ansible-lint -v --exclude=galaxy.yml --exclude=ci_test/ --exclude=manual_tests/ --exclude=.circleci/ --exclude=ansible_collections/

cd ansible_collections/datadog/ || exit
ls -la roles/agent/
ansible-lint -v --exclude=galaxy.yml --exclude=meta/
