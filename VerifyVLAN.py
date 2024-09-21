import paramiko
import time


switches = {
    '10.10.1.5': 'Switch_1',
    '10.10.1.6': 'Switch_2',
    '10.10.1.7': 'Switch_3',
    '10.10.1.8': 'Switch_4',
}

username = 'admin'
password = ''


vlan_ids = [10, 20, 30, 40]

def check_vlan(switch_ip):
   
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        
        client.connect(switch_ip, username=username, password=password, look_for_keys=False, allow_agent=False)

        
        shell = client.invoke_shell()

        
        shell.send('enable\n')
        time.sleep(1)
        shell.send('show vlan\n')
        time.sleep(2)

        
        output = shell.recv(65535).decode('utf-8')

        
        for vlan_id in vlan_ids:
            if f"VLAN{vlan_id}" in output or f"{vlan_id}" in output:
                print(f"VLAN {vlan_id} is configured on switch {switch_ip}.")
            else:
                print(f"VLAN {vlan_id} is NOT configured on switch {switch_ip}.")

    finally:
        
        client.close()


for switch_ip, switch_name in switches.items():
    print(f"Checking VLANs on {switch_name} ({switch_ip})")
    check_vlan(switch_ip)
    print(f"Finished checking VLANs on {switch_name}.\n")
