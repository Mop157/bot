import random, json, asyncio, re

import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
import config
import cogs.text.tekst as tekst
import cogs.Button.Button as button
import cogs.text.Trivia_Quix_text as Quix

list_rps = {}
list_mafia = {}
buskshot = {}
witch = {}
Trivia = {}

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
        await interaction.response.send_message(tekst.DM)
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
      if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
      
      if config.mafia == False:
        await interaction.response.send_message(tekst.nots)
        return
      
      channel_id = interaction.channel.id

      async def add_player(interaction: discord.Interaction):
          interaction1 = interaction.message.id
          member = interaction.user.id
          if channel_id in list_mafia:
              if len(list_mafia[channel_id]['players']) < 13:
                  for add in list_mafia[channel_id]['players']:
                      if add == member:
                          await interaction.response.send_message(tekst.mafia_error_2, ephemeral=True)
                          return
                  list_mafia[channel_id]['players'][member] = {"роль": "мирный", "голос": 0, "гол": 0}
                  await interaction.response.send_message(tekst.mafia_add_player, ephemeral=True)
                  if len(list_mafia[channel_id]['players']) == 4:
                      start_button.disabled = False
                  if len(list_mafia[channel_id]['players']) == 12:
                      add_pley_button.disabled = True
              else:
                await interaction.response.send_message(content=tekst.mafia_error_1, ephemeral=True)
                return  
          else:
            list_mafia[channel_id] = {'players': {member: {"роль": "мирный", "голос": 0, "гол": 0}}, 'info': {'day': 1, 'док': None, 'мафия': None,  'очки1': 0, 'очки2': 0, 'маньяк': None, 'путана': None, 'дон': None, 'user': 0, 'мафия1': 0}}           
            await interaction.response.send_message(tekst.mafia_start, ephemeral=True)
          await interaction.followup.edit_message(message_id=interaction1, content=f"{tekst.mafia_game}\nПрисоединились к игре {len(list_mafia[channel_id]['players'])}\n.", view=view)

      async def game_start(interaction: discord.Interaction):
          stop_event.set()
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

          if len(list_mafia[channel_id]['players']) == 4:
            list_mafia[channel_id]['info']['user'] += 3

            r2 = ["шериф", "доктор"]
            r_2 = ["мафия", "дон"]
              
            rol1 = random.choice(rols)
            list_mafia[channel_id]['players'][rol1]['роль'] = random.choice(r2)
            rols.remove(rol1)

            rol2 = random.choice(rols)
            list_mafia[channel_id]['players'][rol2]['роль'] = random.choice(r_2)
            rols.remove(rol2)

          elif len(list_mafia[channel_id]['players']) > 4 and len(list_mafia[channel_id]['players']) < 7:
            list_mafia[channel_id]['info']['user'] += len(list_mafia[channel_id]['players']) - 2
            
            r1 = ["доктор", "путана", "шериф"]
            r2 = ["мафия", "дон", "маньяк"]

            rol1 = random.choice(rols)
            rol1_1 = random.choice(r1)
            list_mafia[channel_id]['players'][rol1]['роль'] = rol1_1
            rols.remove(rol1)
            r1.remove(rol1_1)


            rol2 = random.choice(rols)
            list_mafia[channel_id]['players'][rol2]['роль'] = random.choice(r1)
            rols.remove(rol2)

            rol3 = random.choice(rols)
            rol1_2 = random.choice(r2)
            list_mafia[channel_id]['players'][rol3]['роль'] = rol1_2
            rols.remove(rol3)
            if rol1_2 == "мафия":
                pass
            else:
                r2.remove(rol1_2)

            rol4 = random.choice(rols)
            list_mafia[channel_id]['players'][rol4]['роль'] = random.choice(r2)
            rols.remove(rol4)
          
          elif len(list_mafia[channel_id]['players']) > 6 and len(list_mafia[channel_id]['players']) < 10:
            list_mafia[channel_id]['info']['user'] += len(list_mafia[channel_id]['players']) - 3 
            
            r2 = ["мафия", "дон", "маньяк"]

            rol0 = random.choice(rols)
            list_mafia[channel_id]['players'][rol0]['роль'] = "доктор"
            rols.remove(rol0)

            rol1 = random.choice(rols)
            list_mafia[channel_id]['players'][rol1]['роль'] = "путана"
            rols.remove(rol1)

            rol2 = random.choice(rols)
            list_mafia[channel_id]['players'][rol2]['роль'] = "шериф"
            rols.remove(rol2)

            rol3 = random.choice(rols)
            rol1_2 = random.choice(r2)
            list_mafia[channel_id]['players'][rol3]['роль'] = rol1_2
            rols.remove(rol3)
            if rol1_2 == "мафия":
                pass
            else:
                r2.remove(rol1_2)

            rol4 = random.choice(rols)
            rol1_3 = random.choice(r2)
            list_mafia[channel_id]['players'][rol4]['роль'] = rol1_3
            rols.remove(rol4)
            if rol1_3 == "мафия":
                pass
            else:
                r2.remove(rol1_3)

            rol5 = random.choice(rols)
            list_mafia[channel_id]['players'][rol5]['роль'] = random.choice(r2)
            rols.remove(rol5)
          
          elif len(list_mafia[channel_id]['players']) > 9:
            list_mafia[channel_id]['info']['user'] += len(list_mafia[channel_id]['players']) - 4

            rol0 = random.choice(rols)
            list_mafia[channel_id]['players'][rol0]['роль'] = "доктор"
            rols.remove(rol0)

            rol1 = random.choice(rols)
            list_mafia[channel_id]['players'][rol1]['роль'] = "путана"
            rols.remove(rol1)

            rol2 = random.choice(rols)
            list_mafia[channel_id]['players'][rol2]['роль'] = "шериф"
            rols.remove(rol2)

            rol3 = random.choice(rols)
            list_mafia[channel_id]['players'][rol3]['роль'] = "мафия"
            rols.remove(rol3)

            rol4 = random.choice(rols)
            list_mafia[channel_id]['players'][rol4]['роль'] = "мафия"
            rols.remove(rol4)

            rol5 = random.choice(rols)
            list_mafia[channel_id]['players'][rol5]['роль'] = "дон"
            rols.remove(rol5)

            rol6 = random.choice(rols)
            list_mafia[channel_id]['players'][rol6]['роль'] = "маньяк"
            rols.remove(rol6)

          rol1 = None # мафия
          rol10 = None # мафия
          rol20 = None # мафия
          rol2 = None # шериф
          rol3 = None # доктор
          rol4 = None # путана
          rol5 = None # маньяк
          rol6 = None # дон

          for rol in list_mafia[channel_id]['players']:
              if list_mafia[channel_id]['players'][rol]['роль'] ==  "шериф":
                  rol2 = rol

              elif list_mafia[channel_id]['players'][rol]['роль'] ==  "доктор":
                  rol3 = rol

              elif list_mafia[channel_id]['players'][rol]['роль'] ==  "путана":
                  rol4 = rol

              elif list_mafia[channel_id]['players'][rol]['роль'] ==  "маньяк":
                  list_mafia[channel_id]['info']['очки2'] += 1
                  rol5 = rol

              elif list_mafia[channel_id]['players'][rol]['роль'] ==  "дон":
                  list_mafia[channel_id]['info']['очки1'] += 1
                  rol6 = rol

              elif list_mafia[channel_id]['players'][rol]['роль'] ==  "мафия":
                  if rol1 is None:
                      rol1 = rol
                      list_mafia[channel_id]['info']['очки1'] += 1
                  else:
                      if rol10 is None:
                          rol10 = rol
                          list_mafia[channel_id]['info']['очки1'] += 1
                      else:
                          if rol20 is None:
                            rol20 = rol
                            list_mafia[channel_id]['info']['очки1'] += 1
    
          if not existing_channel:
            channe = await guild.create_text_channel("mafia", overwrites=overwrites)
            channel_mafia = channe.id
            for x in list_mafia[channel_id]['players']:
                players = guild.get_member(x)
                await players.send(content=f"поздравляю вы {list_mafia[channel_id]['players'][x]['роль']}\nникому не говорите кто вы до окончания игры\nпожалуста перейдите в канал <#{channel_mafia}>")
                await channe.set_permissions(players, read_messages=True, send_messages=True)
          else:
                await interaction.followup.send(":x: | error channel!")
                del list_mafia[channel_id]
                return
          
          await interaction.followup.send(f"""
игра началась
""")
        
          await channe.send(content="в этом канале будет проводиться игра, пожалуйста администрация не отвлекайте участников от игры и следите за игрой")
          await asyncio.sleep(10)

          async def game_play():
              await channe.send(content=f" \nдень {list_mafia[channel_id]['info']['day']}")
              
              for a in list_mafia[channel_id]['players']:
                for s in list_mafia[channel_id]['players']:
                    if a == s:
                        continue
                    ss = guild.get_member(s)
                    await channe.set_permissions(ss, send_messages=False, read_messages=True)
                aa = guild.get_member(a)
                await channe.set_permissions(aa, send_messages=True, read_messages=True)
                await channe.send(content=f" \nучастник <@{a}> ваша речь")
                await asyncio.sleep(20)
              for a in list_mafia[channel_id]['players']:
                aa = guild.get_member(a)
                await channe.set_permissions(ss, send_messages=True, read_messages=True)
              await channe.send(content=" \nу вас 2 менуты для обсуждения")
              await asyncio.sleep(60)
              await channe.send(content=" \nосталась 1 менута")
              await asyncio.sleep(60)
              await channe.send(content=" \nвремя вышло, голосуем кто-то выйдет сегодня или нет")
              await asyncio.sleep(2)
              for z in list_mafia[channel_id]['players']:
                for c in list_mafia[channel_id]['players']:
                    if z == c:
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
                if list_mafia[channel_id]['players'][b]['голос'] > point:
                    point = list_mafia[channel_id]['players'][b]['голос']
                    us = b
                list_mafia[channel_id]['players'][b]['голос'] = 0

              if point == 1 or point == 0:
                  pass
              else:
                  if list_mafia[channel_id]['info']['путана'] is None:
                    uss = guild.get_member(us)
                    await channe.set_permissions(uss, send_messages=False, read_messages=False)
                    await channe.send(f"{list_mafia[channel_id]['players'][us]['роль']} был исключен из игры по количеству голосов: {point}")
                    
                    if list_mafia[channel_id]['players'][us]['роль'] == "маньяк":
                        list_mafia[channel_id]['info']['очки2'] -= 1

                    elif list_mafia[channel_id]['players'][us]['роль'] == "мафия":
                        list_mafia[channel_id]['info']['очки1'] -= 1

                    elif list_mafia[channel_id]['players'][us]['роль'] == "дон":
                        list_mafia[channel_id]['info']['очки1'] -= 1

                    else:
                        list_mafia[channel_id]['info']['user'] -= 1

                    del list_mafia[channel_id]['players'][us]
                  else:
                    usss = guild.get_member_named(list_mafia[channel_id]['info']['путана'])
                    if us == usss.id:
                        await channe.send(f"у участника {us} есть алибы")
                        list_mafia[channel_id]['info']['путана'] = None
                    else:
                        uss = guild.get_member(us)
                        await channe.set_permissions(uss, send_messages=False, read_messages=False)
                        await channe.send(f"{list_mafia[channel_id]['players'][us]['роль']} был исключен из игры по количеству голосов: {point}")
                        
                        if list_mafia[channel_id]['players'][us]['роль'] == "маньяк":
                            list_mafia[channel_id]['info']['очки2'] -= 1

                        elif list_mafia[channel_id]['players'][us]['роль'] == "мафия":
                            list_mafia[channel_id]['info']['очки1'] -= 1

                        elif list_mafia[channel_id]['players'][us]['роль'] == "дон":
                            list_mafia[channel_id]['info']['очки1'] -= 1

                        else:
                            list_mafia[channel_id]['info']['user'] -= 1
                        
                        del list_mafia[channel_id]['players'][us]
              
              if list_mafia[channel_id]['info']['очки1'] == 0 and list_mafia[channel_id]['info']['очки2'] == 0:
                await channe.send("мирных победа!")
                del list_mafia[channel_id]
                await channe.delete()
                return
                
              if list_mafia[channel_id]['info']['user'] <= list_mafia[channel_id]['info']['очки2']:
                await channe.send("маньяка победа!")
                del list_mafia[channel_id]
                await channe.delete()
                return
                
              if list_mafia[channel_id]['info']['user'] <= list_mafia[channel_id]['info']['очки1']:
                await channe.send("мафии победа!")
                del list_mafia[channel_id]
                await channe.delete()
                return

              await asyncio.sleep(5)
              await channe.send("ночь наступает")

              async def weruf():
                await channe.send("шериф просипаеться")

                async def menu_callback(interaction: discord.Interaction):
                    stop_event.set()
                    selected_option = interaction.data['values'][0]
                    we = guild.get_member_named(interaction.data['values'][0])
                    if 'мафия' == list_mafia[channel_id]['players'][we.id]['роль'] or 'дон' == list_mafia[channel_id]['players'][we.id]['роль']:
                        await interaction.response.edit_message(content=f"игрок: {selected_option}, являеться {list_mafia[channel_id]['players'][we.id]['роль']}", view=None)
                    else:
                        await interaction.response.edit_message(content=f"игрок: {selected_option}, являеться мирным игроком", view=None)
                    await doktor()
                      
                options = []

                for opt in list_mafia[channel_id]['players']:
                  opts = guild.get_member(opt)
                  options.append(discord.SelectOption(label=f"{opts}"))

                select = discord.ui.Select(
                            placeholder="выберите игрока",
                            min_values=1,
                            max_values=1,
                            options=options
                        )
                select.callback = menu_callback

                view = discord.ui.View(timeout=25)
                view.add_item(select)
                stop_event = asyncio.Event()

                async def timeout_callback():
                    try:
                        await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
                    except asyncio.TimeoutError:
                        await doktor()
                self.client.loop.create_task(timeout_callback()) 

                ol2 = guild.get_member(rol2)
                await ol2.send("выберите игрока для проверки", view=view)

              async def doktor():
                if rol3 is None:
                    await pytana()
                else:
                    if rol3 in list_mafia[channel_id]['players']:
                        pass
                    else:
                        await pytana()

                    await channe.send("доктор просипаеться")

                    async def menu_callback(interaction: discord.Interaction):
                        stop_event.set()
                        list_mafia[channel_id]['info']['док'] = interaction.data['values'][0]
                        await interaction.response.edit_message(content=f"вы выбрали {list_mafia[channel_id]['info']['док']}", view=None)
                        await pytana()
                            
                        
                    options = []

                    for opt in list_mafia[channel_id]['players']:
                        if list_mafia[channel_id]['info']['док'] is None:
                            pass
                        else:
                            dok = guild.get_member_named(list_mafia[channel_id]['info']['док'])
                            if opt == dok.id:
                                continue
                        opts = guild.get_member(opt)
                        options.append(discord.SelectOption(label=f"{opts}"))

                    select = discord.ui.Select(
                                placeholder="выберите игрока",
                                min_values=1,
                                max_values=1,
                                options=options
                            )
                    select.callback = menu_callback
                        
                    view = discord.ui.View(timeout=20)
                    view.add_item(select)
                    stop_event = asyncio.Event()

                    async def timeout_callback():
                        try:
                            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
                        except asyncio.TimeoutError:
                            list_mafia[channel_id]['info']['док'] = None
                            await pytana()
                    self.client.loop.create_task(timeout_callback()) 

                    ol3 = guild.get_member(rol3)
                    await ol3.send("выберите игрока для леченя", view=view)
                        
              async def pytana():
                if rol4 is None:
                    await manak()
                else:
                    if rol4 in list_mafia[channel_id]['players']:
                        pass
                    else:
                        await manak()

                    await channe.send("путана просипаеться")

                    async def menu_callback(interaction: discord.Interaction):
                        stop_event.set()
                        list_mafia[channel_id]['info']['путана'] = interaction.data['values'][0]
                        await interaction.response.edit_message(content=f"вы выбрали {list_mafia[channel_id]['info']['путана']}", view=None)
                        await manak()
                            
                        
                    options = []

                    for opt in list_mafia[channel_id]['players']:
                        if list_mafia[channel_id]['info']['путана'] is None:
                            pass
                        else:
                            dok = guild.get_member_named(list_mafia[channel_id]['info']['путана'])
                            if opt == dok.id:
                                continue
                        opts = guild.get_member(opt)
                        options.append(discord.SelectOption(label=f"{opts}"))

                    select = discord.ui.Select(
                                placeholder="выберите игрока",
                                min_values=1,
                                max_values=1,
                                options=options
                            )
                    select.callback = menu_callback
                        
                    view = discord.ui.View(timeout=20)
                    view.add_item(select)
                    stop_event = asyncio.Event()

                    async def timeout_callback():
                        try:
                            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
                        except asyncio.TimeoutError:
                            list_mafia[channel_id]['info']['путана'] = None
                            await manak()
                    self.client.loop.create_task(timeout_callback()) 

                    ol4 = guild.get_member(rol4)
                    await ol4.send("выберите игрока для ночьи", view=view)
              
              async def manak():
                if rol5 is None:
                    await don()
                else:
                    if rol5 in list_mafia[channel_id]['players']:
                        pass
                    else:
                        await don()

                    await channe.send("маньяк просипаеться")

                    async def menu_callback(interaction: discord.Interaction):
                        stop_event.set()
                        ma = interaction.data['values'][0]
                        if list_mafia[channel_id]['info']['док'] == ma or list_mafia[channel_id]['info']['путана'] == ma:
                            pass
                        else:
                            list_mafia[channel_id]['info']['маньяк'] = interaction.data['values'][0]
                        await interaction.response.edit_message(content=f"вы отправились ночю к участнику {ma}", view=None)
                        await don()
                        
                    options = []
                    

                    for opt in list_mafia[channel_id]['players']:
                        opts = guild.get_member(opt)
                        options.append(discord.SelectOption(label=f"{opts}"))

                    select = discord.ui.Select(
                                placeholder="выберите игрока",
                                min_values=1,
                                max_values=1,
                                options=options
                            )
                    select.callback = menu_callback
                        
                    view = discord.ui.View(timeout=20)
                    view.add_item(select)
                    stop_event = asyncio.Event()

                    async def timeout_callback():
                        try:
                            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
                        except asyncio.TimeoutError:
                            await don()
                    self.client.loop.create_task(timeout_callback()) 

                    ol5 = guild.get_member(rol5)
                    await ol5.send("выберите игрока", view=view)
                
              async def don():
                if rol6 is None:
                    await mafia()
                else:
                    if rol6 in list_mafia[channel_id]['players']:
                        pass
                    else:
                        await mafia()

                    await channe.send("дон просипаеться")

                    async def menu_callback(interaction: discord.Interaction):
                        stop_event.set()
                        selected_option = interaction.data['values'][0]
                        do = guild.get_member_named(interaction.data['values'][0])
                        if 'шериф' == list_mafia[channel_id]['players'][do.id]['роль']:
                            await interaction.response.edit_message(content=f"игрок: {selected_option}, являеться {list_mafia[channel_id]['players'][do.id]['роль']}", view=None)
                        else:
                            await interaction.response.edit_message(content=f"игрок: {selected_option}, не шериф", view=None)
                        await mafia()
                        
                    options = []

                    for opt in list_mafia[channel_id]['players']:
                        opts = guild.get_member(opt)
                        options.append(discord.SelectOption(label=f"{opts}"))

                    select = discord.ui.Select(
                                placeholder="выберите игрока",
                                min_values=1,
                                max_values=1,
                                options=options
                            )
                    select.callback = menu_callback
                        
                    view = discord.ui.View(timeout=20)
                    view.add_item(select)
                    stop_event = asyncio.Event()

                    async def timeout_callback():
                        try:
                            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
                        except asyncio.TimeoutError:
                            await mafia()
                    self.client.loop.create_task(timeout_callback()) 

                    ol6 = guild.get_member(rol6)
                    await ol6.send("выберите игрока", view=view)
              
              async def mafia():
                if rol1 is None and rol6 is None:
                    await noc()
                else:
                    if rol1 in list_mafia[channel_id]['players'] or rol10 in list_mafia[channel_id]['players'] or rol20 in list_mafia[channel_id]['players'] or rol6 in list_mafia[channel_id]['players']:
                        pass
                    else:
                        await noc()

                    await channe.send("мафия просипаеться")

                    async def menu_callback(interaction: discord.Interaction):
                        stop_event.set()
                        ma = guild.get_member_named(interaction.data['values'][0])
                        list_mafia[channel_id]['players'][ma.id]['гол'] += 1
                        list_mafia[channel_id]['info']['мафия1'] += 1
                        await interaction.response.edit_message(content=f"вы отправились ночю к участнику {ma}", view=None)
                        if list_mafia[channel_id]['info']['очки1'] == list_mafia[channel_id]['info']['мафия1']:
                            list_mafia[channel_id]['info']['мафия1'] = 0
                            await noc()
                        
                    options = []

                    for opt in list_mafia[channel_id]['players']:
                        opts = guild.get_member(opt)
                        options.append(discord.SelectOption(label=f"{opts}"))

                    select = discord.ui.Select(
                                placeholder="выберите игрока",
                                min_values=1,
                                max_values=1,
                                options=options
                            )
                    select.callback = menu_callback
                        
                    view = discord.ui.View(timeout=20)
                    view.add_item(select)
                    stop_event = asyncio.Event()

                    async def timeout_callback():
                        try:
                            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
                        except asyncio.TimeoutError:
                            stop_event.set()
                            await noc()
                    self.client.loop.create_task(timeout_callback()) 

                    for l in list_mafia[channel_id]['players']:
                        if list_mafia[channel_id]['players'][l]['роль'] == 'мафия' or list_mafia[channel_id]['players'][l]['роль'] == 'дон':
                            ol1 = guild.get_member(l)
                            await ol1.send("выберите игрока", view=view)

              if rol2 is None:
                await doktor()
              else:
                if rol2 in list_mafia[channel_id]['players']:
                    await weruf()
                else:
                    await doktor()

              async def noc():
                await channe.send("город просыпаеться")

                us = None
                point = 0
                for b in list_mafia[channel_id]['players']:
                    if list_mafia[channel_id]['players'][b]['гол'] > point:
                        point = list_mafia[channel_id]['players'][b]['гол']
                        us = b
                    list_mafia[channel_id]['players'][b]['гол'] = 0

                uss = guild.get_member(us)
                try:
                    kk = guild.get_member_named(list_mafia[channel_id]['info']['док'])
                except:
                    kk = None
                try:
                    kkk = guild.get_member_named(list_mafia[channel_id]['info']['путана'])
                except:
                    kkk = None
                
                if point == 0:
                    list_mafia[channel_id]['info']['мафия'] = None
                else:
                    print(kk, kkk, uss)
                    if kk == uss or kkk == uss:
                        list_mafia[channel_id]['info']['мафия'] = None
                    else:
                        list_mafia[channel_id]['info']['мафия'] = uss.id


                if list_mafia[channel_id]['info']['мафия'] is None and list_mafia[channel_id]['info']['маньяк'] is None:
                    await channe.send(f"ничю никто не умер")

                if list_mafia[channel_id]['info']['мафия'] is None:
                    pass
                else:
                    print(list_mafia[channel_id]['info']['мафия'])
                    deb = guild.get_member(list_mafia[channel_id]['info']['мафия'])
                    await channe.send(f"ночю был убит игрок {deb}:{list_mafia[channel_id]['players'][deb.id]['роль']}")
                    await channe.set_permissions(deb, send_messages=False, read_messages=False)
                    
                    if list_mafia[channel_id]['players'][deb.id]['роль'] == "маньяк":
                        list_mafia[channel_id]['info']['очки2'] -= 1

                    elif list_mafia[channel_id]['players'][deb.id]['роль'] == "мафия":
                        list_mafia[channel_id]['info']['очки1'] -= 1

                    elif list_mafia[channel_id]['players'][deb.id]['роль'] == "дон":
                        list_mafia[channel_id]['info']['очки1'] -= 1

                    else:
                        list_mafia[channel_id]['info']['user'] -= 1

                    del list_mafia[channel_id]['players'][deb.id]

                if list_mafia[channel_id]['info']['маньяк'] is None:
                    pass
                else:
                    deb = guild.get_member_named(list_mafia[channel_id]['info']['маньяк'])
                    await channe.send(f"ночю был убит игрок {deb}:{list_mafia[channel_id]['players'][deb.id]['роль']}")
                    await channe.set_permissions(deb, send_messages=False, read_messages=False)
                    
                    if list_mafia[channel_id]['players'][deb.id]['роль'] == "маньяк":
                        list_mafia[channel_id]['info']['очки2'] -= 1

                    elif list_mafia[channel_id]['players'][deb.id]['роль'] == "мафия":
                        list_mafia[channel_id]['info']['очки1'] -= 1

                    elif list_mafia[channel_id]['players'][deb.id]['роль'] == "дон":
                        list_mafia[channel_id]['info']['очки1'] -= 1

                    else:
                        list_mafia[channel_id]['info']['user'] -= 1
                    
                    del list_mafia[channel_id]['players'][deb.id]

                list_mafia[channel_id]['info']['day'] += 1
                list_mafia[channel_id]['info']['мафия'] = None
                list_mafia[channel_id]['info']['маньяк'] = None

                if list_mafia[channel_id]['info']['очки1'] == 0 and list_mafia[channel_id]['info']['очки2'] == 0:
                    await channe.send("мирных победа!")
                    del list_mafia[channel_id]
                    await channe.delete()
                    return
                
                if list_mafia[channel_id]['info']['user'] <= list_mafia[channel_id]['info']['очки2']:
                    await channe.send("маньяка победа!")
                    del list_mafia[channel_id]
                    await channe.delete()
                    return
                
                if list_mafia[channel_id]['info']['user'] <= list_mafia[channel_id]['info']['очки1']:
                    await channe.send("мафии победа!")
                    del list_mafia[channel_id]
                    await channe.delete()
                    return
                
                await game_play()
          await game_play()
              
          
      
      async def info(interaction: discord.Interaction):
          await interaction.response.send_message(tekst.mafia_info, ephemeral=True)

      start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
      button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
      add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

      start_button.callback = game_start
      add_pley_button.callback = add_player
      button_info.callback = info

      view = View(timeout=180)
      view.add_item(start_button)
      view.add_item(add_pley_button)
      view.add_item(button_info)
      stop_event = asyncio.Event()

      async def timeout_callback():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
        except asyncio.TimeoutError:
            try:
                del list_mafia[channel_id]
            except:
                pass
            
      self.client.loop.create_task(timeout_callback()) 

      start_button.disabled = True
      await interaction.response.send_message(tekst.mafia_game, view=view)

