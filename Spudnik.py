import discord
import random
from discord.ext import commands,tasks
import asyncio
import os
from discord import Activity, Spotify
import json

intents = discord.Intents().all()
client = commands.Bot(command_prefix = 'spud.',intents=intents)

def save(data):
    f = open('Users.json','w')
    json.dump(data,f, indent=5)
    # f = open('Roles.json','w')
    # json.dump(roles,f, indent=5)
curses = []
warned = []
coins = {}
data = {}
roles = {}
dat = {
    "Member":{},
    "Left":{},
    "Dead":{}
    }
print('Loaded Users...')
# create
with open('Users.json') as f:
        try:
            data = json.load(f)
        except Exception:
            data = {}
with open('Roles.json') as f:
    try:
        roles = json.load(f)
    except Exception:
        roles = {}
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No command found")

@client.command(aliases=['curses_add','addCurses','curse_add','addCurse','add_curse'], brief="Adds a curse to catch in messages")
async def add_curses(ctx, curse):
    await ctx.send(f"Thank you {ctx.author}, for incresing my dictionary")
    curses.append(curse)


@client.command(brief="Shows your Badge")
async def badge(ctx, member : discord.Member=None):
    server = ctx.guild.name
    print("Hello from the underworld")
    member = ctx.author if not member else member
    print(member)
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"Badge of {member}")
    embed.set_footer(text=f"asked by {member.nick if member.nick else member.name}", icon_url=ctx.author.avatar_url)
    embed.add_field(name="Name", value=member.display_name)
    embed.add_field(name="Account Created on",value=member.created_at.strftime("%d.%m.%Y,\n%H:%M.%S"))    
    embed.add_field(name="Joined:", value=member.joined_at.strftime("%d.%m.%Y,\n%H:%M.%S"))    
    embed.add_field(name=f"Roles ({len(roles)})",value="\n".join([role.mention for role in roles]))
    embed.add_field(name="Top Role", value=member.top_role.mention)
    embed.add_field(name="Is Bot", value='Yes' if member.bot else 'No')
    embed.add_field(name="Status", value=member.mobile_status)
    embed.add_field(name="Kicks", value=data[ctx.guild.name]['Member'][member.id]['Kicks'], inline=False)
    embed.add_field(name="Mutes", value=data[ctx.guild.name]['Member'][member.id]['Mutes'])

    #TODO check for every activity
    embed.add_field(name="Nitro", value=member.premium_since)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def alert(ctx,role :discord.Role, *,reason):
    rolestr = str(role)
    for i in roles[ctx.guild.name][rolestr]:
        if bool(random.getrandbits(1)):
            i = int(i)
            user = client.get_user(i)
            print(i)
            await user.send(reason)
            break
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command(brief='Mutes a Member')
@commands.has_role('Soundwave\'s Minicons')
async def mute(ctx, member : discord.Member, hours=0, minutes=10, seconds=0, *,reason=None):
    print(member,hours,minutes,seconds,reason)
    guild = ctx.guild
    print("mute")
    data[guild.name]['Member'][str(member.id)]['Mutes'] += 1
    save(data) 
    muted = discord.utils.get(guild.roles,name='Muted')
    if not (hours == 0 and minutes == 0):
        if not hours == 0:
            hours = hours * 3600
        if not minutes == 0:
            minutes = minutes * 60
    seconds = hours + minutes + seconds
    if not muted:
        muted = await guild.create_role(name='Muted')
        for channel in guild.channels:
            await channel.set_permissions(muted, speak=False,send_messages=False,read_message_history=True,read_messages=True,create_instant_invite=False)
    if not reason:
        reason = 'No Reason Provided'
    await member.add_roles(muted, reason=reason)
    await ctx.send(f'{member} has been muted for {reason}')
    await member.send(f'You were muted in the client {guild.name} for {reason}')
    muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted for {reason} for {hours/3600} hours, {minutes/60} minutes and {seconds} seconds")
    await ctx.send(embed=muted_embed)
    if not seconds == 0:
        await asyncio.sleep(seconds)
        await member.remove_roles(muted)
        await member.send('You have been unmuted')
    else:
        await member.send(f'Until you\'re unmuted by a Soundwave\'s Minicons')

