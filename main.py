#SkylerHere
import discord
import os
import asyncio
import random
from dotenv import load_dotenv
from typing import Final, Dict, List
intents = discord.Intents.all()
intents.members=True
intents.message_content=True
intents.presences=True
intents.guilds=True
intents.messages=True

#Declaring Bot
bot = discord.Bot(intents=intents)

# Constants
QUESTIONS: Final[List[str]] = ["Announcement Title: ", "Announcement Short Description: ", "Field Title: ", "Field Description: ", "Mention The Channel: "]
DICE_NUMBERS: Final[List[str]] = ["1", "2", "3", "4", "5", "6"]
VOTE_URL: Final[str] = "https://top.gg/bot/1053315848980410369/vote"

# Status
STATUS_ONLINE: Final[str] = "I'm online! 🟢"
STATUS_IDLE: Final[str] = "I'm idle! 🌙"
STATUS_DISTURB: Final[str] = "Do not disturb! ⛔"
STATUS_OFFLINE: Final[str] = "I'm going offline... 😔"

PLAYING: Final[str] = "Now I'm playing {}"
QUESTION_PROMPT: Final[str] = "Answer The Following Questions (10 mins left)"
QUESTION_END: Final[str] = "Done! Go check your announcement!"
QUESTION_TIMEOUT: Final[str] = "Ran out of time for the announcement command. Try again!"

RPC_TIE: Final[str] = "{0}: {1} | {2}: {1}. It's a tie!"
RPC_WIN: Final[str] = "{0}: {1} | {2}: {3}. The win goes to {2}!"
RPC_WIN_2: Final[str] = "{0}: {1} | {2}: {3}. The win goes to {1}!"
RPC_TIMEOUT: Final[str] = "Ran out of time for Rock, Papper, Scissors Try again!"

MEMBER_VERIFY: Final[str] = "Verified"
MEMBER_ALREADY_VERIFIED: Final[str] = "Member {} is already verified..."
MEMBER_VERIFIED: Final[str] = "Member {} has been verified!"

DICE_RESPONSE: Final[str] = "{0} rolled a {1}"

PURGE_RESPONSE: Final[str] = "Deleted {} messages sucessfully!"

KICK_RESPONSE: Final[str] = "{0} got kicked! Reason: {1}"
BAN_RESPONSE: Final[str] = "{0} has been banned! Reason: {1}"
NICKNAME_RESPONSE: Final[str] = "Nickname of {0} was changed to {1}"
ROLE_ADD_RESPONSE: Final[str] = "Added the role {0} to {1}!"
ROLE_REMOVE_RESPONSE: Final[str] = "Removed the role {0} from {1}"

NAME: Final[str] = "Name:"
OWNER: Final[str] = "Owner:"
SERVER_CREATION_DATE: Final[str] = "Server Creation Date:"
MEMBER_COUNT: Final[str] = "Member Count:"
SERVER_STATISTICS: Final[str] = "Server Statistics"
USER_INFORMATION: Final[str] = "User Information"
NICKNAME: Final[str] = "Nickname:"
ID: Final[str] = "ID:"
ACCOUNT_CREATION_DATE: Final[str] = "Account Creation Date:"
SERVER_JOIN_DATE: Final[str] = "Server Join Date:"

PUNCH_RESPONSE: Final[str] = "{0} punches {1} 😡"
PAT_RESPONSE: Final[str] = "{0}  pats {1}  😁"
STARE_RESPONSE: Final[str] = "{0} stares at {1} 😬"
HUG_RESPONSE: Final[str] = "{0} hugs {1} 💖"
SLAP_RESPONSE: Final[str] = "{0} slaps {1} 😱"
KISS_RESPONSE: Final[str] = "{0} is kissing {1} 💋"
YELL_RESPONSE: Final[str] = "{0} is yelling at {1} 😶"
EMOJIS: Final[List[str]] = ["☕", "🍕", "🥰", "❤", "🎄", "🎅", "❄", "⛄", "🎉", "🎂", "👋", "😂", "🤣"]

