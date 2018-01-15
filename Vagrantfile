# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/stretch64"
  config.vm.hostname = "sample1.example.com"
  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.provider :virtualbox do |v|
    v.memory = 1024
    v.cpus = 2
  end

  config.vm.provision "shell",
    inline: "sudo apt-get update && apt-get install -y ansible"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/main.yml"
  end
end
