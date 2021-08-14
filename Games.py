import discord
from discord.ext import commands
import random,asyncio
class Games(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Games loaded')

    @commands.command()
    async def command(self,ctx):
        computer = random.randint(1, 10)
        await ctx.send('Guess my number')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        msg = await client.wait_for("message", check=check)

        if int(msg.content) == computer:
            await ctx.send("Correct")
        else:
            await ctx.send(f"Nope it was {computer}")
    @commands.command(name='rps',description='Challenge a player in a best of three game of rock paper scissors')
    async def rps(self,ctx, member:discord.Member):
        host = ctx.author

        await member.send(f'{host} wants to play a Rock Paper Scissor with you,\nDo you accept?(answer in y or n)')
        def check(msg):
            print('yes')
            return msg.author.mention == member.mention

        playerResponse = await client.wait_for('message',check=check,timeout=120)

        print(playerResponse.content + " asd")
        
def setup(client):
    client.add_cog(Games(client))