import discord
import os
import json
import random
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(aliases=['8ball', 'magic8ball', 'magicBall', '8'])
    async def _8ball(self, ctx, *, question=None):
        if question is None:
            await ctx.send(f"Enter a question first {random.choice(['dumbass', 'smarty', 'Einstein', ''])}.")
        else:
            await ctx.send(file=discord.File(f"8ball_responses\\{random.choice(os.listdir('8ball_responses'))}"))


def setup(client):
    client.add_cog(Fun(client))
