import json
import random
import discord
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    # Cards Against Humanity

    @commands.command(aliases=['cah', 'cAgainstHumanity', 'cardsAH', 'evilApples', 'psych'])
    async def cardsAgainstHumanity(self, ctx, *, members):
        pack, rounds = 0, 3
        players = [{'id': ctx.message.author, 'cards': [], 'score': 0, 'judge': False}]
        for player in members.split():
            if str(ctx.message.author.id) not in player:
                players.append({'id': ctx.guild.get_member(int(player[3:-1])), 'cards': [], 'score': 0, 'judge': False})
        cah, pack, cards, rounds = json.load(open('cah-cards-full.json')), 0, [], len(players) + 1

        for player in players:
            for cardNo in range(rounds + 1):
                player['cards'].append(cah[pack]['white'].pop(random.randint(0, len(cah[pack]['white']) - 1))['text'])
            await player['id'].send(f"\n{random.choice(['Here are your cards', 'sup', 'how you doin?'])}\n\n" +
                                    "\n".join(
                                        [f"{cardNo} - {player['cards'][cardNo]}" for cardNo in range(rounds + 1)]))

        for judge in players:

            judge['judge'], responses = True, []

            question = f"{judge['id'].mention} is the judge\n \n " + f"Question -\n **{cah[pack]['black'].pop(random.randint(0, len(cah[pack]['black']) - 1))['text']}**\n \n" + "".join(
                [f" {player['id'].mention}" for player in players if not player['judge']])

            questionMessage = await ctx.send(embed=discord.Embed(title='Pick a card', description=
                question + f"\nReply with your card numbers [{len(responses)}/{len(players) - 1}]", color=discord.Colour(0x206694)))

            def checkResponse(m):
                return m.author in [player['id'] for player in players if not
                                    player['judge']] and m.content.isdigit() and int(m.content) <= rounds + 1

            def checkSelection(m):
                return m.author in [player['id'] for player in players if
                                    player['judge']] and m.content.isdigit() and int(m.content) <= len(players) - 2

            while len(responses) < len(players) - 1:
                response = await self.client.wait_for('message', check=checkResponse)
                for player in players:
                    if player['id'] == response.author:
                        responses.append({'response': response, 'content': player['cards'][int(response.content)]})

                await questionMessage.edit(embed=discord.Embed(title='Cards Against Humanity', description=
                question + f"\nReply with your card numbers [{len(responses)}/{len(players) - 1}]"), color=discord.Colour(0x206694))

            random.shuffle(responses)

            await ctx.send(embed=discord.Embed(title='Judgement', description=f"{judge['id'].mention} reply to this message to select a response\n \n " +
                           "".join([f"{i} - {responses[i]['content']}\n" for i in range(len(responses))]), color=discord.Colour(0xF1C40F)))

            selection = await self.client.wait_for('message', check=checkSelection)
            for player in players:
                if player['id'] == responses[int(selection.content)]['response'].author:
                    player['score'] += 1

            judge['judge'] = False

        await ctx.send("Here are the final scores \n" + "".join(
            [f"{players[i]['id'].mention} - {players[i]['score']}\n" for i in range(len(players))]))

        maxScore, winners = max([players[i]['score'] for i in range(len(players))]), []
        for player in players:
            if player['score'] == maxScore:
                winners.append(player['id'])
        if len(winners) == 1:
            await ctx.send(f"{winners[0].mention} Wins!")


def setup(client):
    client.add_cog(Games(client))
