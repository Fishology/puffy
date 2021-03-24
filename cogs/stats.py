import discord
import json
from discord.ext import commands
from bin.checkuser import CheckUser

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(alaises = ["rank"])
    async def Stats(self, ctx, user):
        await ctx.send("HEY")






def setup(client):
    client.add_cog(Stats(client))
