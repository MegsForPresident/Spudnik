import discord
from discord.ext import commands
owner = 'Megatron'
class Owner(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Cog has been loaded")
    @commands.command()
    @commands.has_role(owner)
    async def bng(self,ctx):
        await ctx.send("Bong!")

    @commands.command()
    @commands.has_role(owner)
    async def addRole(self,ctx, member : discord.Member, *,role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f'{member.mention} now has {role}')

    @commands.command(brief="Changes Status of the bot")
    @commands.has_role(owner) #mute
    async def change_status(self,ctx, status):
        if(status == "idle"):
            await commands.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
        elif status == "online":
            await commands.change_presence(status=discord.Status.online, activity=discord.Game('Hello there!'))
        elif status == "don't disturb":
            await commands.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Hello there!'))
        elif status == "offline":
            await commands.change_presence(status=discord.Status.offline, activity=discord.Game('Hello there!'))
    

def setup(client):
    client.add_cog(Owner(client))