@client.command(brief='Unmutes a User')
@commands.has_role('Megatron')
async def unmute(ctx, member : discord.Member):
    guild = ctx.guild
    unmute = discord.utils.get(guild.roles,name='Muted')
    await member.remove_roles(unmute)
    await member.send(f'You have been unmuted')

@client.command()
async def rps(ctx,member:discord.Member):
    author = ctx.author
    print('success')
    message = None
    def algo(a,b,x):
        return (a*b)/x
    def compare(x,y):
        x = int(x)
        y = int(y)
        if x >= y:
            return "winning"
    print('yo')
    print(data['Member'])
    await ctx.send(f"{member.mention} has {data['Member'][member.id]['RPS']} of winning recored")

    await author.send(f"You, {author.mention}, have a  {algo(int(data['Member'][author.id]['RPS']))} of {compare(data['Member'][author.id]['RPS'],data['Member'][member.id]['RPS'])} recored")
    # print()
    message = f'with prompt\n{message}'if message else ''
    await member.send(f'{author.mention} is prompting to play Rock_Paper_Scissors with him {message}.\n Answer in yes or no')
    await ctx.send(f'Message sent to {member.mention}')
    print(member.mention)
    def check(msg):
        return msg.author.mention == member.mention
    def check2(msg):
        return msg.author.mention == author.mention
    playerReady = await client.wait_for('message',check=check)
    if 'yes' in playerReady.content:
        await author.send(f'{member.mention} is ready!\nPlay here in DM')
        await member.send(f'Play here in DM\'s')

        a = 0
        b = 0 
        def rpsGame(entity,entity2):
            print("Coming from checker,",entity,entity2)
            if entity == entity2:
                return 0
            if entity == 'rock':
                return 2 if entity2 == "paper" else 1
            if entity == 'paper':
                return 2 if entity2 == "scissor" else 1
            if entity == 'scissor':
                return 2 if entity2 == "rock" else 1
        for i in range(3):
            await member.send(f'Waiting for {author.mention}...')
            await author.send('Your Turn')
            choice = await client.wait_for('message',check=check2)
            await author.send(f'Waiting for {member.mention}...') 
            await member.send('Your Turn')
            choice2 = await client.wait_for('message',check=check)
            print(choice.content,choice2.content)
            winner = rpsGame(choice.content, choice2.content)
            print(winner)
            if winner == 2:
                b = b + 1
            else:
                a += 1
        def winner(a,b):
            print("coming from winner",a,b)
            if a > b:
                print('author')
                return f'{author.mention} won the Game by {a-b}'
            elif a < b:
                print('member')
                return f'{member.mention} won the Game by{b-a}'
            else:
                return f'Draw between {author.mention} and {member.mention}'
        print('going')
        await ctx.send(winner(a,b))


