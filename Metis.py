import discord
from random import *
import Data

client = discord.Client() #Create the client link

@client.event #Everything for begining
async def on_ready():

    global guild
    guild = client.get_guild(Data.main_guild)
    
    global gen_channel
    gen_channel = guild.get_channel(Data.general_channel)
    
    global adminOnly
    adminOnly = guild.get_channel(Data.admin_channel)

    if Data.launch_message :
        await adminOnly.send("Bonjour ! Je viens de me lancer.")

@client.event #Define call from channels
async def on_message(text):
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
        await gen_channel.send("**Regardez @everyone ! Un nouveau compagnon est arrivée ! Bienvenue à toi "+joueur.mention+" !**")
        if joueur.dm_channel == None:
        	await joueur.create_dm()
        await joueur.dm_channel.send("**Bienvenue a toi sur Roliste Universe !** N'hésite pas a aller voir les admins pour leurs demander de l'aide et sinon va voir sur https://roliste-universe.fr/presentation.php#serveur pour avoir les mondes qui sont sur le serveur ! Bonne lecture !")

    @client.event #define member leave
    async def on_member_remove(joueur):
        await gen_channel.send("**"+joueur.display_name+" est partie ! Que son retours dans le monde triste de la réalité soit paisible...**")    


print("The bot is ready ! \nConnect to discord...")
client.run(Data.secret_token)