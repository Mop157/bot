import random, json, asyncio, re

import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
import config
import cogs.tekst as tekst
import cogs.Button.Button as button

list_rps = {}
list_mafia = {}

class fun(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.prefix = config.prefix

#######################################################
########## камень, ножничи, бумага ####################
#######################################################


  @app_commands.command(name="rps", description="Камень, ножницы, бумага")
  async def game(self, interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(tekst.rps_DM)
        return

    if config.rps == False:
        await interaction.response.send_message(tekst.nots)
        return

    button_rps_bot = Button(emoji=f"🤖", style=discord.ButtonStyle.blurple, custom_id="button_rps1")
    button_rps_user = Button(emoji=f"👥", style=discord.ButtonStyle.blurple, custom_id="button_rps2")
    button_rps_info = Button(emoji=f"❓", style=discord.ButtonStyle.green, custom_id="button_rps3")
    button_rps_paper = Button(emoji=f"📄", style=discord.ButtonStyle.gray, custom_id="button_rps4")
    button_rps_kamen = Button(emoji=f"⛰️", style=discord.ButtonStyle.gray, custom_id="button_rps5")
    button_rps_noznuci = Button(emoji=f"✂️", style=discord.ButtonStyle.gray, custom_id="button_rps6")
    button_rps_play = Button(emoji="▶️", style=discord.ButtonStyle.green, custom_id="button_rps7")

    view_game = discord.ui.View()
    view_game.add_item(button_rps_bot)
    view_game.add_item(button_rps_user)
    view_game.add_item(button_rps_info)

    async def button_callback_rps_bot(interaction: discord.Interaction):
        view_bot = discord.ui.View(timeout=30)
        view_bot.add_item(button_rps_kamen)
        view_bot.add_item(button_rps_noznuci)
        view_bot.add_item(button_rps_paper)
        stop_event3 = asyncio.Event()
        interaction3 = interaction

        async def timeout3_callback():
            try:
                await asyncio.wait_for(stop_event3.wait(), timeout=view_bot.timeout)
            except asyncio.TimeoutError:
                await interaction3.followup.send(tekst.rps_error_user4)
                return
        self.client.loop.create_task(timeout3_callback()) 

        await interaction.response.send_message(content=tekst.rps_play_bot, view=view_bot)
        async def paper(interaction: discord.Interaction):
            choices = ['камень', 'ножницы', 'бумага']
            user = 'бумага'
            stop_event3.set()

            bot_choice = random.choice(choices)

            if user == bot_choice:                    
                await interaction.response.edit_message(content=f"Ничья!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            elif bot_choice == 'ножницы':
                await interaction.response.edit_message(content=f"Я выиграл!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            elif bot_choice == 'камень':
                await interaction.response.edit_message(content=f"Вы выиграли!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
                    
        async def kamen(interaction: discord.Interaction):
            user = 'камень'
            choices = ['камень', 'ножницы', 'бумага']
            stop_event3.set()

            bot_choice = random.choice(choices)

            if user == bot_choice:                    
                await interaction.response.edit_message(content=f"Ничья!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            elif bot_choice == 'ножницы':
                await interaction.response.edit_message(content=f"Вы выиграли!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            elif bot_choice == 'бумага':
                await interaction.response.edit_message(content=f"Я выиграл!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            
        async def noznuci(interaction: discord.Interaction):
            user = 'ножницы'
            choices = ['камень', 'ножницы', 'бумага']
            stop_event3.set()

            bot_choice = random.choice(choices)

            if user == bot_choice:                    
                await interaction.response.edit_message(content=f"Ничья!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            elif bot_choice == 'бумага':
                await interaction.response.edit_message(content=f"Вы выиграли!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)
            elif bot_choice == 'камень':
                await interaction.response.edit_message(content=f"Я выиграл!\n\nВы выбрали: {user}, я выбрал: {bot_choice}", view=None)

        button_rps_paper.callback = paper
        button_rps_kamen.callback = kamen
        button_rps_noznuci.callback = noznuci

    async def button_callback_rps_user(interaction: discord.Interaction):
        view_game_user = discord.ui.View(timeout=60)
        view_game_user.add_item(button_rps_play)
        view_game_user.add_item(button_rps_user)
        view_game_user.add_item(button_rps_info)

        channel_id = interaction.channel_id
        member = interaction.user.id
        stop_event1 = asyncio.Event()
        interaction1 = interaction

        async def timeout1_callback():
            try:
                await asyncio.wait_for(stop_event1.wait(), timeout=view_game_user.timeout)
            except asyncio.TimeoutError:
                try:
                    del list_rps[channel_id]
                    return
                except KeyError:
                    return
        
        if channel_id in list_rps:
            if len(list_rps[channel_id]['players']) == 1:
                list_rps[channel_id]['players'][member] = None
                if len(list_rps[channel_id]['players']) == 1:
                    await interaction.response.send_message(content=tekst.rps_error_user1, ephemeral=True)
                    return
                user_bol = 2
                button_rps_user.disabled = True
                button_rps_play.disabled = False
            else:
                await interaction.response.send_message(content=tekst.rps_error_user2, ephemeral=True)
                return  
        else:
            list_rps[channel_id] = {'players': {member: None}}
            user_bol = 1
            button_rps_play.disabled = True
            self.client.loop.create_task(timeout1_callback()) 

        async def play(interaction: discord.Interaction):
            view_user = discord.ui.View(timeout=30)
            view_user.add_item(button_rps_kamen)
            view_user.add_item(button_rps_noznuci)
            view_user.add_item(button_rps_paper)
            stop_event2 = asyncio.Event()
            interaction2 = interaction

            async def timeout2_callback():
                try:
                    await asyncio.wait_for(stop_event2.wait(), timeout=view_user.timeout)
                except asyncio.TimeoutError:
                    try:
                        await interaction2.followup.send(tekst.rps_error_user4)
                        del list_rps[channel_id]
                        return
                    except KeyError:
                        return
            self.client.loop.create_task(timeout2_callback()) 

            button_rps_play.disabled = True
            await interaction.response.edit_message(view=view_game_user)
            
            await interaction.followup.send(tekst.rps_play_bot, view=view_user)

            async def paper1(interaction: discord.Interaction):
                await handle_choice(interaction, "Бумага")
            async def kamen1(interaction: discord.Interaction):
                await handle_choice(interaction, "Камень")
            async def noznuci1(interaction: discord.Interaction):
                await handle_choice(interaction, "Ножницы")
                
            button_rps_kamen.callback = kamen1
            button_rps_paper.callback = paper1
            button_rps_noznuci.callback = noznuci1

            async def handle_choice(interaction, choice):
                player_id = interaction.user.id
                if list_rps[channel_id]['players'][player_id] == None:
                    list_rps[channel_id]['players'][player_id] = choice
                else:
                    await interaction.response.send_message(tekst.rps_error_user3, ephemeral=True)
                    return

                for gam in list_rps[channel_id]['players']:
                    if gam == player_id:
                        pass
                    else:
                        break

                try:
                    await interaction.response.send_message(f"Вы выбрали {choice}. Ожидание второго игрока...", ephemeral=True)
                except discord.errors.InteractionResponded:
                    await interaction.followup.send(f"Вы выбрали {choice}. Ожидание второго игрока...", ephemeral=True)

                if (list_rps[channel_id]['players'][player_id] is not None) and (list_rps[channel_id]['players'][gam] is not None):
                    user1 = None
                    user2 = None
                    for gam1 in list_rps[channel_id]['players']:
                        if user1 == None:
                            user1 = gam1
                            continue
                        if user2 == None:
                            user2 = gam1
                    player_1 = list_rps[channel_id]['players'][user1]
                    player_2 = list_rps[channel_id]['players'][user2]
                    stop_event2.set()

                    if player_1 == player_2:
                        result = "Ничья!"
                    elif (player_1 == "Камень" and player_2 == "Ножницы") or \
                        (player_1 == "Ножницы" and player_2 == "Бумага") or \
                        (player_1 == "Бумага" and player_2 == "Камень"):
                        result = f"Игрок <@{user1}> выиграл!"
                    else:
                        result = f"Игрок <@{user2}> выиграл!"
            
                    await interaction.followup.send(f"{result}\n\nигрок: <@{user1}> выбрал {player_1}\nигрок: <@{user2}> выбрал {player_2}")
                    try:
                        del list_rps[channel_id]
                        return
                    except KeyError:
                        return

        button_rps_play.callback = play

        await interaction.response.edit_message(content=f"С кем бы вы хотели сыграть?\nигроков {user_bol}/2\n", view=view_game_user)

    async def button_callback_rps_info(interaction: discord.Interaction):
        await interaction.response.send_message(content=tekst.rps_info, ephemeral=True)

    button_rps_bot.callback = button_callback_rps_bot
    button_rps_user.callback = button_callback_rps_user
    button_rps_info.callback = button_callback_rps_info

    await interaction.response.send_message(content=tekst.rps_play, view=view_game)

#######################################################
    ########## волшебной восьмерке ####################
#######################################################

  @app_commands.command(name="8ball", description="Задает вопрос волшебной восьмерке")
  async def _8ball(self, interaction: discord.Interaction, *, вопрос: str = None):

    if config.Hball == False:
        await interaction.response.send_message(tekst.nots)
        return
    elif вопрос is None:
        await interaction.response.send_message(":x: | Вы не задали вопрос!")
        return
    else:
        responses = [
            "Это точно.",
            "Это решительно так.",
            "Без сомнения.",
            "Да, безусловно.",
            "Вы можете положиться на него.",
            "Насколько я вижу, да.",
            "Вероятно.",
            "Перспективы хорошие.",
            "да.",
            "Знаки указывают на да.",
            "Ответ неясен, попробуйте еще раз.",
            "Спроси позже.",
            "Лучше не говорить тебе сейчас.",
            "Не могу предсказать сейчас.",
            "Сосредоточьтесь и спросите еще раз.",
            "Не рассчитывайте на это.",
            "Перспективы не очень хорошие.",
            "Мои источники говорят, что нет.",
            "Очень сомнительно.",
            "нет.",
            "точно нет.",
        ]

        await interaction.response.send_message(
            f"__Вопрос__: {вопрос}\n__Ответ__: {random.choice(responses)}"
        )
#######################################################
     ########## колесо фортуни ####################
#######################################################

  @app_commands.command(name="slot", description="Играть в игровые автоматы.")
  async def slots(self, interaction: discord.Interaction):
    if config.slots == False:
        await interaction.response.send_message(tekst.nots)
        return
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"

    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    d = random.choice(emojis)
    q = random.choice(emojis)
    w = random.choice(emojis)
    r = random.choice(emojis)
    t = random.choice(emojis)
    y = random.choice(emojis)


    slotmachine = f"""**
    ╔ ◾ 🎰 ◽ ╗
    ║ {d} {q} {w} ║    
    ╠ {a} {b} {c} ╣
    ║ {r} {t} {y} ║
    ╚ ◽ 🎰 ◾ ╝
    **"""

    if a == b == c:
        await interaction.response.send_message(
            f"{slotmachine}\n{interaction.user.name}, Все совпадения, вы выиграли! 🎉"
        )
    elif (a == b) or (a == c) or (b == c):
        await interaction.response.send_message(
            f"{slotmachine}\n{interaction.user.name}, 2 тот матч, ты выиграл! 🎉"
        )
    else:
        await interaction.response.send_message(
            f"{slotmachine}\n{interaction.user.name}, Нет совпадений, ты проиграл 😢",
        )


#######################################################
    ########## сапер ####################
#######################################################

  @app_commands.command(name="mafia", description="Мафия через Discord Бота")
  async def mafia(self, interaction: discord.Interaction):
      channel_id = interaction.channel.id

      async def add_player(interaction: discord.Interaction):
          interaction1 = interaction.message.id
          member = interaction.user.id
          if channel_id in list_mafia:
              if len(list_mafia[channel_id]['players']) < 4:
                  for add in list_mafia[channel_id]['players']:
                      if add == member:
                          await interaction.response.send_message(tekst.mafia_error_2, ephemeral=True)
                          return
                  list_mafia[channel_id]['players'][member] = {"роль": "мирный", "голос": 0}
                  list_mafia[channel_id]['players'][628686422244589561] = {"роль": "мирный", "голос": 0}
                  list_mafia[channel_id]['players'][628686422244589562] = {"роль": "мирный", "голос": 0}
                  await interaction.response.send_message(tekst.mafia_add_player, ephemeral=True)
                  if len(list_mafia[channel_id]['players']) == 4:
                      if len(list_mafia[channel_id]['players']) == 12:
                        add_pley_button.disabled = True
                      start_button.disabled = False
              else:
                await interaction.response.send_message(content=tekst.mafia_error_1, ephemeral=True)
                return  
          else:
            list_mafia[channel_id] = {'players': {member: {"роль": "мирный", "голос": 0}}}
            await interaction.response.send_message(tekst.mafia_start, ephemeral=True)
          await interaction.followup.edit_message(message_id=interaction1, content=f"{tekst.mafia_game}\nПрисоединились к игре {len(list_mafia[channel_id]['players'])}\n", view=view)

      async def game_start(interaction: discord.Interaction):
          add_pley_button.disabled = True
          start_button.disabled = True
          await interaction.response.edit_message(view=view)
          keys = list(list_mafia[channel_id]['players'].keys())
          player_1 = keys[0] if len(keys) > 0 else None
          player_2 = keys[1] if len(keys) > 1 else None
          player_3 = keys[2] if len(keys) > 2 else None
          player_4 = keys[3] if len(keys) > 3 else None
          player_5 = keys[4] if len(keys) > 4 else None
          player_6 = keys[5] if len(keys) > 5 else None
          player_7 = keys[6] if len(keys) > 6 else None
          player_8 = keys[7] if len(keys) > 7 else None
          player_9 = keys[8] if len(keys) > 8 else None
          player_10 = keys[9] if len(keys) > 9 else None
          player_11 = keys[10] if len(keys) > 10 else None
          player_12 = keys[11] if len(keys) > 11 else None

          guild = interaction.guild
          overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}

          existing_channel = discord.utils.get(guild.channels, name="mafia")

          rols = []

          for rolls in list_mafia[channel_id]['players']:
              rols.append(rolls)

          rol1 = random.choice(rols)
          list_mafia[channel_id]['players'][player_1]['роль'] = "мафия"
          rols.remove(rol1)

          rol2 = random.choice(rols)
          list_mafia[channel_id]['players'][player_2]['роль'] = "шериф"
          rols.remove(rol2)

          if len(list_mafia[channel_id]['players']) > 4:
              rol3 = random.choice(rols)
              list_mafia[channel_id]['players'][rol3]['роль'] = "доктор"
              rols.remove(rol3)
    
          if not existing_channel:
            channe = await guild.create_text_channel("mafia", overwrites=overwrites)
            channel_mafia = channe.id
            for x in list_mafia[channel_id]['players']:
                if x == 628686422244589561 or x == 628686422244589562:
                    continue
                players = guild.get_member(x)
                await players.send(content=f"поздравляю вы {list_mafia[channel_id]['players'][x]['роль']}\nникому не говорите кто вы до окончания игры\nпожалуста перейдите в канал <#{channel_mafia}>")
                await channe.set_permissions(players, read_messages=True, send_messages=True)
          else:
                await interaction.followup.send(":x: | error channel!")
                return
          
          await interaction.followup.send(f"{player_1} = {list_mafia[channel_id]['players'][player_1]['роль']},\n{player_2} = {list_mafia[channel_id]['players'][player_2]['роль']},\n{player_3} = {list_mafia[channel_id]['players'][player_3]['роль']},\n{player_4} = {list_mafia[channel_id]['players'][player_4]['роль']}")
        
          await channe.send(content="в этом канале будет проводиться игра, пожалуйста администрация не отвлекайте участников от игры и следите за игрой")
          await asyncio.sleep(30)

          day = 1
          while True:
              
              maf = None
              wef = True
              dok = None
              do = None
              deb = None
              await channe.send(content=f" \nдень {day}")
              for a in list_mafia[channel_id]['players']:
                if a == 628686422244589561 or a == 628686422244589562:
                    continue
                for s in list_mafia[channel_id]['players']:
                    if s == 628686422244589561 or s == 628686422244589562:
                        continue
                    elif a == s:
                        continue
                    ss = guild.get_member(s)
                    await channe.set_permissions(ss, send_messages=False, read_messages=True)
                aa = guild.get_member(a)
                await channe.set_permissions(aa, send_messages=True, read_messages=True)
                await channe.send(content=f" \nучастник <@{a}> ваша речь")
                await asyncio.sleep(20)
              for a in list_mafia[channel_id]['players']:
                if a == 628686422244589561 or a == 628686422244589562:
                    continue
                aa = guild.get_member(a)
                await channe.set_permissions(ss, send_messages=True, read_messages=True)
              await channe.send(content=" \nу вас 2 менуты для обсуждения")
              await asyncio.sleep(60)
              await channe.send(content=" \nосталась 1 менута")
              await asyncio.sleep(60)
              await channe.send(content=" \nвремя вышло, голосуем кто-то выйдет сегодня или нет")
              await asyncio.sleep(5)
              for z in list_mafia[channel_id]['players']:
                if z == 628686422244589561 or z == 628686422244589562:
                    continue
                for c in list_mafia[channel_id]['players']:
                    if c == 628686422244589561 or c == 628686422244589562:
                        continue
                    elif z == c:
                        continue
                    cc = guild.get_member(c)
                    await channe.set_permissions(cc, send_messages=False, read_messages=True)
                zz = guild.get_member(z)
                await channe.set_permissions(zz, send_messages=True, read_messages=True)
                await channe.send(content=f" \nпожалуста <@{z}> проголосуйте за какого-то участника (пинганите его)")
                def check(message):
                    return message.author.id == z
                try:
                    message = await self.client.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await channe.send("Вы не проголосовали вовремя.")
                    list_mafia[channel_id]['players'][z]['голос'] += 1
                else:
                    await channe.send(f"вы проголосовали за {message.content}")
                    user = re.match(r'<@!?(\d+)>', message.content)
                    try:
                        list_mafia[channel_id]['players'][int(user.group(1))]['голос'] += 1
                    except KeyError:
                        pass
                await channe.set_permissions(zz, send_messages=False, read_messages=True)
              us = None
              point = 0
              for b in list_mafia[channel_id]['players']:
                if b == 628686422244589561 or b == 628686422244589562:
                    continue
                if list_mafia[channel_id]['players'][b]['голос'] > point:
                    point = list_mafia[channel_id]['players'][b]['голос']
                    us = b

              if point == 1 or point == 0:
                  pass
              else:
                  uss = guild.get_member(us)
                  await channe.set_permissions(uss, send_messages=False, read_messages=False)
                  await channe.send(f"{list_mafia[channel_id]['players'][us]['роль']} был исключен из игры по количеству голосов: {point}")
                  del list_mafia[channel_id]['players'][us]

              await asyncio.sleep(5)
              await channe.send("ночь наступает")

              for n in list_mafia[channel_id]['players']:
                  if list_mafia[channel_id]['players'][n]['роль'] == "шериф":
                      await channe.send("шериф просипаеться")

                      async def menu_callback1(interaction: discord.Interaction):
                        if wef == True:
                            selected_option = interaction.data['values'][0]
                            we = guild.get_member_named(interaction.data['values'][0])
                            await interaction.response.edit_message(content=f"игрок: {selected_option}, являеться {list_mafia[channel_id]['players'][we.id]['роль']}", view=None)
                        else:
                            await interaction.response.send_message(f"вы уже проверите игрока этой ночю", ephemeral=True)
                      
                      options1 = []

                      for opt1 in list_mafia[channel_id]['players']:
                          if opt1 == 628686422244589561 or opt1 == 628686422244589562:
                            continue
                          opts1 = guild.get_member(opt1)
                          options1.append(discord.SelectOption(label=f"{opts1}", value=f"{opts1}"))

                      select = discord.ui.Select(
                            placeholder="выберите игрока",
                            min_values=1,
                            max_values=1,
                            options=options1
                        )
                      select.callback = menu_callback1

                      viewq = discord.ui.View()
                      viewq.add_item(select)

                      ol2 = guild.get_member(rol2)
                      await ol2.send("выберите игрока для проверки", view=viewq)

                  elif list_mafia[channel_id]['players'][n]['роль'] == "доктор" and len(list_mafia[channel_id]['players']) > 4:
                      
                      await asyncio.sleep(5)
                      await channe.send("доктор просипаеться")

                      async def menu_callback2(interaction: discord.Interaction):
                        if dok is None:
                            do = interaction.data['values'][0]
                            await interaction.response.edit_message(content=f"вы выбрали {do}", view=None)
                        else:
                            await interaction.response.send_message(f"вы уже сделали свой выбор", ephemeral=True)
                      
                      options2 = []

                      for opt2 in list_mafia[channel_id]['players']:
                          if opt2 == 628686422244589561 or opt2 == 628686422244589562:
                            continue
                          opts2 = guild.get_member(opt2)
                          options2.append(discord.SelectOption(label=f"{opts2}"))

                      select = discord.ui.Select(
                            placeholder="выберите игрока",
                            min_values=1,
                            max_values=1,
                            options=options2
                        )
                      select.callback = menu_callback2
                      
                      viewqq = discord.ui.View()
                      viewqq.add_item(select)

                      ol3 = guild.get_member(rol3)
                      await ol3.send("выберите игрока для леченя", view=viewqq)
                      
                  elif list_mafia[channel_id]['players'][n]['роль'] == "мафия":
                      
                      await asyncio.sleep(10)
                      await channe.send("мафия просипаеться")

                      async def menu_callback3(interaction: discord.Interaction):
                        if maf is None:
                            ma = interaction.data['values'][0]
                            if do == ma:
                                pass
                            else:
                                deb = guild.get_member_named(interaction.data['values'][0])
                                del list_mafia[channel_id]['players'][deb.id]
                                await channe.set_permissions(deb, send_messages=False, read_messages=False)
                                await interaction.response.edit_message(content=f"вы отправились ночю к участнику {ma}", view=None)
                        else:
                            await interaction.response.send_message(f"вы сегодня уже отправлялись к участнику", ephemeral=True)
                      
                      options3 = []

                      for opt3 in list_mafia[channel_id]['players']:
                          if opt3 == 628686422244589561 or opt3 == 628686422244589562:
                            continue
                          opts3 = guild.get_member(opt3)
                          options3.append(discord.SelectOption(label=f"{opts3}"))

                      select = discord.ui.Select(
                            placeholder="выберите игрока",
                            min_values=1,
                            max_values=1,
                            options=options3
                        )
                      select.callback = menu_callback3
                      
                      viewqqq = discord.ui.View()
                      viewqqq.add_item(select)

                      ol1 = guild.get_member(rol1)
                      await ol1.send("выберите игрока", view=viewqqq)

              await channe.send("город просыпаеться")
              if deb is None:
                  pass
              else:
                  await channe.send(f"ночю был убит игрок {deb}:{list_mafia[channel_id]['players'][deb.id]['роль']}")
              day += 1
              
          
      
      async def info(interaction: discord.Interaction):
          await interaction.response.send_message(tekst.mafia_info, ephemeral=True)

      start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
      button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
      add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

      start_button.callback = game_start
      add_pley_button.callback = add_player
      button_info.callback = info

      view = View()
      view.add_item(start_button)
      view.add_item(add_pley_button)
      view.add_item(button_info)

      start_button.disabled = True
      await interaction.response.send_message(tekst.mafia_game, view=view)

#######################################################

async def setup(client:commands.Bot) -> None:
  await client.add_cog(fun(client))
