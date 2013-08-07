#!/usr/bin/python
## -*- coding: UTF-8 -*-
import sys
import os
import re
import tweepy

longitudM=138

consumer_key, consumer_secret, access_token, \
    access_token_secret = open('data').read().strip().split(';')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def tuitear(mensaje):
	if len(mensaje)>2:
		print "Twitteando: «"+str(mensaje)+"»"
		api.update_status(mensaje)

def validaLongitud(mensaje):
	if len(mensaje) > longitudM:
		#print "Longitud excesiva "+str(len(mensaje))
		return False
	else:
		#print "Longitud apropiada "+str(len(mensaje))
		return True

def discriminar(mensajePartes):
	if mensajePartes.group(1)==None:
		#print "Envio inmediato"
		tuitear(mensajePartes.group(2))
	else:
		#print "Envio programado"
		programar(mensajePartes.group(1), mensajePartes.group(2))

def mostrardialogo(mensaje):
	inputtext = os.popen( " kdialog --textinputbox 'Escribe tu tuit\n(para cancelar el envio deja la casilla en blanco)' '"+mensaje+"' --icon twitter --name Twittear --title Twittear | sed -r 's/\"/\\\"/gi' " )
	mensaje = inputtext.readline()
	return mensaje

def sanearMensaje(mensaje):
		return mensaje[0:longitudM]

def main(argumento):
	if len(argumento) > 1:
		mensaje=argumento[1]
		#print "Con mensaje:"+str(mensaje)
	else:
		#print "Sin mensaje"
		mensaje = mostrardialogo("")
		#print "Con mensaje:"+str(mensaje)
	#Si no hay indicacion horaria el objeto mensajePartes.group(1) es None
	mensajePartes=re.match("(\d?\d:\d?\d)? ?(.*)", mensaje)
	print mensajePartes.group(2)	
	while validaLongitud(mensajePartes.group(2))!=True:
		if mensajePartes.group(1)!=None:
			h=str(mensajePartes.group(1))+" "
		else:
			h=""
		mensaje=mostrardialogo(h+""+sanearMensaje(mensajePartes.group(2)))
		mensajePartes=re.match("(\d?\d:\d?\d)? ?(.*)", mensaje)
	discriminar(mensajePartes)
if __name__ == '__main__':
	try:
		access_key
	except NameError:
		access_key = None
	main(sys.argv)