#######################################################

  @app_commands.command(name="buckshot_roulette", description="Buckshot roulette")
  async def Buckshot_roulette(self, interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Buckshot_roulette == False:
        await interaction.response.send_message(tekst.nots)
        return
    channe_id = interaction.channel_id

    def cartridg(coin):
        cartridge = ["🔴", "🔵"]
        
        for _ in range(0, coin):
            buskshot[channe_id]['info']['cartridge'] += random.choice(cartridge)
        
        def are_all_cartridges_same(cartridge_list):
            return all(item == cartridge_list[0] for item in cartridge_list)

        cartridges = buskshot[channe_id]['info']['cartridge']

        if are_all_cartridges_same(cartridges):
            if cartridges[0] == "🔴":
                cartridges.remove("🔴")
                cartridges.append("🔵")

            elif cartridges[0] == "🔵":
                cartridges.remove("🔵")
                cartridges.append("🔴")

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        
        player_1 = None
        player_2 = None
        for players in buskshot[channe_id]['players']:
            if player_1 is None:
                player_1 = players
            else:
                player_2 = players

        if buskshot[channe_id]['game'] == 3:
            buskshot[channe_id]['players'][player_1]['Мхп'] = 6
            buskshot[channe_id]['players'][player_1]['хп'] = 6
            buskshot[channe_id]['players'][player_2]['Мхп'] = 6
            buskshot[channe_id]['players'][player_2]['хп'] = 6
            buskshot[channe_id]['lyt'] = 3
            buskshot[channe_id]['game'] = 7

        elif buskshot[channe_id]['game'] == 2:
            buskshot[channe_id]['players'][player_1]['Мхп'] = 4
            buskshot[channe_id]['players'][player_1]['хп'] = 4
            buskshot[channe_id]['players'][player_2]['Мхп'] = 4
            buskshot[channe_id]['players'][player_2]['хп'] = 4
            buskshot[channe_id]['lyt'] = 2
            buskshot[channe_id]['game'] = 5

        elif buskshot[channe_id]['game'] == 1:
            buskshot[channe_id]['players'][player_1]['Мхп'] = 2
            buskshot[channe_id]['players'][player_1]['хп'] = 2
            buskshot[channe_id]['players'][player_2]['Мхп'] = 2
            buskshot[channe_id]['players'][player_2]['хп'] = 2
            buskshot[channe_id]['lyt'] = 1
            buskshot[channe_id]['game'] = 3

        cartridg(buskshot[channe_id]['game'])
        await interaction.response.edit_message(content=f"Игра началась!\nЗапомните патроны:\n{buskshot[channe_id]['info']['cartridge']}", view=None)
        await asyncio.sleep(3)
        await interaction.delete_original_response()
        
        list_lyt = ["лупа", "нож", "енергетик", "наручники", "сыгарета", "магазин", "таблетки", "инвертор"]

        for lyts in range(0, buskshot[channe_id]['lyt']):
            x = random.choice(list_lyt)
            if x in buskshot[channe_id]['players'][player_1]['item']:
                buskshot[channe_id]['players'][player_1][x] += 1
            else:
                buskshot[channe_id]['players'][player_1]['item'].append(x)
                buskshot[channe_id]['players'][player_1][x] += 1
        
        for lyts in range(0, buskshot[channe_id]['lyt']):
            x = random.choice(list_lyt)
            if x in buskshot[channe_id]['players'][player_2]['item']:
                buskshot[channe_id]['players'][player_2][x] += 1
            else:
                buskshot[channe_id]['players'][player_2]['item'].append(x)
                buskshot[channe_id]['players'][player_2][x] += 1

        async def game(player_1, player_2):
            buskshot[channe_id]['info']['x2'] = False
            if buskshot[channe_id]['info']['player'] is None:
                buskshot[channe_id]['info']['player'] = player_1

            if buskshot[channe_id]['players'][player_1]['хп'] == 0:
                await interaction.followup.send(f"игра окончена <@{player_2}> победил")
                del buskshot[channe_id]
                return

            elif buskshot[channe_id]['players'][player_2]['хп'] == 0:
                await interaction.followup.send(f"игра окончена <@{player_1}> победил")
                del buskshot[channe_id]
                return

            if buskshot[channe_id]['info']['cartridge'] == []:
                if buskshot[channe_id]['game'] == 3:
                    cartridg(random.randint(2, 4))

                elif buskshot[channe_id]['game'] == 5:
                    cartridg(random.randint(3, 6))

                elif buskshot[channe_id]['game'] == 7:
                    cartridg(random.randint(3, 8))
                

                bush = await interaction.followup.send(f"новая игра\n{buskshot[channe_id]['info']['cartridge']}")

                list_lyt = ["лупа", "нож", "енергетик", "наручники", "сыгарета", "магазин", "таблетки", "инвертор"]

                for lyts in range(0, buskshot[channe_id]['lyt']):
                    x = random.choice(list_lyt)
                    y = random.choice(list_lyt)
                    if x in buskshot[channe_id]['players'][player_1]['item']:
                        buskshot[channe_id]['players'][player_1][x] += 1
                    else:
                        buskshot[channe_id]['players'][player_1]['item'].append(x)
                        buskshot[channe_id]['players'][player_1][x] += 1

                    if y in buskshot[channe_id]['players'][player_2]['item']:
                        buskshot[channe_id]['players'][player_2][y] += 1
                    else:
                        buskshot[channe_id]['players'][player_2]['item'].append(y)
                        buskshot[channe_id]['players'][player_2][y] += 1

                await asyncio.sleep(3)
                await interaction.followup.delete_message(bush.id)
                

            buskshot[channe_id]['info']['cart'] = random.choice(buskshot[channe_id]['info']['cartridge'])

            async def attac(interaction: discord.Interaction):
                member = interaction.user.id
                if member == buskshot[channe_id]['info']['player']:
                    if buskshot[channe_id]['info']['cart'] == "🔴":
                        if buskshot[channe_id]['info']['x2'] == True:
                            if buskshot[channe_id]['players'][member]['хп'] == 1:
                                buskshot[channe_id]['players'][member]['хп'] -= 1
                                await interaction.response.edit_message(content="Патрон оказался настоящим, у вас -1 хп", view=None)
                            else:
                                buskshot[channe_id]['players'][member]['хп'] -= 2
                                await interaction.response.edit_message(content="Патрон оказался настоящим, у вас -2 хп", view=None)
                            buskshot[channe_id]['info']['x2'] = False
                        else:
                            buskshot[channe_id]['players'][member]['хп'] -= 1
                            await interaction.response.edit_message(content="Патрон оказался настоящим, у вас -1 хп", view=None)
                        if buskshot[channe_id]['info']['наручники'] == True:
                            buskshot[channe_id]['info']['наручники'] = False
                        else:
                            if buskshot[channe_id]['info']['player'] == player_1:
                                buskshot[channe_id]['info']['player'] = player_2
                            elif buskshot[channe_id]['info']['player'] == player_2:
                                buskshot[channe_id]['info']['player'] = player_1
                        buskshot[channe_id]['info']['cartridge'].remove("🔴")
                        await asyncio.sleep(3)
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await game(player_1, player_2)

                    elif buskshot[channe_id]['info']['cart'] == "🔵":
                        await interaction.response.edit_message(content="Ничего не произошло, продолжайте играть", view=None)
                        buskshot[channe_id]['info']['cartridge'].remove("🔵")
                        await asyncio.sleep(3)
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await game(player_1, player_2)

                else:
                    if member in buskshot[channe_id]['players']:
                        await interaction.response.send_message("ожидайте свой ход", ephemeral=True)
                    else:
                        await interaction.response.send_message("игра занятя, создайте свою игру", ephemeral=True)

            async def deffen(interaction: discord.Interaction):
                member = interaction.user.id
                if member == buskshot[channe_id]['info']['player']:
                    if member == player_1:
                        if buskshot[channe_id]['info']['cart'] == "🔴":
                            if buskshot[channe_id]['info']['x2'] == True:
                                if buskshot[channe_id]['players'][player_2]['хп'] == 1:
                                    buskshot[channe_id]['players'][player_2]['хп'] -= 1
                                    await interaction.response.edit_message(content="Выстрел прошёл успешно! Вы сняли игроку 1 хп", view=None)
                                else:
                                    buskshot[channe_id]['players'][player_2]['хп'] -= 2
                                    await interaction.response.edit_message(content="Выстрел прошёл успешно! Вы сняли игроку 2 хп", view=None)
                                buskshot[channe_id]['info']['x2'] = False
                            else:
                                buskshot[channe_id]['players'][player_2]['хп'] -= 1
                                await interaction.response.edit_message(content="Выстрел прошёл успешно! Вы сняли игроку 1 хп", view=None)
                            if buskshot[channe_id]['info']['наручники'] == True:
                                buskshot[channe_id]['info']['наручники'] = False
                            else:
                                buskshot[channe_id]['info']['player'] = player_2
                            buskshot[channe_id]['info']['cartridge'].remove("🔴")
                            await asyncio.sleep(3)
                            await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                            await game(player_1, player_2)

                        elif buskshot[channe_id]['info']['cart'] == "🔵":
                            await interaction.response.edit_message(content="Ничего не произошло", view=None)
                            buskshot[channe_id]['info']['cartridge'].remove("🔵")
                            if buskshot[channe_id]['info']['наручники'] == True:
                                buskshot[channe_id]['info']['наручники'] = False
                            else:
                                buskshot[channe_id]['info']['player'] = player_2
                            await asyncio.sleep(3)
                            await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                            await game(player_1, player_2)
                    
                    if member == player_2:
                        if buskshot[channe_id]['info']['cart'] == "🔴":
                            if buskshot[channe_id]['info']['x2'] == True:
                                if buskshot[channe_id]['players'][player_1]['хп'] == 1:
                                    buskshot[channe_id]['players'][player_1]['хп'] -= 1
                                    await interaction.response.edit_message(content="Выстрел прошёл успешно! Вы сняли игроку 1 хп", view=None)
                                else:
                                    buskshot[channe_id]['players'][player_1]['хп'] -= 2
                                    await interaction.response.edit_message(content="Выстрел прошёл успешно! Вы сняли игроку 2 хп", view=None)
                                buskshot[channe_id]['info']['x2'] = False
                            else:
                                buskshot[channe_id]['players'][player_1]['хп'] -= 1
                                await interaction.response.edit_message(content="Выстрел прошёл успешно! Вы сняли игроку 1 хп", view=None)
                            if buskshot[channe_id]['info']['наручники'] == True:
                                buskshot[channe_id]['info']['наручники'] = False
                            else:
                                buskshot[channe_id]['info']['player'] = player_1
                            buskshot[channe_id]['info']['cartridge'].remove("🔴")
                            await asyncio.sleep(3)
                            await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                            await game(player_1, player_2)

                        elif buskshot[channe_id]['info']['cart'] == "🔵":
                            await interaction.response.edit_message(content="Ничего не произошло", view=None)
                            buskshot[channe_id]['info']['cartridge'].remove("🔵")
                            if buskshot[channe_id]['info']['наручники'] == True:
                                buskshot[channe_id]['info']['наручники'] = False
                            else:
                                buskshot[channe_id]['info']['player'] = player_1
                            await asyncio.sleep(3)
                            await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                            await game(player_1, player_2)

                else:
                    if member in buskshot[channe_id]['players']:
                        await interaction.response.send_message("ожидайте свой ход", ephemeral=True)
                    else:
                        await interaction.response.send_message("игра занятя, создайте свою игру", ephemeral=True)


            async def item(interaction: discord.Interaction):
                member = interaction.user.id
                if member == buskshot[channe_id]['info']['player']:

                    if interaction.data['values'][0] == "лупа":
                        if buskshot[channe_id]['players'][member]['лупа'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        await interaction.response.send_message("пользователь использовал лупу")
                        await interaction.followup.send(f"Дробовик содержит {buskshot[channe_id]['info']['cart']} патрон", ephemeral=True)
                        buskshot[channe_id]['players'][member]['лупа'] -= 1
                        if buskshot[channe_id]['players'][member]['лупа'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("лупа")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await chat()
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()

                    elif interaction.data['values'][0] == "нож":
                        if buskshot[channe_id]['players'][member]['нож'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        if buskshot[channe_id]['info']['x2'] == True:
                            await interaction.response.send_message("вы уже использовали этот предмет", ephemeral=True)
                            return
                        buskshot[channe_id]['info']['x2'] = True
                        await interaction.response.send_message("пользователь использовал нож")
                        buskshot[channe_id]['players'][member]['нож'] -= 1
                        if buskshot[channe_id]['players'][member]['нож'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("нож")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await chat()
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()

                    elif interaction.data['values'][0] == "енергетик":
                        if buskshot[channe_id]['players'][member]['енергетик'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        await interaction.response.send_message(f"пользователь использовал енергетик\nИ тем же разрядил дробовик на {buskshot[channe_id]['info']['cart']} патрон")
                        buskshot[channe_id]['info']['cartridge'].remove(buskshot[channe_id]['info']['cart'])
                        buskshot[channe_id]['info']['cart'] = None
                        buskshot[channe_id]['players'][member]['енергетик'] -= 1
                        if buskshot[channe_id]['players'][member]['енергетик'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("енергетик")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await game(player_1, player_2)
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()

                    elif interaction.data['values'][0] == "наручники":
                        if buskshot[channe_id]['players'][member]['наручники'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        if buskshot[channe_id]['info']['наручники'] == True:
                            await interaction.response.send_message("вы уже использовали этот предмет", ephemeral=True)
                            return
                        buskshot[channe_id]['info']['наручники'] = True
                        await interaction.response.send_message("пользователь использовал нарушники")
                        buskshot[channe_id]['players'][member]['наручники'] -= 1
                        if buskshot[channe_id]['players'][member]['наручники'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("наручники")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await chat()
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()

                    elif interaction.data['values'][0] == "сыгарета":
                        if buskshot[channe_id]['players'][member]['сыгарета'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        await interaction.response.send_message("пользователь использовал сыгарету")
                        if buskshot[channe_id]['players'][member]['хп'] == buskshot[channe_id]['players'][member]['Мхп']:
                            pass
                        else:
                            buskshot[channe_id]['players'][member]['хп'] += 1
                        buskshot[channe_id]['players'][member]['сыгарета'] -= 1
                        if buskshot[channe_id]['players'][member]['сыгарета'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("сыгарета")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await chat()
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()

                    elif interaction.data['values'][0] == "магазин": 
                        if buskshot[channe_id]['players'][member]['магазин'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        await interaction.response.send_message("пользователь использовал магазин")
                        magaz = ["🔴", "🔵"]
                        magazs = random.choice(magaz)
                        buskshot[channe_id]['info']['cartridge'] += magazs
                        await interaction.followup.send(f"в магазине оказался {magazs} патрон", ephemeral=True)
                        buskshot[channe_id]['players'][member]['магазин'] -= 1
                        if buskshot[channe_id]['players'][member]['магазин'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("магазин")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await chat()
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()

                    elif interaction.data['values'][0] == "таблетки":
                        if buskshot[channe_id]['players'][member]['таблетки'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        await interaction.response.send_message("пользователь использовал таблетки")
                        z = random.choice(range(0, 3))
                        if z == 0 or z == 2:
                            buskshot[channe_id]['players'][member]['хп'] -= 1
                            if buskshot[channe_id]['players'][member]['хп'] == 0:
                                if member == player_1:
                                    await interaction.followup.send(f"игра окончена <@{player_2}> победил")
                                    del buskshot[channe_id]
                                    return
                                elif member == player_2:
                                    await interaction.followup.send(f"игра окончена <@{player_1}> победил")
                                    del buskshot[channe_id]
                                    return
                            buskshot[channe_id]['players'][member]['таблетки'] -= 1
                            if buskshot[channe_id]['players'][member]['таблетки'] == 0:
                                buskshot[channe_id]['players'][member]['item'].remove("таблетки")
                            await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                            await chat()
                            await asyncio.sleep(3)
                            await interaction.delete_original_response()

                        elif z == 1:
                            if buskshot[channe_id]['players'][member]['хп'] == buskshot[channe_id]['players'][member]['Мхп']:
                                pass
                            else:
                                buskshot[channe_id]['players'][member]['хп'] += 2
                                if buskshot[channe_id]['players'][member]['хп'] > buskshot[channe_id]['players'][member]['Мхп']:
                                    buskshot[channe_id]['players'][member]['хп'] -= 1
                                
                            buskshot[channe_id]['players'][member]['таблетки'] -= 1
                            if buskshot[channe_id]['players'][member]['таблетки'] == 0:
                                buskshot[channe_id]['players'][member]['item'].remove("таблетки")
                            await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                            await chat()
                            await asyncio.sleep(3)
                            await interaction.delete_original_response()

                    
                    elif interaction.data['values'][0] == "инвертор":
                        if buskshot[channe_id]['players'][member]['инвертор'] == 0:
                            await interaction.response.send_message("у вас закончился этот предмет", ephemeral=True)
                            return
                        await interaction.response.send_message("пользователь использовал инвертор")
                        if buskshot[channe_id]['info']['cart'] == "🔵":
                            buskshot[channe_id]['info']['cartridge'].remove(buskshot[channe_id]['info']['cart'])
                            buskshot[channe_id]['info']['cartridge'] += "🔴"
                            buskshot[channe_id]['info']['cart'] = "🔴"
                        
                        elif buskshot[channe_id]['info']['cart'] == "🔴":
                            buskshot[channe_id]['info']['cartridge'].remove(buskshot[channe_id]['info']['cart'])
                            buskshot[channe_id]['info']['cartridge'] += "🔵"
                            buskshot[channe_id]['info']['cart'] = "🔵"

                        buskshot[channe_id]['players'][member]['инвертор'] -= 1
                        if buskshot[channe_id]['players'][member]['инвертор'] == 0:
                            buskshot[channe_id]['players'][member]['item'].remove("инвертор")
                        await interaction.followup.delete_message(buskshot[channe_id]['info']['id'])
                        await chat()
                        await asyncio.sleep(3)
                        await interaction.delete_original_response()
                    

                else:
                    if member in buskshot[channe_id]['players']:
                        await interaction.response.send_message("ожидайте свой ход", ephemeral=True)
                    else:
                        await interaction.response.send_message("игра занятя, создайте свою игру", ephemeral=True)

            async def chat():

                button1 = Button(label="в себя", style=discord.ButtonStyle.red)
                button2 = Button(label="в игрока", style=discord.ButtonStyle.green)

                button1.callback = attac
                button2.callback = deffen

                view_game = View()
                view_game.add_item(button2)
                view_game.add_item(button1)

                if buskshot[channe_id]['players'][buskshot[channe_id]['info']['player']]['item'] == []:
                    pass
                else:
                    options = []
                    
                    for items in buskshot[channe_id]['players'][buskshot[channe_id]['info']['player']]['item']:
                        options.append(discord.SelectOption(label=f"{items}"))

                    select = discord.ui.Select(placeholder="выберите предмет", min_values=1, max_values=1, options=options)

                    select.callback = item

                    view_game.add_item(select)

                prebmet = None
                
                if buskshot[channe_id]['players'][buskshot[channe_id]['info']['player']]['item'] == []:
                    prebmet = "пусто"
                else:
                    prebmet = ""
                    for lyts in buskshot[channe_id]['players'][buskshot[channe_id]['info']['player']]['item']:
                        prebmet += f"{buskshot[channe_id]['players'][buskshot[channe_id]['info']['player']][lyts]} {lyts}\n"

                
                drobovuk = 1 if buskshot[channe_id]['info']['x2'] == False else 2
                xod = await interaction.followup.send(f"""
                                                      
| игрок <@{buskshot[channe_id]['info']['player']}> | ХП {buskshot[channe_id]['players'][buskshot[channe_id]['info']['player']]['хп']} | урон {drobovuk} |

предметы:
{prebmet}

""", view=view_game)
                
                buskshot[channe_id]['info']['id'] = xod.id
            await chat()



        await game(player_1, player_2)


    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in buskshot:
            if member in buskshot[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(buskshot[channe_id]['players']) == 2:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                buskshot[channe_id]['players'][member] = {"Мхп": 2, "хп": 2, "лупа": 0, "нож": 0, "енергетик": 0, "наручники": 0, "сыгарета": 0, "магазин": 0, "таблетки": 0, "инвертор": 0, "item": []}
                await interaction.response.send_message("вы вышли в комнату", ephemeral=True)
                start_button.disabled = False
                add_pley_button.disabled = True
                await interaction.followup.edit_message(content="Добро пожаловать в Buckshot Roulette создайте комнату, и после выберите режим игры и наслаждайтесь игрой\n2 игроков в комнате ожидания, пожалуста начните игру", message_id=interaction1, view=view)
        else:
            buskshot[channe_id] = {'players': {member: {"Мхп": None, "хп": None, "лупа": 0, "нож": 0, "енергетик": 0, "наручники": 0, "сыгарета": 0, "магазин": 0, "таблетки": 0, "инвертор": 0, "item": []}}, 'info': {"cartridge": [], "cart": None, "player": None, "id": None, "x2": False, "наручники": False}, 'game': None, 'lyt': None}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            view.add_item(selec)
            await interaction.followup.edit_message(content="Добро пожаловать в Buckshot Roulette создайте комнату, и после выберите режим игры и наслаждайтесь игрой\n1 игрок в комнате ожидания", message_id=interaction1, view=view)

    async def info(interaction: discord.Interaction):

        async def info_menu(interaction: discord.Interaction):
            if interaction.data['values'][0] == "лупа":
                await interaction.response.send_message(tekst.buckshot_roulette_1, ephemeral=True)
            elif interaction.data['values'][0] == "нож":
                await interaction.response.send_message(tekst.buckshot_roulette_2, ephemeral=True)
            elif interaction.data['values'][0] == "енергетик":
                await interaction.response.send_message(tekst.buckshot_roulette_3, ephemeral=True)
            elif interaction.data['values'][0] == "наручники":
                await interaction.response.send_message(tekst.buckshot_roulette_4, ephemeral=True)
            elif interaction.data['values'][0] == "сыгарета":
                await interaction.response.send_message(tekst.buckshot_roulette_5, ephemeral=True)
            elif interaction.data['values'][0] == "магазин":
                await interaction.response.send_message(tekst.buckshot_roulette_6, ephemeral=True)
            elif interaction.data['values'][0] == "таблетки":
                await interaction.response.send_message(tekst.buckshot_roulette_7, ephemeral=True)
            elif interaction.data['values'][0] == "инвертор":
                await interaction.response.send_message(tekst.buckshot_roulette_8, ephemeral=True)
            

        options_info = [
        discord.SelectOption(label="лупа"),
        discord.SelectOption(label="нож"),
        discord.SelectOption(label="енергетик"),
        discord.SelectOption(label="наручники"),
        discord.SelectOption(label="сыгарета"),
        discord.SelectOption(label="магазин"),
        discord.SelectOption(label="таблетки"),
        discord.SelectOption(label="инвертор")
    ]
        infoo = discord.ui.Select(placeholder="выберите предмет", min_values=1, max_values=1, options=options_info)
        infoo.callback = info_menu

        view_info = View()
        view_info.add_item(infoo)

        await interaction.response.send_message(tekst.buckshot_roulette, ephemeral=True, view=view_info)

    async def menu(interaction: discord.Interaction):
        if interaction.data['values'][0] == "легкий":
            buskshot[channe_id]['game'] = 1

        elif interaction.data['values'][0] == "средьный":
            buskshot[channe_id]['game'] = 2

        elif interaction.data['values'][0] == "тяжелый":
            buskshot[channe_id]['game'] = 3
        await interaction.response.send_message(f"Вы выбрали {interaction.data['values'][0]}")
        await asyncio.sleep(2)
        await interaction.delete_original_response()

    options_menu = [
        discord.SelectOption(label="легкий"),
        discord.SelectOption(label="средьный"),
        discord.SelectOption(label="тяжелый")
    ]

    start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
    button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
    add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)
    selec = discord.ui.Select(placeholder="выберите сложность", min_values=1, max_values=1, options=options_menu)

    start_button.callback = game_start
    add_pley_button.callback = add_player
    button_info.callback = info
    selec.callback = menu

    view = View(timeout=180)
    view.add_item(start_button)
    view.add_item(add_pley_button)
    view.add_item(button_info)
    stop_event = asyncio.Event()

    async def timeout_callback():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
        except asyncio.TimeoutError:
            try:
                del buskshot[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Добро пожаловать в Buckshot Roulette\nсоздайте комнату, и после выберите режим игры и наслаждайтесь игрой", view=view)

###########################################################

  @app_commands.command(name="ведьма", description="Карточная игра Ведьма")
  async def witch(self, interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.witch == False:
        await interaction.response.send_message(tekst.nots)
        return
    channe_id = interaction.channel_id

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(witch[channe_id]['players'].keys())
        player_1 = keys[0] if len(keys) > 0 else None
        player_2 = keys[1] if len(keys) > 1 else None
        player_3 = keys[2] if len(keys) > 2 else None
        player_4 = keys[3] if len(keys) > 3 else None
        player_5 = keys[4] if len(keys) > 4 else None

        player_0 = [player_1, player_2, player_3, player_4, player_5]
        playerss = []

        for player in player_0:
            if player is None:
                continue
            else:
                playerss.append(player)

        witch[channe_id]['info']['player'] = playerss

        karts = ["7♥️", "8♥️", "9♥️", "🔟♥️", "🇯♥️", "🇶♥️", "🇰♥️", "🇦♥️",
                "7♦️", "8♦️", "9♦️", "🔟♦️", "🇯♦️", "🇶♦️", "🇰♦️", "🇦♦️",
                "7♠️", "8♠️", "9♠️", "🔟♠️", "🇯♠️", "🇶♠️", "🇰♠️", "🇦♠️",
                "7♣️", "8♣️", "9♣️", "🔟♣️", "🇯♣️", "🇰♣️", "🇦♣️"]

        if len(witch[channe_id]['players']) > 3:
            karts = ["2♥️", "3♥️", "4♥️", "5♥️", "6♥️", "7♥️", "8♥️", "9♥️", "🔟♥️", "🇯♥️", "🇶♥️", "🇰♥️", "🇦♥️",
                "2♦️", "3♦️", "4♦️", "5♦️", "6♦️", "7♦️", "8♦️", "9♦️", "🔟♦️", "🇯♦️", "🇶♦️", "🇰♦️", "🇦♦️",
                "2♠️", "3♠️", "4♠️", "5♠️", "6♠️", "7♠️", "8♠️", "9♠️", "🔟♠️", "🇯♠️", "🇶♠️", "🇰♠️", "🇦♠️",
                "2♣️", "3♣️", "4♣️", "5♣️", "6♣️", "7♣️", "8♣️", "9♣️", "🔟♣️", "🇯♣️", "🇰♣️", "🇦♣️"]
        
        while True:
            for players in playerss:
                if karts == []:
                    break
                kart = random.choice(karts)
                my_list = []
                my_list.extend(list(kart))
                my1 = my_list[0]
                my2 = my_list[1]
                if kart == "🇶♠️":
                    witch[channe_id]['players'][players]['карты']["♠️"] = "🇶"
                    karts.remove(kart)
                    continue
                
                if my1 == "8":
                    my1 = "2️⃣"
                elif my1 == "9":
                    my1 = "3️⃣"
                elif my1 == "7":
                    my1 = "4️⃣"
                elif my1 == "8":
                    my1 = "5️⃣"
                elif my1 == "9":
                    my1 = "6️⃣"
                elif my1 == "7":
                    my1 = "7️⃣"
                elif my1 == "8":
                    my1 = "8️⃣"
                elif my1 == "9":
                    my1 = "9️⃣"
                
                if my1 in witch[channe_id]['players'][players]['карты']:
                    del witch[channe_id]['players'][players]['карты'][my1]
                else:
                    witch[channe_id]['players'][players]['карты'][my1] = my2
                karts.remove(kart)
            if karts == []:
                break

        print(f"""<@{player_1}> карты:\n
{witch[channe_id]['players'][player_1]['карты']}
<@{player_2}> карты:
{witch[channe_id]['players'][player_2]['карты']}
""")

        async def chatt(coin):

            try:
                for play in witch[channe_id]['players']:
                    if witch[channe_id]['players'][play]['карты'] == {}:
                        
                        del witch[channe_id]['players'][play]
                        await interaction.followup.send(f"у игрока <@{play}> закончились карты")
                        
            except:
                
                pass

            
            if len(witch[channe_id]['players']) == 1:
                ke = list(witch[channe_id]['players'].keys())
                await interaction.followup.send(f"игрок <@{ke[0]}> стал ведьмой, игра закончилась")
                del witch[channe_id]
                return
            
        
            async def chat(interaction: discord.Interaction):
                keys1 = list(witch[channe_id]['players'].keys())

                if interaction.user.id in witch[channe_id]['players']:
                    pass
                else:
                    await interaction.response.send_message("вы не участник или больше не участвуете в игре", ephemeral=True)
                    return
                
                async def kart(interaction: discord.Interaction):
                    if interaction.user.id == witch[channe_id]['info']['player'][0]:
                        pass
                    else:
                        await interaction.response.send_message("ожидайте свой ход", ephemeral=True)
                        return
                    
                    user = None
                    try:
                        key = list(witch[channe_id]['players'][witch[channe_id]['info']['player'][1]]['карты'].keys())
                        user = witch[channe_id]['players'][witch[channe_id]['info']['player'][1]]['карты']
                    except:
                        key = list(witch[channe_id]['players'][keys1[0]]['карты'].keys())
                        user = witch[channe_id]['players'][keys1[0]]['карты']

                    key_key = int(interaction.data['values'][0])
                    if key[key_key - 1] in witch[channe_id]['players'][interaction.user.id]['карты']:
                        del witch[channe_id]['players'][interaction.user.id]['карты'][key[key_key - 1]]
                        try:
                            await interaction.response.edit_message(content=f"Вы вытянули {key[key_key - 1]}|{user[key[key_key - 1]]} карту\nУ вас оказалась пара из {key[key_key - 1]} и автоматически скинута", view=None)
                        except:
                            pass
                    else:
                        witch[channe_id]['players'][interaction.user.id]['карты'][key[key_key - 1]] = user[key[key_key - 1]]
                        try:
                            await interaction.response.edit_message(content=f"Вы вытянули {key[key_key - 1]}|{user[key[key_key - 1]]} карту", view=None)
                        except:
                            pass
                    
                    del user[key[key_key - 1]]
                    
                    witch[channe_id]['info']['player'].remove(witch[channe_id]['info']['player'][0])
                    if witch[channe_id]['info']['player'] == []:
                        playerss = []

                        for player in player_0:
                            if player is None:
                                continue
                            else:
                                playerss.append(player)

                        witch[channe_id]['info']['player'] = playerss

                    op = await interaction.followup.send(f"игрок {interaction.user} сделал свой ход")
                    try:
                        await interaction.followup.delete_message(witch[channe_id]['info']['id'])
                    except:
                        pass
                    await asyncio.sleep(3)
                    await interaction.followup.delete_message(op.id)
                    await chatt(0)
                
                options = []

                try:
                    option = witch[channe_id]['info']['player'][1]
                except:
                    option = keys1[0]

                for opt in range(len(witch[channe_id]['players'][option]['карты'])):
                    opt += 1
                    options.append(discord.SelectOption(emoji="🃏", label=f"{opt}"))

                select = discord.ui.Select(
            placeholder="выберите карту",
            min_values=1,
            max_values=1,
            options=options
                                )
                select.callback = kart

                view = View()
                view.add_item(select)

                player_kart = ""
                coced = witch[channe_id]['info']['player'][1] if len(witch[channe_id]['info']['player']) == 0 else player_1
                
                if interaction.user.id == witch[channe_id]['info']['player'][0]:
                    for key in witch[channe_id]['players'][witch[channe_id]['info']['player'][0]]['карты']:
                        if key == "♠️":
                            player_kart += f"╠{witch[channe_id]['players'][witch[channe_id]['info']['player'][0]]['карты'][key]}|{key}\n"
                            continue
                        player_kart += f"╠{key}|{witch[channe_id]['players'][witch[channe_id]['info']['player'][0]]['карты'][key]}\n"
                
                    await interaction.response.send_message(f"""
---|<@{witch[channe_id]['info']['player'][0]}>|---

-|карт({len(witch[channe_id]['players'][witch[channe_id]['info']['player'][0]]['карты'])})|-                                           
╔=-----
{player_kart}╚=-----

-|"Возьмите" карту у соседа <@{coced}>|-
""", ephemeral=True, view=view)
    
                else:

                    for key in witch[channe_id]['players'][interaction.user.id]['карты']:
                        if key == "♠️":
                            player_kart += f"╠{witch[channe_id]['players'][interaction.user.id]['карты'][key]}|{key}\n"
                            continue
                        player_kart += f"╠{key}|{witch[channe_id]['players'][interaction.user.id]['карты'][key]}\n"
                
                    await interaction.response.send_message(f"""
---|<@{interaction.user.id}>|---

-|карт({len(witch[channe_id]['players'][interaction.user.id]['карты'])})|-                                           
╔=-----
{player_kart}╚=-----
""", ephemeral=True)
        

            button_menu = Button(emoji="🃏", style=discord.ButtonStyle.blurple)

            button_menu.callback = chat

            view_menu = View()
            view_menu.add_item(button_menu)

            if coin == 1:
                await interaction.response.edit_message(content="Игра началась, удачной игры!", view=None)
                id = await interaction.followup.send(content=f"Первый ход делает пользователь: <@{player_1}>\nВ 🃏 можно посмотреть как свои карты так и взять карту у соседа, в случае если ваш ход.", view=view_menu)
                witch[channe_id]['info']['id'] = id.id
                
            else:
                id = await interaction.followup.send(f"Игрок <@{witch[channe_id]['info']['player'][0]}> ваш ход", view=view_menu)
                witch[channe_id]['info']['id'] = id.id
        await chatt(1)

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in witch:
            if member in witch[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(witch[channe_id]['players']) > 4:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                witch[channe_id]['players'][member] = {"карты": {}}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                if len(witch[channe_id]['players']) == 5:
                    add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Добро пожаловать в 'Ведьма'\nЭто много пользовательская карточная игра в котом вам предстоит НЕ остаться Ведьмой\nВ ожидании: {len(witch[channe_id]['players'])} игрок", message_id=interaction1, view=view)
        else:
            witch[channe_id] = {'players': {member: {"карты": {}}}, "info": {"player": None, "id": None}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Добро пожаловать в 'Ведьма'\nЭто много пользовательская карточная игра в котом вам предстоит НЕ остаться Ведьмой\nВ ожидании: 1 игрок", message_id=interaction1, view=view)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(tekst.witch, ephemeral=True)
    
    start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
    button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
    add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

    start_button.callback = game_start
    add_pley_button.callback = add_player
    button_info.callback = info

    view = View(timeout=180)
    view.add_item(start_button)
    view.add_item(add_pley_button)
    view.add_item(button_info)
    stop_event = asyncio.Event()

    async def timeout_callback():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
        except asyncio.TimeoutError:
            try:
                del witch[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Добро пожаловать в 'Ведьма'\nЭто много пользовательская карточная игра в котом вам предстоит НЕ остаться Ведьмой", view=view)

  @app_commands.command(name="викторина", description="Вопросы викторины на различные темы.")
  async def Trivia_Quiz(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Trivia_Quiz == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    async def game_start(interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
        await interaction.delete_original_response()
        keys = list(Trivia[channe_id]['players'].keys())
        player_1 = keys[0]
        player_2 = keys[1]

        Trivia[channe_id]['info']['вопрос'] = random.choice(list(Quix.text))
        Trivia[channe_id]['info']['ответ'] = Quix.text[Trivia[channe_id]['info']['вопрос']]

        id = await interaction.followup.send("Ожидание..")
        Trivia[channe_id]['info']['id'] = id.id

        async def new_lvl():
            await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                   Викторина 
                      ═──────⊱⋆⊰─────═
                                      уровень {Trivia[channe_id]['info']['lvl']} 

- <@{player_1}>: {Trivia[channe_id]['players'][player_1]['point']} | ответ: {Trivia[channe_id]['players'][player_1]['ответ']}                    
- <@{player_2}>: {Trivia[channe_id]['players'][player_2]['point']} | ответ: {Trivia[channe_id]['players'][player_2]['ответ']}      

╔═━────═──────⊱⋆⊰─────═─────━═╗
                        Правильный ответ - {Trivia[channe_id]['info']['ответ']}
╚═━────═──────⊱⋆⊰─────═─────━═╝
всем кто ответил правильно получают +1
""", view=None)
            
            for game_out in Trivia[channe_id]['players']:
                Trivia[channe_id]['players'][game_out]['ход'] = False
                if str(Trivia[channe_id]['players'][game_out]['ответ']) == str(Trivia[channe_id]['info']['ответ']):
                    Trivia[channe_id]['players'][game_out]['point'] += 1

                if Trivia[channe_id]['players'][player_1]['point'] == 3 and Trivia[channe_id]['players'][player_2]['point'] == 3:
                    await asyncio.sleep(6)
                    await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                 Викторина 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
                    победитель - ничья
╚═━────═──────⊱⋆⊰─────═─────━═╝
""")
                    del Trivia[channe_id]
                    return

                if Trivia[channe_id]['players'][game_out]['point'] == 3:
                    await asyncio.sleep(6)
                    await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                 Викторина 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
                    победитель - <@{game_out}>
╚═━────═──────⊱⋆⊰─────═─────━═╝
""")
                    del Trivia[channe_id]
                    return
            
            Trivia[channe_id]['info']['lvl'] += 1
            Trivia[channe_id]['info']['вопрос'] = random.choice(list(Quix.text))
            Trivia[channe_id]['info']['ответ'] = Quix.text[Trivia[channe_id]['info']['вопрос']]
            await asyncio.sleep(10)
            await chat()

        async def chat():
            async def game(interaction: discord.Interaction):

                if Trivia[channe_id]['players'][interaction.user.id]['ход'] == True:
                    await interaction.response.send_message(f":x: | вы уже сделали свой выбор, ожидайте другого игрока", ephemeral=True)
                    return
                
                if interaction.user.id in Trivia[channe_id]['players']:
                    pass
                else:
                    await interaction.response.send_message(f":x: | к этой игре нельзя больше присоединиться", ephemeral=True)
                    return

                key = interaction.data['custom_id']
                Trivia[channe_id]['players'][interaction.user.id]['ответ'] = key
                Trivia[channe_id]['players'][interaction.user.id]['ход'] = True

                if Trivia[channe_id]['players'][player_1]['ход'] == True and Trivia[channe_id]['players'][player_2]['ход'] == True:
                    await new_lvl()
                else:
                    await chat()
                
            buttonA = Button(emoji=f"🇦", style=discord.ButtonStyle.blurple, custom_id="А")
            buttonB = Button(emoji=f"🇧", style=discord.ButtonStyle.blurple, custom_id="В")
            buttonC = Button(emoji=f"🇨", style=discord.ButtonStyle.blurple, custom_id="С")

            buttonA.callback = game
            buttonB.callback = game
            buttonC.callback = game

            view = View(timeout=180)
            view.add_item(buttonA)
            view.add_item(buttonB)
            view.add_item(buttonC)

            xod1 = "*В ожидании*" if Trivia[channe_id]['players'][player_1]['ход'] == True else " "
            xod2 = "*В ожидании*" if Trivia[channe_id]['players'][player_2]['ход'] == True else " "
            
            
            await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                  Викторина 
                      ═──────⊱⋆⊰─────═
                                     уровень {Trivia[channe_id]['info']['lvl']} 

- <@{player_1}>: {Trivia[channe_id]['players'][player_1]['point']} Очков | {xod1}                     
- <@{player_2}>: {Trivia[channe_id]['players'][player_2]['point']} Очков | {xod2}       

╔═━────═──────⊱⋆⊰─────═─────━═╗                                             
{Trivia[channe_id]['info']['вопрос']}
╚═━────═──────⊱⋆⊰─────═─────━═╝
""", view=view)
        
        await asyncio.sleep(5)
        await chat()

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in Trivia:
            if member in Trivia[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(Trivia[channe_id]['players']) > 1:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                Trivia[channe_id]['players'][member] = {"point": 0, "ход": False, "ответ": None}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Добро пожаловать в викторину.\nПроверьте себя насколько вы умны\n2 Игроков в ожидании", message_id=interaction1, view=view)
        else:
            Trivia[channe_id] = {'players': {member: {"point": 0, "ход": False, "ответ": None}}, "info": {"вопрос": None, "ответ": None, "id": None, "lvl": 1}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Добро пожаловать в викторину.\nПроверьте себя насколько вы умны\n1 Игрок в ожидании", message_id=interaction1)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)

    start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
    button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
    add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

    start_button.callback = game_start
    add_pley_button.callback = add_player
    button_info.callback = info

    view = View(timeout=180)
    view.add_item(start_button)
    view.add_item(add_pley_button)
    view.add_item(button_info)
    stop_event = asyncio.Event()

    async def timeout_callback():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
        except asyncio.TimeoutError:
            try:
                del Trivia[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Добро пожаловать в викторину.\nПроверьте себя насколько вы умны", view=view)


  @app_commands.command(name="угадай_число", description="Игра на угадывание числа, загаданного ботом.")
  async def Guess_the_Number(self, interaction: discord.Interaction):
    
    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Trivia_Quiz == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    async def game_start(interaction: discord.Interaction):
        pass

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in Trivia:
            if member in Trivia[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(Trivia[channe_id]['players']) > 1:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                Trivia[channe_id]['players'][member] = {"point": 0}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"3", message_id=interaction1, view=view)
        else:
            Trivia[channe_id] = {'players': {member: {"point": 0}}, "info": {"player": None, "id": None}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="2", message_id=interaction1)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)

    start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
    button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
    add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

    start_button.callback = game_start
    add_pley_button.callback = add_player
    button_info.callback = info

    view = View(timeout=180)
    view.add_item(start_button)
    view.add_item(add_pley_button)
    view.add_item(button_info)
    stop_event = asyncio.Event()

    async def timeout_callback():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
        except asyncio.TimeoutError:
            try:
                del Trivia[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("1", view=view)

  @app_commands.command(name="виселица", description="игра, где нужно угадать слово по буквам.")
  async def Hangman(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Trivia_Quiz == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    async def game_start(interaction: discord.Interaction):
        pass

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in Trivia:
            if member in Trivia[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(Trivia[channe_id]['players']) > 1:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                Trivia[channe_id]['players'][member] = {"point": 0}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"3", message_id=interaction1, view=view)
        else:
            Trivia[channe_id] = {'players': {member: {"point": 0}}, "info": {"player": None, "id": None}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="2", message_id=interaction1)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message("test", ephemeral=True)

    start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
    button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
    add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

    start_button.callback = game_start
    add_pley_button.callback = add_player
    button_info.callback = info

    view = View(timeout=180)
    view.add_item(start_button)
    view.add_item(add_pley_button)
    view.add_item(button_info)
    stop_event = asyncio.Event()

    async def timeout_callback():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
        except asyncio.TimeoutError:
            try:
                del Trivia[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("1", view=view)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(fun(client))