GIFS: Final[Dict[List]] = {
    "punch": [
        "https://media.tenor.com/DKMb2QPU7aYAAAAd/rin243109-blue-exorcist.gif",
        "https://media.tenor.com/tNkqMLg8l1AAAAAd/taiga.gif",
        "https://media.tenor.com/lWmjgII6fcgAAAAd/saki-saki-mukai-naoya.gif",
        "https://media.tenor.com/OYv6aDua76wAAAAd/hanagaki-takemichi-takemichi.gif",
        "https://media.tenor.com/0vILKVxQcqwAAAAd/anime-punch.gif"
    ],
    "pat": [
        "https://media.tenor.com/7xrOS-GaGAIAAAAd/anime-pat-anime.gif",
        "https://media.tenor.com/OvrmH29V-44AAAAd/pat.gif",
        "https://media.tenor.com/oGbO8vW_eqgAAAAd/spy-x-family-anya.gif",
        "https://media.tenor.com/8DaE6qzF0DwAAAAd/neet-anime.gif",
        "https://media.tenor.com/fOqJrM0oieEAAAAd/pat.gif",
        "https://media.tenor.com/0gCy2NYphkYAAAAd/anime-pat.gif",
        "https://media.tenor.com/XN3UKIE83MMAAAAd/pat-on-the-back.gif"
    ],
    "stare": [
        "https://media.tenor.com/IwyNIipPItQAAAAd/anime-naruto.gif",
        "https://media.tenor.com/-htQlAzVwKcAAAAd/anime-blinking.gif",
        "https://media.tenor.com/1opLl5UEkR4AAAAd/lamy-stare-anime-stare.gif",
        "https://media.tenor.com/T-N05UVpLLMAAAAd/anime-stare.gif",
        "https://media.tenor.com/QRVtHWCNVUoAAAAd/hayase-nagatoro-nagatoro-glare.gif",
        "https://media.tenor.com/W9kzAnY4pQoAAAAd/ram-anime.gif",
        "https://media.tenor.com/Cq87vzUWaKkAAAAd/scared-stare.gif"
    ],
    "hug": [
        "https://media.tenor.com/G_IvONY8EFgAAAAd/aharen-san-anime-hug.gif",
        "https://media.tenor.com/HYkaTQBybO4AAAAd/hug-anime.gif",
        "https://media.tenor.com/9e1aE_xBLCsAAAAd/anime-hug.gif",
        "https://media.tenor.com/Z9zjQy8uEvsAAAAd/clannad-hugs.gif",
        "https://media.tenor.com/RWD2XL_CxdcAAAAd/hug.gif",
        "https://media.tenor.com/cGFtCNuJE6sAAAAd/anime-aesthetic.gif",
        "https://media.tenor.com/PCIu5V-_c1QAAAAd/iloveyousomuch-iloveyou.gif"
    ],
    "slap": [
        "https://media.tenor.com/XiYuU9h44-AAAAAd/anime-slap-mad.gif",
        "https://media.tenor.com/eU5H6GbVjrcAAAAd/slap-jjk.gif",
        "https://media.tenor.com/Ws6Dm1ZW_vMAAAAd/girl-slap.gif",
        "https://media.tenor.com/5jBuDXkDsjYAAAAd/slap.gif",
        "https://media.tenor.com/PeJyQRCSHHkAAAAd/saki-saki-mukai-naoya.gif"
    ],
    "kiss": [
        "https://media.tenor.com/jnndDmOm5wMAAAAd/kiss.gif",
        "https://media.tenor.com/YHxJ9NvLYKsAAAAd/anime-kiss.gif",
        "https://media.tenor.com/F02Ep3b2jJgAAAAd/cute-kawai.gif",
        "https://media.tenor.com/2tB89ikESPEAAAAd/kiss-kisses.gif",
        "https://media.tenor.com/mNPxG38pPV0AAAAd/kiss-love.gif",
        "https://media.tenor.com/woA_lrIFFAIAAAAd/girl-anime.gif",
        "https://media.tenor.com/rS045JX-WeoAAAAd/anime-love.gif",
        "https://media.tenor.com/jEqmKqupnOwAAAAd/anime-kiss.gif",
        "https://media.tenor.com/UlGZ_Q5VIGQAAAAd/beyonsatann.gif"
    ],
    "yell": [
        "https://media.tenor.com/Pz9fOE6TujoAAAAd/miko-anime.gif",
        "https://media.tenor.com/X0PhsWs3DYsAAAAd/angry-mad-max.gif",
        "https://media.tenor.com/SVuIVt9pKa8AAAAd/kaguya-sama-love-is-war-anime.gif",
        "https://media.tenor.com/cc7R8hUdw2sAAAAd/chika-love-is-war.gif",
        "https://media.tenor.com/t9z9hjjRu3sAAAAd/marin-kitagawa.gif",
        "https://media.tenor.com/4tslZb_XFuoAAAAd/nonon-jakuzure-jakuzure.gif",
        "https://media.tenor.com/zIkh-MKfnW0AAAAd/anime-scream.gif"
    ]
}

