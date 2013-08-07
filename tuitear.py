#!/usr/bin/python
## -*- coding: UTF-8 -*-
import sys
import os
import re
import tweepy

longitudM=138

def tuitear(mensaje, consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        if len(mensaje)>2:
            api.update_status(mensaje)
    except tweepy.TweepError as e:
        print 'Error tuiteando:', e

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