@client.command(brief="Unbans a member")
@commands.has_role('Soundwave\'s Minicons')
async def unban(ctx, *, member):
    banned = await ctx.guild.bans()
    user_name, discriminator = member.split('#')
    for ban_entry in banned:
        user = ban_entry.user
        if (user.name, user.discriminator) == (user_name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned @{user}')
            await member.send(f'You have been unbanned in {ctx.guild.name}')
            link = await ctx.channel.create_invite(max_age = 300)
            await member.send("Here is an instant invite to the client: " + link)

@client.event
async def on_member_join(member:discord.Member):
    await member.send(f'Hi **{member.name}**, Welcome to the Server! Be sure to read the rules to stay out of trouble. Have a great time!')
    print("Joined")
    server = member.guild.name
    data[server] = dat
    #print(type(data) + 'asdasdasdasdad')
    if not str(member.id) in data[server]['Left'].keys():
        memberData = {
                'User' : member.name,
                'Nickname':member.nick,
                'Avatar_Url' : str(member.avatar_url),
                'Id' : str(member.id),
                'Good_Deeds': 0,
                'Bad_Deeds' : 0,
                'Mutes': 0,
                'Kicks':0,
                "Wins":0,
                "Loses":0,
                'RPS':'0',
                'Ban': False,
                'Reasons':[]
            }
    else:
        memberData = data['Left'][str(member.id)]
        del data['Left'][str(member.id)]
    data[server]['Member'][str(member.id)] = memberData

    embed = discord.Embed(colour=member.color)
    embed.set_author(name=f"Welcome To the Decepticons")
    embed.add_field(name="Name", value=member.display_name)
    embed.add_field(name="Account Created on",value=member.created_at.strftime("%d.%m.%Y,\n%H:%M.%S"))    
    embed.add_field(name="Joined:", value=member.joined_at.strftime("%d.%m.%Y,\n%H:%M.%S"))    
    embed.add_field(name="Is Bot", value='Yes' if member.bot else 'No')
    embed.add_field(name="Status", value=member.mobile_status)
    embed.add_field(name="Nitro", value=member.premium_since)
    embed.set_image(url=member.avatar_url)
    if member.guild.name == "Decepticons":
        chn = client.get_channel(904579620026859581)
        await chn.send(embed=embed)
    with open('Users.json','w') as f:
            json.dump(data,f, indent=5)
            print('dumped')
    print(member.guild.name)
    followers = discord.utils.get(member.guild.roles,name='Megatron Followers')
    await member.add_roles(followers)
# Create a server name folder and store the nessacary files there
#asdasd

@client.event
async def on_member_remove(member:discord.Member):
    print('Coming from Leaving')
    print(data[member.guild.name]['Member'][str(member.id)])
    print(data[member.guild.name]['Member'][str(member.id)]["Ban"])
    print(data[member.guild.name]['Member'][str(member.id)]['Ban'])
    def determine():
        if data[member.guild.name]['Member'][str(member.id)]['Ban']:
            return 'Dead'
        return 'Left'
    to = determine()
    data[member.guild.name][to][str(member.id)] = data[member.guild.name]['Member'][str(member.id)]
    del data[member.guild.name]['Member'][str(member.id)]

    with open('Users.json','w') as f:
        json.dump(data,f,indent=5)
    
@client.command(aliases=['8ball'],brief='Ask it a Question')
async def _8ball(ctx, *, question):
    responses = ['It is Certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don\'t count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.',]
    await ctx.send(f'Question: {question}\n{random.choice(responses)}')

@client.command(aliases=['clean','cls'])
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def bank(ctx):
    member = ctx.author
    coins_int = 0
    try:
        coins_int = coins[member]
    except Exception as e:
        pass
    await ctx.send(f'You have {coins_int} :coin:')

@client.command()
@commands.has_role("Soundwave's Minicons")
async def kick(ctx, member :discord.Member, *,reason=None):
    print('Allowed')
    await member.kick(reason=reason)
    print('Kicked')
    await member.send(f'You have been kicked from {ctx.guild.name} for {reason}')
    data[ctx.guild.name]['Member'][member.id]['Kicks'] += 1
    #embed = discord.Embed() on_member_join

@kick.error #alert
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send('The Correct way is \nspud.kick <member> (reason)\nwhere the <> is a must and () is optional')

@client.command(brief="Bans a member")
@commands.has_role('Soundwave\'s Minicons')
async def ban(ctx, member :discord.Member, *,reason=None):
    print(reason)
    data[ctx.guild.name]['Member'][str(member.id)]['Bans'] = True
    await member.ban(reason=reason)

@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
     await ctx.send("I don't have arguments")

@client.command()
async def changeNickname(ctx, *, name):
    member = ctx.author
    await member.edit(nick=name)

@client.command()
async def song(ctx, *, member :discord.Member=None):
    member = member if member else ctx.author
    print("activity recognized")
    for activity in member.activities:
        print(activity)
        if isinstance(activity, Spotify):
            print(True)
            embed = discord.Embed(
                title = activity.title,
                description = "Song Activity of "+member.user+' asked by '+ ctx.author.user,
                colour = activity.colour
            )
            print(title = activity.title,
                description = "Song Activity of "+member.user+' asked by '+ ctx.author.user,
                colour = activity.colour)
            await ctx.send(embed=embed)
            break

@client.command()
async def status(ctx):
    await ctx.send(ctx.author.activities)
    activities = (ctx.author.activities)
    for activity in activities:
        print(activity)
        print(activity.ActivityType)
        ctx.send(activity)
    print(ctx)

@client.command()
async def grabSong(ctx,member:discord.Member):
    embed = discord.Embed

@client.command()
@commands.has_role('Megatron')
async def clean_slate(self,ctx,member:discord.Member):
    data[ctx.guild.name]['Member'][member.id] = {
        'User' : member.name,
        'Nickname':member.nick,
        'Avatar_Url' : str(member.avatar_url),
        'Id' : str(member.id),
        'Good_Deeds': 0, # data['Left'][str(member.id)]['Good_Deeds'] Meagtron
        'Bad_Deeds' : 0,
        'Mutes': 0,
        'Kicks':0,
        "Wins":0,
        "Loses":0,
        'RPS':'0',
        'Bans': False,
        'Reasons':[]
    }
    with open('Users.json','w') as f:
            json.dump(data,f, indent=5)

@client.event
async def on_reaction_add(reaction, user):
    ctx = await client.get_context(reaction.message)
    if "verification" in  reaction.message.content :
        print(reaction.message.content, user.name)

@client.event
async def on_message(message):
    print(message.author,"messaged",message.content)
    ctx = await client.get_context(message)
    if(message.author == client.user):
        return
    if not len(curses) == 0 and not "spud." in message.content and (curse in message for curse in curses):
        if message.author in warned:
            await mute(ctx, message.author ,hours=1 ,minutes=1 ,seconds=1 ,reason="For Cursing")
            #ctx, member : discord.Member, hours=0, minutes=0, seconds=0, *,reason=None):
        else:
            await message.author.send(f"{message.author.mention} This is your First and Last warning! Anymore curses and you will be kicked")
            warned.append(message.author)
        print(curses)
    elif message.content ==  "save all" and message.author == ctx.guild.owner:
        x = message.guild.members
        server = ctx.message.guild.name
        data[server] = dat
        roles[server] = {}
        for role in ctx.message.guild.roles:
            memebers = {}
            for member in role.members:
                memberData = {
                    'User' : member.name,
                    'Nickname':member.nick,
                    'Id' : str(member.id),
                }
                memebers[str(member.id)] = memberData
            roles[server][str(role)] = memebers
        print(memberData)
        memberData = {}
        with open('Roles.json','w') as f:
            json.dump(roles,f, indent=5)
        print(data)
        for member in x:
                memberData = {
                    'User' : member.name,
                    'Nickname':member.nick,
                    'Avatar_Url' : str(member.avatar_url),
                    'Id' : str(member.id),
                    'Good_Deeds': 0, # data['Left'][str(member.id)]['Good_Deeds'] Meagtron
                    'Bad_Deeds' : 0,
                    'Mutes': 0,
                    'Kicks':0,
                    "Wins":0,
                    "Loses":0,
                    'RPS':'0',
                    'Ban': False,
                    'Reasons':[]
                }
                data[server]['Member'][str(member.id)] = memberData
        with open('Users.json','w') as f:
            json.dump(data,f, indent=5)
    elif "pathetic" in message.content.lower():
        await ctx.send(message.content)
    await client.process_commands(message)

for fileName in os.listdir('./cogs'):
    if fileName.endswith('.py'):
        client.load_extension(f'cogs.{fileName[:-3]}') 
client.run('ODcwNjY5Mjc2ODcxMjYyMjE4.YQQH8w.ehGmhZzR6_Mx0EPqQUc9lC6rjuE')