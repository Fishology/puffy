import discord
import json
from discord.ext import commands
from operator import itemgetter
from bin.checkuser import CheckUser
from bin.timenow import TimeNow

class LeaderBoardCommand(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases = ["top"])
    async def LeaderBoard(self, ctx):
        if ctx.channel.name != "puffy":
            return

        print(f"{TimeNow()} {ctx.author.name} issued the leaderboard command")

        with open("data/userinfo.json") as fileleader:
            data = json.load(fileleader)

        fileleader.close()
        
        leaderboard = []

        for user in data:
            if data[user]["cur_xp"] > 0 or data[user]["level"] > 1:
                leaderboard.append(data[user])

        for user in leaderboard:
            dog = (user["level"] * 1000) + user["cur_xp"] * 0.1 
            user["gscore"] = dog
            name = user["name"]
            print(f"{name} gscore of {dog}")

        final_list = sorted(leaderboard, key = itemgetter("gscore"), reverse = True)

        size = len(final_list)
        if size > 25:
            size = 25

        embed = discord.Embed(title = f"LEADERBOARD SEASON IV", description = f"Top {size} Gamers", color = 0x7289da)
        #embed.set_image(url = gamer.avatar_url)
        #embed.set_footer(text=f"Account Created On {born}")
        cat = 0
        for user in final_list:
            cat += 1
            if cat == 26:
                break
            name = user["name"]
            level = user["level"]
            cur_xp = int(user["cur_xp"])
            max_xp = int(user["max_xp"])
            secs = user["mins"]
            hours = round(((secs*60) / 3600),2)
            if cat == 1:
                embed.add_field(name=f":first_place:{cat}.\t{name}\t{hours} Hours", value=f"Level {level}\t[{cur_xp}/{max_xp}] XP",inline=False)
            elif cat == 2:
                embed.add_field(name=f":second_place:{cat}.\t{name}\t{hours} Hours", value=f"Level {level}\t[{cur_xp}/{max_xp}] XP",inline=False)
            elif cat == 3:
                embed.add_field(name=f":third_place:{cat}.\t{name}\t{hours} Hours", value=f"Level {level}\t[{cur_xp}/{max_xp}] XP",inline=False)
            else:
                embed.add_field(name=f":medal:{cat}.\t{name}\t{hours} Hours", value=f"Level {level}\t[{cur_xp}/{max_xp}] XP",inline=False)
        #embed.add_field(name=f"Gamer Hours", value=f"{hours}", inline=False)
        #embed.add_field(name=f"Schmeckles", value=f"${cash}", inline=False)
        #embed.add_field(name=f"Messeges Sent", value=f"{msgSent}", inline=False)
        #embed.add_field(name=f"Images Sent", value=f"{imgSent}", inline=False)
        await ctx.send(embed = embed)
        return

def setup(client):
    client.add_cog(LeaderBoardCommand(client))
