import paramiko

username = "admin"
password = ""  # Update with the correct password if needed
devices = [
    {"name": "switch1", "ip": "10.10.1.7"},
    {"name": "switch2", "ip": "10.10.1.5"},
    {"name": "switch3", "ip": "10.10.1.24"},
    {"name": "switch4", "ip": "10.10.1.6"},
    {"name": "switch5", "ip": "10.10.1.8"}
]

def get_vlans(switch_ip, username, password):
    vlan_command = "show vlan"  # Updated command to retrieve VLAN information
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(switch_ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(vlan_command)
        
        # Capture output and errors
        vlans = stdout.read().decode()
        error = stderr.read().decode()
        
        if error:
            print(f"Error retrieving VLANs on {switch_ip}:\n{error}")
        else:
            print(f"VLANs on {switch_ip}:\n{vlans}")
    except Exception as e:
        print(f"Failed to connect to {switch_ip}: {str(e)}")
    finally:
        client.close()

for device in devices:
    get_vlans(device["ip"], username, password)
