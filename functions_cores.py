import json
from urllib import request
from urllib.error import HTTPError
from random import *
import pickle
import asyncio

import Types_for_metis
import Dara

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

"""
Fonctions qui compte les xps en vocal
"""
def vocal_xps(levels,guild,gen_channel,new_channel):
	await asyncio.sleep(60)
	voice_chan = guild.voice_channels
	for i in range(len(voice_chan)):
	    voice_members = vocalmembers_wnobots(voice_chan[i].members)
	    if voice_chan[i].id != Data.afk and (len(voice_members)) > 1 : 
	        for y in range(len(voice_members)):
	        up = levels.add_to_player(voice_members[y].id,False,None)
	        if up:
	            if in_list(voice_members[y].roles , member) :
	                await gen_channel.send("**Bravo  " + voice_members[y].mention + " tu viens de monter de 1 niveau, tu es donc niveau " + str(levels.return_in_place()[levels.search_for_place(voice_members[y].id)-1].level) + " !**")
	            else :
	                await new_channel[where_send_xp_mess(voice_members[y],new_role)].send("**Bravo  " + voice_members[y].mention + " tu viens de monter de 1 niveau, tu es donc niveau " + str(levels.return_in_place()[levels.search_for_place(voice_members[y].id)-1].level) + " !**")
	save_levels(levels)

"""
Fonction d'affichage du niveau d'un joueur
name     : "!levels"
args_min : 0
is_text  : 0
"""
def __levels(must_arg_list, followed_arg_list, msg_discord, levels):
    Member_xp = levels.search_for_player(msg_discord.author.id)
    s = "```css\n[" + str(levels.search_for_place(msg_discord.author.id)-1) + "]\n#" + msg_discord.author.display_name + " est niveau " + str(Member_xp.level) + "\n" + functions_cores.level_bar(Member_xp) + "\nXps_restants " + str(Member_xp.xps_lefts()) + "\n" + "msg : " + str(Member_xp.nmbmess) + " / tmp en vocal : " + str(Member_xp.voctime) + "\n```"
    return s

"""
Fonction d'affichage du classement
name     : "!ranking"
args_min : 0
is_text  : 0
"""
def __ranking(must_arg_list, followed_arg_list, msg_discord, levels):
    s = "```css\nCLASSEMENT DE RU :\n"
    i = 1
    for C in levels.return_in_place():
        s+= "#" + str(i) + " " + text.channel.guild.get_member(C.id_discord).display_name + " est niveau " + str(C.level) + " / xp : " + str(C.xp) + " / msg : " + str(C.nmbmess) + " / tmp en vocal : " + str(C.voctime) + '\n'
        i += 1
    s += "```"
    return s
    