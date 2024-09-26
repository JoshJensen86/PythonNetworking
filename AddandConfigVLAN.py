import paramiko
import time


switches = {
    '10.10.1.7': 'Switch_1',
    '10.10.1.5': 'Switch_2',
    '10.10.1.6': 'Switch_4',
    '10.10.1.8': 'Switch_5',
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

        
        time.sleep(1)
        shell.recv(1000) 

    
        shell.send(f'create vlan {vlan_name} tag {vlan_id}\n')
        time.sleep(1)
        
        
        shell.send(f'configure vlan {vlan_name} add ports all\n')
        time.sleep(1)

    
        shell.send('save configuration\n')
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
