import discord
import os
import asyncio
import random
from dotenv import load_dotenv
intents = discord.Intents.all()
intents.members=True
intents.message_content=True
intents.presences=True

#Adding bot prefix
from discord.ext import commands
bot = commands.Bot(command_prefix='$', intents=intents)

#Declaring guild
guild = discord.Guild

#Adding bot status
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="$help"))
    print("Bot {0.user} is running...".format(bot))

#Add message reactions
#Always add await bot.process_commands(message) at the end of an on_message event
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

    if 'my birthday' in msg.content:
        await msg.add_reaction('🎉')
        await msg.add_reaction('🎂')

    if 'Hello' in msg.content or 'Hi' in msg.content:
        await msg.add_reaction('👋')
    
    await bot.process_commands(msg)

#Give verified role to a member/verify a member command
@bot.command('verify', brief=' Make a member verified')
@commands.has_permissions(manage_roles=True)
async def verify(ctx, member: discord.Member):
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
        await ctx.send(msg)

#Say command
@bot.command(name='say', brief=' Make Sofie say anything!')
async def say(ctx, *, text):
    await ctx.message.delete()
    async with ctx.typing():
        await asyncio.sleep(2)
        await ctx.send(text)

#Server stats command
@bot.command(name='serverstats', brief=' Shows server statistics')
async def serverstats(ctx):
    stats_embed = discord.Embed(title="Server Statistics", colour=discord.Colour.random())
    stats_embed.add_field(name='Name:', value=ctx.guild.name, inline=False)
    stats_embed.add_field(name='Owner:', value=ctx.guild.owner, inline=False)
    stats_embed.add_field(name='Server Created Date:', value=ctx.guild.created_at, inline=False)
    stats_embed.add_field(name='Member Count:', value=ctx.guild.member_count, inline=False)
    stats_embed.set_thumbnail(url=ctx.guild.icon)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send(embed=stats_embed)
    
#Dice roll command
@bot.command(name='dice', brief=' Roll a dice')
async def dice(ctx):
    dice_numbers = ["1", "2", "3", "4", "5", "6"]
    author = ctx.author
    roll = random.choice(dice_numbers)
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.send(f"{author} rolled a {roll}")

#User avatar command
@bot.command(name='useravatar', brief=" Get a member's avatar or your own", description='(Mentioning a member is optional)')
async def useravatar(ctx, *, member: discord.Member=None):
    member = ctx.author if not member else member
    avatar_embed = discord.Embed(title=member.name)
    avatar_embed.set_image(url=member.avatar)
    async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.send(embed = avatar_embed)

#User info command (Soon)
@bot.command(name='userinfo', brief=' Get information of a member or your own', description='(Mentioning a member is optional)')
async def userinfo(ctx, *, member: discord.Member=None):
    if not member:
        member = ctx.author
    info_embed = discord.Embed(title='User Information', colour=discord.Colour.random())
    info_embed.set_thumbnail(url=member.avatar)
    info_embed.add_field(name='Name:', value=member.name, inline=False)
    info_embed.add_field(name='Nickname:', value=member.nick, inline=False)
    info_embed.add_field(name='ID:', value=member.id, inline=False)
    info_embed.add_field(name='Account Created Date:', value=member.created_at, inline=False)
    info_embed.add_field(name='Joined Server Date:', value=member.joined_at, inline=False)
    async with ctx.typing():
        await asyncio.sleep(3)
        await ctx.send(embed = info_embed)

#Purge command (Admin)
@bot.command(name='purge', brief=' Delete messages in a channel')
@commands.has_permissions(manage_channels=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    feedback = await ctx.send(f"Deleted {amount} messages sucessfully!")
    await asyncio.sleep(3)
    await feedback.delete()

#Kick command (Admin)
@bot.command(name='kick', brief=' Kick a member')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str):
    await member.kick(reason = reason)
    await ctx.send(f"{member} got kicked! Reason: {reason}")

#Ban command (Admin)
@bot.command(name='ban', brief=' Ban a member')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned! Reason: {reason}")

#Change nickname command
@bot.command(name='nickname', brief=" Change nickname of a member")
@commands.has_permissions(administrator=True)
async def nickname(ctx, member: discord.Member, *, name):
    await member.edit(nick=name)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send(f"Nickname of {member.mention} was changed to {name}")

#Add role command
@bot.command(name='addrole', brief=' Give a role to a member')
@commands.has_permissions(administrator=True)
async def giverole(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send(f"Added the role {role.mention} to {member.mention}!")

#Delete role command
@bot.command(name='delrole', brief=' Remove a role from a member')
@commands.has_permissions(administrator=True)
async def removerole(ctx, member: discord.Member, *, role: discord.Role):
    await member.remove_roles(role)
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send(f"Removed the role {role.mention} from {member.mention}")

#Punch command
@bot.command(name='punch', brief=' Punch someone')
async def punch(ctx, member: discord.Member):
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
    await ctx.send(embed = punch_embed)

#Hug command
@bot.command(name='hug', brief=' Hug someone')
async def hug(ctx, member: discord.Member):
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
    await ctx.send(embed = hug_embed)

#Slap command
@bot.command(name='slap', brief=' Slap someone')
async def slap(ctx, member: discord.Member):
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
    await ctx.send(embed = slap_embed)

#Kiss command
@bot.command(name='kiss', brief=' Kiss someone')
async def kiss(ctx, member: discord.Member):
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
    await ctx.send(embed = kiss_embed)

#Calling the bot token
load_dotenv
bot.run(os.getenv('TOKEN'))