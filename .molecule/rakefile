# Molecule managed

require 'rake'
require 'rspec/core/rake_task'
require 'yaml'
require 'fileutils'

task spec: 'serverspec:all'
task default: :spec

hosts = YAML.load_file('.molecule/state.yml')['hosts']

namespace :serverspec do
  task all: hosts.keys
  hosts.each do |name, host|
    desc "Run serverspec on #{name}"
    pattern = ['spec/*_spec.rb', "spec/#{name}/*_spec.rb", "spec/hosts/#{name}/*_spec.rb"]

    host['groups'].each do |group|
      pattern << "spec/#{group}/*_spec.rb"
      pattern << "spec/groups/#{group}/*_spec.rb"
    end

    RSpec::Core::RakeTask.new(name.to_sym) do |target|
      puts "*** Run serverspec on #{name} ***"
      ENV['TARGET_HOST'] = name
      target.pattern = pattern.join(',')
    end
  end
end
