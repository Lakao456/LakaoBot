import json
import os
import random

import discord
from discord.ext import commands


class Games(commands.Cog):
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

    @commands.command(aliases=['escape', 'stop', 'end'])
    async def exit(self, ctx):
        await discord.utils.get(ctx.message.guild.roles, name='Player').delete()
        await discord.utils.get(ctx.message.guild.roles, name='Judge').delete()

    # Cards Against Humanity
    @commands.command(aliases=['cardsagainsthumanity', 'cagainsthumanity', 'cardsah', 'evilapples', 'psych'])
    async def cah(self, ctx, *, members):
        pack, rounds = 0, 3
        players = [{'id': ctx.message.author, 'cards': [], 'score': 0}]
        for player in members.split():
            if str(ctx.message.author.id) not in player:
                players.append({'id': ctx.guild.get_member(int(player[3:-1])), 'cards': [], 'score': 0})
        cah, pack, cards, rounds = json.load(open('cah-cards-full.json')), 0, [], len(players) + 1

        await ctx.guild.create_role(name="Judge", colour=discord.Colour(0xF1C40F))
        judgeRole = discord.utils.get(ctx.message.guild.roles, name='Judge')
        await ctx.guild.create_role(name="Player", colour=discord.Colour(0x206694))
        playerRole = discord.utils.get(ctx.message.guild.roles, name='Player')

        for player in players:
            await player['id'].add_roles(playerRole)
            for cardNo in range(rounds + 1):
                player['cards'].append(cah[pack]['white'].pop(random.randint(0, len(cah[pack]['white']) - 1))['text'])
            await player['id'].send(random.choice(['Here are your cards', 'sup', 'how you doin?']) + '\n \n' +
                                    "\n".join(
                                        [f"{cardNo} - {player['cards'][cardNo]}" for cardNo in range(rounds + 1)]))

        for judge in players:
            await judge['id'].remove_roles(playerRole)
            await judge['id'].add_roles(judgeRole)
            responses, question = [], f"Question - {cah[pack]['black'].pop(random.randint(0, len(cah[pack]['black']) - 1))['text']}\n \n"
            questionMessage = await ctx.send(f"{judge['id'].mention} is the judge\n \n " +
                                             question +
                                             f"{playerRole.mention}s Reply to this message with your card numbers [{len(responses)}/{len(players) - 1}]")

            def checkResponse(m):
                return playerRole in m.author.roles and m.content.isdigit() and int(m.content) <= rounds + 1

            def checkSelection(m):
                return judgeRole in m.author.roles and m.content.isdigit() and int(m.content) <= len(players) - 2

            while len(responses) < len(players) - 1:
                response = await self.client.wait_for('message', check=checkResponse)
                for player in players:
                    if player['id'] == response.author:
                        responses.append({'response': response, 'content': player['cards'][int(response.content)]})

                await questionMessage.edit(content=
                                           f"{judge['id'].mention} is the judge\n \n" +
                                           question +
                                           f"\n \n {playerRole.mention}s Reply to this message with your card numbers [{len(responses)}/{len(players) - 1}]")

            random.shuffle(responses)

            await ctx.send(f"{judge['id'].mention} reply to this message to select a response\n \n " +
                           "".join([f"{i} - {responses[i]['content']}\n" for i in range(len(responses))]))

            selection = await self.client.wait_for('message', check=checkSelection)
            for player in players:
                if player['id'] == responses[int(selection.content)]['response'].author:
                    player['score'] += 1

            await judge['id'].add_roles(playerRole)
            await judge['id'].remove_roles(judgeRole)

        await ctx.send("Here are the final scores \n" + "".join(
            [f"{players[i]['id'].mention} - {players[i]['score']}\n" for i in range(len(players))]))

        maxScore, winners = max([players[i]['score'] for i in range(len(players))]), []
        for player in players:
            if player['score'] == maxScore:
                winners.append(player['id'])
        if len(winners) == 1:
            await ctx.send(f"{winners[0].mention} Wins!")

        await judgeRole.delete()
        await playerRole.delete()


def setup(client):
    client.add_cog(Games(client))
