import os
import discord
from discord import Embed
from discord.ext import commands,tasks
from discord_buttons_plugin import *

import random
from datetime import datetime, timedelta
from pytz import timezone

client = commands.Bot(command_prefix='^')
buttons = ButtonsClient(client)
valid_create = 0




@client.event
async def on_ready():
    print("{0.user} is online".format(client))
    channel = client.get_channel(870635831927398412)
    #await channel.send("**CEO is online**")
    run.start()



@client.command()
async def purge(ctx, number):
    msg = []
    channel = ctx.message.channel
    number = int(number)
    async for x in channel.history(limit=number):
        await x.delete()
        #msg.append(x)
    #await client.delete_message(msg)


@client.command(name='start', help='Schedule a Task')
async def start(ctx):
    embed = discord.Embed(title="Schedule a Task", url="https://asgphone.netlify.app/", color=discord.Color.purple(), description="You can schedule a task here")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://image.shutterstock.com/image-vector/illustration-calendar-mascot-wearing-eyeglasses-260nw-749034274.jpg")
    embed.add_field(name="^profile", value="Update your profile information")
    embed.add_field(name="^add", value="Add a task")
    embed.add_field(name="^show", value="Show all current tasks")
    embed.add_field(name="^points", value="Display your current points")
    embed.add_field(name="^reward", value="You can claim points after you've done your tasks")
    embed.add_field(name="^time", value="Check how much time left for a particular task")
    embed.add_field(name="^me", value="Show current profile and tasks") 
    embed.add_field(name="^complete", value="Enter your task name when you are done to show that you've completed a task")
    embed.set_footer(text="Currently in progress")
    await ctx.channel.send(embed=embed)

@tasks.loop(seconds=20)
async def run():
    channel = client.get_channel(870635831927398412)
    
    #utc = datetime.now(timezone('UTC'))
    #asia = utc.astimezone(timezone('Asia/Shanghai'))
    asia = datetime.now()
    date = asia.strftime("%d/%m/%Y")
    time = asia.strftime("%H:%M:%S")
    time = time.split(":")
    for file in os.listdir("./"):
        if file.endswith(".txt"):
            if len(file) == 22:
                # a user
                #await channel.send(file)
                lines = None
                tmp_data = []
                with open(file, "r") as f:
                    f.seek(0)
                    rmv = []
                    lines = f.readlines()
                    tmp_data += [lines[0].rstrip("\n"), lines[1].rstrip("\n")]
                    for i in range(2, len(lines)):
                        cmp_time = lines[i]
                        if cmp_time == "" or cmp_time == '\n':
                            continue
                        else:
                            t_name, t_d, t_t, s_d, s_t = cmp_time.split('+')
                            t_t = t_t.split(":")
                            if date == t_d:
                                if int(time[0]) > int(t_t[0]):
                                    # time already passed 
                                    rmv += [cmp_time]
                                    await channel.send(f'Times up on {t_name}', tts=True)

                                elif int(time[0]) == int(t_t[0]):
                                    if int(time[1]) > int(t_t[1]):
                                        rmv += [cmp_time]
                                        await channel.send(f'Times up on {t_name}', tts=True)
                                    elif int(time[1]) == int(t_t[1]):
                                        if int(time[2]) >= int(t_t[2]):
                                            # times up
                                            rmv += [cmp_time]
                                            await channel.send(f'Times up on {t_name}', tts=True)

                            if cmp_time not in rmv:
                                cmp_time = cmp_time.rstrip("\n")
                                tmp_data += [cmp_time]
                #print(rmv)
                #print(tmp_data)
                if len(rmv) != 0:
                    with open(file, "w") as f:
                        for line in tmp_data:
                            if line != tmp_data[-1]:
                                f.write(line + "\n")
                            else:
                                f.write(line)

                    
"""
@run.before_loop
async def check_time():
"""    

@client.command()
async def add(ctx):
    channel = ctx.message.channel
    author_id = ctx.message.author.id
    my_time = datetime.now()
    date = my_time.strftime("%d/%m/%Y")
    time = my_time.strftime("%H:%M:%S") 

   #if ctx.message.author.id != 576998392463491084:
    #utc = datetime.now(timezone('UTC'))
    #asia = utc.astimezone(timezone('Asia/Shanghai'))
    #date = asia.strftime("%d/%m/%Y")
    #time = asia.strftime("%H:%M:%S")

    await channel.send(f'**Schedule format "DD/MM/YYYY+HH:MM:SS". Current time is {date} {time}**')
    target_time = await client.wait_for('message', timeout=120)
    if "+" not in target_time.content or target_time.content.count('+') != 1 or len(target_time.content) != 19:
        await channel.send("**Incorrect Format**")
        return
    await channel.send("Enter your task name")
    task = await client.wait_for('message', timeout=120)
    get_files = str(author_id) + ".txt"
    with open(get_files, "a") as f:
        f.write("\n"+task.content + "+" + target_time.content + "+" + date + "+" + time)


