import json
from urllib import request
from urllib.error import HTTPError
from random import *
import pickle

import Types_for_metis

def Test_token(secretToken):
 	return len(secretToken) == 59

def read_last():
	file = open("last_new.txt",'r')
	content = file.read()
	file.close()
	content = int(content)
	file = open("last_new.txt",'w')
	if content == 2:
		file.write("0")
	else:
		file.write(str(content+1))
	file.close()
	return int(content)

"""
in_list permet de savoir si un arg se trouve dans une liste lis
return -> bolean
lis    <- list[a]
arg    <- a

f <= anonymus function
"""
def in_list(lis,arg, f=(lambda x : x),place=False):
	length = len(lis)
	i = 0
	while (i<length and f(lis[i]) != arg):
		i += 1
	if place:
		if i<length:
			return i
		else:
			return -1
	else:
		return i<length

"""
search_name renvoie le 1er texte entre guillmet dans une chaine de caractère, si la chaine ne contient pas de double guillemet, la fonction renvoie None
return <- str
text   -> str
"""
def search_name(text):
	a = str.find(text,'"')
	if a == -1:
		return None
	else :
		value = ""
		while a<len(text) and text[a]!='"':
			value += text[a]
			a += 1
		if text[a]!='"':
			return None
		else:
			return value

"""

"""
def suppr_all_char(text,char):
	value = ""
	for i in range(len(text)):
		if text[i] != char:
			value += text[i]
	return value

def webhook_request(url, content):
	payload = {
	    'content': content
	}
	headers = {
	    'Content-Type': 'application/json',
	    'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
	}
	req = request.Request(url=url, data=json.dumps(payload).encode('utf-8'),headers=headers,method='POST')
	try:
	    response = request.urlopen(req)
	    return True
	except HTTPError as e:
	    print('ERROR')
	    print(e.reason)
	    print(e.hdrs)
	    print(e.file.read())
	    return False

"""
Fonction qui sauvegarde les niveaux
"""
def save_levels(dictionary):
	with open("savefile.txt","wb") as fichier:
		mon_pickler = pickle.Pickler(fichier)
		mon_pickler.dump(dictionary)

"""
Fonction qui réccupère et retourne les niveaux qui se trouvent dans le fichier levels
"""
def open_levels():
	with open("savefile.txt","rb") as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		dictionary = mon_depickler.load()
	return dictionary

"""
Fonction utiliser pour savoir où envoyer un message système si un utilisateur n'es pas membre mais qu'il a monté de niveau
"""
def where_send_xp_mess(user,lisRole) :
	res = -1
	for i in range(len(lisRole)):
		if functions_cores.in_list(user.role, lisRole[i]):
			res = i
	return res

"""
Fonction prenannt l'entré du dictionnaire des XPs corespondant à un joueur et renvoie une jauge exprimant les niveau du joueur
"""
def level_bar(PXP): #5*(level*level)+50*level+100
	xpsupp = 5*(PXP.level*PXP.level)+50*PXP.level+100
	x = int(100*(PXP.xp/xpsupp))
	text_value = "["
	for i in range(20):
		if i < x//5:
			text_value += "$"
		else:
			text_value += "_"
	text_value += "]"
	return text_value

"""
Renvoie une liste de tous les membres dans un vocal SANS les bots
"""
def vocalmembers_wnobots(liste_vocal):
	liste = []
	for e in liste_vocal:
		if not e.bot:
			liste.append(e)
	return liste