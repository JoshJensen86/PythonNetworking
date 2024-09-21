import paramiko
import winrm
import yaml
import os

# Credentials
username = "student"
password = "P@ssw0rd"

# Device inventory
devices = [
    {"name": "Windows1", "ip": "10.10.1.10", "type": "windows"},
    {"name": "Windows2", "ip": "10.10.1.11", "type": "windows"},
    {"name": "Linux1", "ip": "10.10.1.12", "type": "linux"},
    {"name": "Linux2", "ip": "10.10.1.13", "type": "linux"},
    {"name": "TestBox1", "ip": "10.10.1.20", "type": "windows"},
    {"name": "TestBox2", "ip": "10.10.1.21", "type": "windows"},
]

# Function to gather info from Windows devices using WinRM
def gather_windows_info(device):
    try:
        session = winrm.Session(f'http://{device["ip"]}:5985/wsman', auth=(username, password))
        result = session.run_cmd('systeminfo')
        output = result.std_out.decode()

        # Parse output to extract relevant information
        print(f"Successfully gathered information from {device['name']} at {device['ip']}")
        return {"name": device["name"], "info": output}
    except Exception as e:
        print(f"Failed to gather information from {device['name']} ({device['ip']}): {e}")
        return None

# Function to gather info from Linux devices using Paramiko
def gather_linux_info(device):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device["ip"], username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command("uname -a")
        output = stdout.read().decode('utf-8')

        # Collect other required information
        device_info = {
            "name": device["name"],
            "info": output,
        }
        print(f"Successfully gathered information from {device['name']} at {device['ip']}")
        ssh.close()
        return device_info
    except Exception as e:
        print(f"Failed to connect to {device['name']} ({device['ip']}): {e}")
        return None

# Inventory structure
inventory = {"all": {"children": {"workstations": {"hosts": {}}}}}

# Loop through devices and gather information
for device in devices:
    if device["type"] == "windows":
        details = gather_windows_info(device)
    else:
        details = gather_linux_info(device)

    if details:
        inventory["all"]["children"]["workstations"]["hosts"][device["name"]] = details

# Attempt to write the inventory to a YAML file
try:
    with open('workstations_inventory.yaml', 'w') as file:
        yaml.dump(inventory, file, default_flow_style=False)
        print(f"Workstations inventory successfully saved to {os.path.abspath('workstations_inventory.yaml')}")
except Exception as e:
    print(f"Failed to write YAML file: {e}")
