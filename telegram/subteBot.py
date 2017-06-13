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
ramales = {u'L. Sarmiento': '1', u'L. Mitre (Tigre)' : '5', u'L. Mitre (Mitre)' : '7', u'L. Mitre (J.L.Suárez)' : '9', \
        u'L. Roca (La Plata)' : '11', u'L. Roca (Claypole)' : '15', u'L. Roca (Gutierrez)' : '29', u'L. Roca (A. Korn)' : '17', \
        u'L. Roca (Haedo)' : '27', u'L. Roca (Ezeiza)' : '19', u'L. Roca (Cañuelas)' : '37', u'L. Belg Sur (M.C.G. Belgrano)' : '21', \
        u'L. Belg Sur (Aldo Bonzi)' : '23', u'L. Belg Sur (Gonzales Catán)' : '25', u'L. San Martin' : '31'}
estaciones_data ={'11': [u'E. Constituci\xf3n', u'E. Santill\xe1n y Kosteki', u'E. Sarand\xed', u'E. Villa Dom\xednico', u'E. Wilde', u'E. Don Bosco', u'E. Bernal',\
        u'E. Quilmes', u'E. Ezpeleta', u'E. Berazategui', u'E. Pl\xe1tanos', u'E. Hudson', u'E. Pereyra', u'E. Villa Elisa', u'E. City Bell', u'E. Gonnet', u'E. Ringuelet', \
        u'E. Tolosa', u'E. La Plata'], \
        '25': [u'E. Buenos Aires', u'E. Dr Sa\xe9nz', u'E. Villa Soldati', u'E. Presidente Illia', u'E. Villa Lugano', u'E. Villa Madero', \
        u'E. Marinos del Fournier', u'E. Tapiales', u'E. Ingeniero Castello', u'E. Querand\xed', u'E. Laferrere', u'E. Mar\xeda Eva Duarte', u'E. Independencia', \
        u'E. Gonz\xe1lez Cat\xe1n'], \
        '27': [u'E. Temperley', u'E. Hospital Espa\xf1ol', u'E. Santa Catalina', u'E. Juan XXIII', u'E. KM 34', u'E. P. Turner', \
        u'E. Agust\xedn de El\xeda', u'E. Tablada', u'E. San Justo', u'E. Ingeniero S. Brian', u'E. Haedo'], \
        '15': [u'E. Constituci\xf3n', u'E. Hip\xf3lito Yrigoyen', \
        u'E. Gerli', u'E. Lan\xfas', u'E. Remedios de Escalada', u'E. Banfield', u'E. Lomas de Zamora', u'E. Temperley', u'E. Jos\xe9 M\xe1rmol', u'E. Rafael Calzada', u'E. Claypole'], \
        '21': [u'E. Buenos Aires', u'E. Dr Sa\xe9nz', u'E. Villa Soldati', u'E. Presidente Illia', u'E. Villa Lugano', u'E. Villa Madero', u'E. Marinos del Fournier', u'E. Tapiales', \
        u'E. Aldo Bonzi', u'E. Sanchez de Mendeville', u'E. Jos\xe9 Ingenieros', u'E. Justo Villegas', u'E. Isidro Casanova', u'E. Rafael Castillo', u'E. Merlo Gomez', u'E. Libertad', \
        u'E. Marinos C. G Belgrano'], \
        '17': [u'E. Constituci\xf3n', u'E. Hip\xf3lito Yrigoyen', u'E. Gerli', u'E. Lan\xfas', u'E. Remedios de Escalada', u'E. Banfield', \
        u'E. Lomas de Zamora', u'E. Temperley', u'E. Adrogu\xe9', u'E. Burzaco', u'E. Longchamps', u'E. Glew', u'E. Guernica', u'E. Alejandro Korn'], \
        '23': [u'E. Puente Alsina', u'E. Villa Diamante', u'E. Villa Caraza', u'E. Villa Fiorito', u'E. Ing. Budge', u'E. La Salada', u'E. Apeadero Km 12', u'E. Aldo Bonzi'], \
        '19': [u'E. Constituci\xf3n', u'E. Hip\xf3lito Yrigoyen', u'E. Gerli', u'E. Lan\xfas', u'E. Remedios de Escalada', u'E. Banfield', u'E. Lomas de Zamora', \
        u'E. Temperley', u'E. Turdera', u'E. Llavallol', u'E. Luis Guill\xf3n', u'E. Monte Grande', u'E. El Jag\xfcel', u'E. Ezeiza'], \
        '31': [u'E. Retiro', u'E. Palermo', u'E. Villa Crespo', u'E. La Paternal', u'E. Villa del Parque', u'E. Devoto', u'E. Saenz Pe\xf1a', u'E. Santos Lugares', \
        u'E. Caseros', u'E. El Palomar', u'E. Hurlingham', u'E. William Morris', u'E. Bella Vista', u'E. Mu\xf1iz', u'E. San Miguel', u'E. Jos\xe9 C Paz', u'E. Sol y Verde', \
        u'E. Derqui', u'E. Villa Astolfi', u'E. Pilar', u'E. Manzanares', u'E. Cabred'], \
        '37': [u'E. Temperley', u'E. Turdera', u'E. Llavallol', u'E. Luis Guill\xf3n', u'E. Monte Grande', u'E. El Jag\xfcel', u'E. Ezeiza', u'E. Uni\xf3n Ferroviaria', \
        u'E. Trist\xe1n Su\xe1rez', u'E. Carlos Spegazzini', u'E. M\xe1ximo Paz', 'Vicente Casares', u'E. Alejandro Peti\xf3n', u'E. Apeadero Kloosterman', \
        u'E. Ricardo Levene', u'E. Ca\xf1uelas'], \
        '29': [u'E. Temperley', u'E. Jos\xe9 M\xe1rmol', u'E. Rafael Calzada', u'E. Claypole', u'E. Dante Ardig\xf3', u'E. Florencio Varela', u'E. Zeballos', \
        u'E. Bosques', u'E. Santa Sof\xeda', u'E. Guti\xe9rrez'], \
        '1': [u'E. Once', u'E. Caballito', u'E. Flores', u'E. Floresta', u'E. Villa Luro', u'E. Liniers', u'E. Ciudadela', u'E. Ramos Mej\xeda', u'E. Haedo', u'E. Mor\xf3n', u'E. Castelar', \
        u'E. Ituzaing\xf3', u'E. S.A. de Padua', u'E. Merlo', u'E. Paso del Rey', u'E. Moreno'], \
        '5': [u'E. Retiro', u'E. Lisandro de la Torre', u'E. Belgrano C', u'E. Nu\xf1ez', u'E. Rivadavia', u'E. Vicente L\xf3pez', u'E. Olivos', u'E. La Lucila', \
        u'E. Mart\xednez', u'E. Acassuso', u'E. San Isidro C', u'E. B\xe9ccar', u'E. Victoria', u'E. Virreyes', u'E. San Fernando C', u'E. Carup\xe1', u'E. Tigre'], \
        '7': [u'E. Retiro', u'E. 3 de Febrero', u'E. Ministro Carranza', u'E. Colegiales', u'E. Belgrano R', u'E. Coghlan', u'E. Saavedra', u'E. Juan B. Justo', u'E. Florida', \
        u'E. Dr. Cetr\xe1ngolo', u'E. Mitre'], \
        '9': [u'E. Retiro', u'E. 3 de Febrero', u'E. Ministro Carranza', u'E. Colegiales', u'E. Belgrano R', u'E. L.M.Drago', u'E. General Urquiza', u'E. Pueyrred\xf3n', \
        u'E. Miguelete', u'E. San Mart\xedn', u'E. San Andr\xe9s', u'E. Malaver', u'E. Villa Ballester', u'E. Chilavert', u'E. J.L. Su\xe1rez']}

