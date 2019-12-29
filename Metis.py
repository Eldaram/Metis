import discord
import Data

client = discord.Client() #Create the client link

@client.event #Everything for begining
async def on_ready():

    global guild
    guild = client.get_guild(Data.main_guild)
    
    global gen_channel
    papotage = guild.get_channel(Data.general_channel)
    
    global adminOnly
    adminOnly = guild.get_channel(Data.admin_channel)


print("The bot is ready ! \nConnect to discord...")
client.run(Data.secret_token)