## import statements
from random import randrange
from threading import Thread
from time import sleep, ctime

from ping3 import ping
from requests import get
from os import system as system_caller, remove, system
import minestat

## all tunnels to be made along with their name in dictionary, port, other details
tunnels_to_be_made = {
1: {
"key":"Main Survival",
"status": "",
"port":'50000',
"address": "",
"config":"""
version: "2"
region: in
authtoken: 28oH7jQPeXTDGWXs8oyIhb5KxUY_385T8rqtT1q1r2LAGYbb
web_addr: 127.0.0.1:INSPECT_PORT
inspect_db_size: -1
log_level: crit
tunnels:
    main_survival:
        addr: REPLACE Port
        inspect: false
        proto: tcp
"""},


2: {
"key": "Main Creative",
"status": "",
"port":'50001',
"address": "",
"config": """
version: "2"
region: in
authtoken: 28oHDeNqYqv9yv4ohcj5ky7RtXU_7eY3GNVFzZPpbJyNm2yzq
web_addr: 127.0.0.1:INSPECT_PORT
inspect_db_size: -1
log_level: crit
tunnels:
    main_creative:
        addr: REPLACE Port
        inspect: false
        proto: tcp
"""}
}

readme_template = """
# Minecraft Server IPs

</br></br>Main Survival: `REPLACE Main Survival` </br> Status: `REPLACE STATUS Main Survival` </br> Last Checked: REPLACE TIME Main Survival
</br></br>Main Creative: `REPLACE Main Creative` </br> Status: `REPLACE STATUS Main Creative` </br> Last Checked: REPLACE TIME Main Survival
"""


def check_server_connection(port, ip='127.0.0.1'):
    ms = minestat.MineStat(ip, int(port))
    if ms.online:
        return ms.latency
    else:
        return -1


def check_ngrok_yml_location():
    default_locations = [
        r"C:\Users\Administrator\AppData\Local\ngrok\ngrok.yml",
        r"C:\Users\Administrator\.ngrok2\ngrok.yml"
    ]
    for location in default_locations:
        try:
            open(location, 'r').read()
            return location
        except:
            pass


def check_and_lock_yml():
    string = str(randrange(1, 10000))
    for _ in range(5):
        try:
            open(config_location.replace("ngrok.yml", "ngrok.yml.lock"),'r')
            sleep(1)
        except:
            break
    open(config_location.replace("ngrok.yml", "ngrok.yml.lock"), 'w').write(string)
    return string


def free_yml(string):
    try:
        if open(config_location.replace("ngrok.yml", "ngrok.yml.lock"), 'r').read() == string:
            remove(config_location.replace("ngrok.yml", "ngrok.yml.lock"))
    except:
        pass


def create_tunnel(index):
    url = ''
    while True:
        inspect_port = randrange(51000, 53000)
        with open(config_location, 'w') as file:
            file.write(tunnels_to_be_made[index]['config'].replace("INSPECT_PORT", str(inspect_port)).replace("REPLACE Port", tunnels_to_be_made[index]['port']))
        Thread(target=system_caller, args=("ngrok start --all",)).start()
        for _ in range(100):
            xml_data = eval(get(f"http://127.0.0.1:{inspect_port}/api/tunnels").text.replace("false", "False").replace("true", "True"))
            tunnels = xml_data["tunnels"]
            if len(tunnels) != 0:
                break
            sleep(0.1)
        else:
            input("\n\nno tunnels\n\n")
            continue
        for tunnel_index in range(len(tunnels)):
            url = tunnels[tunnel_index]['public_url']
        break
    return url


def check_and_commit():
    readme_ip_data = readme_template
    for index in tunnels_to_be_made:
        key = tunnels_to_be_made[index]['key']
        url = tunnels_to_be_made[index]['address']
        readme_ip_data = readme_ip_data.replace(f"REPLACE {key}", url)
    with open('README.md', 'w') as file:
        file.write(readme_ip_data)
    system('git add .')
    system(f'git commit -m "{ctime()}"')
    system('git push')

    while True:
        ## Check local availability
        readme_local_connectivity_data = readme_ip_data
        for index in tunnels_to_be_made:
            key = tunnels_to_be_made[index]['key']
            latency = check_server_connection(tunnels_to_be_made[index]['port'])
            if latency >= 0:
                if tunnels_to_be_made[index]['status'] not in ["Available Globally", "Available Locally"]:
                    tunnels_to_be_made[index]['status'] = "Available Locally" ## yellow circle
            else:
                tunnels_to_be_made[index]['status'] = "Unavailable"  ## red circle
            readme_local_connectivity_data = readme_local_connectivity_data.replace(f"REPLACE STATUS {key}", tunnels_to_be_made[index]['status'])
        with open('README.md', 'w') as file:
            file.write(readme_local_connectivity_data)
        system('git add .')
        system(f'git commit -m "{ctime()}"')
        system('git push')

        ## Check global availability
        readme_global_connectivity_data = readme_ip_data
        for index in tunnels_to_be_made:
            key = tunnels_to_be_made[index]['key']
            ip, port = tunnels_to_be_made[index]['address'].split(":")
            port = int(port)
            latency = check_server_connection(port, ip)
            if latency >= 0:
                if tunnels_to_be_made[index]['status'] != "Available Globally":
                    tunnels_to_be_made[index]['status'] = "Available Globally"  ## green circle
            readme_global_connectivity_data = readme_global_connectivity_data.replace(f"REPLACE STATUS {key}", tunnels_to_be_made[index]['status'])
        with open('README.md', 'w') as file:
            file.write(readme_global_connectivity_data)
        system('git add .')
        system(f'git commit -m "{ctime()}"')
        system('git push')


config_location = check_ngrok_yml_location()
for index in tunnels_to_be_made:
    while not type(ping('8.8.8.8')) == float:
        sleep(1)
    lock_string = check_and_lock_yml()
    url = create_tunnel(index).replace("tcp://","")
    key = tunnels_to_be_made[index]['key']
    tunnels_to_be_made[index]['address'] = url
    free_yml(lock_string)
ip_change_time = ctime()
check_and_commit()
