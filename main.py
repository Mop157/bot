import discord
from discord.ext import commands, tasks
from colorama import Back, Fore, Style
import time
import json
import platform
import config
import random
import asyncio

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=discord.Intents().all())
        self.cogslist = ["cogs.command.fun", "cogs.command.moderator"]
        if config.SQLite == True:
            self.cogslist.append("cogs.SQLite.SQLite")

    async def setup_hook(self):
      for ext in self.cogslist:
        await self.load_extension(ext)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " загрузка бота " + Fore.YELLOW + self.user.name)
        print(prfx + " бот ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Дискорд версия " + Fore.YELLOW + discord.__version__)
        print(prfx + " пайтон версия " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " количество серверов: " + Fore.YELLOW + str(len(client.guilds)))
        print(prfx + " все слэш команды: " + Fore.YELLOW + str(len(synced)))
        all_commands = client.commands
        print(prfx + " все команды: " + Fore.YELLOW + str(len(all_commands)))
        self.my_task.start()
        
    @tasks.loop(seconds=120)
    async def my_task(self):
        activs = random.choice(config.activ)
        await self.change_presence(activity=discord.CustomActivity(name=activs))

    
client = Client()
client.remove_command('help')

client.run(config.TOKEN)
