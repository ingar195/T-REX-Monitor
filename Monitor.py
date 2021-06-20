import requests
from colorama import Fore, init


def getData(address):
    try:
        url = "http://{}:4067/summary".format(address)
        response = requests.get(url)
        data = response.json()
        response = requests.get(url)
        data = response.json()
        return data

    except Exception as e:
        print("No connection to server {}".format(address))
        return None


def getHashRate(address):
    data = getData(address)
    if data is not None:
        hashRate = int(data["hashrate"]/1000000)
        print(Fore.GREEN + "{} MH/s".format(hashRate))
        return hashRate


def getGPU(address):
    data = getData(address)
    if data is not None:
        GPU = data["gpus"][0]["name"]
        print(Fore.GREEN + GPU)
        return GPU


init(autoreset=True)


servers = ["192.168.1.15",  "192.168.1.12"]

gpuFile = "gpu"

with open(gpuFile) as f:
    lines = f.readlines()

for server in servers:
    hashRate = getHashRate(server)
    gpu = getGPU(server)

    for line in lines:
        if gpu in line:
            tmp = line.split("=")
            minHash = int(tmp[1])
            if hashRate <= minHash:
                print(
                    Fore.RED + f"Hashrate on {server} with a {tmp[0]} is below minimal requrement:{hashRate}/{minHash} MH/s")
