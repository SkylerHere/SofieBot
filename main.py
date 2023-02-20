#SkylerHere
import discord
import os
import asyncio
import random
from dotenv import load_dotenv
intents = discord.Intents.all()
intents.members=True
intents.message_content=True
intents.presences=True
intents.guilds=True
intents.messages=True

#Declaring Bot
bot = discord.Bot(intents=intents)

#Adding Bot Activity
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Fallout 4"))
    print("Bot {0.user} is running...".format(bot))

#Add message reactions
@bot.event
async def on_message(msg): 
    if 'coffee' in msg.content:
        await msg.add_reaction('☕')

    if 'pizza' in msg.content:
        await msg.add_reaction('🍕')

    if 'love you' in msg.content:
        await msg.add_reaction('🥰')

    if 'miss you' in msg.content:
        await msg.add_reaction('❤')

    if 'christmas' in msg.content or 'xmas' in msg.content:
        await msg.add_reaction('🎄')
        await msg.add_reaction('🎅')
        await msg.add_reaction('❄')

    if 'snowman' in msg.content or 'Olaf' in msg.content:
        await msg.add_reaction('⛄')

    if 'my birthday' in msg.content or 'birthday' in msg.content:
        await msg.add_reaction('🎉')
        await msg.add_reaction('🎂')

    if 'Hello' in msg.content or 'Hi' in msg.content:
        await msg.add_reaction('👋')
    
    if 'lol' in msg.content or 'LOL' in msg.content:
        await msg.add_reaction('😂')

    if 'xd' in msg.content or 'xD' in msg.content:
        await msg.add_reaction('🤣')

#Patch Notes Command
@bot.slash_command(name='patchnotes', description='Details about the latest SofieBot updates')
async def self(ctx: discord.ApplicationContext):
    patchnotes_embed = discord.Embed(title='Patch Notes 1.2.2', colour=discord.Colour.random())
    patchnotes_embed.set_thumbnail(url = 'https://i.ibb.co/fdkCK3Q/gz-KQ1l-Mn-KDPg-L2-Dj0-TTV-1-86w58.jpg')
    patchnotes_embed.add_field(name="Announcement Command Timeout", value='Time limit of announcement command has been decreased to 10 minutes', inline=False)
    await ctx.respond(embed = patchnotes_embed)

#Vote Command
@bot.slash_command(name='vote', description='Vote for Sofie on top.gg')
async def vote(ctx: discord.ApplicationContext):
    await ctx.respond('https://top.gg/bot/1053315848980410369/vote')

#Change Bot's Status Command
@bot.slash_command(name='status', description='Change the current status of the bot')
async def status(ctx: discord.ApplicationContext, status_text: str):
    if ctx.author.guild_permissions.administrator:
        if status_text == 'Online' or status_text == 'online':
            await bot.change_presence(status = discord.Status.online)
            await ctx.respond("I'm online! 🟢")
    
        elif status_text == 'Idle' or status_text == 'idle':
            await bot.change_presence(status = discord.Status.idle)
            await ctx.respond("I'm idle! 🌙")

        elif status_text == 'Disturb' or status_text == 'disturb':
            await bot.change_presence(status = discord.Status.do_not_disturb)
            await ctx.respond("Do not disturb! ⛔")

        elif status_text == 'Offline' or status_text == 'offline':
            await ctx.respond("I'm going offline... 😔")
            await bot.change_presence(status = discord.Status.offline)
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Change Bot's Playing Activity Command
@bot.slash_command(name='playing', description='Change the game that the bot is playing')
async def playing(ctx: discord.ApplicationContext, *, text: str):
    if ctx.author.guild_permissions.administrator:
        bot_game = text
        await bot.change_presence(activity = discord.Game(name = bot_game))
        await ctx.respond(f"Now I'm playing {bot_game}")

