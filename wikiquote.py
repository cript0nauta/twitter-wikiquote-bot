#-*- coding: utf- -*-

import urllib
import re
import requests
from pyquery import PyQuery as PQ

URL_BASE = 'http://es.wikiquote.org/w/'

QUOTE_RE = r'\* "([^"]+)"'

def get_source(page_name):
    """ Retorna el contenido en formato Wiki de la página
    especificada """
    url = URL_BASE + 'index.php'
    page_name = page_name.replace(' ', '_') # Formato wiki
    get_params = dict(title=page_name, action='edit')
    url = url + '?' + urllib.urlencode(get_params)
    
    content = requests.get(url).text
    pq = PQ(content)
    textarea = pq('textarea').text() # El contenido del textarea
    return textarea

def get_quotes(page_name):
    """ Retorna una lista con las citas encontradas en la página """
    source = get_source(page_name)
    return re.findall(QUOTE_RE, source)

if __name__ == '__main__':
    for quote in get_quotes('Fito Páez'):
        print quote
