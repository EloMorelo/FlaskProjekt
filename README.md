# Projekt aplikacji wraz ze srodowiskiem do testowania logowania itd.

## Wymagania potrzebne do uruchomienia projektu (Linux / libvirt)

Ten projekt jest skonfigurowany do uruchomienia lokalnego środowiska przy pomocy providera `libvirt` (KVM/QEMU). Poniższe instrukcje zakładają system Linux (Debian/Ubuntu lub pochodne). Jeśli chcesz uruchamiać projekt z Windows przy pomocy Hyper-V, pozostaw starą instrukcję, ale ta sekcja koncentruje się na środowisku Linux.

- Zainstalowany `vagrant` (2.x lub nowszy)
- `libvirt` + `qemu` + `virt-manager` na hoście
- Wtyczki Vagrant:
	- `vagrant-libvirt`
	- `vagrant-hostmanager` (opcjonalnie, do aktualizacji `/etc/hosts`)
- `ansible` dostępny na hoście (może być systemowy pakiet lub `pip`)
- `git` (do pobrania repo)
- Konto użytkownika dodane do grupy `libvirt` (lub uruchomienie komend z sudo)

Instalacja przykładowa (Debian/Ubuntu):

```bash
# Zainstaluj qemu/libvirt i narzędzia
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager

# Dodaj użytkownika do grupy libvirt (relokacja sesji po dodaniu)
sudo usermod -aG libvirt $(whoami)

# Zainstaluj Vagrant (jeśli nie masz)
# Pobierz paczkę ze strony Vagrant lub użyj menedżera pakietów (zależnie od dystrybucji)

# Zainstaluj wymagane pluginy Vagrant (upewnij się że masz build-essential)
vagrant plugin install vagrant-libvirt
vagrant plugin install vagrant-hostmanager

# Upewnij się, że ansible jest dostępny
sudo apt install -y ansible || pip install --user ansible
```

Ustawienie URI libvirt (jeśli wymagane)

W niektórych konfiguracjach warto ustawić URI do `qemu:///system`. Przykładowe polecenia (opcjonalne):

```bash
# stałe ustawienie dla libvirt (możesz utworzyć lub dopisać w pliku)
mkdir -p ~/.config/libvirt
echo 'uri_default = "qemu:///system"' >> ~/.config/libvirt/libvirt.conf

# eksporty sesji — w tej samej sesji terminala przed uruchomieniem vagranta
export LIBVIRT_DEFAULT_URI="qemu:///system"
export VAGRANT_LIBVIRT_URI="qemu:///system"
```

## Uruchomienie maszyn wirtualnych (libvirt)

Przejdź do katalogu projektu (gdzie jest `Vagrantfile`) i uruchom:

```bash
# Start wszystkich maszyn z providerem libvirt
vagrant up --provider=libvirt

# Start konkretnej maszyny
vagrant up app --provider=libvirt

# Sprawdź status
vagrant status
```

## Reprovisioning maszyn wirtualnych

Provisioning wszystkich maszyn:

```bash
vagrant up --provision --provider=libvirt
```

Provisioning konkretnej maszyny:

```bash
vagrant provision NAZWA_MASZYNY
```

gdzie `NAZWA_MASZYNY` to np. `app`, `elasticsearch`, `client` lub `wireshark`.

Prezentacja: https://m365ht-my.sharepoint.com/:p:/r/personal/wrx81748_student_wroclaw_merito_pl/Documents/Analiza%20log%C3%B3w.pptx?d=w423a616329a64be3aa22648ccf0d3862&csf=1&web=1&e=AZrIVe


## Przydatne polecenia i troubleshooting

Jeśli coś pójdzie nie tak z maszynami lub storage, poniższe polecenia mogą pomóc:

```bash
# Ustawienie domyślnego URI (powtórka/skrót)
echo 'uri_default = "qemu:///system"' >> ~/.config/libvirt/libvirt.conf
export LIBVIRT_DEFAULT_URI="qemu:///system"
export VAGRANT_LIBVIRT_URI="qemu:///system"

# Jeśli Ansible nie jest zainstalowany: (jedna z opcji)
sudo apt install -y ansible
# lub
pip install --user ansible

# Zainstaluj brakujące pluginy Vagrant (jeśli potrzeba)
vagrant plugin install vagrant-libvirt
vagrant plugin install vagrant-hostmanager

# Zamykanie wszystkich domen zawierających "Flask"
virsh list --all | grep "Flask" | awk '{print $2}' | xargs -r -I {} virsh destroy {}
virsh list --all | grep "Flask" | awk '{print $2}' | xargs -r -I {} virsh undefine --remove-all-storage {}

# Usuwanie wolumenów storage związanych z nazwą projektu
virsh vol-list default | grep "Flask" | awk '{print $1}' | xargs -r -I {} virsh vol-delete --pool default {}

# Sprawdź status sieci libvirt (domyślna sieć powinna być aktywna)
virsh net-list --all
virsh net-start default || true
virsh net-autostart default || true

# Więcej wskazówek:
# https://superuser.com/questions/1776277/no-internet-connection-in-vm-with-libvirt-nat
```

## libvirt + nftables (iptables compatibility) tip

libvirt historically has interoperability issues with nftables-only firewalls. If your distribution uses nftables and you experience networking problems for libvirt/KVM guests, the common workaround is to switch libvirt's firewall backend to use the iptables compatibility layer.

Steps (requires root):

```bash
# Install the iptables compatibility package (Debian/Ubuntu example)
sudo apt install -y iptables-nft

# Edit libvirt network config and set backend to iptables
sudo sed -i "s/^#\?\s*firewall_backend.*/firewall_backend = \"iptables\"/" /etc/libvirt/network.conf

# Restart or recycle the default network from virsh
sudo virsh net-destroy default || true
sudo virsh net-start default

# Or restart libvirt service if preferred
sudo systemctl restart libvirtd
```

Note: after changing `firewall_backend` you may need to destroy and start networks (or restart libvirt) for the change to take effect. If you are unsure about package names on your distro, check your package manager (e.g., `dnf`/`yum` on Fedora/CentOS or `apt` on Debian/Ubuntu).

## Fedora / RHEL — libvirt NAT and `firewalld` masquerade tip

On Fedora/RHEL derivatives `firewalld` controls NAT for libvirt networks. Sometimes the `libvirt` zone does not have masquerading enabled by default which prevents guests from accessing the Internet through NAT. Check the zone and enable masquerade if it's off:

```bash
# Inspect the libvirt zone (shows if masquerade is enabled)
sudo firewall-cmd --list-all --zone=libvirt

# If the output contains "masquerade: no", enable masquerade permanently:
sudo firewall-cmd --zone=libvirt --add-masquerade --permanent
sudo firewall-cmd --reload

# Restart services / networks to ensure changes are applied
sudo systemctl restart libvirtd
sudo systemctl restart firewalld

# Optionally restart the default network
sudo virsh net-destroy default || true
sudo virsh net-start default || true
```

This is a common fix on Fedora when guests cannot reach the Internet while the host firewall is active. If you manage libvirt networks manually, ensure the `libvirt` zone is the one applied to the virtual network interface(s) or adjust the zone accordingly.


## Elasticsearch Management

### Resetting the Elasticsearch Password

If you need to reset the password for the `elastic` user in Elasticsearch, you can use the following command:

```bash
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```

This command resets the password for the `elastic` user, which is the default superuser in Elasticsearch.