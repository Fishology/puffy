import discord
import json
from discord.ext import commands,tasks
from bin.checkuser import CheckUser # Custom json data production
from bin.timenow import TimeNow # Custom current time function
from discord.utils import get # ???
import random

REFRESH_SECONDS = 5 # Everytime the discord servers will be searched
BASE_XP = 3 # Every loop with give +3 XP
XP_SCALE = 1.05

guildFile = open("data/private/mainguildid.txt", "r")
KING_HEAD_ID = int(guildFile.read())
guildFile.close()

study_channel_names = []
with open("data/academic.txt","r") as file:
    for line in file:
        for word in line.split():
            study_channel_names.append(word)
    file.close()

class XpSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.guilds = []
        self.XpCheck.start()

    @tasks.loop(seconds=REFRESH_SECONDS)
    async def XpCheck(self):
        print(f"{TimeNow()} starting xpcheck...")
        gamers = [] # Gaming channels
        nerds = []  # Study channels
        users = []
        afk_chans = []
        for guild in self.guilds:
            if guild.afk_channel != None:
                afk_chans.append(guild.afk_channel)
            for vchannels in guild.voice_channels:
                if vchannels not in afk_chans:
                    if vchannels.name.lower() not in study_channel_names:
                        for member in vchannels.members:
                            if (not member.bot):
                                gamers.append(member)
                                users.append(member)
                                print(f"\t{member} is gaming")
                    else:
                        for member in vchannels.members:
                            if (not member.bot):
                                nerds.append(member)
                                users.append(member)
                                print(f"\t{member} is studying")
        if (not len(users)):
            print(f"{TimeNow()} all comms empty")
            return

        for user in users:
            await CheckUser(user)



    # Defines the total guilds the bot is in
    @XpCheck.before_loop
    async def BeforeXpCheck(self):
        await self.client.wait_until_ready()
        guilds = await self.client.fetch_guilds(limit=150).flatten()
        self.mainguild = self.client.get_guild(KING_HEAD_ID)
        for textchan in self.mainguild.text_channels:
            if textchan.name == "puffy":
                self.puffychan = textchan
        for guild in guilds:
            self.guilds.append(self.client.get_guild(guild.id))

def setup(client):
    client.add_cog(XpSystem(client))
