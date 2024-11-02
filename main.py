import os, discord
from discord.ext import tasks, commands
import discord.state
from get_jokes import Joking

myjokes = Joking()

"""
Create Environment for The Discord bot
"""
discord_environment = {
    "TOKEN": os.getenv("THRONEBOT_TOKEN"),
    "BOT_NAME": "",
    "BOT_GUILDS": "",
    "Default_Channel": "",
    "BOT_DEFAULT_GUILD": ""
}

INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True


bot = commands.Bot(
    command_prefix='/',
    intents=INTENTS
)
"""
Startup Functions
"""
@bot.event
async def on_ready():
    """
        Output to have full controll where the Bot is.\n
        Save stuff into the Environment dictionary.
            -> bot username
            -> bot guilds <list>
    """
    discord_environment["BOT_NAME"] = bot.user.name
    guild_list = list()
    async for guild in bot.fetch_guilds():
        guild_list.append(guild.name)
    discord_environment["BOT_GUILDS"] = guild_list 
    print(f"Logged in as { discord_environment["BOT_NAME"]} ({bot.user.id})")
    for name in discord_environment["BOT_GUILDS"]:
        print(f"guild: {name} - joined")
    print("BOT READY")
    print("[BOT]: Starting loop tasks")
    user_lookup.start()
    

@tasks.loop(seconds=15)
async def user_lookup():
    print("[BOT]: TASK - user_lookup")
    default_channel = bot.get_channel(discord_environment["Default_Channel"])
    default_guild = bot.get_guild("PUT GUILD INT HERE")

    MESSAGE = [member for member in default_guild.members if member.global_name is not None]
    for name in MESSAGE:
        await default_channel.send(f"Name: {name.global_name}, status: {name.raw_status} state: {name._state}")
        
"""
Create Functionality
"""
@bot.command()
async def get_joke(ctx):
    myjokes.newJoke()
    joke = myjokes.getJoke()
    
    await ctx.send(joke)


@bot.command()
async def send_embed(ctx):
    embed = discord.Embed(
        title="Welcome to Our Server!",
        description="This is a sample message styled with Discord's embed feature.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Feature 1", value="Description of Feature 1", inline=False)
    embed.add_field(name="Feature 2", value="Description of Feature 2", inline=False)
    embed.set_footer(text="Footer text here")
    embed.set_thumbnail(url="https://example.com/yourimage.png")
    
    default_channel = bot.get_channel(discord_environment["Default_Channel"])
    if default_channel:
        await default_channel.send(embed=embed)
        await ctx.send("Embed sent to the default channel!")
    else:
        await ctx.send("Default channel not found!")


bot.run(discord_environment["TOKEN"])