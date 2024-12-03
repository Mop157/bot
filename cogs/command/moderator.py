import asyncio, random

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import requests
import config
import cogs.text.slad as slad

lolo = ["slot", "pop", "joji"]

l_values = {
    "l1": 0,
    "l2": 0,
    "l3": 0,
    "l4": 0,
    "l": 1
}
l1 = ["1", "2", "3", "4", "5"]

class moderator(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.prefix = config.prefix

  async def menu_callback(self, interaction: discord.Interaction):
    print(interaction.data)
    selected_option = interaction.data['custom_id']
    await interaction.response.send_message(f"{selected_option}", ephemeral=True)        

  @app_commands.command(name="help", description="help")
  async def help(self, interaction: discord.Interaction):
      await interaction.response.send_message(
      content=f"""```ini
список команд | Префикс: {self.prefix}

      )==]|•-=> (1 игрок) <=-•|[==(
[{self.prefix}slot] Игровый автомат.
[{self.prefix}8ball] Вольшебная восьмерка.
[{self.prefix}угадай_число] Игра на угадывание числа.

     -)==]|•-=> (2 игрока) <=-•|[==(-
[{self.prefix}rps] Камень, ножницы, бумага.
[{self.prefix}Buckshot roulette] Русская рулетка.

    ~-)==]|•-=> (2+ игрока) <=-•|[==(-~
[{self.prefix}ведьма] Карточная игра ведьма.
[{self.prefix}role_playing] Ролевые диалоги.(beta)
[{self.prefix}викторина] Вопросы викторины.
[{self.prefix}виселица] Угадать слово по буквам.
[{self.prefix}truth_or_lie] Правда или ложь.
[{self.prefix}anagrams] Расшифровка слова.

   -=-)==]|•-=> (4+ игрока) <=-•|[==(-=-
[{self.prefix}mafia] Мафия в дискорде.


[{self.prefix}info] информация об боте
```""")
      
  @app_commands.command(name="info", description="info")
  async def info(self, interaction: discord.Interaction):     
      async def help(interaction: discord.Interaction):
         await interaction.response.send_message("""
Если у вас появились вопросы по поводу меня, или вы обнаружили баг, заходите на мой [сервер поддержки](https://discord.gg/2exCUfVv8z). Там вы найдете все новости обо мне, а также сможете получить помощь, если мой автор занят и не может ответить сразу.\n сервер - https://discord.gg/2exCUfVv8z 
""", ephemeral=True)

      async def info(interaction: discord.Interaction):
         await interaction.response.send_message("""
# Важная информация для всех пользователей!

Все игры, в которых есть возможность играть втроём и более, не прошли бета-тестирование на 3+ игроков. Поэтому, пожалуйста, в случае багов или неисправностей напишите моему создателю или перейдите на мой сервер поддержки.

Спасибо за понимание! Причина такой ситуации — недостаток бета-тестеров.
""", ephemeral=True)
      
      button_help = Button(emoji="☎️", label="Пуддержка", style=discord.ButtonStyle.green)
      button_infa = Button(emoji="❗", label="Важно", style=discord.ButtonStyle.red)

      button_help.callback = help
      button_infa.callback = info

      view = View()
      view.add_item(button_infa)
      view.add_item(button_help)

      synced = await self.client.tree.sync()
      synceds = len(synced)
      all_command = self.client.commands
      all_commands = len(all_command)
      await interaction.response.send_message(f"""
Привет! Я бот **{self.client.user.name}** и я создан для игр на этом сервере.
Мои функции включают игровые команды, чтобы поддерживать развлечения для участников.
Вот немного информации обо мне:
```ini
Автор: mop157
Версия: {config.versia}
Количество серверов: {len(self.client.guilds) - 4}
Количество всех игр: {synceds - 2}
Количество всех команд: {all_commands}
```
Спасибо за использование меня в играх! Если у вас есть вопросы или нужна помощь, обратитесь к моему автору.""", view=view)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(moderator(client))