@client.command() 
async def time(ctx):
    channel = ctx.message.channel
    author = ctx.message.author.id

    avatar = ["https://i.pinimg.com/736x/51/96/b3/5196b34be5aec2079e4b68190299a544.jpg", 
                "https://i.pinimg.com/originals/08/27/23/082723ad570164eb39b670dbad5ee92a.jpg",
                "https://avatarfiles.alphacoders.com/671/thumb-67133.jpg",
                "https://i.pinimg.com/originals/b1/92/4d/b1924dce177345b5485bb5490ab3441f.jpg",
                "https://as1.ftcdn.net/jpg/01/75/17/38/500_F_175173865_kd6eeWCchusPNf0FisA0ZhKRT95k5oqg.jpg",
                "https://i.pinimg.com/originals/2a/39/ea/2a39eac5ac43df309e8ad6109cb38e0a.png"]
   
    time_now = datetime.now()
    for file in os.listdir("./"):
        if file.endswith(".txt") and len(file) == 22:
            # is a profile 

            with open(file, "r") as f:
                lines = f.readlines()
                embed = discord.Embed(title=lines[0], url="https://asgphone.netlify.app/", color=discord.Color.red(), description=lines[1])
                embed.set_author(name=lines[0], icon_url=avatar[random.randint(0 , len(avatar) -1)])
                embed.set_thumbnail(url="https://i.pinimg.com/originals/f0/1d/bc/f01dbc4b82496fd86428079d76c2f9c2.png") 

                if len(lines) <= 2:
                    embed.add_field(name="Error", value="No Tasks available")
                else:
                    for i in range(2, len(lines)):
                        time_cmp = lines[i].split("+")
                        d,t = time_cmp[1], time_cmp[2]
                        task = time_cmp[0]
                        date = d.split("/")
                        time = t.split(":")
                        d = list(map(int, date))
                        t = list(map(int, time))
                        construct = datetime(d[2], d[1], d[0], t[0], t[1], t[2])
                        #print(construct)
                        diff = str(construct - time_now)
                        #diff = diff.strftime("%H:%M:%S")
                        diff = diff.split(":")
                        #print(diff)
                        d,h,m,s = [0] * 4
                        tmp = diff[0]

                        if ', ' in tmp:
                            days = diff[0].split(', ')
                            num_days = days[0].split()
                            d = int(num_days[0])
                            h, m = int(days[1]), int(diff[1])
                       
                            
                        else:
                            h,m = int(diff[0]), int(diff[1])

                        s = diff[2].split('.')
                        s = int(s[0])
                        time_left = ""
                        if d != 0:
                            time_left += f'{d} Days '
                        if h != 0:
                            time_left += f'{h} Hours '
                        if m != 0:
                            time_left += f'{m} Minutes '
                        if s != 0:
                            time_left += f'{s} Seconds'
                        time_left += ' left'
                        embed.add_field(name=f'**{time_left}**', value = f'*Task {i-1}: {task}*', inline=False)

                await channel.send(embed=embed)




@client.command()
async def profile(ctx):
    channel = ctx.channel
    #await channel.send("**Currently in Progress**")
    global valid_create
    valid_create = ctx.message.author.id
    await buttons.send(
        content = "**Please Click on the button to Schedule a Task**",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label="Create",
                    style=ButtonType().Primary,
                    custom_id="create_btn"
                ),
                Button(
                    label="Update",
                    style=ButtonType().Danger,
                    custom_id="update_btn"

                )
            ])
        ] 
    )


@buttons.click
async def create_btn(ctx):
    await ctx.reply("")
    channel = ctx.channel
    global valid_create
    file_name = str(valid_create) + '.txt'
    if os.path.isfile(file_name):
        await channel.send("**You have already created a profile, Do ^me to see your profile**")
        return
    
    await channel.send("Please Enter your Username")
    name = await client.wait_for('message', timeout=60)
    #print(name.content)

    await channel.send("Please Enter your Description") 
    desc = await client.wait_for('message', timeout=60)
    #print(desc.content)
    with open(file_name, 'w') as f:
        # create file
        f.write(name.content)
        f.write('\n')
        f.write(desc.content)
    avatar = ["https://i.pinimg.com/736x/51/96/b3/5196b34be5aec2079e4b68190299a544.jpg", 
                "https://i.pinimg.com/originals/08/27/23/082723ad570164eb39b670dbad5ee92a.jpg",
                "https://avatarfiles.alphacoders.com/671/thumb-67133.jpg",
                "https://i.pinimg.com/originals/b1/92/4d/b1924dce177345b5485bb5490ab3441f.jpg",
                "https://as1.ftcdn.net/jpg/01/75/17/38/500_F_175173865_kd6eeWCchusPNf0FisA0ZhKRT95k5oqg.jpg",
                "https://i.pinimg.com/originals/2a/39/ea/2a39eac5ac43df309e8ad6109cb38e0a.png"]


    embed = discord.Embed(title=name.content + "'s Profile", url="https://asgphone.netlify.app/", color=discord.Color.gold(), description=desc.content)
    embed.set_author(name=name.content, icon_url=avatar[random.randint(0, len(avatar) -1)])
    embed.set_thumbnail(url="https://i.pinimg.com/originals/f0/1d/bc/f01dbc4b82496fd86428079d76c2f9c2.png")
    await channel.send("**Profile successfully created.**\n", embed=embed)


