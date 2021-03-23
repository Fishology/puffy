#===========================
# Author: Devin Benninghoven
# Date: 1/16/2021
#===========================

import os
import discord
from discord.ext import commands, tasks
from bin.timenow import TimeNow

client = commands.Bot(command_prefix='!', case_insensitive=True)
# Get private token
token_file = open("data/private/token.txt", "r")
token = token_file.read()
token_file.close()
# Set up cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

print(f"{TimeNow()} launching bot")
client.run(token)
