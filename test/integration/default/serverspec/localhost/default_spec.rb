require 'spec_helper'

describe 'ansible-datadog::default' do
  describe file('/etc/datadog-agent') do
    it { should be_directory }
  end

  describe service('datadog-agent') do
    it { should be_enabled }
    it { should be_running }
  end
end
