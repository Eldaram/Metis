import asyncio
import time
import discord
from random import *
import pickle
import json
from urllib import request
from urllib.error import HTTPError

import Data
import functions_cores
import Types_for_metis

client = discord.Client() #Create the client link

@client.event #Everything for begining
async def on_ready():
    #guilds
    global guild
    guild = client.get_guild(Data.main_guild)
    
    #channels
    global gen_channel
    gen_channel = guild.get_channel(Data.general_channel)
    
    global adminOnly
    adminOnly = guild.get_channel(Data.admin_channel)

    global parents_channel
    parents_channel = guild.get_channel(Data.parents_channel)

    global new_channel
    new_channel = [0,0,0]
    new_channel[0] = guild.get_channel(Data.new_channel[0])
    new_channel[1] = guild.get_channel(Data.new_channel[1])
    new_channel[2] = guild.get_channel(Data.new_channel[2])

    #roles
    global member
    member = guild.get_role(Data.membre)

    global parents
    parents = guild.get_role(Data.parents)

    global new_role
    new_role = [0,0,0]
    new_role[0] = guild.get_role(Data.new_role[0])
    new_role[1] = guild.get_role(Data.new_role[1])
    new_role[2] = guild.get_role(Data.new_role[2])

    if Data.launch_message :
        await adminOnly.send("Bonjour ! Je viens de me lancer.")
    if Data.XPs_modules:
        global levels
        levels = functions_cores.open_levels()
        while True:
            await asyncio.sleep(60)
            voice_chan = guild.voice_channels
            for i in range(len(voice_chan)):
                voice_members = functions_cores.vocalmembers_wnobots(voice_chan[i].members)
                if voice_chan[i].id != Data.afk and (len(voice_members)) > 0 : #ne pas oublier de ne pas compter les bots
                    for y in range(len(voice_members)):
                        up = levels.add_to_player(voice_members[y].id,False,None)
                        if up:
                            if functions_cores.in_list(voice_members[y].roles , member) :
                                await gen_channel.send("**Bravo  " + voice_members[y].mention + " tu viens de monter de 1 niveau, tu es donc niveau " + str(levels.return_in_place()[levels.search_for_place(voice_members[y].id)-1].level) + " !**")
                            else :
                                await new_channel[where_send_xp_mess(voice_members[y],new_role)].send("**Bravo  " + voice_members[y].mention + " tu viens de monter de 1 niveau, tu es donc niveau " + str(levels.return_in_place()[levels.search_for_place(voice_members[y].id)-1].level) + " !**")
            functions_cores.save_levels(levels)
            