#Adding Bot Activity
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Fallout 4"))
    print("Bot {0.user} is running...".format(bot))

#Add message reactions
@bot.event
async def on_message(msg): 
    match msg.content.lower():
        case "coffee":
            await msg.add_reaction(EMOJIS[0])
        case "pizza":
            await msg.add_reaction(EMOJIS[1])
        case "love you":
            await msg.add_reaction(EMOJIS[2])
        case "miss you":
            await msg.add_reaction(EMOJIS[3])
        case "christmas" | "xmas":
            await msg.add_reaction(EMOJIS[4])
            await msg.add_reaction(EMOJIS[5])
            await msg.add_reaction(EMOJIS[6])
        case "snowman" | "olaf":
            await msg.add_reaction(EMOJIS[7])
        case "my birthday" | "bday" | "birthday":
            await msg.add_reaction(EMOJIS[8])
            await msg.add_reaction(EMOJIS[9])
        case "hello" | "hi":
            await msg.add_reaction(EMOJIS[10])
        case "lol":
            await msg.add_reaction(EMOJIS[11])
        case "xd":
            await msg.add_reaction(EMOJIS[12])

#Patch Notes Command
@bot.slash_command(name='patchnotes', description='Details about the latest SofieBot updates')
async def self(ctx: discord.ApplicationContext):
    patchnotes_embed = discord.Embed(title='Patch Notes 1.2.5', colour=discord.Colour.random())
    patchnotes_embed.set_thumbnail(url = 'https://i.ibb.co/fdkCK3Q/gz-KQ1l-Mn-KDPg-L2-Dj0-TTV-1-86w58.jpg')
    patchnotes_embed.add_field(name="Rock Paper Scissors", value="Now you can play Rock Paper Scissors with other members", inline=False)
    await ctx.respond(embed = patchnotes_embed)