sentidos_data = {'11': ('La Plata', 'Plaza Constitución'), '25': ('Gonzalez Catán', 'Buenos Aires'), 
        '27': ('Haedo', 'Temperley'), '15': ('Claypole', 'Plaza Constitución'), '21': ('M.C.G. Belgrano', 'Buenos Aires'), 
        '17': ('Korn', 'Plaza Constitución'), '23': ('Aldo Bonzi', 'Pte. Alsina'), '19': ('Ezeiza', 'Plaza Constitución'), 
        '31': ('Cabred', 'Retiro'), '37': ('Cañuelas', 'Ezeiza'), '29': ('Gutierrez', 'Temperley'), '1': ('Moreno', 'Once'), 
        '5': ('Tigre', 'Retiro'), '7': ('Mitre', 'Retiro'), '9': ('J.L. Suarez', 'Retiro')}

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

def get_tiempos(id_ramal):
    response_data = u'incorrect key'
    headers = {'Referer' : 'https://trenes.sofse.gob.ar/v2_pg/arribos/index.php?ramal='+id_ramal}
    i = 5
    while response_data == u'incorrect key' and i > 0 :
        response_data = requests.get('https://trenes.sofse.gob.ar/v2_pg/arribos/ajax_arribos.php?ramal=' + id_ramal + \
            '&rnd=DEFGHIJKLMNOPQRS&key=NRVQjcjTUF0I30EVFBDTqdWp%23', 
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
    for i, ramal in enumerate(ramales):
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
                respuesta = estacion['nombre'] + '\n'
                table= [['Prox: ', tiempo_to_text(estacion['minutos_1'])], [' Sig: ', tiempo_to_text(estacion['minutos_2'])]]
                t1 = AsciiTable(table, 'A ' + sentido[0])
                table= [['Prox: ', tiempo_to_text(estacion['minutos_3'])], [' Sig: ', tiempo_to_text(estacion['minutos_4'])]]
                t2 = AsciiTable(table, 'A ' + sentido[1])
                bot.sendMessage(chat_id, '``` Estacion ' + respuesta + t1.table + '\n' + t2.table + '```', reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
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
        elif command[:3] == 'E. ':
            estacion(chat_id, user_data[chat_id], command[3:])
    except Exception, e:
        print e

TOKEN = open('subteBot.token').read().strip()
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(1)
