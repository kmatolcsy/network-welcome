import json
from time import sleep, gmtime
from subprocess import Popen, PIPE
from googlecontroller import GoogleAssistant
from telegram import Bot


def open_config(path='./config.json'):
    with open(path) as f: config = json.load(f)
    return config


def list_ip_addresses(broadcast, packets=2):
    addresses = list()
    proc = Popen(['ping', '-c', str(packets), '-b', broadcast], stdout=PIPE)

    while line := proc.stdout.readline().decode('utf-8').split():
        if not line: break
        addresses.append(line[3].strip(':'))

    proc.terminate()
    return addresses


def main(e):
    ip = open_config()

    # bedroom = GoogleAssistant(ip.get('bedroom'))
    kitchen = GoogleAssistant(ip.get('kitchen'))
    telebot = Bot(ip.get('bot'))

    is_connected = False
    was_connected = False

    while True:
        time = gmtime()
        addresses = list_ip_addresses(ip.get('broadcast'))
        print(addresses)

        was_connected = is_connected
        is_connected = True if ip.get('irene') in addresses else False

        message = None

        if coming := (is_connected and not was_connected):
            message = 'Irene is coming home!'

        if leaving := (was_connected and not is_connected):
            message = 'Irene is leaving!'

        if (coming or leaving) and (8 <= time.tm_hour <= 21):
             kitchen.say(message)
             telebot.send_message(chat_id=ip.get('chat'), text=message)

        sleep(9)
        e.wait()


def test(e):
    while True:
        e.wait()
        print('working hard...')
        sleep(20)
