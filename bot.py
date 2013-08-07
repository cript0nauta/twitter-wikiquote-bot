#-*- coding: utf- -*-

import random
import time
import wikiquote
import tuitear

INTERVALO = 20

PAGINAS = [
        'Andrés Calamaro',
        'Fito Páez',
        'Charly García',
        'Luis Alberto Spinetta',
        'Gustavo Cerati',
        'León Gieco',
        'Ricardo Iorio',
        'Joaquín Sabina',
        'Manu Chao',
        ]

citas = []
for pagina in PAGINAS:
    print 'Cargando', pagina
    quotes = wikiquote.get_quotes(pagina)
    quotes = [(q, pagina) for q in quotes]
    citas += quotes

while True:
    quote, pagina = random.choice(citas)
    tweet = '%s: "%s"' % (pagina, quote.encode('utf8'))
    if len(tweet) > 138:
            #print 'tweet largo'
        continue
    tuitear.tuitear(tweet)
    time.sleep(INTERVALO)
