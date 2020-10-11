from random import *
from datetime import *

class XP_list:
	"""docstring for XP_list"""
	def __init__(self):
		self.liste = []

	def add_to_list(self,id_discord):
		self.liste.append(Player_XP(id_discord))

	def search_for_place(self,id_discord):
		i = 0
		while i < len(self.liste) and self.liste[i].id_discord != id_discord:
			i += 1
		if i < len(self.liste):
			return i+1
		else:
			return -1

	def search_for_player(self,id_discord):
		i = 0
		while i < len(self.liste) and self.liste[i].id_discord != id_discord:
			i += 1
		if i < len(self.liste):
			return self.liste[i]
		else:
			return Player_XP(None)

	def return_in_place(self):
		return self.liste

	def add_to_player(self,id_discord,m_or_v,time):
		i = 0
		while i < len(self.liste) and self.liste[i].id_discord != id_discord:
			i += 1
		if not i < len(self.liste):
			self.add_to_list(id_discord)
		up = False
		if m_or_v:
			up = self.liste[i].add_message(time)
		else:
			up = self.liste[i].add_vocal()
		if i != 0 and self.liste[i].is_more_than(self.liste[i-1]):
			(self.liste[i],self.liste[i-1]) = (self.liste[i-1], self.liste[i])
		return up

class Player_XP:
	"""docstring for Player_XP"""
	def __init__(self,id_discord):
		self.id_discord	= id_discord
		self.level 		= 0
		self.xp 		= 0
		self.nmbmess 	= 0
		self.voctime 	= 0
		self.lastmsg	= datetime.min

	def add_message(self,time):
		up = False
		self.nmbmess += 1
		if time.year > self.lastmsg.year or time.month > self.lastmsg.month or time.day > self.lastmsg.day or time.hour > self.lastmsg.hour or time.minute > self.lastmsg.minute:
			self.xp += randint(15,25)
			if self.xp >= 5*(self.level*self.level)+50*self.level+100:
				self.xp -= 5*(self.level*self.level)+50*self.level+100
				self.level += 1
				up = True
		return up

	def add_vocal(self):
		up = False
		self.voctime += 1
		self.xp += 10
		if self.xp >= 5*(self.level*self.level)+50*self.level+100:
			self.xp -= 5*(self.level*self.level)+50*self.level+100
			self.level += 1
			up = True
		return up

	def is_more_than(self,PXP):
		if self.level > PXP.level:
			return True
		elif self.level == PXP.level:
			return self.xp > PXP.xp
		else :
			return False
		
	def xps_lefts(self):
		return 5*(self.level*self.level)+50*self.level+100 - self.xp