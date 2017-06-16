#-*- coding: utf8 -*-
import time
import json
import telepot
import random
import requests
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from terminaltables import AsciiTable

user_data = {}

ramales_file = open('ramales.json', 'r')
ramales = json.loads(ramales_file.read())
ramales_file.close()

estaciones_file = open('estaciones.json', 'r')
estaciones_data = json.loads(estaciones_file.read())
estaciones_file.close()


sentidos_file = open('sentidos.json', 'r')
sentidos_data = json.loads(sentidos_file.read())
sentidos_file.close()

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

def randomString():
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz"
    randomstring = ''
    for i in range(16):
        randomstring += random.choice(chars)
    return randomstring;

def get_tiempos(id_ramal):
    response_data = u'incorrect key'
    headers = {'Referer' : 'https://trenes.sofse.gob.ar/v2_pg/arribos/index.php?ramal='+id_ramal}
    i = 5
    while response_data == u'incorrect key' and i > 0 :
        response_data = requests.get('https://trenes.sofse.gob.ar/v2_pg/arribos/ajax_arribos.php?ramal=' + id_ramal + \
            '&rnd=' + randomString() +'&key=NRVQjcjTUF0I30EVFBDTqdWp%23', 
        headers=headers, timeout=5).text
        i -= 1
    return response_data
    
def tiempo_to_text(t):
    if t == '-1' or t == '-':
        return '-'
    elif t == '0':
        return 'En anden'
    return t + ' min.'

def select_ramal(chat_id, ramales):
    buttons = []
    btn_row = []
    for i, ramal in enumerate(sorted(ramales)):
        btn_row.append(KeyboardButton(text=ramal))
        if i % 3 == 2:
            buttons.append(btn_row)
            btn_row = []
    if btn_row:
        buttons.append(btn_row)
    bot.sendMessage(chat_id, 'Seleccione la linea/ramal', reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

def select_estacion(chat_id, id_ramal):    
    estaciones = estaciones_data[id_ramal]
    buttons = []
    btn_row = []
    for i, estacion in enumerate(estaciones):
        btn_row.append(KeyboardButton(text=estacion))
        if i % 3 == 2:
            buttons.append(btn_row)
            btn_row = []
    if btn_row:
        buttons.append(btn_row)
    bot.sendMessage(chat_id, 'Seleccione la estacion', reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))


def estacion(chat_id, id_ramal, estacion_act):
    response_data = get_tiempos(id_ramal)
    sentido = sentidos_data[id_ramal]
    if response_data == u'incorrect key':
        bot.sendMessage(chat_id, 'El servicio de trenes no responde.', reply_markup=ReplyKeyboardRemove())
    else:
        estaciones = json.loads(response_data)
        respuesta = ''
        for estacion in estaciones:
            if estacion_act == estacion['nombre']:
                respuesta = 'Estacion ' + estacion['nombre'] + '\n'
                table= [['Prox: ', tiempo_to_text(estacion['minutos_1'])], [' Sig: ', tiempo_to_text(estacion['minutos_2'])]]
                respuesta += 'A ' + sentido[0] + '\n'
                respuesta += AsciiTable(table).table
                table= [['Prox: ', tiempo_to_text(estacion['minutos_3'])], [' Sig: ', tiempo_to_text(estacion['minutos_4'])]]
                respuesta += '\nA ' + sentido[1] + '\n'
                respuesta += AsciiTable(table).table
                bot.sendMessage(chat_id, '``` ' + respuesta + ' ```', reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
                return

def handle(msg):
    try:
        chat_id = msg['chat']['id']
        command = msg['text']
        if command == '/estado' or command[:8] == '/estado@':
            estado(chat_id)
        elif command == '/tren' or command[:6] == '/tren@':
            select_ramal(chat_id, ramales.keys())
        elif command in ramales:
            user_data[chat_id] = ramales[command]
            select_estacion(chat_id, ramales[command])
        elif command == '/estacion' or command[:10] == '/estacion@':
            if chat_id in user_data:
                select_estacion(chat_id, user_data[chat_id])
            else:
                bot.sendMessage(chat_id, 'Primero seleccione un ramal')
                select_ramal(chat_id, ramales.keys())
        elif command[:3] == 'E. ':
            estacion(chat_id, user_data[chat_id], command[3:])
    except Exception, e:
        print e

TOKEN = open('subteBot.token').read().strip()
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(1)
