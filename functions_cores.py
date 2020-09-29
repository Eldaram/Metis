import json
from urllib import request
from urllib.error import HTTPError
from random import *

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
epxs_supp permet d'ajouter de l'xp dans une bibliothèque
library représente les xps et le niveau des joueurs liée à une clé qui est leurs ID unique discord
key est l'ID spécifique du membre a qui on veut ajouter de l'XP

la valeur de sortie est library modifié

library = {IDJOUEUR : (XP,niveau, nombre de message, temps en vocal)}
"""
def epxs_supp(library,key,vocal=False):
	exist = False
	for i in library:
		if key == i:
			exist = True
	if not exist:
		library[key] = (0,0,0,0)
	(library[key],up) = player_win_xp(library[key],vocal)
	return (library,up)

"""
Cette fonction fait augmente les xps avec un nombre aléatoire compris entre 15 et 25
Si les XPs totaux dépssent 5*(n*n)+50*n+100 avec n le niveau actuel, alors le niveau monte de 1 et on retirel'ancien total à xp

a = (level, xp, nmbmess, vochours) <- (int,int,int,int)
(level, xp, nmbmess, vochours) -> (int,int,int,int)
"""
def player_win_xp(a, vocal):
	(level, xp, nmbmess, vochours) = a
	up = False
	if vocal:
		xpsupp = 10
		vochours += 1
	else :
		xpsupp = randint(15,25)
		nmbmess += 1
	xp += xpsupp
	if xp >= 5*(level*level)+50*level+100:
		xp -= 5*(level*level)+50*level+100
		level += 1
		up = True
	return ((level, xp, nmbmess, vochours),up)

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
def level_bar(a): #5*(level*level)+50*level+100
	(level, xp, nmbmess, vochours) = a
	xpsupp = 5*(level*level)+50*level+100
	x = int(100*(xp/xpsupp))
	text_value = "["
	for i in range(20):
		if i < x//5:
			text_value += "$"
		else:
			text_value += "_"
	text_value += "]"
	return text_value

"""
Fonction renvoyant le texte à envoyer lors d'une commande pour connaitre sont niveau
"""
def level_messages():
	pass