@client.event #Define call from channels
async def on_message(text):
    #add exps 5*(n**2)+50*n+100
    if Data.XPs_modules and text.channel.type != discord.ChannelType.private and not functions_cores.in_list(Data.not_xp_channels, text.channel.id) and not str.find(text.content.lower(), "!roll") == 0 and not text.author.bot :
        if str.find(text.content.lower(), "!levels") == 0:
            Member_xp = levels.search_for_player(text.author.id)
            s = "```css\n[" + str(levels.search_for_place(text.author.id)-1) + "]\n#" + text.author.display_name + " est niveau " + str(Member_xp.level) + "\n" + functions_cores.level_bar(Member_xp) + "\nXps_restants " + str(Member_xp.xps_lefts()) + "\n" + "msg : " + str(Member_xp.nmbmess) + " / tmp en vocal : " + str(Member_xp.voctime) + "\n```"
            await text.channel.send(s)
        elif str.find(text.content.lower(), "!ranking") == 0:
            s = "```css\nCLASSEMENT DE RU :\n"
            i = 1
            for C in levels.return_in_place():
                s+= "#" + str(i) + " " + text.channel.guild.get_member(C.id_discord).display_name + " est niveau " + str(C.level) + " / xp : " + str(C.xp) + " / msg : " + str(C.nmbmess) + " / tmp en vocal : " + str(C.voctime) + '\n'
                i += 1
            s += "```"
            await text.channel.send(s)
        else:
            up = levels.add_to_player(text.author.id,True,text.created_at)
            if up:
                if functions_cores.in_list(text.author.roles , member) :
                    await gen_channel.send("**Bravo  " + text.author.mention + " tu viens de monter de 1 niveau, tu es donc niveau " + str(levels.return_in_place()[levels.search_for_place(text.author.id)-1].level) + " !**")
                else :
                    await new_channel[where_send_xp_mess(text.author,new_role)].send("**Bravo  " + text.author.mention + " tu viens de monter de 1 niveau, tu es donc niveau " + str(levels.return_in_place()[levels.search_for_place(text.author.id)-1].level) + " !**")
    if Data.webhook_profile and text.channel.type != discord.ChannelType.private and text.channel.category_id != Data.admin_category and text.channel.category_id != Data.new_category and text.channel.category_id != Data.HRP_category and text.channel.category_id != Data.DMAS_category : #fonctions liee aux webhooks
        if str.find(text.content.lower(), "!addpnj ") == 0: #create a webhook
            image = text.attachments
            mess  = text.content
            mess  = mess.replace("!addpnj ", '')
            if functions_cores.in_list(await text.channel.webhooks(), mess, f=(lambda x:x.name)):
                await text.channel.send("(Oups, un·e PnJ porte déjà ce nom !)")
            else :
                if len(image)==1 and (str.find(image[0].filename, ".png") or str.find(image[0].filename, ".jpg") or str.find(image[0].filename, ".jpeg")):
                    image = await image[0].read()
                else:
                    image = None
                if mess != "":
                    reason_by = "Ask by "+text.author.display_name
                    await text.channel.create_webhook(name=mess, avatar=image, reason=reason_by)
                else :
                    await text.channel.send("(Oups, je n'ai pas pus créer le·la pnj !)")
            await text.delete(delay=None)

        if str.find(text.content.lower(), '!talkas ') == 0:
            mess  = text.content
            mess  = mess.replace("!talkas ", '')
            if mess[0] == '"':
                mess = mess.replace('"','',1)
                mess  = mess.split('" ',1)
                if len(mess) == 2:
                    webhooks = await text.channel.webhooks()
                    place = functions_cores.in_list(webhooks, mess[0], f=(lambda x:x.name),place=True)
                    if place != -1:
                        if not functions_cores.webhook_request(webhooks[place].url,mess[1]) :
                            await text.channel.send("(Oups, une erreur inconnue s'est produite ! Parle en tout de suite aux admins qu'ils aillent voire ce qui ne va pas !)")
                    else:
                        await text.channel.send("(Aucun·e PnJ porte ce nom sur ce salon)")
                else:
                    await text.channel.send("(Oups, la syntaxe est mauvaise)")
            else:
                await text.channel.send("(Oups, la syntaxe est mauvaise)")
            await text.delete(delay=None)

        if str.find(text.content.lower(), "!pnjhere") == 0:
            webhooks = await text.channel.webhooks()
            if text.author.dm_channel == None:
                await text.author.create_dm()
            if len(webhooks) > 0:
                texte = "```Les PnJs de ce channel sont :"
                for i in range(len(webhooks)):
                    texte += "\n  - " + webhooks[i].name
                texte += "```"
            else:
                texte = "Il n'y a pas de PnJs dans ce salon"
            await text.author.dm_channel.send(texte)
            await text.delete(delay=None)
    #DICE FUNCIONS
    if text.content[0] == "!" and Data.dice_module:
        mess = text.content + " "
        if str.find(text.content, "roll") == 1: #Function for dices
            mess = mess.replace(' ', '')
            mess = mess.replace('!roll', '')
            mess = mess+' '
            try :
                details = "Détails : "
                while "d" in mess :
                    place = mess.find("d")
                    placeB = place + 0
                    nmbDice = ''
                    while mess[placeB-1] in "1234567890" and placeB-1 >= 0:
                        placeB = placeB - 1
                        nmbDice = mess[placeB] + nmbDice
                    nmbDice = int(nmbDice)
                    placeA = place + 0
                    dice = ''
                    while mess[placeA+1] in "1234567890" and placeA+1 < len(mess)-1:
                        placeA = placeA + 1
                        dice = dice + mess[placeA]
                    dice = int(dice)
                    details += "\n" + str(nmbDice) +"d" + str(dice) +" : "
                    total = 0
                    for i in range(nmbDice):
                        if i != 0:
                            details += " "
                        y = randint(1,dice)
                        total += y
                        details += str(y)
                    details += " (" + str(total) + ")"
                    mess = mess.replace(str(nmbDice) +"d"+ str(dice), str(total), 1)
                result = eval(mess)
                chaine = "```Markdown\n#{0}\n{1}\n```".format(result,details)
                await text.channel.send(chaine)
            except ZeroDivisionError :
                await text.channel.send("Il y a eu une division par 0... Je ne peut donc pas faire de résultat réel !")
            except :
                await text.channel.send("La syntaxe n'est pas correcte... Il faut l'écrire \"!roll 1d20 +3\" par exemple.")

    elif Data.to_admin_message and text.channel.type == discord.ChannelType.private and not text.author.bot: #function for "send to amdin"
        textToSend = text.author.name + ' a dit : "' + text.content + '"'
        await adminOnly.send(textToSend)
        await text.channel.send("C'est transmit aux admins. Ils te répondront sous peu ne t'en fait pas ! :wink:")


if Data.guild_join_leave :
    @client.event #define member join
    async def on_member_join(joueur):
        num = functions_cores.read_last()
        await joueur.add_roles(new_role[num])
        await new_channel[num].send("**Regardez @everyone ! " + joueur.mention + "viens tout juste d'arriver ! Bienvenue parmis nous !**")
        await parents_channel.send("**Regardez un·e nouveau·elle compagnon·ne est arrivé·e sur le salon " + str(num+1) + " ! Il·Elle s'appelle "+joueur.display_name+" ! N'oubliez pas de lui demander qui l'a inviter sur le serveur !**")
        if joueur.dm_channel == None:
        	await joueur.create_dm()
        await joueur.dm_channel.send("**Bienvenue a toi sur Roliste Universe !** N'hésite pas a aller voir les admins et les parents pour leurs demander de l'aide et sinon va voir sur https://roliste-universe.fr/presentation.php#serveur pour avoir les mondes qui sont sur le serveur ! Bonne lecture !")

    @client.event
    async def on_member_update(before, after):
        if before.guild == guild:
            if not functions_cores.in_list(before.roles, member):
                if functions_cores.in_list(after.roles , member):
                    await gen_channel.send("**Regardez @everyone ! Un·e nouveau·elle compagnon·ne est arrivé·e ! Bienvenue à toi " + after.mention + " !**")


    @client.event #define member leave
    async def on_member_remove(joueur):
        if not functions_cores.in_list(joueur.roles , member):
            await parents_channel.send("**"+joueur.display_name+" est parti·e ! Il·Elle n'a pas eu l'occasion de devenir membre...**")
        else :
            await gen_channel.send("**"+joueur.display_name+" est parti·e ! Que son retours dans le monde triste de la réalité soit paisible...**")    


print("The bot is ready ! \nConnect to discord...")
client.run(Data.secret_token)