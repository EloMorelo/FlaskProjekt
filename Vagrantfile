# -*- mode: ruby -*-
# vi: set ft=ruby :

# Uruchamianie (konsola w trybie administratora): vagrant up --provider=hyperv

Vagrant.configure("2") do |config|
  config.vm.box = "assurea/ubuntu-24-04"
  config.vm.box_version = "1.2"

  # elasticsearch vm
  config.vm.define "elasticsearch" do |elasticsearch|
    elasticsearch.vm.provider "hyperv" do |h|
      h.vm_integration_services = {
        guest_service_interface: true,
        CustomVMSRV: true
      }
      h.cpus = 2
      h.maxmemory = 4096
      h.vmname = "elasticsearch"
    end
    elasticsearch.vm.network "private_network", ip: "192.168.200.10", bridge: "LabInternal"
    elasticsearch.vm.synced_folder ".", "/vagrant", disabled: true

    elasticsearch.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/elk.yml"
    end
  end

  # application vm
  config.vm.define "app" do |app|
    app.vm.provider "hyperv" do |h|
      h.vm_integration_services = {
        guest_service_interface: true,
        CustomVMSRV: true
      }
      h.cpus = 2
      h.maxmemory = 3072
      h.vmname = "app"
    end
    app.vm.network "private_network", ip: "192.168.200.11", bridge: "LabInternal"
    app.vm.synced_folder ".", "/vagrant", disabled: true

    app.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/app.yml"
    end
  end

  # client vm
  config.vm.define "client" do |client|
    client.vm.provider "hyperv" do |h|
      h.vm_integration_services = {
        guest_service_interface: true,
        CustomVMSRV: true
      }
      h.cpus = 1
      h.maxmemory = 1024
      h.vmname = "client"
    end
    client.vm.network "private_network", ip: "192.168.200.12", bridge: "LabInternal"
    client.vm.synced_folder ".", "/vagrant", disabled: true

    client.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/client.yml"
    end
end

  # wireshark vm
  config.vm.define "wireshark" do |wireshark|
    wireshark.vm.provider "hyperv" do |h|
      h.vm_integration_services = {
        guest_service_interface: true,
        CustomVMSRV: true
      }
      h.cpus = 1
      h.maxmemory = 2048
      h.vmname = "wireshark"
    end
    wireshark.vm.network "private_network", ip: "192.168.200.13", bridge: "LabInternal"
    wireshark.vm.synced_folder ".", "/vagrant", disabled: true

    wireshark.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/wireshark.yml"
    end
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
