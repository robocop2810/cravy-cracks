token = "ODA4Mjc4Mzg3MzEwOTg1MjY2.YCEN6A.umWtaekkPYattFH7leXO5oCGcaY"
###########################################################################################################################################################################################################



from requests import get
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import json
import os
import time
import random


status = "offline"
botversion = "0.0.1"


type = "none"
num = 0

tickettypes = {"disney": 1, "spotify": 2, "netflix": 3, "hulu": 4}
ticketrchannels = {"1": "accounts", "2": "giftcards", "3": "tv"}

global ticketctx

intents = discord.Intents().all()
PREFIX = ("?")
bot = commands.Bot(command_prefix=PREFIX, intents=intents, description='Experimental, working on rn ;)')


@bot.event
async def log(message, priority):
    log_channel = bot.get_channel(808278257430167582)
    logembed = discord.Embed(Color=discord.Color.green())
    logembed.title = "New log:"
    logembed.add_field(name="priority:", value=priority, inline=False)
    logembed.add_field(name="message:", value=message, inline=False)
    logembed.set_footer(icon_url=bot.user.avatar_url)

    await log_channel.send(embed=logembed)

@bot.event
async def update_stock():

    with open("stocks.json", "r") as stockfile:
        stocks = json.load(stockfile)

    with open("pref.json", "r") as preffile:
        prefs = json.load(preffile)

    oldmessageid = prefs["lastmessage"]

    stockchannel = bot.get_channel(807320087714856990)

    if oldmessageid != 0:
        accounts_channel = bot.get_channel(807320087714856990)

        oldmsg = await stockchannel.fetch_message(oldmessageid)
        await oldmsg.delete()


    account_channel = bot.get_channel(807320087714856990)

    disney_emoji = discord.utils.get(bot.emojis, name='disney')
    spotify_emoji = discord.utils.get(bot.emojis, name='spotify')
    netflix_emoji = discord.utils.get(bot.emojis, name='netflix')
    hulu_emoji = discord.utils.get(bot.emojis, name='hulu')

    valid_reactions = [disney_emoji, spotify_emoji, netflix_emoji, hulu_emoji]

    e = discord.Embed(color=discord.Color.gold())
    e.title = "STOCK: "
    e.description = f"{disney_emoji} Disney+ : {str(stocks['disney'])} \n  \n {spotify_emoji} Spotify : {str(stocks['spotify'])} \n \n {netflix_emoji} Netflix : {str(stocks['netflix'])} \n \n {hulu_emoji} Hulu : {str(stocks['hulu'])}"
    e.set_footer(icon_url=bot.user.avatar_url)

    vote_msg = await account_channel.send(embed=e)

    for emoji in valid_reactions:
        await vote_msg.add_reaction(emoji)

    prefs["lastmessage"] = vote_msg.id

    with open("pref.json", "w") as preffile:
        json.dump(prefs, preffile)





@bot.event
async def senddm(user, message):
    dmchannel = await user.create_dm()
    dm = discord.Embed(Color=discord.Color.red())
    dm.title = "Ticket error!"
    dm.description = message
    dm.set_footer(icon_url=bot.user.avatar_url)

    await dmchannel.send(embed=dm)

@bot.event
async def close_ticket(user):
    with open("pref.json", "r") as preffile:
        prefs = json.load(preffile)

    closing_channel_id = prefs[str(user)]

    closing_channel = bot.get_channel(closing_channel_id)
    secs = 5

    closemsg = await closing_channel.send(f"Ticket will be closed in {secs}...")

    while secs != 0:
        await closemsg.edit(content=f"Ticket will be closed in {secs}...")
        await asyncio.sleep(1)
        secs = secs -1
    await closing_channel.delete()

    prefs[str(user)] = 0

    with open("pref.json", "w") as preffile:
        json.dump(prefs, preffile)


