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

def gather_windows_info(device):
    session = winrm.Session(f'http://{device["ip"]}:5985/wsman', auth=(username, password))
    result = session.run_cmd('systeminfo')
    output = result.std_out.decode()
    
    # Parse output to extract relevant information as needed
    return {"name": device["name"], "info": output}

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
            # Add additional details here as necessary
        }

        ssh.close()
        return device_info
    except Exception as e:
        print(f"Failed to connect to {device['ip']}: {e}")
        return None

inventory = {"all": {"children": {"workstations": {"hosts": {}}}}}

for device in devices:
    if device["type"] == "windows":
        details = gather_windows_info(device)
    else:
        details = gather_linux_info(device)
    
    if details:
        inventory["all"]["children"]["workstations"]["hosts"][device["name"]] = details

with open('workstations_inventory.yaml', 'w') as file:
    yaml.dump(inventory, file, default_flow_style=False)

print("Workstations inventory saved to workstations_inventory.yaml")
