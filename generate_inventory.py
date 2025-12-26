#!/usr/bin/env python3
import subprocess
from pathlib import Path


proc = subprocess.Popen(
    ["vagrant", "ssh-config"],
    stdout=subprocess.PIPE,
    universal_newlines=True,
    stderr=subprocess.PIPE
)

output, error = proc.communicate()

hosts = {}
current = None


if proc.stdout is None:
    raise RuntimeError("Failed to get ssh-config from Vagrant")


for line in output.splitlines():
    if line.startswith("Host "):
        current = line.split()[1]
        hosts[current] = {}
    elif current and "HostName" in line:
        hosts[current]["ip"] = line.split()[1]
    elif current and "User " in line:
        hosts[current]["user"] = line.split()[1]
    elif current and "IdentityFile" in line:
        hosts[current]["key"] = line.split()[1]

config = dict()
for name, data in hosts.items():
    config[name] = f"ansible_host={data['ip']} ansible_user={data['user']} ansible_ssh_private_key_file={data['key']}"

with open("inventory.ini", "w") as configfile:
    for name, entries in config.items():
        configfile.write(f"[{name}]\n")
        configfile.write(entries+"\n\n")

print("inventory.ini generated")