@bot.event
async def newticket(ticket_type, num, user):
    with open("pref.json", "r") as preffile:
        prefs = json.load(preffile)

    print(str(prefs))
    logchannel = await bot.fetch_channel(809763735706402827)

    if str(user) not in str(prefs):
        guild = await bot.fetch_guild(guild_id=807247821467942922)

        category = discord.utils.get(guild.categories, id=808329082185711676)

        newchannelname = ticketrchannels[str(num)]

        admin_role = guild.get_role(807679603220283452)

        everyone_role = guild.get_role(808291040599605258)

        ticketNumber = random.randint(100, 999)


        channelname = str(f'🎟️-{newchannelname}-{ticket_type}-{ticketNumber}')

        overwrites = {
            everyone_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }

        ticketchannel = await guild.create_text_channel(name=str(channelname), overwrites=overwrites, category=category)


        welcome_message = "Welcome, <@" + str(user.id) + ">"

        await ticketchannel.send(welcome_message)

        ticketembed = discord.Embed(Color=discord.Color.green())
        ticketembed.title = "New ticket"
        ticketembed.description = f"You opened a ticket for {ticket_type}, staff will be here shortly to help you with your purchase! If you change your mind, close the ticket with \N{LOCK}"
        ticketembed.set_footer(icon_url=bot.user.avatar_url)

        ticketmessage = await ticketchannel.send(embed=ticketembed)

        await ticketmessage.add_reaction('\N{LOCK}')

        await logchannel.send(f'<@&807679603220283452>, new ticket!: <#{ticketchannel.id}>')

        prefs[str(user)] = ticketchannel.id

        with open("pref.json", "w") as preffile:
            json.dump(prefs, preffile)

    elif prefs[str(user)] == 0:
        guild = await bot.fetch_guild(guild_id=807247821467942922)

        category = discord.utils.get(guild.categories, id=808329082185711676)

        newchannelname = ticketrchannels[str(num)]

        admin_role = guild.get_role(807679603220283452)

        everyone_role = guild.get_role(808291040599605258)

        ticketNumber = random.randint(100, 999)

        channelname = str(f'🎫-{newchannelname}-{ticket_type}-{ticketNumber}')

        overwrites = {
            everyone_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }

        ticketchannel = await guild.create_text_channel(name=str(channelname), overwrites=overwrites, category=category)

        welcome_message = "Welcome, <@" + str(user.id) + ">"

        await ticketchannel.send(welcome_message)

        ticketembed = discord.Embed(Color=discord.Color.green())
        ticketembed.title = "New ticket"
        ticketembed.description = f"You opened a ticket for {ticket_type}, staff will be here shortly to help you with your purchase! If you change your mind, close the ticket with \N{LOCK}"
        ticketembed.set_footer(icon_url=bot.user.avatar_url)

        ticketmessage = await ticketchannel.send(embed=ticketembed)

        await ticketmessage.add_reaction('\N{LOCK}')

        await logchannel.send(f'<@&807679603220283452>, NEW TICKET: <#{ticketchannel.id}> (opened by <@{user.id}>)')

        with open("pref.json", "r") as preffile:
            prefs = json.load(preffile)

        prefs[str(user)] = ticketchannel.id

        with open("pref.json", "w") as preffile:
            json.dump(prefs, preffile)
    else:
        message = f'hi <@{user.id}>, you tried to create a ticket while you already have an open one. To open another one you must close your open ticket.'
        await senddm(user, message)