#Rock Paper Scissors Command
@bot.slash_command(name='rockpaper', description='Play Rock Paper Scissors')
async def rockpaper(ctx: discord.ApplicationContext, member: discord.Member, choice: str):
    user_value: Final[str] = choice.lower()
    member_value: Final[str] = message.content.lower()
    author: Final[str] = ctx.author

    def check(message: discord.Message):
        return message.author == member and message.channel == ctx.channel
    
    try:
        await ctx.respond(f"Hey {member.mention}, {author.name} challenged you to Rock Paper Scissors and it's your turn:")
        message =  await bot.wait_for('message', check=check, timeout=120)
    except asyncio.TimeoutError:
        await ctx.respond(RPC_TIMEOUT)
        return
    
    match user_value:
        case "rock":
            match member_value:
                case "rock":
                    await ctx.respond(RPC_TIE.format(author.name, "🗿", member.name))
                case "paper":
                    await ctx.respnd(RPC_WIN.format(author.name, "🗿", member.name, "📄"))
                case "scissors":
                    await ctx.respond(RPC_WIN_2.format(author.name, "🗿", member.name, "✂"))
        case "paper":
            match member_value:
                case "rock":
                    await ctx.respond(RPC_WIN_2.format(author.name, "📄", member.name, "🗿"))
                case "paper":
                     await ctx.respond(RPC_TIE.format(author.name, "📄", member.name))
                case "scissors":
                    await ctx.respond(RPC_WIN.format(author.name, "📄", member.name, "✂"))
        case "scissors":
            match member_value:
                case "rock":
                    await ctx.respond(RPC_WIN.format(author.name, "✂", member.name, "🗿"))
                case "paper":
                    await ctx.respond(RPC_WIN_2.format(author.name, "✂", member.name, "📄"))
                case "scissors":
                    await ctx.respond(RPC_TIE.format(author.name, "✂", member.name))

#Vote Command
@bot.slash_command(name='vote', description='Vote for Sofie on top.gg')
async def vote(ctx: discord.ApplicationContext):
    await ctx.respond(VOTE_URL)

#Change Bot's Status Command
@bot.slash_command(name='status', description='Change the current status of the bot')
@discord.default_permissions(administrator=True)
async def status(ctx: discord.ApplicationContext, status_text: str):
    match status_text.lower():
        case "online":
            await bot.change_presence(status = discord.Status.online)
            await ctx.respond(STATUS_ONLINE)
        case "idle":
            await bot.change_presence(status = discord.Status.idle)
            await ctx.respond(STATUS_IDLE)
        case "disturb":
            await bot.change_presence(status = discord.Status.do_not_disturb)
            await ctx.respond(STATUS_DISTURB)
        case "offline":
            await ctx.respond(STATUS_OFFLINE)
            await bot.change_presence(status = discord.Status.offline)

#Change Bot's Playing Activity Command
@bot.slash_command(name='playing', description='Change the game that the bot is playing')
@discord.default_permissions(administrator=True)
async def playing(ctx: discord.ApplicationContext, *, text: str):
    await bot.change_presence(activity = discord.Game(name=text))
    await ctx.respond(PLAYING.format(text))

#Announcement Command
@bot.slash_command(name='announcement', description='Make an announcement in an embed message')
@discord.default_permissions(administrator=True)
async def announce(ctx: discord.ApplicationContext):
    await ctx.respond(QUESTION_PROMPT)
    replies: List[str] = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel

    for question in QUESTIONS:
        await ctx.send(question)

        try:
            msg = await bot.wait_for('message', timeout=600, check=check)
        except asyncio.TimeoutError:
            await ctx.send(QUESTION_TIMEOUT)
            return
        else:
            replies.append(msg.content)

    if len(replies) != 5:
        return
    
    channel = bot.get_channel(int(replies[4][2:-1]))
    announcement = discord.Embed(title=replies[0], description=replies[1], colour = discord.Colour.random())
    announcement.add_field(name=replies[2], value=replies[3], inline=False)
    announcement.set_thumbnail(url = ctx.guild.icon)

    await channel.send(embed = announcement)
    await ctx.respond(QUESTION_END)