#Announcement Command
@bot.slash_command(name='announcement', description='Make an announcement in an embed message')
async def announce(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        await ctx.respond('Answer The Following Questions (10 mins left)')

        questions = ["Announcement Title: ", "Announcement Short Description: ", "Field Title: ", "Field Description: ", "Mention The Channel: "]
        replies = []

        def check(user):
            return user.author == ctx.author and user.channel == ctx.channel

        for question in questions:
            await ctx.send(question)

            try:
                msg = await bot.wait_for('message', timeout=600, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Ran out of time for the announcement command. Try again!")
                return
            else:
                replies.append(msg.content)

        main_title = replies[0]
        main_desc = replies[1]
        field_title = replies[2]
        field_desc = replies[3]

        channel_id = int(replies[4][2:-1])
        channel = bot.get_channel(channel_id)

        announcement = discord.Embed(title = main_title, description = main_desc, colour = discord.Colour.random())
        announcement.add_field(name = field_title, value = field_desc, inline = False)
        announcement.set_thumbnail(url = ctx.guild.icon)

        await channel.send(embed = announcement)
        await ctx.respond("Done! Go check your announcement!")
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Give verified role to a member/verify a member command
@bot.slash_command(name='verify', description='Make a member verified')
async def verify(ctx: discord.ApplicationContext, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        role = discord.utils.get(ctx.guild.roles, name = 'Verified')
        server = ctx.guild.roles
        if role in member.roles:
            msg = f"Member {member.mention} is already verified..."
        elif role not in member.roles and role in server:
            await member.add_roles(role)
            msg = f"Member {member.mention} has been verified!"
        elif role not in member.roles and role not in server:
            await ctx.guild.create_role(name = 'Verified', color = discord.Colour(0x2ecc71))
            created_role = discord.utils.get(ctx.guild.roles, name = 'Verified')
            await member.add_roles(created_role)
            msg = f"Member {member.mention} has been verified!"
        async with ctx.typing():
            await asyncio.sleep(0.5)
            await ctx.respond(msg)
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Say command
@bot.slash_command(name='say', description='Make Sofie say anything!')
async def say(ctx: discord.ApplicationContext, *, text):
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.respond(text)

#Server stats command
@bot.slash_command(name='serverstats', description='Shows server statistics')
async def serverstats(ctx: discord.ApplicationContext):
    stats_embed = discord.Embed(title="Server Statistics", colour=discord.Colour.random())
    stats_embed.add_field(name='Name:', value=ctx.guild.name, inline=False)
    stats_embed.add_field(name='Owner:', value=ctx.guild.owner, inline=False)
    stats_embed.add_field(name='Server Created Date:', value=ctx.guild.created_at, inline=False)
    stats_embed.add_field(name='Member Count:', value=ctx.guild.member_count, inline=False)
    stats_embed.set_thumbnail(url=ctx.guild.icon)
    await ctx.respond(embed = stats_embed)
    
#Dice roll command
@bot.slash_command(name='dice', description='Roll a dice')
async def dice(ctx: discord.ApplicationContext):
    dice_numbers = ["1", "2", "3", "4", "5", "6"]
    author = ctx.author
    roll = random.choice(dice_numbers)
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.respond(f"{author} rolled a {roll}")

#User avatar command
@bot.slash_command(name='useravatar', description="Get a member's avatar or your own")
async def useravatar(ctx: discord.ApplicationContext, *, member: discord.Member=None):
    member = ctx.author if not member else member
    avatar_embed = discord.Embed(title=member.name)
    avatar_embed.set_image(url=member.avatar)
    await ctx.respond(embed = avatar_embed)

#User info command
@bot.slash_command(name='userinfo', description='Get user information')
async def userinfo(ctx: discord.ApplicationContext, *, member: discord.Member=None):
    if member is None:
        member = ctx.author
    info_embed = discord.Embed(title='User Information', colour=discord.Colour.random())
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name='Name:', value=member.name, inline=False)
    info_embed.add_field(name='Nickname:', value=member.nick, inline=False)
    info_embed.add_field(name='ID:', value=member.id, inline=False)
    info_embed.add_field(name='Account Created Date:', value=member.created_at, inline=False)
    info_embed.add_field(name='Joined Server Date:', value=member.joined_at, inline=False)
    await ctx.respond(embed = info_embed)

#Purge command
@bot.slash_command(name='purge', description='Delete messages in a channel')
async def purge(ctx: discord.ApplicationContext, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount)
        feedback = await ctx.respond(f"Deleted {amount} messages sucessfully!")
        await asyncio.sleep(3)
        await feedback.delete()
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Kick command
@bot.slash_command(name='kick', description='Kick a member')
async def kick(ctx: discord.ApplicationContext, member: discord.Member, *, reason: str):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason = reason)
        await ctx.respond(f"{member} got kicked! Reason: {reason}")
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Ban command
@bot.slash_command(name='ban', description='Ban a member')
async def ban(ctx: discord.ApplicationContext, member: discord.Member, *, reason: str):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.respond(f"{member} has been banned! Reason: {reason}")
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Change nickname command
@bot.slash_command(name='nickname', description="Change nickname of a member")
async def nickname(ctx: discord.ApplicationContext, member: discord.Member, *, name):
    if ctx.author.guild_permissions.manage_nicknames:
        await member.edit(nick=name)
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.respond(f"Nickname of {member.mention} was changed to {name}")
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Add role command
@bot.slash_command(name='addrole', description='Give a role to a member')
async def giverole(ctx: discord.ApplicationContext, member: discord.Member, *, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        await member.add_roles(role)
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.respond(f"Added the role {role.mention} to {member.mention}!")
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Delete role command
@bot.slash_command(name='delrole', description='Remove a role from a member')
async def removerole(ctx: discord.ApplicationContext, member: discord.Member, *, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        await member.remove_roles(role)
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.respond(f"Removed the role {role.mention} from {member.mention}")
    else:
        await ctx.respond("You don't have the right permissions for this command!")

#Punch command
@bot.slash_command(name='punch', description=' Punch someone')
async def punch(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/DKMb2QPU7aYAAAAd/rin243109-blue-exorcist.gif",
        "https://media.tenor.com/tNkqMLg8l1AAAAAd/taiga.gif",
        "https://media.tenor.com/lWmjgII6fcgAAAAd/saki-saki-mukai-naoya.gif",
        "https://media.tenor.com/OYv6aDua76wAAAAd/hanagaki-takemichi-takemichi.gif",
        "https://media.tenor.com/0vILKVxQcqwAAAAd/anime-punch.gif"
    ]
    random_punch = random.choice(gif)
    author = ctx.author
    punch_embed = discord.Embed(description=f'{author.name} punches {member.mention} 😡', colour=discord.Colour.random())
    punch_embed.set_thumbnail(url = random_punch)
    await ctx.respond(embed = punch_embed)

#Pat command
@bot.slash_command(name='pat', description='Pat someone')
async def pat(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/7xrOS-GaGAIAAAAd/anime-pat-anime.gif",
        "https://media.tenor.com/OvrmH29V-44AAAAd/pat.gif",
        "https://media.tenor.com/oGbO8vW_eqgAAAAd/spy-x-family-anya.gif",
        "https://media.tenor.com/8DaE6qzF0DwAAAAd/neet-anime.gif",
        "https://media.tenor.com/fOqJrM0oieEAAAAd/pat.gif",
        "https://media.tenor.com/0gCy2NYphkYAAAAd/anime-pat.gif",
        "https://media.tenor.com/XN3UKIE83MMAAAAd/pat-on-the-back.gif"
    ]
    random_pat = random.choice(gif)
    author = ctx.author
    pat_embed = discord.Embed(description=f'{author.name}  pats {member.mention}  😁', colour=discord.Colour.random())
    pat_embed.set_thumbnail(url = random_pat)
    await ctx.respond(embed = pat_embed)

#Stare command
@bot.slash_command(name='stare', description='Stare at someone')
async def stare(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/IwyNIipPItQAAAAd/anime-naruto.gif",
        "https://media.tenor.com/-htQlAzVwKcAAAAd/anime-blinking.gif",
        "https://media.tenor.com/1opLl5UEkR4AAAAd/lamy-stare-anime-stare.gif",
        "https://media.tenor.com/T-N05UVpLLMAAAAd/anime-stare.gif",
        "https://media.tenor.com/QRVtHWCNVUoAAAAd/hayase-nagatoro-nagatoro-glare.gif",
        "https://media.tenor.com/W9kzAnY4pQoAAAAd/ram-anime.gif",
        "https://media.tenor.com/Cq87vzUWaKkAAAAd/scared-stare.gif"
    ]
    random_stare = random.choice(gif)
    author = ctx.author
    stare_embed = discord.Embed(description=f'{author.name} stares at {member.mention} 😬', colour=discord.Colour.random())
    stare_embed.set_thumbnail(url = random_stare)
    await ctx.respond(embed = stare_embed)

#Hug command
@bot.slash_command(name='hug', description='Hug someone')
async def hug(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/G_IvONY8EFgAAAAd/aharen-san-anime-hug.gif",
        "https://media.tenor.com/HYkaTQBybO4AAAAd/hug-anime.gif",
        "https://media.tenor.com/9e1aE_xBLCsAAAAd/anime-hug.gif",
        "https://media.tenor.com/Z9zjQy8uEvsAAAAd/clannad-hugs.gif",
        "https://media.tenor.com/RWD2XL_CxdcAAAAd/hug.gif",
        "https://media.tenor.com/cGFtCNuJE6sAAAAd/anime-aesthetic.gif",
        "https://media.tenor.com/PCIu5V-_c1QAAAAd/iloveyousomuch-iloveyou.gif"
    ]
    random_hug = random.choice(gif)
    author = ctx.author
    hug_embed = discord.Embed(description=f'{author.name} hugs {member.mention} 💖', colour=discord.Colour.random())
    hug_embed.set_thumbnail(url = random_hug)
    await ctx.respond(embed = hug_embed)

#Slap command
@bot.slash_command(name='slap', description='Slap someone')
async def slap(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/XiYuU9h44-AAAAAd/anime-slap-mad.gif",
        "https://media.tenor.com/eU5H6GbVjrcAAAAd/slap-jjk.gif",
        "https://media.tenor.com/Ws6Dm1ZW_vMAAAAd/girl-slap.gif",
        "https://media.tenor.com/5jBuDXkDsjYAAAAd/slap.gif",
        "https://media.tenor.com/PeJyQRCSHHkAAAAd/saki-saki-mukai-naoya.gif"
    ]
    random_slap = random.choice(gif)
    author = ctx.author
    slap_embed = discord.Embed(description=f'{author.name} slaps {member.mention} 😱', colour=discord.Colour.random())
    slap_embed.set_thumbnail(url = random_slap)
    await ctx.respond(embed = slap_embed)

#Kiss command
@bot.slash_command(name='kiss', description='Kiss someone')
async def kiss(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/jnndDmOm5wMAAAAd/kiss.gif",
        "https://media.tenor.com/YHxJ9NvLYKsAAAAd/anime-kiss.gif",
        "https://media.tenor.com/F02Ep3b2jJgAAAAd/cute-kawai.gif",
        "https://media.tenor.com/2tB89ikESPEAAAAd/kiss-kisses.gif",
        "https://media.tenor.com/mNPxG38pPV0AAAAd/kiss-love.gif",
        "https://media.tenor.com/woA_lrIFFAIAAAAd/girl-anime.gif",
        "https://media.tenor.com/rS045JX-WeoAAAAd/anime-love.gif",
        "https://media.tenor.com/jEqmKqupnOwAAAAd/anime-kiss.gif",
        "https://media.tenor.com/UlGZ_Q5VIGQAAAAd/beyonsatann.gif"
    ]
    random_kiss = random.choice(gif)
    author = ctx.author
    kiss_embed = discord.Embed(description=f'{author.name} is kissing {member.mention} 💋', colour=discord.Colour.random())
    kiss_embed.set_thumbnail(url = random_kiss)
    await ctx.respond(embed = kiss_embed)

#Yell command
@bot.slash_command(name='yell', description='Yell at someone')
async def yell(ctx: discord.ApplicationContext, member: discord.Member):
    gif = [
        "https://media.tenor.com/Pz9fOE6TujoAAAAd/miko-anime.gif",
        "https://media.tenor.com/X0PhsWs3DYsAAAAd/angry-mad-max.gif",
        "https://media.tenor.com/SVuIVt9pKa8AAAAd/kaguya-sama-love-is-war-anime.gif",
        "https://media.tenor.com/cc7R8hUdw2sAAAAd/chika-love-is-war.gif",
        "https://media.tenor.com/t9z9hjjRu3sAAAAd/marin-kitagawa.gif",
        "https://media.tenor.com/4tslZb_XFuoAAAAd/nonon-jakuzure-jakuzure.gif",
        "https://media.tenor.com/zIkh-MKfnW0AAAAd/anime-scream.gif"
    ]
    random_yell = random.choice(gif)
    author = ctx.author
    yell_embed = discord.Embed(description=f'{author.name} is yelling at {member.mention} 😶', colour=discord.Colour.random())
    yell_embed.set_thumbnail(url = random_yell)
    await ctx.respond(embed = yell_embed)

#Running the bot
load_dotenv
try:
    bot.run(os.getenv('TOKEN'))
except:
    os.system("kill 1")