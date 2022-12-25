import discord
from discord.ext import commands
from discord import Intents
from discord.ext.commands import Bot
import os 
import random 
from PIL import Image, ImageDraw, ImageSequence
import imagecreator
from secrets import BOT_TOKEN
from settings import Settings

gifs = os.listdir("gokugifs")

bot = commands.Bot(command_prefix='.',intents=Intents.default())
GuildSettings = {}


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

    filename = imagecreator.writeText(Image.open("gokugifs/" + random.choice(gifs)), rule_number, rule_text,str(ctx.message.id))
    settings = getGuildSettings(ctx.guild.id)

    if settings.getRuleChannel() != None:
        await bot.get_channel(settings.getRuleChannel()).send(file=discord.File(filename))
        await ctx.send("Done!")   
    else:
        await ctx.send(file=discord.File(filename))
    
    os.remove(filename)

@commands.has_permissions(administrator=True)
@bot.hybrid_command("setrulechannel")
async def setrulechannel(ctx, channel: discord.TextChannel):
    settings = getGuildSettings(ctx.guild.id)
    settings.setRuleChannel(channel.id)
    await ctx.send(f"Rule channel set to {channel.mention}")

def getGuildSettings(guildID):
    if not guildID in GuildSettings:
        GuildSettings[guildID] = Settings(guildID)
    return GuildSettings[guildID]


bot.run(BOT_TOKEN)