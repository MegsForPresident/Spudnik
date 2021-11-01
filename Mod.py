import discord
from discord.ext import commands
class ModCog(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod Cog has been loaded")
    @commands.command()
    @commands.has_role('Mod')
    async def cong(self,ctx):
        await ctx.send("Bong!")
def setup(client):
    client.add_cog(ModCog(client))