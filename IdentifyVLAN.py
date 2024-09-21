import paramiko

username = "admin"
password = ""  
devices = [
    {"name": "switch1", "ip": "10.10.1.7"},
    {"name": "switch2", "ip": "10.10.1.5"},
    {"name": "switch3", "ip": "10.10.1.24"},
    {"name": "switch4", "ip": "10.10.1.6"},
    {"name": "switch5", "ip": "10.10.1.8"}
]

def get_vlans(switch_ip, username):
    vlan_command = "show vlan brief"  
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(switch_ip, username=username)
        stdin, stdout, stderr = client.exec_command(vlan_command)
        vlans = stdout.read().decode()
        print(f"VLANs on {switch_ip}:\n{vlans}")
    except Exception as e:
        print(f"Failed to connect to {switch_ip}: {str(e)}")
    finally:
        client.close()


switches = ["10.10.1.5", "10.10.1.6", "10.10.1.7", "10.10.1.8"]
username = "admin"
password = ""

for switch in switches:
    get_vlans(switch, username)
