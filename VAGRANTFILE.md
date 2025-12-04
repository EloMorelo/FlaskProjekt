# Vagrantfile documentation

Purpose
-------

This Vagrant configuration defines a small multi-VM lab for the FlaskProjekt workspace. It creates four virtual machines using the `libvirt` provider:

- `elasticsearch` — Elasticsearch node (provisioned with `ansible/elk.yml`)
- `app` — Application server (provisioned with `ansible/app.yml`)
- `client` — Client/test host (provisioned with `ansible/client.yml`)
- `wireshark` — Capture/analysis host (provisioned with `ansible/wireshark.yml`)

All VMs use the `generic/ubuntu2204` box (version pinned to `4.3.12`) and are attached to the libvirt `default` network with DHCP.

Prerequisites
-------------

- Vagrant (2.x recommended)
- libvirt + QEMU on the host
- Vagrant plugins:
  - `vagrant-libvirt` (provider)
  - `vagrant-hostmanager` (manages `/etc/hosts` entries on the host)
- Ansible (playbooks executed from host)

Installation examples
---------------------

```bash
# On a typical Debian/Ubuntu host
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients ebtables dnsmasq-base
sudo usermod -aG libvirt $(whoami)

# Install Vagrant (if not installed) and plugins
vagrant plugin install vagrant-libvirt
vagrant plugin install vagrant-hostmanager

# Ensure ansible is available
pip install --user ansible
```

Usage
-----

From the `FlaskProjekt` directory (where this `Vagrantfile` lives):

```bash
# Start all VMs with libvirt
vagrant up --provider=libvirt

# Start a single VM
vagrant up app --provider=libvirt

# Re-run the provisioners for a VM
vagrant provision <vm-name>

# Halt / Destroy
vagrant halt
vagrant destroy -f

# Check status
vagrant status
```

Provisioning notes
------------------

- Each VM runs a small shell provisioner that attempts to run `dhclient` and writes `nameserver 8.8.8.8` into `/etc/resolv.conf`.
- Primary provisioning is performed by Ansible playbooks located at `ansible/elk.yml`, `ansible/app.yml`, `ansible/client.yml`, and `ansible/wireshark.yml`.
- Hostnames are set inside each VM (e.g. `elasticsearch.lab.local`) and `vagrant-hostmanager` is used to update your host's `/etc/hosts` for convenience.

Customizing resources
---------------------

Edit the provider blocks in the `Vagrantfile` to change CPU and memory allocations. Example fields in the provider block:

- `h.cpus`
- `h.memory`
- `h.qemu_use_session` (set to `true` to use session libvirt instead of system)

Troubleshooting
---------------

- If Vagrant/libvirt fails with permission errors, ensure your user is in the `libvirt` group and relogin.
- If host entries are not created/updated, ensure the `vagrant-hostmanager` plugin is installed and enabled. You can also run `vagrant hostmanager`.
- If networking behaves unexpectedly, confirm the libvirt `default` network is active: `virsh net-list --all`.

Where to look next
------------------

- Ansible playbooks: the `ansible/` directory next to this `Vagrantfile` contains the provisioning logic for each VM.
- To change the base OS, update `main_config.vm.box` and the pinned `main_config.vm.box_version` in the `Vagrantfile`.

Polish (krótko)
---------------

Jest to konfiguracja Vagrant wykorzystująca provider `libvirt`. Uruchamia cztery maszyny (elasticsearch, app, client, wireshark) i provisionuje je przy pomocy Ansible. Uruchamianie: `vagrant up --provider=libvirt`.

---

If you want, I can also:

- Add a short `README.md` to the project root that references this documentation.
- Add example `vagrant` commands to a `Makefile` or script for convenience.
