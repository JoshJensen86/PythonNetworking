import paramiko
import time


switches = {
    '10.10.1.5': 'Switch_1',
    '10.10.1.6': 'Switch_2',
    '10.10.1.7': 'Switch_3',
    '10.10.1.8': 'Switch_4',
}

username = 'admin'
password = 'P@ssw0rd'


vlan_config = {
    'User_Network': {'vlan_id': 10, 'name': 'User_Network'},
    'ACCT_Network': {'vlan_id': 20, 'name': 'ACCT_Network'},
    'MGMT_Network': {'vlan_id': 30, 'name': 'MGMT_Network'},
    'IT_Network': {'vlan_id': 40, 'name': 'IT_Network'},
}

def configure_vlan(switch_ip, vlan_id, vlan_name):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        
        client.connect(switch_ip, username=username, password=password, look_for_keys=False, allow_agent=False)

        
        shell = client.invoke_shell()

        
        shell.send('enable\n')
        time.sleep(1)
        shell.send(f'configure terminal\n')
        time.sleep(1)
        shell.send(f'vlan {vlan_id}\n')
        time.sleep(1)
        shell.send(f'name {vlan_name}\n')
        time.sleep(1)
        shell.send(f'exit\n')
        time.sleep(1)

        
        shell.send('write memory\n')
        time.sleep(2)

        
        output = shell.recv(65535).decode('utf-8')
        print(f"Configuration Output for {switch_ip}:\n{output}")
        
    finally:
        
        client.close()


for switch_ip, switch_name in switches.items():
    print(f"Configuring VLANs on {switch_name} ({switch_ip})")
    for vlan in vlan_config.values():
        configure_vlan(switch_ip, vlan['vlan_id'], vlan['name'])
    print(f"Finished configuration on {switch_name}.\n")
