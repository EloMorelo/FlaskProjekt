# Projekt aplikacji wraz ze srodowiskiem do testowania logowania itd.

## Wymagania potrzebne do uruchomienia projektu:
- nalezy posiadac zainstalowany WSL2 (https://devwords.pl/linux-wsl2-instalacja-na-windows-10/)
- włączone wsparcie HyperV w windows (https://learn.microsoft.com/pl-pl/windows-server/virtualization/hyper-v/get-started/install-hyper-v?tabs=powershell&pivots=windows)
- zainstalowany Vagrant zarowno na WSL jak i na Windows (https://developer.hashicorp.com/vagrant/install)
- zainstalowany w WSL-u git i ansible
- dostepny tryb administratora na maszynie z Windows

> [!CAUTION]
> Docker Desktop na Windows musi byc wylaczony przed uruchomieniem Vagranta z hyper-v jako providerem!

> [!IMPORTANT]   
> koniecznie Vagrant na Windows oraz WSL musi byc w tej samej wersji!
> Wszelkie uruchomienia Vagranta nalezy wykonywac z WSL-a ale w ścieżce Windowsowej (np. /mnt/c/Users/PC/user/projekt).
> Rozwiazanie powinno byc uruchamiane na Windows z polaczeniem kablowym (ethernet) poniewaz hyper-v ma problemy z przyznawaniem adresow IPv4, zamiast nich przypisuje IPv6 ktorego vagrant nie chce.

## Stworzenie sieci w hyper-v
Ponizej sa opisane kroki ktore nalezy wykonac w *powershellu w trybie administratora*, tworza one interfejs sieciowy w hyper-v ktory jest typu internal ale bedzie oferowac maszynom dostep do internetu

```powershell
New-VMSwitch -SwitchName "LabInternal" -SwitchType Internal
New-NetIPAddress -IPAddress 192.168.200.1 -PrefixLength 24 -InterfaceAlias "vEthernet (LabInternal)"
New-NetNat -Name "LabNat" -InternalIPInterfaceAddressPrefix "192.168.200.0/24"
```

## Uruchomienie maszyn wirtualnych
Aby to wykonac nalezy przejsc do WSL oraz do folderu zawierajaceo projekt a nastepnie wykonac:

```bash
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
vagrant up --provider=hyperv
```

## Reprovisioning maszyn wirtualnych
Aby zaczytac najnowsze zmiany konfiguracji ansible na maszynach wirtualnych nalezy uruchomic WSL i przejsc do folderu projektu:

Provisioning wszystkich maszyn:
```bash
vagrant up --provision
```

Provisioning konkretnej maszyny:
```bash
vagrant provision NAZWA_MASZYNY
```
gdzie NAZWA_MASZYNY to nazwa konkretnej maszyny.

Prezentacja: https://m365ht-my.sharepoint.com/:p:/r/personal/wrx81748_student_wroclaw_merito_pl/Documents/Analiza%20log%C3%B3w.pptx?d=w423a616329a64be3aa22648ccf0d3862&csf=1&web=1&e=AZrIVe