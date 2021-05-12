import os
from itertools import cycle
import discord
from discord.ext import commands, tasks

intents = discord.Intents().all()

client = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)
statuses = cycle(['1', '2', '3'])

# Events


# Commands

@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f'{extension} Cog loaded.')



@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f'{extension} Cog unloaded.')


# Tasks
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Game(next(statuses)))



# @client.command(aliases=['cardsagainthumanity', 'evilapples', 'cardsah'])
# async def cah(ctx, *players, rounds):
#     print('Playing Cards against Humanity')


# @client.event
# async def on_member_join(member):
#     print(f"{member} has joined a server")


# @client.event
# async def on_member_remove(member):
#     print(f"{member} has left a server")

for file in os.listdir('cogs'):
    if file.endswith('.py') and 'nsfw' not in file:
        client.load_extension(f"cogs.{file[:-3]}")

client.run(open('token.txt').read())
