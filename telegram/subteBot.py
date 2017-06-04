#-*- coding: utf8 -*-
import time
import json
import telepot
import requests
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop


def estado(chat_id):

    status_strings = json.loads(requests.get('http://subte-data.null.com.ar').text)
    subte_data = BeautifulSoup(requests.get("http://www.metrovias.com.ar").text, 'html.parser')
    result = []
    for line in ["A", "B", "C", "D", "E", "H"]:
        line_data = subte_data.find(id="status-line-{}".format(line)).string
        symbol = "✓"
        if line_data == "":
            # Service down
            result.append("El servicio web de Metrovias no responde, no es posible obtener el estado del Subte.")
            break
        if any([x in line_data for x in status_strings['warn']]):
            symbol = "⚠"
        elif not any([x in line_data for x in status_strings['ok']]):
            symbol = "✗"
        result.append("{} {}: {}".format(symbol, line, line_data))
    bot.sendMessage(chat_id, "\n".join(result), parse_mode='Markdown')


def handle(msg):
    try:
        chat_id = msg['chat']['id']
        command = msg['text']
        if command == '/estado' or command[:8] == '/estado@':
            estado(chat_id)
    except Exception, e:
        print e

TOKEN = open('subteBot.token').read().strip()
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(1)
