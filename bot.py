#-*- coding: utf- -*-

import os
import sys
import random
import time
import json
import wikiquote
import tuitear
from threading import Thread

CONGIG_JSON = 'bots.json'

# Variable local, para modificar el intervalo real cambiar la configuración
INTERVALO = 1

stop = False

def start_bot(bot):
    """ Hilo que inicia el bot pasado como argumento (diccionario) """
    citas = []
    for pagina in bot['paginas']:
        print 'Cargando', pagina
        quotes = wikiquote.get_quotes(pagina.encode('utf8'))
        quotes = [(q, pagina) for q in quotes]
        citas += quotes

    tiempo = 0
    while not stop:
        if tiempo >= bot['intervalo']:
            quote, pagina = random.choice(citas)
            tweet = bot['format'].encode('utf8') % dict(pagina = \
                    pagina.encode('utf8'), frase = quote.encode('utf8'))
            if len(tweet) > 138:
                    #print 'tweet largo'
                continue
            print "%s: %s" % (bot['name'], tweet.decode('utf8'))
            tuitear.tuitear(tweet, bot['consumer_key'], bot['consumer_secret'],
                bot['access_token'], bot['access_token_secret'])
            tiempo = 0
        tiempo += INTERVALO
        time.sleep(INTERVALO)
    print 'Thread para', bot['name'], 'detenido'

def main():
    path = os.path.dirname(__file__)
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = os.path.join(path, CONGIG_JSON)
    print 'Cargando bots en', filename

    j = json.load(file(filename))
    for bot in j['bots']:
        if bot.get('disabled'):
            continue
        thread = Thread(target = start_bot, args=[bot])
        thread.daemon = True
        thread.start()
        print 'Thread para', bot['name'], 'iniciado'
    while True: 
        # Para que no terminen los hilos
        pass

if __name__ == '__main__':
    main()

