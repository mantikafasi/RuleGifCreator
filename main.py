import discord
from discord.ext import commands
from discord import Intents
from discord.ext.commands import Bot
import os 
import random 
from PIL import Image, ImageDraw, ImageSequence
import imagecreator
from secrets import BOT_TOKEN

gifs = os.listdir("gokugifs")

bot = commands.Bot(command_prefix='.',intents=Intents.default())

@bot.event
async def on_ready():
    print("Logged In As")

    print(bot.user.name)

    print("------")

    #await bot.tree.sync()

    print(bot.user.id)

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Nothing")
    )

@bot.hybrid_command("rule")
async def rule(ctx , rule_number: int, *, rule_text: str):
    # get message id
    
    filename = imagecreator.writeText(Image.open("gokugifs/" + random.choice(gifs)), rule_number, rule_text,str(ctx.message.id))
    await ctx.send(file=discord.File(filename))
    os.remove(filename)

bot.run(BOT_TOKEN)