#Give verified role to a member/verify a member command
@bot.slash_command(name='verify', description='Make a member verified')
@discord.default_permissions(manage_roles=True)
async def verify(ctx: discord.ApplicationContext, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name=MEMBER_VERIFY)
    msg: str = None

    if role in member.roles:
        msg = MEMBER_ALREADY_VERIFIED.format(member.mention)
    elif role not in member.roles and role in ctx.guild.roles:
        await member.add_roles(role)
        msg = MEMBER_VERIFIED.format(member.mention)
    elif role not in member.roles and role not in ctx.guild.roles:
        await ctx.guild.create_role(name = MEMBER_VERIFY, color = discord.Colour(0x2ecc71))
        await member.add_roles(discord.utils.get(ctx.guild.roles, name = MEMBER_VERIFY))
        msg = MEMBER_VERIFIED.format(member.mention)
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.respond(msg)

#Say command
@bot.slash_command(name='say', description='Make Sofie say anything!')
async def say(ctx: discord.ApplicationContext, *, text):
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.respond(text)

#Server stats command
@bot.slash_command(name='serverstats', description='Shows server statistics')
async def serverstats(ctx: discord.ApplicationContext):
    stats_embed: discord.Embed = discord.Embed(title=SERVER_STATISTICS, colour=discord.Colour.random())
    stats_embed.add_field(name=NAME, value=ctx.guild.name, inline=False)
    stats_embed.add_field(name=OWNER, value=ctx.guild.owner, inline=False)
    stats_embed.add_field(name=SERVER_CREATION_DATE, value=ctx.guild.created_at, inline=False)
    stats_embed.add_field(name=MEMBER_COUNT, value=ctx.guild.member_count, inline=False)
    stats_embed.set_thumbnail(url=ctx.guild.icon)
    await ctx.respond(embed = stats_embed)
    
#Dice roll command
@bot.slash_command(name='dice', description='Roll a dice')
async def dice(ctx: discord.ApplicationContext):
    roll: Final[str] = random.choice(DICE_NUMBERS)
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.respond(DICE_RESPONSE.format(ctx.author, roll))

#User avatar command
@bot.slash_command(name='useravatar', description="Get a member's avatar or your own")
async def useravatar(ctx: discord.ApplicationContext, *, member: discord.Member=None):
    member = ctx.author if not member else member
    avatar_embed: discord.Embed = discord.Embed(title=member.name)
    avatar_embed.set_image(url=member.avatar)
    await ctx.respond(embed = avatar_embed)

#User info command
@bot.slash_command(name='userinfo', description='Get user information')
async def userinfo(ctx: discord.ApplicationContext, *, member: discord.Member=None):
    member: discord.Member = ctx.author if member is None else member
    info_embed: discord.Embed = discord.Embed(title=USER_INFORMATION, colour=discord.Colour.random())
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name=NAME, value=member.name, inline=False)
    info_embed.add_field(name=NICKNAME, value=member.nick, inline=False)
    info_embed.add_field(name=ID, value=member.id, inline=False)
    info_embed.add_field(name=ACCOUNT_CREATION_DATE, value=member.created_at, inline=False)
    info_embed.add_field(name=SERVER_JOIN_DATE, value=member.joined_at, inline=False)
    await ctx.respond(embed = info_embed)

#Purge command
@bot.slash_command(name='purge', description='Delete messages in a channel')
@discord.default_permissions(manage_messages=True)
async def purge(ctx: discord.ApplicationContext, amount: int):
    await ctx.channel.purge(limit=amount)
    feedback = await ctx.respond(PURGE_RESPONSE.format(amount))
    await asyncio.sleep(3)
    await feedback.delete()

#Kick command
@bot.slash_command(name='kick', description='Kick a member')
@discord.default_permissions(kick_members=True)
async def kick(ctx: discord.ApplicationContext, member: discord.Member, *, reason: str):
    await member.kick(reason=reason)
    await ctx.respond(KICK_RESPONSE.format(member, reason))

#Ban command
@bot.slash_command(name='ban', description='Ban a member')
@discord.default_permissions(ban_members=True)
async def ban(ctx: discord.ApplicationContext, member: discord.Member, *, reason: str):
    await member.ban(reason=reason)
    await ctx.respond(BAN_RESPONSE.format(member, reason))

