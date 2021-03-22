import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
'''
    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"bot online")

    # commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pongus")
'''
def setup(client):
    client.add_cog(Example(client))
