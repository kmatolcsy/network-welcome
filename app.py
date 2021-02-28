import json
from time import sleep
from subprocess import Popen, PIPE
from googlecontroller import GoogleAssistant


def open_config(path='./config.json'):
    with open(path) as f: config = json.load(f)
    return config


def list_ip_addresses(broadcast, interval):
    addresses = list()
    proc = Popen(['ping', '-i', interval, '-b', broadcast], stdout=PIPE)

    while True:
        line = proc.stdout.readline()

        if not line:
            proc.terminate()
            return addresses
        
        line = line.decode('utf-8').split()
        addresses.append(line[3])


def main():
    conf = open_config()
    
    # bedroom = GoogleAssistant(conf.get('bedroom'))
    kitchen = GoogleAssistant(conf.get('kitchen'))
    
    connected = False
    lag = False

    while True:
        addresses = list_ip_addresses(conf.get('broadcast'), 30)

        lag = connected
        connected = True if conf.get('irene') in addresses else False

        if connected and not lag:
            message = 'Irene is coming home!'

        if lag and not connected:
            message = 'Irene is leaving!'

        kitchen.say(message)
        sleep(40)
            

if __name__ == '__main__':
    main()
    