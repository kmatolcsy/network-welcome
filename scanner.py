import json
from time import sleep
from subprocess import Popen, PIPE
from googlecontroller import GoogleAssistant


def open_config(path='./config.json'):
    with open(path) as f: config = json.load(f)
    return config


def list_ip_addresses(broadcast, packets):
    addresses = list()
    proc = Popen(['ping', '-c', str(packets), '-b', broadcast], stdout=PIPE)

    while line := proc.stdout.readline().decode('utf-8').split():

        if not line:
            proc.terminate()
            return addresses

        addresses.append(line[3].strip(':'))

    proc.terminate()
    return addresses


def main():
    conf = open_config()

    bedroom = GoogleAssistant(conf.get('bedroom'))
    kitchen = GoogleAssistant(conf.get('kitchen'))

    connected = False
    lag = False

    while True:
        addresses = list_ip_addresses(conf.get('broadcast'), 2)
        print(addresses)

        lag = connected
        connected = True if conf.get('irene') in addresses else False
        print(f'{lag=}\t{connected=}')

        message = None

        if coming := connected and not lag:
            message = 'Irene is coming home!'

        if leaving := lag and not connected:
            message = 'Irene is leaving!'

        if coming or leaving:
             bedroom.say(message)

        sleep(40)


def test():
    sleep(5)
    print('Done')
