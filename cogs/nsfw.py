import discord
from discord.ext import commands
import random


class Nsfw(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(aliases=['boob', 'boobies', 'breasts', 'tits'])
    @commands.is_nsfw()
    async def b(self, ctx):
        await ctx.send("( . Y . )")

    @commands.command(aliases=['penis', 'dick'])
    @commands.is_nsfw()
    async def pp(self, ctx):
        await ctx.send(f"{ctx.message.author.mention}'s pp :\n 8{'='*random.randint(1, 10)}D")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            ctx.message.title = "NSFW Command"
            ctx.message.description = error.args[0]
            return await ctx.send(embed=message)


def setup(client):
    client.add_cog(Nsfw(client))