#Change nickname command
@bot.slash_command(name='nickname', description="Change nickname of a member")
@discord.default_permissions(manage_nicknames=True)
async def nickname(ctx: discord.ApplicationContext, member: discord.Member, *, name):
    await member.edit(nick=name)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.respond(NICKNAME_RESPONSE.format(member.mention, name))

#Add role command
@bot.slash_command(name='addrole', description='Give a role to a member')
@discord.default_permissions(manage_roles=True)
async def giverole(ctx: discord.ApplicationContext, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.respond(ROLE_ADD_RESPONSE.format(role.mention, member.mention))

#Delete role command
@bot.slash_command(name='delrole', description='Remove a role from a member')
@discord.default_permissions(manage_roles=True)
async def removerole(ctx: discord.ApplicationContext, member: discord.Member, *, role: discord.Role):
    await member.remove_roles(role)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.respond(ROLE_REMOVE_RESPONSE.format(role.mention, member.mention))

#Punch command
@bot.slash_command(name='punch', description=' Punch someone')
async def punch(ctx: discord.ApplicationContext, member: discord.Member):
    random_punch: Final[str] = random.choice(GIFS["punch"])
    punch_embed: discord.Embed = discord.Embed(description=PUNCH_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    punch_embed.set_thumbnail(url = random_punch)
    await ctx.respond(embed = punch_embed)

#Pat command
@bot.slash_command(name='pat', description='Pat someone')
async def pat(ctx: discord.ApplicationContext, member: discord.Member):
    random_pat = random.choice(GIFS["pat"])
    pat_embed: discord.Embed = discord.Embed(description=PAT_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    pat_embed.set_thumbnail(url = random_pat)
    await ctx.respond(embed = pat_embed)

#Stare command
@bot.slash_command(name='stare', description='Stare at someone')
async def stare(ctx: discord.ApplicationContext, member: discord.Member):
    random_stare = random.choice(GIFS["stare"])
    stare_embed: discord.Embed = discord.Embed(description=STARE_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    stare_embed.set_thumbnail(url = random_stare)
    await ctx.respond(embed = stare_embed)

#Hug command
@bot.slash_command(name='hug', description='Hug someone')
async def hug(ctx: discord.ApplicationContext, member: discord.Member):
    random_hug = random.choice(GIFS["hug"])
    hug_embed: discord.Embed = discord.Embed(description=HUG_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    hug_embed.set_thumbnail(url = random_hug)
    await ctx.respond(embed = hug_embed)

#Slap command
@bot.slash_command(name='slap', description='Slap someone')
async def slap(ctx: discord.ApplicationContext, member: discord.Member):
    random_slap = random.choice(GIFS["slap"])
    slap_embed: discord.Embed = discord.Embed(description=SLAP_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    slap_embed.set_thumbnail(url = random_slap)
    await ctx.respond(embed = slap_embed)

#Kiss command
@bot.slash_command(name='kiss', description='Kiss someone')
async def kiss(ctx: discord.ApplicationContext, member: discord.Member):
    random_kiss = random.choice(GIFS["kiss"])
    kiss_embed: discord.Embed = discord.Embed(description=KISS_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    kiss_embed.set_thumbnail(url = random_kiss)
    await ctx.respond(embed = kiss_embed)

#Yell command
@bot.slash_command(name='yell', description='Yell at someone')
async def yell(ctx: discord.ApplicationContext, member: discord.Member):
    random_yell = random.choice(GIFS["yell"])
    yell_embed: discord.Embed = discord.Embed(description=YELL_RESPONSE.format(ctx.author.name, member.mention), colour=discord.Colour.random())
    yell_embed.set_thumbnail(url = random_yell)
    await ctx.respond(embed = yell_embed)

#Running the bot
load_dotenv
try:
    bot.run(os.getenv('TOKEN'))
except:
    os.system("kill 1")