@client.command()
async def me(ctx):
    channel = ctx.message.channel
    check_file = str(ctx.message.author.id) + '.txt'
    if not os.path.isfile(check_file):
        await channel.send("**You haven't created a profile yet**")
        return

    avatar = ["https://i.pinimg.com/736x/51/96/b3/5196b34be5aec2079e4b68190299a544.jpg", 
                "https://i.pinimg.com/originals/08/27/23/082723ad570164eb39b670dbad5ee92a.jpg",
                "https://avatarfiles.alphacoders.com/671/thumb-67133.jpg",
                "https://i.pinimg.com/originals/b1/92/4d/b1924dce177345b5485bb5490ab3441f.jpg",
                "https://as1.ftcdn.net/jpg/01/75/17/38/500_F_175173865_kd6eeWCchusPNf0FisA0ZhKRT95k5oqg.jpg",
                "https://i.pinimg.com/originals/2a/39/ea/2a39eac5ac43df309e8ad6109cb38e0a.png"]
    with open(check_file, "r") as f:
        f.seek(0)
        data = f.readlines()
        embed = discord.Embed(title=data[0], url="https://asgphone.netlify.app/", color=discord.Color.green(), description=data[1])
        embed.set_author(name=data[0], icon_url=avatar[random.randint(0 , len(avatar) -1)])
        embed.set_thumbnail(url="https://i.pinimg.com/originals/f0/1d/bc/f01dbc4b82496fd86428079d76c2f9c2.png") 
        if len(data) != 2:
            embed.add_field(name="**Not Completed**", value=u'\u2718')

        for i in range(2, len(data)):
            if data[i] == "" or data[i] == "\n":
                continue
            else:
                t_name, t_d, t_t, s_d, s_t = data[i].split('+')
                #embed.add_field(name=u'\u2713', value="testing")
                embed.add_field(name=f'Due: {t_d} {t_t}\n', value=f'*Task {i-1}: {t_name}*', inline=False)
            #in_embed = discord.Embed(title = "testing", url="https://asgphone.netlify.app/", color=discord.Color.red(), description="RIP")

        #embed.add_field(name="**Completed**", value=u'\u2713')
        await channel.send(embed=embed)

    



@buttons.click
async def update_btn(ctx):
    channel = ctx.channel
    check_file = str(valid_create) + '.txt'
    if not os.path.isfile(check_file):
        await channel.send("**Profile not found, please create a profile with ^profile**")
        return
    await ctx.reply("")
    await buttons.send(
        content = "**What do you want to change**",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label="Name",
                    style=ButtonType().Primary,
                    custom_id="up_name"
                ),
                Button(
                    label="Description",
                    style=ButtonType().Success,
                    custom_id="up_desc"

                ),
                Button(
                    label="Profile Picture",
                    style=ButtonType().Danger,
                    custom_id="up_profile"

                )
            ])
        ] 
    )

@buttons.click
async def up_name(ctx):
    await ctx.reply("")
    channel = ctx.channel
    await channel.send("Please enter new username.")
    new_name = await client.wait_for("message", timeout=60)
    check_file = str(valid_create) + '.txt'
    data = None
    with open(check_file, 'r') as f:
        data = f.readlines()
    data[0] = new_name.content + '\n'
    with open(check_file, 'w') as f:
        f.writelines(data)
    await channel.send("**Profile username modified. Please do ^me**")

@buttons.click
async def up_desc(ctx):
    await ctx.reply("")
    channel = ctx.channel
    await channel.send("Please enter new description.")
    new_desc = await client.wait_for("message", timeout=60)
    check_file = str(valid_create) + '.txt'
    data = None
    with open(check_file, 'r') as f:
        data = f.readlines()
    data[1] = new_desc.content + '\n'
    with open(check_file, 'w') as f:
        f.writelines(data)
    await channel.send("**Profile username modified. Please do ^me**")


@buttons.click
async def up_profile(ctx):
    await ctx.reply("**Not available**")



@client.command()
async def log(ctx, amount:int):
    log = []
    channel = ctx.channel
    async for message in channel.history(limit=int(amount)):
        log.append(message)

    with open('log.txt', 'a') as f:
        for c in range(len(log)):
            f.write(f'{log[c].author}: {log[c].content}\n')



client.run("ODczMDc5MTMzNzQ2Mzg0OTQ3.YQzMTg.TCEm6yhfdoNZC9s-06vbAIzO7E0")

