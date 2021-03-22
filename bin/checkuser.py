import json

async def CheckUser(member):
    # I do not want any bot accounts added into my database
    if member.bot:
        print(f"{member.name} is a bot!")
        return
    # Open the json data and pour it into a list
    with open ("data/userinfo.json") as f:
        data = json.load(f)
    users = list(data.keys()) # Keys are unique discord IDs

    if str(member.id) not in users:
        data[member.id]={"name":member.name,"level":1,"cur_xp":0,"max_xp":100,"onToday":False,"streak":0,"img_sent":0,"msg_sent":0,"gold":0,"role":"unknown","mins":0,"gscore":0,"pollution":0,"study_mins":0}
        with open("data/userinfo.json", 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{member.name} added to data")
        return
    else:
        # print(f"{member.name} already exist in data")
        return
