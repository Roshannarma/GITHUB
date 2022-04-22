from PIL import Image
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
import os
import io

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix='!')

# client = discord.Client()

@bot.command(name="test",pass_context = True)
async def imageTest(ctx):
    im = Image.open(r"C:\Users\rosha\github\GITHUB\DiscordBot\temp.png")
    arr = io.BytesIO()
    im.save(arr,format="PNG")
    arr.seek(0)
    # await bot.send_file(ctx.message.channel,arr)
    # await bot.send_file(ctx.message.channel ,r"C:\Users\rosha\github\GITHUB\DiscordBot\temp.png")
    file = discord.File(arr,'cool_image.png')
    # print(file)
    # await ctx.send(file=arr)
    await ctx.send(file=file)
    # await ctx.message.channel.send()

bot.run(TOKEN)
# im = Image.open("download.png")



# print(im)
