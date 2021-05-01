import discord
import json
from discord.ext import commands
from bin.checkuser import CheckUser

class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(alaises = ["rank"])
    async def Stats(self, ctx, user):
        #FIXME: Make a better vet for user input
        if not user[3:-1].isdigit() or len(user) != 22:
            await ctx.send("[OOF] Invalid Gamer")
            return

        # Check user off rip with valid ID
        user_id = int(user[3:-1])
        memb = await self.client.fetch_user(user_id)
        await CheckUser(memb)
        with open("data/userinfo.json", 'r') as stat_file:
            data = json.load(stat_file)

        gamer = data[str(memb.id)]
        mins = gamer["mins"]
        study_mins = gamer["study_mins"]
        hours = round((mins * 60) / 3600,2)
        study_hours = round((study_mins * 60) / 3600,2)
        gold = gamer["gold"]
        level = gamer["level"]
        cur_xp = gamer["cur_xp"]
        max_xp = gamer["max_xp"]
        msg_sent = gamer["msg_sent"]
        img_sent = gamer["img_sent"]
        name = gamer["name"]
        pollution = gamer["pollution"]
        born = ctx.message.author.created_at.strftime("%m/%d/%Y")
        stat_file.close()
            
        embed = discord.Embed(title = f"{name} Level {level}", description = f"oof", color = 0x7289da)
        embed.set_thumbnail(url = memb.avatar_url)
        embed.add_field(name=f"Experience", value=f"{int(cur_xp)}/{int(max_xp)}", inline = False)
        embed.add_field(name=f"Average Hours Per Day", value=f"WIP", inline = False)
        embed.add_field(name=f"Total Hours", value=f"{hours}", inline = False)
        embed.add_field(name=f"Study Hours", value=f"{study_hours}", inline = False)
        embed.add_field(name=f"Messages Sent", value=f"{msg_sent}", inline = False)
        embed.add_field(name=f"Files Sent", value=f"{img_sent}", inline = False)
        embed.add_field(name=f"Pollution Caused", value=f"{pollution}", inline = False)

        embed.set_footer(text=f"Account created on {born}")
        await ctx.send(embed = embed)




    @Stats.error
    async def StatsError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            with open("data/userinfo.json", 'r') as stat_file:
                data = json.load(stat_file)

            gamer = data[str(ctx.message.author.id)]
            mins = gamer["mins"]
            study_mins = gamer["study_mins"]
            hours = round((mins * 60) / 3600,2)
            study_hours = round((study_mins * 60) / 3600,2)
            gold = gamer["gold"]
            level = gamer["level"]
            cur_xp = gamer["cur_xp"]
            max_xp = gamer["max_xp"]
            msg_sent = gamer["msg_sent"]
            img_sent = gamer["img_sent"]
            name = gamer["name"]
            pollution = gamer["pollution"]
            born = ctx.message.author.created_at.strftime("%m/%d/%Y")
            stat_file.close()
            
            embed = discord.Embed(title = f"{name} Level {level}", description = f"oof", color = 0x7289da)
            embed.set_thumbnail(url = ctx.message.author.avatar_url)
            embed.add_field(name=f"Experience", value=f"{int(cur_xp)}/{int(max_xp)}", inline = False)
            embed.add_field(name=f"Average Hours Per Day", value=f"WIP", inline = False)
            embed.add_field(name=f"Total Hours", value=f"{hours}", inline = False)
            embed.add_field(name=f"Study Hours", value=f"{study_hours}", inline = False)
            embed.add_field(name=f"Messages Sent", value=f"{msg_sent}", inline = False)
            embed.add_field(name=f"Files Sent", value=f"{img_sent}", inline = False)
            embed.add_field(name=f"Pollution Caused", value=f"{pollution}", inline = False)

            embed.set_footer(text=f"Account created on {born}")
            await ctx.send(embed = embed)





def setup(client):
    client.add_cog(Stats(client))
