import discord
import os
import youtube_dl
from discord.ext import commands,tasks
from discord_buttons_plugin import *
from csv import writer

# fetch data
import requests
import json


#bot = discord.Client()
help_command = commands.DefaultHelpCommand(no_category = "All Functioning commands for Jane\n\n")
client = commands.Bot(command_prefix="*", help_command = help_command)
buttons = ButtonsClient(client)


@client.event
async def on_ready():
    print("We are logged in as {0.user}".format(client))
    channel = client.get_channel(870635831927398412)
    
    #await channel.send(f' **Im currently in {channel.name}** ')
      #request = 'https://private-anon-bf5c7e8319-olympicsapi.apiary-mock.com/scrape/olympics'
    #response_body = urlopen(request).read()
    reminder.start()
    

@tasks.loop(hours=1.0)
async def reminder():
    
    channel = client.get_channel(870635831927398412)
    #await channel.send("""```ini\n\t\t\t\t\t\t\t\t\t\t[***Working on Scheduling/Reminder Function ***]```""")
    game = discord.Game("Idling ...")
    await client.change_presence(status=discord.Status.online, activity=game)
    #await channel.send("""```yaml\nProfile status changed```""")
    

@client.command(name="quiz", help="Do *quiz [topic] to learn")
async def quiz(ctx, topic:str):
    channel = ctx.message.channel
    topic = topic.lower()
    if topic == "english":
        await channel.send("First 5 vocabs")
        q_num = 1
        with open("vocab.txt", "r") as data:
            lines = data.readlines()
            for line in lines:
                await channel.send(f'{q_num}. {line}')
                q_num += 1
                if q_num == 6:
                    return
    else:
        await channel.send("**We don't have this topic currently** <:Grape:40e0130a4411323cdbed71b01ee0268e>")

        
    
   
@client.command(name="news", help="Do *news to find out the latest incidents around the world")
async def news(ctx):
    channel = ctx.message.channel
    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": "85d2aca11b6046688e154776c12794dc"
    }
    url = "https://newsapi.org/v1/articles" 
    response = requests.get(url, params=query_params)
    response_json = response.json()

    with open("bbc_json.txt", "w") as man_data:
        json.dump(response_json, man_data, ensure_ascii=False, indent=4)

    #await channel.send(f'BBC response JSON struct {response_json}')    
    #await channel.send("JSON data dumped to 'bbc_json.txt'")

    bbc_news = response_json["articles"]
    news_title = []
    await channel.send("**Top News from BBC**")
    cnt = 1
    for data in bbc_news:
        title = data["title"]
        await channel.send(f'{cnt}. {title}')
        news_title.append(title)
        cnt += 1
    
    await buttons.send(
        content = "**Pick a number from 1 - 10**",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "1",
                    style = ButtonType().Link,
                    url = bbc_news[0]['url']
                    
                ),
                Button(
                    label = "2",
                    style = ButtonType().Link,
                    url = bbc_news[1]['url']
                ),
                Button(
                    label = "3",
                    style = ButtonType().Link,
                    url = bbc_news[2]['url']
                ),
                Button(
                    label = "4",
                    style = ButtonType().Link,
                    url = bbc_news[3]['url']
                ),
                Button(
                    label = "5",
                    style = ButtonType().Link,
                    url = bbc_news[4]['url']
                )
            ]),
            ActionRow([
                Button(
                    label = "6",
                    style = ButtonType().Link,
                    url = bbc_news[5]['url']
                ),
                Button(
                    label = "7",
                    style = ButtonType().Link,
                    url = bbc_news[6]['url']
                ),
                Button(
                    label = "8",
                    style = ButtonType().Link,
                    url = bbc_news[7]['url']
                ),
                Button(
                    label = "9",
                    style = ButtonType().Link,
                    url = bbc_news[8]['url']
                ),
                Button(
                    label = "10",
                    style = ButtonType().Link,
                    url = bbc_news[9]['url']
                )
            ])
        ]
    )


@client.command(name="reset", help="This is an admin command")
async def reset(ctx, file_name:str):
    #print(ctx.message.author.id)
    if ctx.message.author.id == 576998392463491084:
        os.remove(file_name)              # remove file
        with open(file_name, 'a') as new_file:     # new file
            pass
        await ctx.send('**FILE REMOVED**')
    else:
        await ctx.send("** You have no permission **")



