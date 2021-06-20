import requests
from colorama import Fore, init
from pushbullet import Pushbullet


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
    else:
        return "Error"


def getGPU(address):
    data = getData(address)
    if data is not None:
        GPU = data["gpus"][0]["name"]
        print(Fore.GREEN + GPU)
        return GPU
    else:
        return "Error"


def ReadFile(fileName, lines):
    with open(fileName) as f:
        if lines == True:
            fileLines = f.readlines()
        else:
            fileLines = f.readline()
    return fileLines


init(autoreset=True)


servers = ["192.168.1.15",  "192.168.1.12", "192.1"]

gpuFile = "gpu"
gpuFileContent = ReadFile(gpuFile, True)

pb = Pushbullet(ReadFile("pushbulletapikey", False))


for server in servers:
    hashRate = getHashRate(server)
    gpu = getGPU(server)
    if hashRate != "Error" and gpu != "Error":
        for line in gpuFileContent:
            if gpu in line:
                tmp = line.split("=")
                minHash = int(tmp[1])
                if hashRate <= minHash:
                    msg = f"Hashrate on {server} with a {tmp[0]} is below minimal requirement:{hashRate}/{minHash} MH/s"
                    print(Fore.RED + msg)
                    pb.push_note(f"Low hashrate {server}", msg)
    else:
        pb.push_note(f"{server} Offline", f"{server} is offline")
