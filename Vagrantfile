# -*- mode: ruby -*-
# vi: set ft=ruby :

=begin
Vagrant environment for the FlaskProjekt lab (libvirt provider).

Purpose:
- Defines four VMs: `elasticsearch`, `app`, `client`, and `wireshark`.
- Each VM is provisioned via Ansible playbooks located in `ansible/*.yml`.

Quick usage:
- Start: `vagrant up --provider=libvirt`
- Re-provision a VM: `vagrant provision <name>`
- Halt: `vagrant halt`
- Destroy: `vagrant destroy -f`

Prerequisites:
- Vagrant (>=2.2 recommended)
- `vagrant-libvirt` plugin (for libvirt/KVM provider)
- `vagrant-hostmanager` plugin (optional, used here to manage host entries)
- `ansible` installed locally or available to Vagrant
- libvirt/qemu configured on the host

Troubleshooting tips:
- If libvirt/qemu permission errors occur, add your user to `libvirt` group and relogin:
  `sudo usermod -aG libvirt $(whoami)`
- If you prefer session mode, set `h.qemu_use_session = true` in provider blocks.
- Hostname-to-IP mapping is handled by `vagrant-hostmanager`; check its config if hosts aren't updated.

Notes:
- VMs use DHCP on the libvirt `default` network. Each VM runs a small shell provisioner to request DHCP and set `/etc/resolv.conf` to `8.8.8.8`.
- Adjust CPU/memory in the provider blocks for each VM as needed.
=end

enable_https = ENV["ENABLE_HTTPS"] == "1"

Vagrant.configure("2") do |main_config|
  main_config.vm.box = "generic/ubuntu2204"
  main_config.vm.box_version = "4.3.12"

  main_config.hostmanager.ignore_private_ip = false
  main_config.hostmanager.include_offline = true
  # main_config.hostmanager.manage_host = false

  # elasticsearch vm
  main_config.vm.define "elasticsearch" do |config|
    config.vm.provider "libvirt" do |h|
      h.cpus = 2
      h.memory = 4096
      h.random_hostname = false
      h.qemu_use_session = false
      h.nic_model_type = "virtio"
      h.nic_adapter_count = 1
      h.machine_arch = "x86_64"
    end

    config.vm.provision :hostmanager

    config.vm.network "private_network",
      libvirt__network_name: "default",
      type: "dhcp"

    config.vm.hostname = "elasticsearch.lab.local"

  config.vm.provision "shell" do |sh|
    sh.inline = <<-EOF
      sudo dhclient -v || true
      echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf
    EOF
  end

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/elk.yml"

      if enable_https
        ansible.extra_vars = {enable_https: true}
      else
        ansible.extra_vars = {enable_https: false}
      end
    end
  end

  # application vm
  main_config.vm.define "app" do |config|
    config.vm.provider "libvirt" do |h|
      h.cpus = 2
      h.memory = 3072
      h.random_hostname = false
      h.qemu_use_session = false
      h.nic_model_type = "virtio"
      h.nic_adapter_count = 1
      h.machine_arch = "x86_64"
    end

    config.vm.network "private_network",
      libvirt__network_name: "default",
      type: "dhcp"

    config.vm.provision :hostmanager

    config.vm.hostname = "app.lab.local"

    config.vm.provision "shell" do |sh|
      sh.inline = <<-EOF
        sudo dhclient -v || true
        echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf
      EOF
    end

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/app.yml"

      if enable_https
        ansible.extra_vars = {enable_https: true}
      else
        ansible.extra_vars = {enable_https: false}
      end
    end
  end

  # client vm
  main_config.vm.define "client" do |config|
    config.vm.provider "libvirt" do |h|
      h.cpus = 1
      h.memory = 1024
      h.random_hostname = false
      h.qemu_use_session = false
      h.nic_model_type = "virtio"
      h.nic_adapter_count = 1
      h.machine_arch = "x86_64"
    end

    config.vm.network "private_network",
      libvirt__network_name: "default",
      type: "dhcp"
    
    config.vm.provision :hostmanager

    config.vm.provision "shell" do |sh|
      sh.inline = <<-EOF
        sudo dhclient -v || true
        echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf
      EOF
    end

    config.vm.hostname = "client.lab.local"

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/client.yml"
    end
  end

  # wireshark vm
  main_config.vm.define "wireshark" do |config|
    config.vm.provider "libvirt" do |h|
      h.cpus = 1
      h.memory = 2048
      h.random_hostname = false
      h.qemu_use_session = false
      h.nic_model_type = "virtio"
      h.nic_adapter_count = 1
      h.graphics_type = "spice"
      h.video_accel3d = true
      h.machine_arch = "x86_64"
      
      # libvirt.xml = <<-EOF
      #   <graphics type='spice' autoport='yes' listen='none'>
      #     <gl enable='yes'/>
      #   </graphics>
  
      #   <video>
      #     <model type='virtio' accel3d='yes' primary='yes'/>
      #   </video>
  
      #   <channel type='spicevmc'>
      #     <target type='virtio' name='com.redhat.spice.0'/>
      #   </channel>
      # EOF
    end
    
    config.vm.provision :hostmanager

    config.vm.provision "shell" do |sh|
      sh.inline = <<-EOF
        sudo dhclient -v || true
        echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf
      EOF
    end

    config.vm.network "private_network",
      libvirt__network_name: "default",
      type: "dhcp"

    config.vm.hostname = "wireshark.lab.local"

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/wireshark.yml"
    end
  end
end
