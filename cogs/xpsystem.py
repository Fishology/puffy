import discord
import json
from discord.ext import commands,tasks
from bin.checkuser import CheckUser # Custom json data production
from bin.timenow import TimeNow # Custom current time function
from discord.utils import get # ???
import random
from datetime import date

REFRESH_SECONDS = 180 # Everytime the discord servers will be searched
BASE_MINS = 3
BASE_XP = 3 # Every loop with give +3 XP
BONUS_XP = 2 # 10x the woots!
XP_SCALE = 1.05

RoleID1   = 791281068119556136 
RoleID10  = 791278665328754708
RoleID20  = 791278664837890048
RoleID30  = 791278664045821962
RoleID40  = 791278663332397057
RoleID50  = 791278662799851530
RoleID60  = 791278662078824458
RoleID70  = 791278661013733386
RoleID80  = 791278660215898112
RoleID90  = 791278659096543244
RoleID100 = 791278658299101195

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

churchID = 791287662827798548
forgeID = 675205322511482922
puffyChanID = 729274494408982559


guildFile = open("data/private/mainguildid.txt", "r")
KING_HEAD_ID = int(guildFile.read())
guildFile.close()

study_channel_names = []
with open("data/academic.txt","r") as file:
    for line in file:
        for word in line.split():
            study_channel_names.append(word)
    file.close()

compliments = []
with open("data/compliments.txt","r") as file2:
    for line in file2:
        compliments.append(line)
    file2.close()

class XpSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.guilds = []
        self.XpCheck.start()

    @tasks.loop(seconds=REFRESH_SECONDS)
    async def XpCheck(self):
        # Check if it is finally the right day to open the voice channel
        if date.today().weekday() == SUNDAY:
            if self.isClosed:
                print(f"{TimeNow()} opening church")
                self.perms.connect=True
                await self.churchChan.set_permissions(self.mainguild.default_role, overwrite=self.perms)
                self.isClosed = False
                await self.puffyChan.send("Church is now open!")
        else:
            if not self.isClosed:
                print(f"{TimeNow()} closing church")
                self.perms.connect=False
                await self.churchChan.set_permissions(self.mainguild.default_role, overwrite=self.perms)
                self.isClosed = True
                await self.puffyChan.send("Church is now closed!") #FIXME: ADD A GIF >:(
                if len(self.churchChan.members):
                    for member in self.churchChan.members:
                        await member.move_to(self.forgeChan)

        
        print(f"{TimeNow()} starting xpcheck...")
        gamers = [] # Gaming channels
        nerds = []  # Study channels
        users = []  # Total users
        afk_chans = []
        bonus_chans = []
        for guild in self.guilds:
            if guild.afk_channel != None:
                afk_chans.append(guild.afk_channel)
            for vchannels in guild.voice_channels:
                if vchannels not in afk_chans:
                    if vchannels.name.lower() not in study_channel_names:
                        if vchannels.name == "church":
                            for member in vchannels.members:
                                if (not member.bot):
                                    print(f"{TimeNow()} {member} is in a bonus channel")
                                    bonus_chans.append(member);
                                    users.append(member)
                        else:            
                            for member in vchannels.members:
                                if (not member.bot):
                                    gamers.append(member)
                                    users.append(member)
                                    print(f"{TimeNow()} {member} is gaming")
                    else:
                        for member in vchannels.members:
                            if (not member.bot):
                                nerds.append(member)
                                users.append(member)
                                print(f"{TimeNow()} {member} is studying")
        # If all voice channels are empty
        if (not len(users)): 
            print(f"{TimeNow()} all voice channels empty")
            return
        # Check if discord user is in our DB, if not ADD THEM :)
        for user in users:
            await CheckUser(user)

        with open("data/userinfo.json") as f:
            data = json.load(f)
        for user in users:
            gamer = data[str(user.id)]
            # Add xp and mins to database
            if (user in bonus_chans):
                gamer["cur_xp"] += BASE_XP * BONUS_XP
            else:
                gamer["cur_xp"] += BASE_XP

            if (user in nerds):
                gamer["study_mins"] += BASE_MINS
            else:
                gamer["mins"] += BASE_MINS

            # Check if lvl up
            while (gamer["cur_xp"] >= gamer["max_xp"]):
                gamer["cur_xp"] = gamer["cur_xp"] - gamer["max_xp"]
                gamer["max_xp"] *= XP_SCALE
                gamer["level"] += 1
                gamer["gold"] += 10
                level = gamer["level"]
                msg = ""
                compli = compliments[random.randint(0,len(compliments)-1)]
                compli = compli[:-1] # get rid of endline
                msg += compli
                msg += f" {user.mention}, you are now level {level}"

                # Update roles if in MAIN GUILD
                main_guild_users = self.mainguild.members
                inMainServer = False

                for kh_user in main_guild_users:
                    if user.id == kh_user.id:
                        inMainServer = True
                        break

                # If the current user has joined the main guild, updaite their roles
                changedRole = False
                if inMainServer:
                    if level == 10:
                        changedRole = True
                        prevRoleID = RoleID1
                        newRoleID = RoleID10
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 20:
                        changedRole = True
                        prevRoleID = RoleID10
                        newRoleID = RoleID20
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 30:
                        changedRole = True
                        prevRoleID = RoleID20
                        newRoleID = RoleID30
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 40:
                        changedRole = True
                        prevRoleID = RoleID30
                        newRoleID = RoleID40
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 50:
                        changedRole = True
                        prevRoleID = RoleID40
                        newRoleID = RoleID50
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 60:
                        changedRole = True
                        prevRoleID = RoleI510
                        newRoleID = RoleID60
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 70:
                        changedRole = True
                        prevRoleID = RoleID60
                        newRoleID = RoleID70
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 80:
                        changedRole = True
                        prevRoleID = RoleID70
                        newRoleID = RoleID80
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 90:
                        changedRole = True
                        prevRoleID = RoleID80
                        newRoleID = RoleID90
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)
                    elif level == 100:
                        changedRole = True
                        prevRoleID = RoleID90
                        newRoleID = RoleID100
                        prev_role = get(self.mainguild.roles, id = prevRoleID)
                        new_role = get(self.mainguild.roles, id = newRoleID)


                if changedRole:
                    msg += f" and unlocked a shiny new role! | {new_role.name}"
                    gamer["role"] = new_role.name
                    await kh_user.add_roles(new_role,reason=None,atomic=True)
                    await kh_user.remove_roles(prev_role,reason=None,atomic=True)

                await self.puffychan.send(msg)

        # Now save all data to DB
        with open("data/userinfo.json","w") as f2:
            json.dump(data,f2,indent=4)
            print(f"{TimeNow()} saved {len(users)} player(s) to database")

    # Defines the total guilds the bot is in
    @XpCheck.before_loop
    async def BeforeXpCheck(self):
        await self.client.wait_until_ready()
        guilds = await self.client.fetch_guilds(limit=150).flatten()
        self.mainguild = self.client.get_guild(KING_HEAD_ID)

        self.puffyChan = self.client.get_channel(puffyChanID)
        self.forgeChan = self.client.get_channel(forgeID)
        self.churchChan = self.client.get_channel(churchID)
        self.perms = self.churchChan.overwrites_for(self.mainguild.default_role)
        self.isClosed = not self.perms.connect

        for textchan in self.mainguild.text_channels:
            if textchan.name == "puffy":
                self.puffychan = textchan
        for guild in guilds:
            self.guilds.append(self.client.get_guild(guild.id))

def setup(client):
    client.add_cog(XpSystem(client))
