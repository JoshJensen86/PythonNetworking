import paramiko
import winrm
import yaml

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

# Gather information from Windows workstations using WinRM
def gather_windows_info(device):
    try:
        session = winrm.Session(f'http://{device["ip"]}:5985/wsman', auth=(username, password))
        result = session.run_cmd('systeminfo')
        output = result.std_out.decode()
        
        # Parse output to extract relevant information
        return {"name": device["name"], "info": output}
    except Exception as e:
        print(f"Failed to gather information from {device['name']} ({device['ip']}): {e}")
        return None

# Gather information from Linux workstations using Paramiko
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

        ssh.close()
        return device_info
    except Exception as e:
        print(f"Failed to connect to {device['ip']}: {e}")
        return None

# Initialize inventory structure
inventory = {"all": {"children": {"workstations": {"hosts": {}}}}}

# Iterate over devices and gather information
for device in devices:
    if device["type"] == "windows":
        details = gather_windows_info(device)
    else:
        details = gather_linux_info(device)
    
    if details:
        inventory["all"]["children"]["workstations"]["hosts"][device["name"]] = details

# Save inventory to a YAML file
try:
    with open('workstations_inventory.yaml', 'w') as file:
        yaml.dump(inventory, file, default_flow_style=False)
    print("Workstations inventory successfully saved to workstations_inventory.yaml")
except Exception as e:
    print(f"Failed to write inventory to file: {e}")
