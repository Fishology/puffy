import discord
from discord.ext import commands
from bin.timenow import TimeNow

class Startup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_connect(self):
        print(f"{TimeNow()} {self.client.user.name} connected")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{TimeNow()} {self.client.user.name} ready")

def setup(client):
    client.add_cog(Startup(client))
