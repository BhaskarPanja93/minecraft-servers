## import statements
from random import randrange
from threading import Thread
from time import sleep, ctime
from requests import get
from os import system as system_caller, remove, system


## all tunnels to be made along with their name in dictionary, port, other details
tunnels_to_be_made = {
1: {
"key":"Main Survival",
"config":"""
version: "2"
region: in
authtoken: 28oH7jQPeXTDGWXs8oyIhb5KxUY_385T8rqtT1q1r2LAGYbb
web_addr: 127.0.0.1:INSPECT_PORT
inspect_db_size: -1
log_level: crit
tunnels:
    main_survival:
        addr: 50000
        inspect: false
        proto: tcp
"""},


2: {
"key": "Main Creative",
"config": """
version: "2"
region: in
authtoken: 28oHDeNqYqv9yv4ohcj5ky7RtXU_7eY3GNVFzZPpbJyNm2yzq
web_addr: 127.0.0.1:INSPECT_PORT
inspect_db_size: -1
log_level: crit
tunnels:
    main_creative:
        addr: 50001
        inspect: false
        proto: tcp
"""}
}

final_readme_data = """
# Minecraft Server IPs

</br>Main Survival: `REPLACE Main Survival`
</br>Main Creative: `REPLACE Main Creative`
"""

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
        inspect_port = randrange(51000, 52000)
        with open(config_location, 'w') as file:
            file.write(tunnels_to_be_made[index]['config'].replace("INSPECT_PORT", str(inspect_port)))
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


def git_commit():
    with open('README.md', 'w') as file:
        file.write(final_readme_data)
    system('git add .')
    system(f'git commit -m "{ctime()}"')
    system('git push')


config_location = check_ngrok_yml_location()
for index in tunnels_to_be_made:
    lock_string = check_and_lock_yml()
    url = create_tunnel(index).replace("tcp://","")
    key = tunnels_to_be_made[index]['key']
    final_readme_data = final_readme_data.replace(f"REPLACE {key}", url)
    free_yml(lock_string)
git_commit()


