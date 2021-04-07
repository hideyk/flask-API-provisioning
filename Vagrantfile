# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
    v.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    v.customize ["modifyvm", :id, "--ioapic", "on"]
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/vagrant", "1"]
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/current", "1"]
    v.memory = "2048"
  end

  config.vm.synced_folder ".", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=664"]

  config.vm.define "db" do |machine|
    machine.vm.box = "ubuntu/xenial64"
    machine.vm.hostname = "flask-db1"
    machine.vm.network "private_network", ip: "172.17.177.22"
    machine.vm.provision :ansible_local do |ansible|
      ansible.playbook       = "provisioning/db.yml"
      ansible.verbose        = true
      ansible.install        = true
      ansible.limit          = "db" # or only "nodes" group, etc.
      ansible.inventory_path = "provisioning/inventory"
      ansible.galaxy_role_file = "requirements.yml"
      vagrant_synced_folder_default_type = ""
    end
  end

  config.vm.define "app" do |machine|
    machine.vm.box = "ubuntu/xenial64"
    machine.vm.hostname = "flask-app1"
    machine.vm.network :private_network, ip: "172.17.177.21"
    machine.vm.network :forwarded_port, guest: 5000, host: 5000
    machine.vm.provision :ansible_local do |ansible|
      ansible.playbook       = "provisioning/app.yml"
      ansible.verbose        = true
      ansible.install        = true
      ansible.limit          = "app" # or only "nodes" group, etc.
      ansible.inventory_path = "provisioning/inventory"
      
    end
  end
end
