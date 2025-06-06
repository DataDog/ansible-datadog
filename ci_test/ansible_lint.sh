#!/bin/bash -e

# Install Python 3.10 if not already installed
if ! command -v python3.10 &> /dev/null; then
    echo "Installing Python 3.10..."
    apt update
    apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
    wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
    tar -xf Python-3.10.13.tgz
    cd Python-3.10.13
    ./configure --enable-optimizations
    make -j $(nproc)
    make altinstall
    cd ..
    rm -rf Python-3.10.13 Python-3.10.13.tgz
fi

# Check Python version
python_version=$(python3.10 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$python_version < 3.10" | bc -l) )); then
    echo "Error: Python 3.10 or higher is required. Found version $python_version"
    exit 1
fi

# Create and activate virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

# galaxy-importer requires ansible-lint https://github.com/ansible/galaxy-importer/blob/master/setup.cfg#L22
python3.10 -m pip install -r requirements.txt

# Dry-run of galaxy-importer on legacy-role.
repo_dir=$(pwd) # use of importer must be done from parent repository
pushd ..
echo "Using Python version: $(python3.10 --version)"
echo "Python path: $(which python3.10)"
python3.10 -m galaxy_importer.main --legacy-role "$repo_dir" --namespace datadog 2>&1 | tee tmp_importer.log
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

# Install required collections for linting
ansible-galaxy collection install ansible.windows

# lint the ansible-role alone
ansible-lint -v --exclude=galaxy.yml --exclude=ci_test/ --exclude=manual_tests/ --exclude=.circleci/ --exclude=ansible_collections/ --exclude=.ansible/ --exclude=.venv/

cd ansible_collections/datadog/ || exit
ls -la roles/agent/
ansible-lint -v --exclude=galaxy.yml --exclude=meta/ --exclude=.ansible/ --exclude=.venv/