@bot.event
async def on_reaction_add(reaction, user):

    with open("pref.json", "r") as preffile:
        prefs = json.load(preffile)

    disney_emoji = discord.utils.get(bot.emojis, name='disney')
    spotify_emoji = discord.utils.get(bot.emojis, name='spotify')
    netflix_emoji = discord.utils.get(bot.emojis, name='netflix')
    hulu_emoji = discord.utils.get(bot.emojis, name='hulu')


    if user.id != bot.user.id:
        choice = reaction.emoji
        print(choice)

        if str(choice) == "🔒":
            await log(f'[INFO] user {user} closed his ticket.', "LOW")
            await close_ticket(user)

        valid_reactions = [disney_emoji, spotify_emoji, netflix_emoji, hulu_emoji]

        if choice in valid_reactions:

            if str(reaction.emoji) == str(disney_emoji):

                print(user, "disney")
                type = "disney"
                num = 1
                message = f'[INFO] user {user} has chosen type {type}'

                if prefs['disney'] > 0:
                    prefs['disney'] = prefs['disney'] - 1
                    await log(message, "LOW")
                    await newticket(type, num, user)
                else:
                    await senddm(user, "Sorry, we are currently out of stock :/")

            elif str(reaction.emoji) == str(spotify_emoji):

                print(user, "spotify")
                type = "spotify"
                num = 1
                message = f'[INFO] user {user} has chosen type {type}'

                if prefs['spotify'] > 0:
                    prefs['spotify'] = prefs['spotify'] - 1
                    await log(message, "LOW")
                    await newticket(type, num, user)
                else:
                    await senddm(user, "Sorry, we are currently out of stock :/")

            elif str(reaction.emoji) == str(netflix_emoji):

                print(user, "netflix")
                type = "netflix"
                num = 1
                message = f'[INFO] user {user} has chosen type {type}'

                if prefs['netflix'] > 0:
                    prefs['netflix'] = prefs['netflix'] - 1
                    await log(message, "LOW")
                    await newticket(type, num, user)
                else:
                    await senddm(user, "Sorry, we are currently out of stock :/")

            elif str(reaction.emoji) == str(hulu_emoji):

                print(user, "hulu")
                type = "hulu"
                num = 1
                message = f'[INFO] user {user} has chosen type {type}'

                if prefs['hulu'] > 0:
                    prefs['hulu'] = prefs['hulu'] - 1
                    await log(message, "LOW")
                    await newticket(type, num, user)
                else:
                    await senddm(user, "Sorry, we are currently out of stock :/")

            else:
                message = f'[ERROR] unexpected emoji; {choice}'
                await log(message, "LOW")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="Experimental, working on rn ;)"))
    print("Bot is ready!")



@bot.command(pass_context=True)
async def startup(ctx):
    await update_stock()
@bot.command()
async def ip(ctx):
    print("#")

@bot.command()
async def ping(ctx):
    await ctx.send(f"pong {round(bot.latency * 1000)}ms")


@bot.command()
async def version(ctx):
    await ctx.send("im on version:  `" + str(botversion) + "` !")

@bot.command()
async def serverlock(ctx):
    serverlock_role = ctx.guild.get_role(809554444143951872)

    bots_role = ctx.guild.get_role(807247821467942925)
    staff_role = ctx.guild.get_role(807679603220283452)

    guild = await bot.fetch_guild(guild_id=807247821467942922)
    for member in guild.members:
        if bots_role or staff_role not in member.roles:
            await member.add_roles(serverlock_role)
    print("server locked...")

@bot.command()
async def serverunlock(ctx):
    serverlock_role = ctx.guild.get_role(809554444143951872)

    guild = await bot.fetch_guild(guild_id=807247821467942922)
    for member in guild.members:
        if serverlock_role in member.roles:
            await member.remove_roles(serverlock_role)
    print("server unlocked...")

@bot.command()
async def stockupdate(ctx, stock, new_stock):
    with open("stocks.json", "r") as stockfile:
        stocks = json.load(stockfile)
    if str(stock) in str(stocks):
        await log(f"[INFO]: (stock update) {stock} has been updated from {stocks[stock]} to {new_stock}", "LOW")
        stocks[stock] = int(new_stock)
        with open("stocks.json", "w") as stockfile:
            json.dump(stocks, stockfile)
        await update_stock()
    else:
        await ctx.send("```Sorry, this stock wasn't found :/```")


bot.run(token)