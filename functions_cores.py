import json
from urllib import request
from urllib.error import HTTPError

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