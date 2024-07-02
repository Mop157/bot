import asyncio

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import requests
import config

class moderator(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.prefix = config.prefix

  async def menu_callback(self, interaction: discord.Interaction):
    selected_option = interaction.data['values'][0]
    x = interaction.guild.get_member_named(interaction.data['values'][0])
    await interaction.response.send_message(f"You selected: {x}, {x.id}", ephemeral=True)

# Команда для отображения меню
  @commands.command(name="menu")
  async def menu(self, ctx: commands.Context):
    # Создаем опции для выпадающего меню
    
    member = [670163392979271710, 628686422244589569]
    options = []

    for members in member:
       print(members)
       c = ctx.guild.get_member(int(members))
       options.append(discord.SelectOption(label=f"{c}"))
    # Создаем Select меню
    select = discord.ui.Select(
        placeholder="Choose an option...",
        min_values=1,
        max_values=1,
        options=options
    )
    select.callback = self.menu_callback

    # Создаем View и добавляем Select меню в View
    view = discord.ui.View()
    view.add_item(select)

    # Отправляем сообщение с View
    await ctx.send("\n\nSelect an option from the menu below:", view=view)

  @commands.command()
  async def test(self, ctx):
    id = 670163392979271710
    def check(message):
        return message.author.id == id
    try:
        message = await self.client.wait_for('message', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Вы не отправили сообщение вовремя.")
    else:
        await ctx.send(f"Вы отправили: {message.content}")
        print(message.content)

  @commands.command(name="help")
  async def help(self, ctx: commands.Context):
      await ctx.send(
      content=f"""```ini
список команд | Префикс: {self.prefix}

[{self.prefix}rps] камень, ножницы, бумага
[{self.prefix}slot] игровый автомат
[{self.prefix}8ball] вольшебная восьмерка
[{self.prefix}mafia] мафия в дискорде
[{self.prefix}Buckshot roulette] русская рулетка)
[{self.prefix}ведьма] карточная игра ведьма

[{self.prefix}info] информация об боте
```""")
      
  @commands.command(name="info")
  async def info(self, ctx: commands.Context):     
      async def help(interaction: discord.Interaction):
         await interaction.response.send_message("""
Если у вас появились вопросы по поводу меня, или вы обнаружили баг, заходите на мой [сервер поддержки](https://discord.gg/2exCUfVv8z). Там вы найдете все новости обо мне, а также сможете получить помощь, если мой автор занят и не может ответить сразу.
""", ephemeral=True)

      async def info(interaction: discord.Interaction):
         await interaction.response.send_message("""
# Важная информация для всех пользователей!

**Список игр, которые не прошли бета-тест**:

- Мафия (больше 4 игроков) — оформление игры и код подлежат скорейшему изменению.
- Ведьма (больше 2 игроков)

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
      await ctx.send(f"""
Привет! Я бот **{self.client.user.name}** и я создан для игр на этом сервере.
Мои функции включают игровые команды, чтобы поддерживать развлечения для участников.
Вот немного информации обо мне:
```ini
Автор: mop157
Версия: {config.versia}
Количество серверов: {len(self.client.guilds)}
Количество всех игр: {synceds}
Количество всех команд: {all_commands}
```
Спасибо за использование меня в играх! Если у вас есть вопросы или нужна помощь, обратитесь к моему автору.""", view=view)

  # @commands.command(name="info")
  # async def info(self, ctx: commands.Context):
       

async def setup(client:commands.Bot) -> None:
  await client.add_cog(moderator(client))