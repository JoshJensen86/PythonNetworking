import paramiko
import yaml
from datetime import datetime

# Define user credentials
username = "Local-Admin"
password = "WGU123"  # Placeholder for actual password

# Define devices (Windows desktops and test boxes)
devices = [
    {"name": "DesktopUser1", "ip": "10.10.1.10"},
    {"name": "DesktopUser2", "ip": "10.10.1.11"},
    {"name": "DesktopUser3", "ip": "10.10.1.12"},
    {"name": "DesktopUser4", "ip": "10.10.1.13"},
    {"name": "TestUser1_ACCT", "ip": "10.10.1.20"},  # ACCT_Network
    {"name": "TestUser2_MGMT", "ip": "10.10.1.21"}   # MGMT_Network
]

# Function to connect and gather details for each device
def connect_and_gather_details(device):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(device["ip"], username=username, password=password)

        # Placeholder for commands to gather general and network settings
        # Replace with actual commands to fetch the required settings
        general_settings_command = "get-general-settings"  # Replace with actual command
        network_settings_command = "get-network-settings"   # Replace with actual command

        general_settings_output = client.exec_command(general_settings_command)[1].read().decode('utf-8')
        network_settings_output = client.exec_command(network_settings_command)[1].read().decode('utf-8')

        # Constructing the device_info based on gathered data
        device_info = {
            "name": device["name"],
            "general_settings": {
                "ram": "8 GB",  # Example value, replace with parsed output
                "vcpus": "2",    # Example value, replace with parsed output
                "qemu_binary": "/usr/bin/qemu-system-x86_64",  # Example value
                "boot_priority": "HDD",  # Example value
                "on_close": "Power off",  # Example value
                "console_type": "RDP"  # Example value
            },
            "network_settings": {
                "adapters": [
                    {
                        "total": "1",
                        "base_mac": "00:1A:2B:3C:4D:5E",  # Example value, replace with parsed output
                        "type": "Virtual Ethernet",  # Example value
                        "replicate_network_state": True,
                        "ip": device["ip"]
                    }
                ]
            }
        }

        client.close()
        return device_info
    except Exception as e:
        print(f"Failed to connect to {device['ip']}: {e}")
        return None

# Inventory structure
inventory = {"all": {"children": {"workstations": {"hosts": {}}}}}
for device in devices:
    details = connect_and_gather_details(device)
    if details:
        inventory["all"]["children"]["workstations"]["hosts"][device["name"]] = details

# Save to YAML file
with open('workstations_inventory.yaml', 'w') as file:
    yaml.dump(inventory, file, default_flow_style=False)

print("Workstations inventory saved to workstations_inventory.yaml")
