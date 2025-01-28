from pythonping import ping
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

with open("ping_success.txt", "a") as f:
    f.write("< " + 9*"-" + " START " + 9*"-" + " >\n")
    f.write("date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
def check_ping(host):
    response_list = ping(host, verbose=False)
    if response_list.success():
        print(f"Ping to {host} was successful.")
        with open("ping_success.txt", "a") as f:
            f.write(f"{host}\n")    
    else:
        print(f"Ping to {host} failed.")

hosts = [f"192.168.0.{i}" for i in range(1, 199)]

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(check_ping, hosts)

hosts = [f"192.168.1.{i}" for i in range(1, 199)]

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(check_ping, hosts)

with open("ping_success.txt", "a") as f:
    f.write("< " + 10*"-" + " END " + 10*"-" + " >\n")
