import discord
from discord.ext import commands


class Control(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online) # , activity=discord.Game("Sup.")
        print("Bot is Online.")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong ! {round(self.client.latency * 1000)} ms.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)


def setup(client):
    client.add_cog(Control(client))
