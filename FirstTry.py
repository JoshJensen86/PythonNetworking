import paramiko
import yaml

# SSH credentials
username = "admin"
password = ""  # No password for the devices
devices = [
    {"name": "switch1", "ip": "10.10.1.7"},
    {"name": "switch2", "ip": "10.10.1.5"},
    {"name": "switch3", "ip": "10.10.1.2"},
    {"name": "switch4", "ip": "10.10.1.6"},
    {"name": "switch5", "ip": "10.10.1.8"}
]

# Function to connect to a switch and retrieve information
def connect_and_gather_details(device):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device["ip"], username=username, password=password)

        # Example command to gather switch information
        stdin, stdout, stderr = ssh.exec_command("show version")
        output = stdout.read().decode('utf-8')

        # For simplicity, we'll use the output directly. You can parse details from 'show version' if needed
        device_info = {
            "name": device["name"],
            "general_settings": {
                "ram": "512 MB",  # Placeholder values
                "vcpus": "1",
                "qemu_binary": "/usr/bin/qemu-system-x86_64",
                "boot_priority": "CD/DVD-ROM or HDD",
                "on_close": "Power off the VM",
                "console_type": "telnet"
            },
            "network_settings": {
                "adapters": [
                    {
                        "total": "13",
                        "base_mac": "0c:xx:xx:xx:xx:xx",  # Placeholder
                        "type": "Realtek 8139 Ethernet (rtl8139)",
                        "replicate_network_state": True,
                        "ip": device["ip"],
                        "managementIP": device["ip"]  # Assuming same for management
                    }
                ]
            }
        }

        ssh.close()
        return device_info
    except Exception as e:
        print(f"Failed to connect to {device['ip']}: {e}")
        return None

# Gather details from all devices
inventory = {"all": {"children": {"switches": {"hosts": {}}}}}
for device in devices:
    details = connect_and_gather_details(device)
    if details:
        inventory["all"]["children"]["switches"]["hosts"][device["name"]] = details

# Save inventory to YAML file
with open('switches_inventory.yaml', 'w') as file:
    yaml.dump(inventory, file, default_flow_style=False)

print("Switches inventory saved to switches_inventory.yaml")
