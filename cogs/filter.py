import discord
import json
from bin.checkuser import CheckUser
from bin.timenow import TimeNow
from discord.ext import commands

groovyID = 234395307759108106 # We do not want to interact with this guy

hotWords = []
with open("data/hotwords.txt", 'r') as hword_file:
    for line in hword_file:
        for word in line.split():
            hotWords.append(word)
hword_file.close()

class Filter(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't want the bot to filter own messages
        if (message.author.id == self.client.user.id):
            return

        await CheckUser(message.author)

        with open("data/userinfo.json") as f:
            data = json.load(f)
        f.close()

        if (len(message.content)): # is a string
            message.content = message.content.lower()

        # Filter out all the GARBAGE
        if message.author.id == groovyID and message.channel.name != "music":
            await message.delete()
            return

        elif message.channel.name != "music" and message.content.split(' ', 1)[0] in hotWords:
            print(f"{TimeNow()} {message.author.name} tried to play music in the wrong channel")
            data[str(message.author.id)]["pollution"] += 1
            await message.delete()

        elif message.channel.name != "music" and message.content.split(' ', 1)[0] in hotWords:
            print(f"{TimeNow()} {message.author.name} tried to play music in the wrong channel")
            data[str(message.author.id)]["pollution"] += 1
            await message.delete()

        elif message.channel.name == "summons" and message.content[0:2] != "<@": # make sure summons channel cannot recieve file uploads
            print(f"{TimeNow()} {message.author.name} tried to pollute summons channel")
            data[str(message.author.id)]["pollution"] += 1
            await message.delete()
        elif len(message.content):
            if message.channel.name != "puffy" and message.content[0] == '!': # Do not use bot commands outside of given channel
                print(f"{TimeNow()} {message.author.name} tried to talk to puffy in the wrong channel")
                data[str(message.author.id)]["pollution"] += 1
                await message.delete()

        # Message is either a FILE or a STRING update DB
        if (not len(message.content)):
            # This is empty! This is a file! files uploaded :o
            data[str(message.author.id)]["img_sent"] += 1
            print(f"{TimeNow()} {message.author.name} sent a file")
        else:
            data[str(message.author.id)]["msg_sent"] += 1
            print(f"{TimeNow()} {message.author.name}: {message.content}")
        with open("data/userinfo.json",'w') as save_file:
            json.dump(data,save_file,indent=4)
        save_file.close()

def setup(client):
    client.add_cog(Filter(client))
