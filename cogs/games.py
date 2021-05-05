import discord
import random
import os
import json
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(aliases=['8Ball', '8ball'])
    async def _8ball(self, ctx, *, question=None):
        if question is None:
            await ctx.send(f"Enter a question first {random.choice(['dumbass', 'smarty', 'Einstein', ''])}.")
        else:
            await ctx.send(file=discord.File(f"8ball_responses\\{random.choice(os.listdir('8ball_responses'))}"))

    #Cards Against Humanity
    @commands.command(aliases=['cardsagainsthumanity', 'cagainsthumanity', 'cardsah', 'evilapples', 'psych'])
    async def cah(self, ctx, *, members):
        mode, rounds = 'normal', 2
        players = [{'id': ctx.message.author, 'cards': []}]
        for player in members.split():
            if str(ctx.message.author.id) not in player:
                players.append({'id': ctx.guild.get_member(int(player[3:-1])), 'cards': []})
        cah, cards = json.load(open('cah.json')), []

        await ctx.guild.create_role(name="Judge", colour=discord.Colour(0xF1C40F))
        judgeRole = discord.utils.get(ctx.message.guild.roles, name='Judge')
        await ctx.guild.create_role(name="Player", colour=discord.Colour(0x206694))
        playerRole = discord.utils.get(ctx.message.guild.roles, name='Player')

        for player in players:
            await player['id'].add_roles(playerRole)
            for cardNo in range(rounds+1):
                player['cards'].append(cah[mode]['cards'].pop(random.randint(0, len(cah[mode]['cards'])-1)))
                await player['id'].send(f"{cardNo} - {player['cards'][cardNo]}")

        for player in players:
            await player['id'].remove_roles(playerRole)
            await player['id'].add_roles(judgeRole)

            await ctx.send(f"{player['id'].mention} is the judge\n \n "+
                           f"Question - {cah[mode]['questions'].pop(random.randint(0, len(cah[mode]['questions'])))}"+
                           f"{playerRole.mention}s Reply to this message with your card numbers [0/0]")

        await judgeRole.delete()
        await playerRole.delete()

def setup(client):
    client.add_cog(Games(client))
