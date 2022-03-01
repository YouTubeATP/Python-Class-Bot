## Imports
import nextcord
from nextcord.ext import commands
from decouple import config  # A better way to access .env files
import os
import sys
import io
import traceback
from datetime import datetime

## Bot setup
bot = commands.Bot(command_prefix="m!", intents=nextcord.Intents.all())

owner = config("OWNER")  # User ID of the bot owner

## Boilerplate here

def loadExtensions(exts: list = None):
    if not exts:
        for i in os.listdir("./cogs"):
            if i.endswith(".py"):
                bot.load_extension(f"cogs.{i[:-3]}")
    else:
        for i in exts:
            bot.load_extension(f"cogs.{i}")
    print("Extensions loaded!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}!\nBot is ready.")
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name="Hindi tutorials"
        )
    )
    print("Bot status changed!")
    loadExtensions()  # Then load extensions


@bot.event
async def on_member_join(member):
    embed = nextcord.Embed(
        title=f"{member.name}#{member.discriminator} joined!",
        description="",
        color=0x36393F,
    )
    embed.timestamp = datetime.utcnow()
    embed.set_footer(
        text="Python Class Bot",
        icon_url="https://i.imgur.com/ro0fIYq.png",
    )
    await member.send(embed=embed)


## Mention for prefix
@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send(f"My prefix is `m!`")
    await bot.process_commands(message)


## Message edit detection
@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)


@bot.command()
async def ping(ctx):
    await ctx.send(
        f":ping_pong: Pong! The latency is **{round(bot.latency * 1000)}ms**."
    )


@bot.command(name="exec")
async def exec_command(ctx, *, arg1):
    if str(ctx.author.id) == owner:
        arg1 = arg1[6:-4]
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            exec(arg1)
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
        except:
            x = traceback.format_exc()
            embed = nextcord.Embed(title=f"Execution Failed!", color=0xFF0000)
            embed.set_author(name="ATP Utility")
            embed.add_field(name="Code", value=f"```py\n{str(arg1)}\n```", inline=False)
            embed.add_field(name="Output", value=f"```\n{str(x)}\n```", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(title=f"Execution Success!", color=0x00FF00)
            embed.set_author(name="ATP Utility")
            embed.add_field(name="Code", value=f"```py\n{str(arg1)}\n```", inline=False)
            embed.add_field(
                name="Output", value=f"```\n{str(output)}\n```", inline=False
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")


@bot.command()
async def send_empty_json(ctx):
    if str(ctx.author.id) == str(owner):
        await ctx.send("{}")
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")


## Extension control commands
@bot.command()
async def extload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Loaded extension `{cog}`!")
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")


@bot.command()
async def extunload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Unloaded extension `{cog}`!")
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")


@bot.command()
async def extreload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded extension `{cog}`!")
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")


@bot.command()
async def extlist(ctx):
    if str(ctx.author.id) == str(owner):
        exts = [i[:-3] for i in os.listdir("./cogs") if i.endswith(".py")]
        message1 = "".join(f"""`{j}`\n""" for j in exts)
        await ctx.send(message1)
    else:
        await ctx.send("Sorry, but you don't have permission to do that.")


bot.run(config("TOKEN"))