@client.command(name="save", help="Do *save [msg] to save data")
async def save(ctx, data:str):
    #await ctx.send("Crashed...fixing")
    person = ctx.message.author
    channel = ctx.message.channel
    #await ctx.send(f'{person} has talked in {channel} text channel')
    save_content = [person, ctx.message.created_at, data]
    save_file = "storage.csv"
    flag = 0
    if os.stat(save_file).st_size == 0:
        flag = 1
    with open(save_file, 'a') as csv_obj:
        csv_writer = writer(csv_obj)
        if flag == 1:
            col = ["Author", "Time Created", "Content"]
            csv_writer.writerow(col)
            csv_writer.writerow("\n")
        csv_writer.writerow(save_content)
        csv_writer.writerow("\n")

    await ctx.send(f'Message saved to {save_file}')
    await ctx.send("""Retrieve file by doing ```ini\n[*retrieve]```""")
     

@client.command(name="retrieve", help="Do *retrieve to retrieve saved files")
async def retrieve(ctx):
    channel = ctx.message.channel
    await ctx.send(file=discord.File("./storage.csv"))
    await ctx.send(file=discord.File("./bbc_json.txt"))
    await ctx.send(file=discord.File("./log.txt"))

@client.command(name="play", help="Do *play [youtube url] to play music")
async def play(ctx, url:str):

    if url == "":
        await ctx.send("Please enter a youtube url...")
        return
    valid = 0
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != "generic":
            valid = 1
    if valid:
        #await ctx.send(f'This is the video you want to play {url}')
        song = os.path.isfile("song.mp3")
        try:
            if song:        
                os.remove("song.mp3")
        
        except PermissionError:
            await ctx.send("A audio is currently playing. Please wait or use the '*stop' command")
            return 
        is_con = discord.utils.get(client.voice_clients, guild=ctx.guild)
        
        voice_channel = ctx.message.author.voice.channel
        if is_con == None:    #if not connected to voice channel
            #voice_channel = ctx.message.author.voice.channel
            #voice_channel = discord.utils.get(ctx.guild.voice_channels, name="ALL THE BYTES!!!")
            #connected = await voice_channel.connect()       # connect to voice channels
            connected = await voice_channel.connect()
        else:
            await is_con.move_to(voice_channel)
            #await voice_channel.connect()
#            await ctx.send("Im already connected...")
            
       # print(f'{client} is in voice channel')
        
        await ctx.send("Please enter a volume number between 0 - 100")
        # wait for client respond
        
        vol = 0
        async def check(m): 
            try:
                is_num = int(m.content)
                if is_num < 0 or is_num > 100:
                    await ctx.send("Please enter a number between 0 - 100")
                    return False
                vol = is_num
                return True
            except TypeError:
                await ctx.send(f'{m.content} is not a number')
                return False
        client_v = await client.wait_for("message", check=check)
        while not client_v:
            # if it is false, continue
            client_v =  await client.wait_for("message", check=check)

        print("Got volume")
        await ctx.send(f'Volume {vol} chosen')
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloaded Successfully")
            ydl.download([url])
        for file in os.listdir("./"):       # current directory
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

        await ctx.send("Playing audio...")

        #connected.source = discord.PCMVolumeTransformer(connected.source)
        #connected.source.volume = vol

    else:
        await ctx.send("Please enter a valid Youtube url...")
        return


@client.command(name="leave", help="Do *leave to disconnect the bot")
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await ctx.send("Leaving the voice channel...")
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command(name="pause", help="Do *pause to pause an audio")
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("Audio paused...")
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")

@client.command(name="resume", help="Do *resume to continue playing")
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await ctx.send("Continue playing...")
        voice.resume()
    else:
        await ctx.send("The audio is not paused")

@client.command(name="stop", help="Do *stop to stop audio")
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.send("Force stopped")
    voice.stop()
    
    
"""
            Youtube Audio Extraction

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}


@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")



@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

"""


if __name__ == '__main__':
    client.run("ODcwMTMwODk3MDg3Nzc0Nzcw.YQISjA.fspTq7nWFOcGczOjnvd00k1q8Ss")
