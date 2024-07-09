import asyncio

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import requests
import config
import cogs.text.slad as slad

lolo = ["slot", "pop", "joji"]

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

  @app_commands.command(name="help", description="help")
  async def help(self, interaction: discord.Interaction):
      await interaction.response.send_message(
      content=f"""```ini
список команд | Префикс: {self.prefix}

      )==]|•-=> (1 игрок) <=-•|[==(
[{self.prefix}slot] Игровый автомат.
[{self.prefix}8ball] Вольшебная восьмерка.
[{self.prefix}угадай_число] Игра на угадывание числа.

     -)==]|•-=> (2 игрок) <=-•|[==(-
[{self.prefix}rps] Камень, ножницы, бумага.(beta)
[{self.prefix}Buckshot roulette] Русская рулетка.

    --)==]|•-=> (2+ игрок) <=-•|[==(--
[{self.prefix}ведьма] Карточная игра ведьма.
[{self.prefix}role_playing] Ролевые диалоги.(beta)
[{self.prefix}викторина] Вопросы викторины.
[{self.prefix}виселица] Угадать слово по буквам.
[{self.prefix}truth_or_lie] Правда или ложь.
[{self.prefix}anagrams] Расшифровка слова.

   ---)==]|•-=> (4+ игрок) <=-•|[==(---
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
      await interaction.response.send_message(f"""
Привет! Я бот **{self.client.user.name}** и я создан для игр на этом сервере.
Мои функции включают игровые команды, чтобы поддерживать развлечения для участников.
Вот немного информации обо мне:
```ini
Автор: mop157
Версия: {config.versia}
Количество серверов: {len(self.client.guilds) - 4}
Количество всех игр: {synceds - 2}
Количество всех команд: {all_commands - 1}
```
Спасибо за использование меня в играх! Если у вас есть вопросы или нужна помощь, обратитесь к моему автору.""", view=view)

  @commands.command(name="Haiko")
  async def haiko(self, ctx: commands.Context):
    message = await ctx.send("""
╭─━━━━━───━──━━━⊱⋆⊰━━━─────━━━━━━─╮
  `Хайло — добрый и отзывчивый друг, с кото`
╰─━━━━━━━━─────━⊱⋆⊰━━━──━───━━━━━─╯
""")

    animate = [slad.animate1, slad.animate2, slad.animate3, slad.animate4, slad.animate5, slad.animate6, slad.animate7, slad.animate8, slad.animate9, slad.animate10,
               slad.animate11, slad.animate12, slad.animate13, slad.animate14, slad.animate15, slad.animate16, slad.animate17, slad.animate18, slad.animate19, slad.animate20,
               slad.animate21, slad.animate22, slad.animate23, slad.animate24, slad.animate25, slad.animate26, slad.animate27, slad.animate28, slad.animate29, slad.animate30,
               slad.animate31, slad.animate32, slad.animate33, slad.animate34, slad.animate35, slad.animate36, slad.animate37, slad.animate38, slad.animate39, slad.animate40,
               slad.animate41, slad.animate42, slad.animate43, slad.animate44, slad.animate45, slad.animate46, slad.animate47, slad.animate48, slad.animate49, slad.animate50,
               slad.animate51, slad.animate52, slad.animate53, slad.animate54, slad.animate55, slad.animate56, slad.animate57, slad.animate58, slad.animate59, slad.animate60,
               slad.animate61, slad.animate62, slad.animate63, slad.animate64, slad.animate65, slad.animate66, slad.animate67, slad.animate68, slad.animate69, slad.animate70,
               slad.animate71, slad.animate72, slad.animate73, slad.animate74, slad.animate75, slad.animate76, slad.animate77, slad.animate78, slad.animate79, slad.animate80,
               slad.animate81, slad.animate82, slad.animate83, slad.animate84, slad.animate85]
    
    await asyncio.sleep(2)
    for i in animate:
      await asyncio.sleep(0.4)
      await message.edit(content=f"{i}")
    


async def setup(client:commands.Bot) -> None:
  await client.add_cog(moderator(client))