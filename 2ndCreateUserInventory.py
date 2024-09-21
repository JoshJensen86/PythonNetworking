import paramiko
import winrm
import yaml


devices = {
    'workstation1': {
        'ip': '10.10.1.35',
        'type': 'windows',
        'general_settings': {
            'name': 'WindowsDesktop-1',
            'ram': '4096 MB',
            'vcpus': '2',
            'qemu_binary': '/bin/qemu-system-x86_64',
            'boot_priority': 'HDD',
            'on_close': 'Send the shutdown signal (ACPI)',
            'console_type': 'vnc'
        },
        'network_settings': {
            'adapters': [{
                'name': 'Ethernet0',
                'base_mac': '0c:4b:3c:0a:00:00',
                'type': 'Intel Gigabit Ethernet (e1000)',
                'replicate_network_state': True,
                'ip': '10.10.1.35'
            }]
        }
    },
    'workstation2': {
        'ip': '10.10.1.36',
        'type': 'windows',
        'general_settings': {
            'name': 'Workstation2WindowsDesktop-2',
            'ram': '4096 MB',
            'vcpus': '2',
            'qemu_binary': '/bin/qemu-system-x86_64',
            'boot_priority': 'HDD',
            'on_close': 'Send the shutdown signal (ACPI)',
            'console_type': 'vnc'
        },
        'network_settings': {
            'adapters': [{
                'name': 'Ethernet0',
                'base_mac': '0c:59:fd:86:00:00',
                'type': 'Intel Gigabit Ethernet (e1000)',
                'replicate_network_state': True,
                'ip': '10.10.1.36'
            }]
        }
    },
    'workstation3': {
        'ip': '10.10.1.43',
        'type': 'windows',
        'general_settings': {
            'name': 'WindowsDesktop-3',
            'ram': '4096 MB',
            'vcpus': '2',
            'qemu_binary': '/bin/qemu-system-x86_64',
            'boot_priority': 'HDD',
            'on_close': 'Send the shutdown signal (ACPI)',
            'console_type': 'vnc'
        },
        'network_settings': {
            'adapters': [{
                'name': 'Ethernet0',
                'base_mac': '0c:e2:07:f3:00:00',
                'type': 'Intel Gigabit Ethernet (e1000)',
                'replicate_network_state': True,
                'ip': '10.10.1.43'
            }]
        }
    },
    'workstation4': {
        'ip': '10.10.1.29',
        'type': 'windows',
        'general_settings': {
            'name': 'WindowsDesktop-4',
            'ram': '4096 MB',
            'vcpus': '2',
            'qemu_binary': '/bin/qemu-system-x86_64',
            'boot_priority': 'HDD',
            'on_close': 'Send the shutdown signal (ACPI)',
            'console_type': 'vnc'
        },
        'network_settings': {
            'adapters': [{
                'name': 'Ethernet0',
                'base_mac': '0c:46:74:35:00:00',
                'type': 'Intel Gigabit Ethernet (e1000)',
                'replicate_network_state': True,
                'ip': '10.10.1.29'
            }]
        }
    },
   
    'workstation5': {
        'ip': '10.10.1.56',
        'type': 'linux',
        'general_settings': {
            'name': 'Test_Box_1',
            'ram': '4096 MB',
            'vcpus': '2',
            'qemu_binary': '/bin/qemu-system-x86_64',
            'boot_priority': 'HDD',
            'on_close': 'Send the shutdown signal (ACPI)',
            'console_type': 'vnc'
        },
        'network_settings': {
            'adapters': [{
                'name': 'Ethernet0',
                'base_mac': '0c:cb:a8:90:00:00',
                'type': 'Intel Gigabit Ethernet (e1000)',
                'replicate_network_state': True,
                'ip': '10.10.1.56'
            }]
        }
    },
    'workstation6': {
        'ip': '10.10.1.57',
        'type': 'linux',
        'general_settings': {
            'name': 'Test_Box_2',
            'ram': '4096 MB',
            'vcpus': '2',
            'qemu_binary': '/bin/qemu-system-x86_64',
            'boot_priority': 'HDD',
            'on_close': 'Send the shutdown signal (ACPI)',
            'console_type': 'vnc'
        },
        'network_settings': {
            'adapters': [{
                'name': 'Ethernet0',
                'base_mac': '0c:50:a2:8a:00:00',
                'type': 'Intel Gigabit Ethernet (e1000)',
                'replicate_network_state': True,
                'ip': '10.10.1.57'
            }]
        }
    }
}


def gather_linux_info(ip):
    try:
        print(f"Gathering information from Linux workstation at {ip}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username='student', password='P@ssw0rd')
        stdin, stdout, stderr = ssh.exec_command('uname -a')
        output = stdout.read().decode().strip()
        print(output)
        ssh.close()
    except Exception as e:
        print(f"Failed to connect to Linux workstation at {ip}: {e}")


def gather_windows_info(ip, username, password):
    try:
        print(f"Gathering information from Windows workstation at {ip}...")
        session = winrm.Session(f'http://{ip}:5985/wsman', auth=(username, password))
        result = session.run_cmd('systeminfo')
        print(result.std_out.decode())
    except Exception as e:
        print(f"Failed to connect to Windows workstation at {ip}: {e}")


def create_inventory_file(devices):
    inventory = {'all': {'hosts': {}}}
    
    for name, device in devices.items():
        inventory['all']['hosts'][name] = {
            'general_settings': device['general_settings'],
            'network_settings': device['network_settings']
        }

    with open('inventory.yaml', 'w') as file:
        yaml.dump(inventory, file, default_flow_style=False)
    print("Inventory file 'inventory.yaml' created successfully.")


for name, device in devices.items():
    if device['type'] == 'linux':
        gather_linux_info(device['ip'])
    elif device['type'] == 'windows':
        gather_windows_info(device['ip'], 'Administrator', 'P@ssw0rd')

create_inventory_file(devices)
