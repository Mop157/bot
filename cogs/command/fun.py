import random, json, asyncio, re

import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
import config
import cogs.text.tekst as tekst
import cogs.Button.Button as button
import cogs.text.Trivia_Quix_text as Quix
import cogs.text.Hangman_text as Hangman
import cogs.text.truth_or_lie_text as Truth_or_lie
import cogs.text.Anagrams as Anagrams
import cogs.text.Role_playing_text as Role_play

list_rps = {}
list_mafia = {}
buskshot = {}
witch = {}
Trivia = {}
Guess_the_Number = {}
hangman = {}
truth_or_lie = {}
anagrams = {}
role_playing = {}
puzzle = {}

class fun(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client
    self.prefix = config.prefix

#######################################################
########## камень, ножничи, бумага ####################
#######################################################

  @app_commands.command(name="rps", description="Камень, ножницы, бумага")
  async def rps(self, interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return

    if config.rps == False:
        await interaction.response.send_message(tekst.nots)
        return

    button_rps_bot = Button(emoji=f"🤖", style=discord.ButtonStyle.blurple, custom_id="button_rps1")
    button_rps_user = Button(emoji=f"👥", style=discord.ButtonStyle.blurple, custom_id="button_rps2")
    button_rps_info = Button(emoji=f"❓", style=discord.ButtonStyle.green, custom_id="button_rps3")
    button_rps_paper = Button(emoji=f"📄", style=discord.ButtonStyle.gray, custom_id="бумага")
    button_rps_kamen = Button(emoji=f"⛰️", style=discord.ButtonStyle.gray, custom_id="камень")
    button_rps_noznuci = Button(emoji=f"✂️", style=discord.ButtonStyle.gray, custom_id="ножницы")

    view_game = discord.ui.View()
    view_game.add_item(button_rps_bot)
    view_game.add_item(button_rps_user)
    view_game.add_item(button_rps_info)

    async def button_callback_rps_bot(interaction: discord.Interaction):
        async def game(interaction: discord.Interaction):
            choices = ['камень', 'ножницы', 'бумага']
            user = interaction.data['custom_id']
            stop_event3.set()

            bot_choice = random.choice(choices)
            final = None

            if user == bot_choice:                    
                final = ">-⸩ НИЧЬЯ ⸨-<"
            elif (user == 'камень' and bot_choice == 'ножницы') or \
                 (user == 'ножницы' and bot_choice == 'бумага') or \
                 (user == 'бумага' and bot_choice == 'камень'):
                final = ">-⸩ Вы выиграли! ⸨-<"
            else:
                final = ">-⸩ Я выиграл! ⸨-<"

            await interaction.response.edit_message(content=f"""
=[]=-~-+·༒⟮⟯༺༻⟮⟯༒·+-~-=[]=
      +(GameWiz)=-0-=({interaction.user})+
  >-⸩ {bot_choice} ⸨-<*>-⸩ {user} ⸨-<

⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
            {final}
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
""", view=None)
        
        button_rps_paper.callback = game
        button_rps_kamen.callback = game
        button_rps_noznuci.callback = game

        view_bot = discord.ui.View(timeout=60)
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

    async def button_callback_rps_user(interaction: discord.Interaction):
        channel_id = interaction.channel.id
        if channel_id in list_rps:
            await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
            return
        
        async def play_add(interaction: discord.Interaction):
            member = interaction.user.id
            if channel_id in list_rps:
                if interaction.user.id in list_rps[channel_id]['players']:
                    await interaction.response.send_message(content=tekst.rps_error_user1, ephemeral=True)
                    return

                if len(list_rps[channel_id]['players']) == 1:
                    list_rps[channel_id]['players'][member] = {"xod": None, "out": False}
                    button_rps_add.disabled = True
                    button_rps_play.disabled = False
                else:
                    await interaction.response.send_message(content=tekst.rps_error_user2, ephemeral=True)
                    return  
            else:
                list_rps[channel_id] = {'players': {member: {"xod": None, "out": False}}}

            await interaction.response.edit_message(content=f"С кем бы вы хотели сыграть?\nигроков {len(list_rps[channel_id]['players'])}/2\n", view=view_game_user)

        async def play(interaction: discord.Interaction):
            keys = list(list_rps[channel_id]['players'].keys())

            if interaction.user.id == keys[0]:
                    pass
            else:
                    await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
                    return

            async def games(interaction: discord.Interaction):
                stop_event2.set()
                if interaction.user.id not in list_rps[channel_id]['players']:
                    await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
                    return
                
                if list_rps[channel_id]['players'][interaction.user.id]['out'] == True:
                    await interaction.response.send_message(tekst.rps_error_user3, ephemeral=True)
                    return
                
                list_rps[channel_id]['players'][interaction.user.id]['xod'] = interaction.data['custom_id']
                list_rps[channel_id]['players'][interaction.user.id]['out'] = True

                if list_rps[channel_id]['players'][keys[0]]['out'] == True and list_rps[channel_id]['players'][keys[1]]['out'] == True:
                    player_1 = list_rps[channel_id]['players'][keys[0]]['xod']
                    player_2 = list_rps[channel_id]['players'][keys[1]]['xod']
                    final = None

                    if player_1 == player_2:                    
                        final = ">-⸩ Выиграл! | НИЧЬЯ ⸨-<"
                    elif (player_1 == 'камень' and player_2 == 'ножницы') or \
                        (player_1 == 'ножницы' and player_2 == 'бумага') or \
                        (player_1 == 'бумага' and player_2 == 'камень'):
                        final = f">-⸩ Выиграл! | <@{keys[0]}> ⸨-<"
                    else:
                        final = f">-⸩ Выиграл! | <@{keys[1]}> ⸨-<"        

                    await interaction.response.edit_message(content=f"""
=[]=-~-+·༒⟮⟯༺༻⟮⟯༒·+-~-=[]=
      +(<@{keys[0]}>)=-0-=(<@{keys[1]}>)+
  >-⸩ {player_1} ⸨-<*>-⸩ {player_2} ⸨-<
  
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
    {final}
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
""", view=None)
                    del list_rps[channel_id]
                    return
                else:
                    player_1 = "*пусто*" if list_rps[channel_id]['players'][keys[0]]['out'] == False else "*в ожидание*"
                    player_2 = "*пусто*" if list_rps[channel_id]['players'][keys[1]]['out'] == False else "*в ожидание*"
                    await interaction.response.edit_message(content=f"""
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
+(<@{keys[0]}>)=-0-=(<@{keys[1]}>)+
>-⸩ {player_1} ⸨-<*>-⸩ {player_2} ⸨-<
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
""")

            button_rps_kamen.callback = games
            button_rps_noznuci.callback = games
            button_rps_paper.callback = games

            view_user = discord.ui.View(timeout=60)
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

            player_1 = "*пусто*" if list_rps[channel_id]['players'][keys[0]]['out'] == False else "*в ожидание*"
            player_2 = "*пусто*" if list_rps[channel_id]['players'][keys[1]]['out'] == False else "*в ожидание*"
            await interaction.response.edit_message(content=f"""
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
+(<@{keys[0]}>)=-0-=(<@{keys[1]}>)+
>-⸩ {player_1} ⸨-<*>-⸩ {player_2} ⸨-<
⸨⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⹈꧁꧂⹈⹆⹈⹅⹇⹅⹇⹅⹇⹅⹇⹅⹈⹆⸩
""", view=view_user)
            
                    
        button_rps_add = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)
        button_rps_play = Button(emoji="▶️", style=discord.ButtonStyle.green)

        button_rps_play.callback = play
        button_rps_add.callback = play_add

        view_game_user = discord.ui.View(timeout=60)
        view_game_user.add_item(button_rps_play)
        view_game_user.add_item(button_rps_add)
        view_game_user.add_item(button_rps_info)

        channel_id = interaction.channel_id
        member = interaction.user.id
        stop_event1 = asyncio.Event()

        async def timeout1_callback():
            try:
                await asyncio.wait_for(stop_event1.wait(), timeout=view_game_user.timeout)
            except asyncio.TimeoutError:
                try:
                    del list_rps[channel_id]
                    return
                except KeyError:
                    return
        self.client.loop.create_task(timeout1_callback())

        button_rps_play.disabled = True
        await interaction.response.edit_message(content=f"Создайте комнату и ожидайте игроков", view=view_game_user)

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
    ########## мафия ####################
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

      if channel_id in list_mafia:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

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

          if interaction.user.id == keys[0]:
                pass
          else:
                await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
                return
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
    ########## блэк шот рулет ####################
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

    if channe_id in buskshot:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

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
        keys55 = list(buskshot[channe_id]['players'].keys())

        if interaction.user.id == keys55[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return
        
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

                view_game = View(timeout=None)
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

#######################################################
    ########## ведьма ####################
#######################################################

  @app_commands.command(name="ведьма", description="Карточная игра Ведьма")
  async def witch(self, interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.witch == False:
        await interaction.response.send_message(tekst.nots)
        return
    channe_id = interaction.channel_id

    if channe_id in witch:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(witch[channe_id]['players'].keys())

        if interaction.user.id == keys[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return
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

#######################################################
    ########## викторина ####################
#######################################################

  @app_commands.command(name="викторина", description="Вопросы викторины на различные темы.")
  async def Trivia_Quiz(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Trivia_Quiz == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    if channe_id in Trivia:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(Trivia[channe_id]['players'].keys())

        if interaction.user.id == keys[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return
        await interaction.response.edit_message(view=None)
        await interaction.delete_original_response()

        Trivia[channe_id]['info']['вопрос'] = random.choice(list(Quix.text))
        Trivia[channe_id]['info']['ответ'] = Quix.text[Trivia[channe_id]['info']['вопрос']]

        id = await interaction.followup.send("Ожидание..")
        Trivia[channe_id]['info']['id'] = id.id

        async def new_lvl():
            player1 = ""

            for players1 in Trivia[channe_id]['players']:
                player1 += f"- <@{players1}>: {Trivia[channe_id]['players'][players1]['point']} | ответ: {Trivia[channe_id]['players'][players1]['ответ']}\n"

            await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                      Викторина 
                      ═──────⊱⋆⊰─────═
                                      уровень {Trivia[channe_id]['info']['lvl']} 

{player1}
╔═━────═──────⊱⋆⊰─────═─────━═╗
                        Правильный ответ - {Trivia[channe_id]['info']['ответ']}
╚═━────═──────⊱⋆⊰─────═─────━═╝
всем кто ответил правильно получают +1
""", view=None)
            
            yees1 = None
            
            for game_out in Trivia[channe_id]['players']:
                Trivia[channe_id]['players'][game_out]['ход'] = False
                if str(Trivia[channe_id]['players'][game_out]['ответ']) == str(Trivia[channe_id]['info']['ответ']):
                    Trivia[channe_id]['players'][game_out]['point'] += 1

                if yees1 == False:
                    continue
                if Trivia[channe_id]['players'][game_out]['point'] == 5:
                    yees1 = True
                else:
                    yees1 = False

            if yees1 == True:
                await asyncio.sleep(5)
                await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                    Викторина 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
                    победитель - ничья
╚═━────═──────⊱⋆⊰─────═─────━═╝
""")
                del Trivia[channe_id]
                return


            for game_ou in Trivia[channe_id]['players']:
                if Trivia[channe_id]['players'][game_ou]['point'] == 5:
                    await asyncio.sleep(5)
                    await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                    Викторина 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
                    победитель - <@{game_ou}>
╚═━────═──────⊱⋆⊰─────═─────━═╝
""")
                    del Trivia[channe_id]
                    return

            Trivia[channe_id]['info']['lvl'] += 1
            Trivia[channe_id]['info']['вопрос'] = random.choice(list(Quix.text))
            Trivia[channe_id]['info']['ответ'] = Quix.text[Trivia[channe_id]['info']['вопрос']]
            await asyncio.sleep(7)
            await chat()

        async def chat():
            async def game(interaction: discord.Interaction):
                stop_event1.set()

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

                yees = None
                for out1 in Trivia[channe_id]['players']:
                    if yees == False:
                        continue
                    if Trivia[channe_id]['players'][out1]['ход'] == True:
                        yees = True
                    else:
                        yees = False

                if yees == True:
                    await asyncio.sleep(3)
                    await new_lvl()
                else:
                    await chat()
                
            buttonA = Button(emoji=f"🇦", style=discord.ButtonStyle.blurple, custom_id="А")
            buttonB = Button(emoji=f"🇧", style=discord.ButtonStyle.blurple, custom_id="В")
            buttonC = Button(emoji=f"🇨", style=discord.ButtonStyle.blurple, custom_id="С")

            buttonA.callback = game
            buttonB.callback = game
            buttonC.callback = game

            view1 = View(timeout=120)
            view1.add_item(buttonA)
            view1.add_item(buttonB)
            view1.add_item(buttonC)
            stop_event1 = asyncio.Event()
        
            async def timeout_callback1():
                try:
                    await asyncio.wait_for(stop_event1.wait(), timeout=view1.timeout)
                except asyncio.TimeoutError:
                    yees4 = None
                    for out3 in Trivia[channe_id]['players']:
                        if Trivia[channe_id]['players'][out3]['ход'] == False:
                            Trivia[channe_id]['players'][out3]['ответ'] = "*пусто*"

                        if yees4 == False:
                            continue

                        if Trivia[channe_id]['players'][out3]['ход'] == False:
                            yees4 = True
                        else:
                            yees4 = False
                    
                    if yees4 == True:
                        await asyncio.sleep(5)
                        await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                    Викторина 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
            Термин ожидания достиг лимиту,
                     комната была удалена
╚═━────═──────⊱⋆⊰─────═─────━═╝
""", view=None)
                        del Trivia[channe_id]
                        return
                    else:
                        await new_lvl()
                    
            self.client.loop.create_task(timeout_callback1()) 
            
            player = ""

            for players in Trivia[channe_id]['players']:
                xod = "*В ожидании*" if Trivia[channe_id]['players'][players]['ход'] == True else " "
                player += f"- <@{players}>: {Trivia[channe_id]['players'][players]['point']} Очков | {xod}\n"
            
            await interaction.followup.edit_message(message_id=Trivia[channe_id]['info']['id'], content=f"""
.                                     Викторина 
                      ═──────⊱⋆⊰─────═
                                     уровень {Trivia[channe_id]['info']['lvl']} 

{player}
╔═━────═──────⊱⋆⊰─────═─────━═╗                                             
{Trivia[channe_id]['info']['вопрос']}
╚═━────═──────⊱⋆⊰─────═─────━═╝
""", view=view1)
        
        await asyncio.sleep(5)
        await chat()

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in Trivia:
            if member in Trivia[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(Trivia[channe_id]['players']) >= 4:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                Trivia[channe_id]['players'][member] = {"point": 0, "ход": False, "ответ": None}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                if len(Trivia[channe_id]['players']) >= 4:
                    add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Добро пожаловать в викторину.\nПроверьте себя насколько вы умны\n{len(Trivia[channe_id]['players'])} Игроков в ожидании", message_id=interaction1, view=view)
        else:
            Trivia[channe_id] = {'players': {member: {"point": 0, "ход": False, "ответ": None}}, "info": {"вопрос": None, "ответ": None, "id": None, "lvl": 1}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Добро пожаловать в викторину.\nПроверьте себя насколько вы умны\n1 Игрок в ожидании", message_id=interaction1)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(tekst.trivia, ephemeral=True)

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

#######################################################
    ########## угадай число ####################
#######################################################

  @app_commands.command(name="угадай_число", description="Игра на угадывание числа, загаданного ботом.")
  async def guess_the_Number(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Guess_the_Number == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    target_number = random.randint(1, 100)
    channe_id = interaction.channel.id
    member = interaction.user.id
    
    if channe_id in Guess_the_Number:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return
    else:
        Guess_the_Number[channe_id] = {member: {"HP": 3}, "info": {"id": None, "1": None, "2": None, "3": None, "out": False}}

    await interaction.response.send_message("Загадиваю число..")
    await asyncio.sleep(5)
    await interaction.delete_original_response()
    id = await interaction.followup.send("""
Всё, а сейчас пожалуйста запомните вот эти цвета:

- 🟥 (± 15)
- 🟧 (± 40)
- 🟨 (± 70)
- 🟩 (очень далеко)
""")
    Guess_the_Number[channe_id]['info']['id'] = id.id
    await asyncio.sleep(10)
    
    async def game():
        xod1 = "*Пусто*" if Guess_the_Number[channe_id]['info']['1'] is None else Guess_the_Number[channe_id]['info']['1']
        xod2 = "*Пусто*" if Guess_the_Number[channe_id]['info']['2'] is None else Guess_the_Number[channe_id]['info']['2']
        xod3 = "*Пусто*" if Guess_the_Number[channe_id]['info']['3'] is None else Guess_the_Number[channe_id]['info']['3']

        if Guess_the_Number[channe_id]['info']['out'] == True:
            await interaction.followup.edit_message(message_id=Guess_the_Number[channe_id]['info']['id'], content=f"""
╔════════-----[угадай число]-
╠═══╣<@{member}>╠--
║
╠══ {xod1}
║
╠═ {xod2}
║
╠ {xod3}
║
╠═══[осталось {Guess_the_Number[channe_id][member]['HP']}]═-
╚══════════════---
          🎉 Победа! 🎉
""")
            del Guess_the_Number[channe_id]
            return
        
        elif Guess_the_Number[channe_id][member]['HP'] == 0:
            await interaction.followup.edit_message(message_id=Guess_the_Number[channe_id]['info']['id'], content=f"""
╔════════-----[угадай число]-
╠═══╣<@{member}>╠--
║
╠══ {xod1}
║
╠═ {xod2}
║
╠ {xod3}
║
╠═══[осталось {Guess_the_Number[channe_id][member]['HP']}]═-
╚══════════════---
           ❌ Поражение! ❌
""")
            del Guess_the_Number[channe_id]
            return

        await interaction.followup.edit_message(message_id=Guess_the_Number[channe_id]['info']['id'], content=f"""
╔════════-----[угадай число]-
╠═══╣<@{member}>╠--
║
╠══ {xod1}
║
╠═ {xod2}
║
╠ {xod3}
║
╠═══[осталось {Guess_the_Number[channe_id][member]['HP']}]═-
╚══════════════---
""")

        def check(message):
            return message.author.id == member
        try:
            message = await self.client.wait_for('message', timeout=180.0, check=check)
            messag = int(message.content)
        except asyncio.TimeoutError:
            await interaction.followup.send('❌ | Время вышло! Вы не успели угадать число.')
            del Guess_the_Number[channe_id]
            return
        except ValueError:
            await interaction.followup.send('❌ | Пожалуйста, введите корректное число.', ephemeral=True)
            try:
                await message.delete()
            except discord.NotFound:
                pass  
            await game()
            return

        if messag == target_number:
            if Guess_the_Number[channe_id][member]['HP'] == 3:
                Guess_the_Number[channe_id]['info']['1'] = f"{messag}| 🎉"
            elif Guess_the_Number[channe_id][member]['HP'] == 2:
                Guess_the_Number[channe_id]['info']['2'] = f"{messag}| 🎉"
            elif Guess_the_Number[channe_id][member]['HP'] == 1:
                Guess_the_Number[channe_id]['info']['3'] = f"{messag}| 🎉"
            Guess_the_Number[channe_id]['info']['out'] = True

        elif abs(messag - target_number) <= 15:
            if Guess_the_Number[channe_id][member]['HP'] == 3:
                Guess_the_Number[channe_id]['info']['1'] = f"{messag}| 🟥"
            elif Guess_the_Number[channe_id][member]['HP'] == 2:
                Guess_the_Number[channe_id]['info']['2'] = f"{messag}| 🟥"
            elif Guess_the_Number[channe_id][member]['HP'] == 1:
                Guess_the_Number[channe_id]['info']['3'] = f"{messag}| 🟥"
    
        elif abs(messag - target_number) <= 40:
            if Guess_the_Number[channe_id][member]['HP'] == 3:
                Guess_the_Number[channe_id]['info']['1'] = f"{messag}| 🟧"
            elif Guess_the_Number[channe_id][member]['HP'] == 2:
                Guess_the_Number[channe_id]['info']['2'] = f"{messag}| 🟧"
            elif Guess_the_Number[channe_id][member]['HP'] == 1:
                Guess_the_Number[channe_id]['info']['3'] = f"{messag}| 🟧"
            
        elif abs(messag - target_number) <= 70:
            if Guess_the_Number[channe_id][member]['HP'] == 3:
                Guess_the_Number[channe_id]['info']['1'] = f"{messag}| 🟨"
            elif Guess_the_Number[channe_id][member]['HP'] == 2:
                Guess_the_Number[channe_id]['info']['2'] = f"{messag}| 🟨"
            elif Guess_the_Number[channe_id][member]['HP'] == 1:
                Guess_the_Number[channe_id]['info']['3'] = f"{messag}| 🟨"
           
        else:
            if Guess_the_Number[channe_id][member]['HP'] == 3:
                Guess_the_Number[channe_id]['info']['1'] = f"{messag}| 🟩"
            elif Guess_the_Number[channe_id][member]['HP'] == 2:
                Guess_the_Number[channe_id]['info']['2'] = f"{messag}| 🟩"
            elif Guess_the_Number[channe_id][member]['HP'] == 1:
                Guess_the_Number[channe_id]['info']['3'] = f"{messag}| 🟩"
            
        try:
            await message.delete()
        except discord.NotFound:
            pass  
        Guess_the_Number[channe_id][member]['HP'] -= 1
        await asyncio.sleep(2)
        await game()
            
    await game()

#######################################################
    ########## виселица ####################
#######################################################

  @app_commands.command(name="виселица", description="игра, где нужно угадать слово по буквам.")
  async def Hangman(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Hangman == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    if channe_id in hangman:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(hangman[channe_id]['players'].keys())

        if interaction.user.id == keys[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return

        await interaction.response.edit_message(content="Загадиваю слово..", view=None)
        await asyncio.sleep(5)

        await interaction.delete_original_response()
        id = await interaction.followup.send("Загадиваю слово...")
        hangman[channe_id]['info']['id'] = id.id

        # player_1 = keys[0]
        # player_2 = keys[1]

        text = random.choice(Hangman.text)
        print(text)

        for texts in text:
            hangman[channe_id]['info']['list_all'].append(texts)
            if hangman[channe_id]['text']['1'] is None:
                hangman[channe_id]['text']['1'] = texts
            else:
                if hangman[channe_id]['text']['2'] is None:
                    hangman[channe_id]['text']['2'] = texts
                else:
                    if hangman[channe_id]['text']['3'] is None:
                        hangman[channe_id]['text']['3'] = texts
                    else:
                        if hangman[channe_id]['text']['4'] is None:
                            hangman[channe_id]['text']['4'] = texts
                        else:
                            if hangman[channe_id]['text']['5'] is None:
                                hangman[channe_id]['text']['5'] = texts
                            else:
                                if hangman[channe_id]['text']['6'] is None:
                                    hangman[channe_id]['text']['6'] = texts
                                else:
                                    if hangman[channe_id]['text']['7'] is None:
                                        hangman[channe_id]['text']['7'] = texts
                                    else:
                                        if hangman[channe_id]['text']['8'] is None:
                                            hangman[channe_id]['text']['8'] = texts
        
        for deat in list(hangman[channe_id]['text']):
            if hangman[channe_id]['text'][deat] is None:
                del hangman[channe_id]['text'][deat]

        hangman[channe_id]['info']['player'] = keys[0]
        keys.remove(keys[0])
        
        async def chat(keys):
            clovo = ""

            for clovos in list(hangman[channe_id]['text']):
                if hangman[channe_id]['text'][clovos] in hangman[channe_id]['info']['list']:
                    clovo += f"⟮{hangman[channe_id]['text'][clovos]}⟯"
                else:
                    clovo += "⟮◾⟯"

            if "◾" not in clovo or hangman[channe_id]['info']['final'] is not None:
                user5 = ""
                if hangman[channe_id]['info']['final'] is not None:
                    user5 += f"\nПобедитель | <@{hangman[channe_id]['info']['final']}>\n≠==========================≠"
                else:
                    yees5 = None
                    coin = 0
                    coin_user = None

                    for players1 in hangman[channe_id]['players']:
                        if hangman[channe_id]['players'][players1]['point'] > coin:
                            if coin_user is None:
                                coin_user = hangman[channe_id]['players'][players1]['point']
                            coin = hangman[channe_id]['players'][players1]['point']
                        if yees5 == False:
                            continue
                        if hangman[channe_id]['players'][players1]['point'] == coin_user:
                            yees5 = True
                        else:
                            yees5 = False

                    if yees5 == True:
                        user5 += "\nПобедитель | Ничья\n≠==========================≠"
                    else:
                        for players2 in hangman[channe_id]['players']:
                            if hangman[channe_id]['players'][players2]['point'] == coin:
                                user5 += f"\nПобедитель | <@{players2}> | {coin}\n≠==========================≠"

                await interaction.followup.edit_message(message_id=hangman[channe_id]['info']['id'], content=f"""
.        | Угадай слово |
            ༼ (КОНЕЦ) ༽
︿︿︿︿︿︿︿︿︿︿︿
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
|
⧽ {clovo}
|
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀
≠==========================≠{user5}
""")
                del hangman[channe_id]
                return

            player = ""

            for players in hangman[channe_id]['players']:
                player += f"\n<@{players}>]-({hangman[channe_id]['players'][players]['point']})\n≠==========================≠"

            await interaction.followup.edit_message(message_id=hangman[channe_id]['info']['id'], content=f"""
.           | Угадай слово |
            ༼ (<@{hangman[channe_id]['info']['player']}>) ༽
︿︿︿︿︿︿︿︿︿︿︿
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
|
⧽ {clovo}
|
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀
≠==========================≠{player}
""")
            
            async def mess(keys):
                def check(message):
                    return message.author.id == hangman[channe_id]['info']['player']
                try:
                    message = await self.client.wait_for('message', timeout=180.0, check=check)
                    if len(message.content) == 1:
                        try:
                            await message.delete()
                        except discord.NotFound:
                            pass
                    else:
                        if len(message.content) > 2:
                            final = message.content.lower()
                            if final == text:
                                for tex in text:
                                    hangman[channe_id]['info']['list'].append(tex)
                                hangman[channe_id]['info']['final'] = hangman[channe_id]['info']['player']
                                try:
                                    await message.delete()
                                except discord.NotFound:
                                    pass
                                await chat(keys)
                                return
                            
                            else:
                                if (hangman[channe_id]['players'][hangman[channe_id]['info']['player']]['point'] - 3) >= 0:
                                    hangman[channe_id]['players'][hangman[channe_id]['info']['player']]['point'] -= 3
                                    awa = await interaction.followup.send('❌ | Не угадали, у вас - 3 очка.')
                                    try:
                                        await message.delete()
                                    except discord.NotFound:
                                        pass
                                    await asyncio.sleep(5)
                                    await interaction.followup.delete_message(awa.id)

                                else:
                                    try:
                                        await message.delete()
                                    except discord.NotFound:
                                        pass
                                    awa = await interaction.followup.send(f"❌ | <@{hangman[channe_id]['info']['player']}> ответ оказался отрицательный, у вас оказалось недостаточно очков для снятия и поэтому вы покидаете игру.")
                                    del hangman[channe_id]['players'][hangman[channe_id]['info']['player']]
                                    await asyncio.sleep(5)
                                    await interaction.followup.delete_message(awa.id)
                                   
                        else:
                            try:
                                await message.delete()
                            except discord.NotFound:
                                pass  
                            awa = await interaction.followup.send('❌ | Пожалуйста, введите корректную букву.')
                            await asyncio.sleep(3)
                            await interaction.followup.delete_message(awa.id)
                            await mess(keys)
                            return
                        
                except asyncio.TimeoutError:
                    await interaction.followup.send('❌ | Время вышло! Вы не успели угадать слово.')
                    del hangman[channe_id]
                    return
                
                messag = message.content

                if messag.isupper():
                    messag = messag.lower()
                    

                for m in hangman[channe_id]['info']['list_all']:
                    if messag == m:
                        if messag in hangman[channe_id]['info']['list']:
                            pass
                        else:
                            hangman[channe_id]['info']['list'].append(messag)
                            hangman[channe_id]['players'][hangman[channe_id]['info']['player']]['point'] += 1
                            await chat(keys)
                            return

                if messag in hangman[channe_id]['info']['list_all']:
                    await chat(keys)
                else:
                    if len(hangman[channe_id]['players']) == 1:
                        for tex in text:
                            hangman[channe_id]['info']['list'].append(tex)
                        for fi in hangman[channe_id]['players']:
                            hangman[channe_id]['info']['final'] = fi

                    else:
                        if keys == []:
                            keys = list(hangman[channe_id]['players'].keys())
                            hangman[channe_id]['info']['player'] = keys[0]
                            keys.remove(keys[0])
                            
                        else:
                            hangman[channe_id]['info']['player'] = keys[0]
                            keys.remove(keys[0])

                    await chat(keys)

            await mess(keys)

        await chat(keys)

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in hangman:
            if member in hangman[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(hangman[channe_id]['players']) > 1:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                hangman[channe_id]['players'][member] = {"point": 0}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Добро пожаловать в игру **угадай слово**\nВ этой игре цель легка - угадать слово!\n2 Игроков в ожидании", message_id=interaction1, view=view)
        else:
            hangman[channe_id] = {'players': {member: {"point": 0}}, "info": {"player": None, "id": None, "list": [], "list_all": [], "final": None}, "text": {"1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None }}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Добро пожаловать в игру **угадай слово**\nВ этой игре цель легка - угадать слово!\n1 Игрок в ожидании", message_id=interaction1)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(tekst.Hangman, ephemeral=True)

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
                del hangman[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Добро пожаловать в игру **угадай слово**\nВ этой игре цель легка - угадать слово!", view=view)

#######################################################
    ########## правда или ложь ####################
#######################################################

  @app_commands.command(name="truth_or_lie", description="truth_or_lie")
  async def Truth_or_lie(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.truth_or_lie == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    if channe_id in truth_or_lie:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(truth_or_lie[channe_id]['players'].keys())

        if interaction.user.id == keys[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return
        await interaction.response.edit_message(view=None)
        await interaction.delete_original_response()

        truth_or_lie[channe_id]['info']['вопрос'] = random.choice(list(Truth_or_lie.text))
        truth_or_lie[channe_id]['info']['ответ'] = Truth_or_lie.text[truth_or_lie[channe_id]['info']['вопрос']]

        id = await interaction.followup.send("Ожидание..")
        truth_or_lie[channe_id]['info']['id'] = id.id

        async def new_lvl():
            
            player1 = ""

            for players1 in truth_or_lie[channe_id]['players']:
                if truth_or_lie[channe_id]['players'][players1]['ответ'] == "*пусто*":
                    player1 += f"- <@{players1}>: {truth_or_lie[channe_id]['players'][players1]['point']} | ответ: {truth_or_lie[channe_id]['players'][players1]['ответ']}\n"

                else:
                    player1 += f"- <@{players1}>: {truth_or_lie[channe_id]['players'][players1]['point']} | ответ: {"Правда" if truth_or_lie[channe_id]['players'][players1]['ответ'] == "А" else "Ложь"}\n"

            await interaction.followup.edit_message(message_id=truth_or_lie[channe_id]['info']['id'], content=f"""
.                                Правда/Ложь 
                      ═──────⊱⋆⊰─────═
                                      уровень {truth_or_lie[channe_id]['info']['lvl']} 

{player1}                                     
╔═━────═──────⊱⋆⊰─────═─────━═╗
                        Правильный ответ - {"Правда" if truth_or_lie[channe_id]['info']['ответ'] == "А" else "Ложь"}
╚═━────═──────⊱⋆⊰─────═─────━═╝
всем кто ответил правильно получают +1
""", view=None)

            yees1 = None
            
            for game_out in truth_or_lie[channe_id]['players']:
                truth_or_lie[channe_id]['players'][game_out]['ход'] = False
                if str(truth_or_lie[channe_id]['players'][game_out]['ответ']) == str(truth_or_lie[channe_id]['info']['ответ']):
                    truth_or_lie[channe_id]['players'][game_out]['point'] += 1

                if yees1 == False:
                    continue
                if truth_or_lie[channe_id]['players'][game_out]['point'] == 5:
                    yees1 = True
                else:
                    yees1 = False

            if yees1 == True:
                await asyncio.sleep(5)
                await interaction.followup.edit_message(message_id=truth_or_lie[channe_id]['info']['id'], content=f"""
.                               Правда/Ложь 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
                    победитель - ничья
╚═━────═──────⊱⋆⊰─────═─────━═╝
""")
                del truth_or_lie[channe_id]
                return

            for game_ou in truth_or_lie[channe_id]['players']:
                if truth_or_lie[channe_id]['players'][game_ou]['point'] == 5:
                    await asyncio.sleep(5)
                    await interaction.followup.edit_message(message_id=truth_or_lie[channe_id]['info']['id'], content=f"""
.                             Правда/Ложь 
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
                    победитель - <@{game_ou}>
╚═━────═──────⊱⋆⊰─────═─────━═╝
""")
                    del truth_or_lie[channe_id]
                    return
            
            truth_or_lie[channe_id]['info']['lvl'] += 1
            truth_or_lie[channe_id]['info']['вопрос'] = random.choice(list(Truth_or_lie.text))
            truth_or_lie[channe_id]['info']['ответ'] = Truth_or_lie.text[truth_or_lie[channe_id]['info']['вопрос']]
            await asyncio.sleep(7)
            await chat()

        async def chat():
            async def game(interaction: discord.Interaction):
                stop_event1.set()

                if truth_or_lie[channe_id]['players'][interaction.user.id]['ход'] == True:
                    await interaction.response.send_message(f":x: | вы уже сделали свой выбор, ожидайте другого игрока", ephemeral=True)
                    return
                
                if interaction.user.id in truth_or_lie[channe_id]['players']:
                    pass
                else:
                    await interaction.response.send_message(f":x: | к этой игре нельзя больше присоединиться", ephemeral=True)
                    return

                key = interaction.data['custom_id']
                truth_or_lie[channe_id]['players'][interaction.user.id]['ответ'] = key
                truth_or_lie[channe_id]['players'][interaction.user.id]['ход'] = True

                yees = None
                for out1 in truth_or_lie[channe_id]['players']:
                    if yees == False:
                        continue
                    if truth_or_lie[channe_id]['players'][out1]['ход'] == True:
                        yees = True
                    else:
                        yees = False

                if yees == True:
                    await asyncio.sleep(3)
                    await new_lvl()
                else:
                    await chat()
                
            buttonA = Button(label=f"Правда", style=discord.ButtonStyle.green, custom_id="А")
            buttonB = Button(label=f"Ложь", style=discord.ButtonStyle.red, custom_id="Б")

            buttonA.callback = game
            buttonB.callback = game

            view1 = View(timeout=120)
            view1.add_item(buttonA)
            view1.add_item(buttonB)
            stop_event1 = asyncio.Event()
        
            async def timeout_callback1():
                try:
                    await asyncio.wait_for(stop_event1.wait(), timeout=view1.timeout)
                except asyncio.TimeoutError:
                    yees4 = None
                    for out3 in truth_or_lie[channe_id]['players']:
                        if truth_or_lie[channe_id]['players'][out3]['ход'] == False:
                            truth_or_lie[channe_id]['players'][out3]['ответ'] = "*пусто*"

                        if yees4 == False:
                            continue

                        if truth_or_lie[channe_id]['players'][out3]['ход'] == False:
                            yees4 = True
                        else:
                            yees4 = False
                    
                    if yees4 == True:
                        await interaction.followup.edit_message(message_id=truth_or_lie[channe_id]['info']['id'], content=f"""
.                                Правда/Ложь
            
╔═━────═──────⊱⋆⊰─────═─────━═╗
            Термин ожидания достиг лимиту,
                     комната была удалена
╚═━────═──────⊱⋆⊰─────═─────━═╝
""", view=None)
                        del truth_or_lie[channe_id]
                        return
                    else:
                        await new_lvl()
                    
            self.client.loop.create_task(timeout_callback1()) 

            player = ""

            for players in truth_or_lie[channe_id]['players']:
                xod = "*В ожидании*" if truth_or_lie[channe_id]['players'][players]['ход'] == True else " "
                player += f"- <@{players}>: {truth_or_lie[channe_id]['players'][players]['point']} Очков | {xod}\n"
            
            await interaction.followup.edit_message(message_id=truth_or_lie[channe_id]['info']['id'], content=f"""
.                               Правда/Ложь
                      ═──────⊱⋆⊰─────═
                                     уровень {truth_or_lie[channe_id]['info']['lvl']} 

{player}     
╔═━────═──────⊱⋆⊰─────═─────━═╗                                             
{truth_or_lie[channe_id]['info']['вопрос']}
╚═━────═──────⊱⋆⊰─────═─────━═╝
""", view=view1)
        
        await asyncio.sleep(5)
        await chat()

    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in truth_or_lie:
            if member in truth_or_lie[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(truth_or_lie[channe_id]['players']) >= 4:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                truth_or_lie[channe_id]['players'][member] = {"point": 0, "ход": False, "ответ": None}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                if len(truth_or_lie[channe_id]['players']) >= 4:
                    add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Кто-то говорит правда, а другие ложь\nА что окажется правдой, давайте узнаем вместе?\n{len(truth_or_lie[channe_id]['players'])} Игроков в ожидании", message_id=interaction1, view=view)
        else:
            truth_or_lie[channe_id] = {'players': {member: {"point": 0, "ход": False, "ответ": None}}, "info": {"вопрос": None, "ответ": None, "id": None, "lvl": 1}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Кто-то говорит правда, а другие ложь\nА что окажется правдой, давайте узнаем вместе?\n1 Игрок в ожидании", message_id=interaction1)



    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(tekst.Truth_or_lie, ephemeral=True)

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
                del truth_or_lie[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Кто-то говорит правда, а другие ложь\nА что окажется правдой, давайте узнаем вместе?", view=view)

#######################################################
    ########## анаграма ####################
#######################################################

  @app_commands.command(name="anagrams", description="Anagrams")
  async def Anagrams(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.anagrams == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    if channe_id in anagrams:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(anagrams[channe_id]['players'].keys())

        if interaction.user.id == keys[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return
        
        await interaction.response.edit_message(content="Загадиваю слово...", view=None)
        await asyncio.sleep(5)

        await interaction.delete_original_response()
        id = await interaction.followup.send("Загадиваю слово..")
        anagrams[channe_id]['info']['id'] = id.id
        anagrams[channe_id]['info']['player'] = keys[0]
        keys.remove(keys[0])

        text = random.choice(Anagrams.text)

        async def chat(keys):
            yees = None
            for out in anagrams[channe_id]['players']:
                if yees == False:
                    continue
                if anagrams[channe_id]['players'][out]['point'] == 0:
                    yees = True
                else:
                    yees = False

            if yees == True:
                await asyncio.sleep(2)
                await interaction.followup.edit_message(message_id=anagrams[channe_id]['info']['id'], content=f"""
.        | Угадай слово |
            ༼ (КОНЕЦ) ༽
︿︿︿︿︿︿︿︿︿︿︿
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
|
⧽--[{text}]--᚜
|
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀
≠==========================≠
]-=-[]-НИЧЬЯ-[]-=-[
≠==========================≠
""")
                del anagrams[channe_id]
                return

            def ad_text():
                for texts in text:
                    anagrams[channe_id]['info']['list'].append(texts)

                while True:
                    add_text = random.choice(anagrams[channe_id]['info']['list'])
                    anagrams[channe_id]['info']['clovo'] += f"{add_text}"
                    anagrams[channe_id]['info']['list'].remove(add_text)
                    if anagrams[channe_id]['info']['list'] == []:
                        break
            ad_text()

            if text == anagrams[channe_id]['info']['clovo']:
                ad_text()

            player = ""

            for players in anagrams[channe_id]['players']:
                player += f"\n[<@{players}>]--[осталось попыток {anagrams[channe_id]['players'][players]['point']} ]\n≠==========================≠"

            await interaction.followup.edit_message(message_id=anagrams[channe_id]['info']['id'], content=f"""
.          | Угадай слово |
            ༼ (<@{anagrams[channe_id]['info']['player']}>) ༽
︿︿︿︿︿︿︿︿︿︿︿
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
|
⧽--[{anagrams[channe_id]['info']['clovo']}]--᚜
|
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀
≠==========================≠{player}
""")
            def check(message):
                return message.author.id == anagrams[channe_id]['info']['player']
            try:
                message = await self.client.wait_for('message', timeout=180.0, check=check)
                messag = message.content.lower()
            except asyncio.TimeoutError:
                await interaction.followup.send('❌ | Время вышло! Вы не успели угадать слово.')
                del anagrams[channe_id]
                return
            
            try:
                await message.delete()
            except discord.NotFound:
                pass  

            if messag == text:
                await asyncio.sleep(2)
                await interaction.followup.edit_message(message_id=anagrams[channe_id]['info']['id'], content=f"""
.        | Угадай слово |
            ༼ (КОНЕЦ) ༽
︿︿︿︿︿︿︿︿︿︿︿
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
|
⧽--[{text}]--᚜
|
᚛⦒⦑⦒⦒⦒⦒⦑⦒⦑⦒⦑⦑⦑⦑⦒⦑᚜>-----=⸎
﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀﹀
≠==========================≠
Победитель | <@{anagrams[channe_id]['info']['player']}>
≠==========================≠
""")
                del anagrams[channe_id]
                return
            
            else:
               
                anagrams[channe_id]['players'][anagrams[channe_id]['info']['player']]['point'] -= 1
                anagrams[channe_id]['info']['clovo'] = ""

                if keys == []:
                    keys = list(anagrams[channe_id]['players'].keys())
                    anagrams[channe_id]['info']['player'] = keys[0]
                    keys.remove(keys[0])
                    
                else:
                    anagrams[channe_id]['info']['player'] = keys[0]
                    keys.remove(keys[0])

                await chat(keys)

        await chat(keys)

        
    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in anagrams:
            if member in anagrams[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(anagrams[channe_id]['players']) >= 4:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                anagrams[channe_id]['players'][member] = {"point": 5}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                if len(anagrams[channe_id]['players']) >= 4:
                    add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Захотели расшифровать слова с другом?\nТогда создайте команду и начните игру!\n{len(anagrams[channe_id]['players'])} Игроков в ожидании", message_id=interaction1, view=view)
        else:
            anagrams[channe_id] = {'players': {member: {"point": 5}}, "info": {"player": None, "id": None, "list": [], "clovo": ""}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Захотели расшифровать слова с другом?\nТогда создайте команду и начните игру!\n1 Игрок в ожидании", message_id=interaction1)


    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(tekst.anagrams, ephemeral=True)

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
                del anagrams[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Захотели расшифровать слова с другом?\nТогда создайте команду и начните игру!", view=view)

#######################################################
    ########## ролевые диалоги ####################
#######################################################

  @app_commands.command(name="role_playing", description="Role-playing")
  async def Role_playing(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.role_playing == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    if channe_id in role_playing:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(role_playing[channe_id]['players'].keys())

        if interaction.user.id == keys[0]:
            pass
        else:
            await interaction.response.send_message("Начать игру может только создатель комнаты", ephemeral=True)
            return
        
        await interaction.response.edit_message(content="Ожидание..", view=None)
        await asyncio.sleep(5)
        coins = random.randint(1, 5)

        if len(role_playing[channe_id]['players']) == 2:
            key = list(role_playing[channe_id]['players'].keys())
            text = random.choice(list(Role_play.text1))
            role_playing[channe_id]['info']['rol2'] = random.choice(Role_play.text1[text]['list'])
            meta = Role_play.text1[text]['m']
            kye1 = random.choice(key)
            rol = random.choice(Role_play.text1[text]['rol'])
            role_playing[channe_id]['info']['rol1'] += f"\n[<@{kye1}>]=-=[{rol}]\n  -=()=-=====-=()=-"
            key.remove(kye1)
            Role_play.text1[text]['rol'].remove(rol)
            role_playing[channe_id]['info']['rol1'] += f"\n[<@{key[0]}>]=-=[{Role_play.text1[text]['rol'][0]}]\n  -=()=-=====-=()=-"
        
        elif len(role_playing[channe_id]['players']) == 3:
            key = list(role_playing[channe_id]['players'].keys())
            text = random.choice(list(Role_play.text2))
            role_playing[channe_id]['info']['rol2'] = random.choice(Role_play.text2[text]['list'])
            meta = Role_play.text2[text]['m']
            while True:
                if key == []:
                    break
                kye1 = random.choice(key)
                rol = random.choice(Role_play.text2[text]['rol'])
                role_playing[channe_id]['info']['rol1'] += f"\n[<@{kye1}>]=-=[{rol}]\n  -=()=-=====-=()=-"
                key.remove(kye1)
                Role_play.text2[text]['rol'].remove(rol)

        else:
            key = list(role_playing[channe_id]['players'].keys())
            text = random.choice(list(Role_play.text3))
            role_playing[channe_id]['info']['rol2'] = random.choice(Role_play.text3[text]['list'])
            meta = Role_play.text3[text]['m']
            while True:
                if key == []:
                    break
                kye1 = random.choice(key)
                rol = random.choice(Role_play.text3[text]['rol'])
                role_playing[channe_id]['info']['rol1'] += f"\n[<@{kye1}>]=-=[{rol}]\n  -=()=-=====-=()=-"
                key.remove(kye1)
                Role_play.text3[text]['rol'].remove(rol)
      
        async def chat():
            await interaction.followup.edit_message(message_id=role_playing[channe_id]['info']['id'], content=f"""
══════════════════════
            »»———<{meta}>———-««
══════════════════════
   
>═════════════════════<
{text}
>═════════════════════<

  -=()=-=====-=()=-{role_playing[channe_id]['info']['rol1']}
""")
            
            async def mess():
                if role_playing[channe_id]['info']['rol'] == coins:
                    await interaction.followup.send(role_playing[channe_id]['info']['rol2'])
                    if len(role_playing[channe_id]['players']) == 2:
                        Role_play.text1[text]['list'].remove(role_playing[channe_id]['info']['rol2'])

                    elif len(role_playing[channe_id]['players']) == 3:
                        Role_play.text2[text]['list'].remove(role_playing[channe_id]['info']['rol2'])

                    else:
                        Role_play.text3[text]['list'].remove(role_playing[channe_id]['info']['rol2'])
                
                elif role_playing[channe_id]['info']['rol'] > coins:
                    coin1 = random.randint(1, 50)
                    if coin1 == 5:
                        if len(role_playing[channe_id]['players']) == 2:
                            coin = random.choice(Role_play.text1[text]['list'])
                            await interaction.followup.send(coin)
                            Role_play.text1[text]['list'].remove(coin)

                        elif len(role_playing[channe_id]['players']) == 3:
                            coin = random.choice(Role_play.text2[text]['list'])
                            await interaction.followup.send(coin)
                            Role_play.text2[text]['list'].remove(coin)

                        else:
                            coin = random.choice(Role_play.text3[text]['list'])
                            await interaction.followup.send(coin)
                            Role_play.text3[text]['list'].remove(coin)

                def check(message):
                    return message.author.id in role_playing[channe_id]['players']
                try:
                    message = await self.client.wait_for('message', timeout=180.0, check=check)
                except asyncio.TimeoutError:
                    await interaction.followup.send('❌ | Время вышло! Игра окончена.')
                    del role_playing[channe_id]
                    return
                
                role_playing[channe_id]['info']['rol'] += 1
                await mess()

            await mess()

        await chat()

      
    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in role_playing:
            if member in role_playing[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(role_playing[channe_id]['players']) >= 3: # 4
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                role_playing[channe_id]['players']["user"] = {"point": 0}
                role_playing[channe_id]['players'][member] = {"point": 0}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                if len(role_playing[channe_id]['players']) >= 3: # 4
                    add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"Желаете сыграть?\nНу же, чего вы ждите, начинайте игру!\n{len(role_playing[channe_id]['players'])} Игроков в ожидании", message_id=interaction1, view=view)
        else:
            role_playing[channe_id] = {'players': {member: {"point": 0}}, "info": {"player": None, "id": None, "coin": None, "rol1": "", "rol": 0, "rol2": None}}
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content="Желаете сыграть?\nНу же, чего вы ждите, начинайте игру!\n1 Игрок в ожидании", message_id=interaction1)
            role_playing[channe_id]['info']['id'] = interaction1

    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(tekst.role_playing, ephemeral=True)

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
                del role_playing[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message("Желаете сыграть?\nНу же, чего вы ждите, начинайте игру!", view=view)

######################################################
    ######### головоломки ####################
######################################################

  @app_commands.command(name="головоломка", description="Коп. Головоломки")
  async def Puzzle(self, interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(tekst.DM)
        return
    if config.Puzzle == False:
        await interaction.response.send_message(tekst.nots)
        return
    
    channe_id = interaction.channel_id

    if channe_id in puzzle:
        await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
        return

    async def game_start(interaction: discord.Interaction):
        stop_event.set()
        keys = list(puzzle[channe_id]['players'].keys())
        player_1 = keys[0]
        player_2 = keys[1]
        dm_player_1 = interaction.guild.get_member(keys[0])
        dm_player_2 = interaction.guild.get_member(keys[1])
        # id1 = await dm_player_1.send("hello1")
        # id2 = await dm_player_2.send("425364")
        # puzzle[channe_id]['info']['id1'] = id1.id
        # puzzle[channe_id]['info']['id2'] = id2.id
        puzzle[channe_id]['info']['player'] = 1
        box1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        box2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        box3 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        caskets = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        clock1 = ["0", "1", "2"]
        clock2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        clock3 = ["0", "1", "2", "3", "4", "5", "6"]
        clock4 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        
        async def chat(interaction: discord.Interaction):
            if interaction.user.id not in puzzle[channe_id]['players']:
                await interaction.response.send_message("комната занята", ephemeral=True)
                return
            
            elif interaction.user.id == player_1:
                await interaction.response.send_message(f"{player_1}", ephemeral=True)


            elif interaction.user.id == player_2:
                
                async def Puzzle2(interaction: discord.Interaction):
                    if interaction.data['custom_id'] == "буфет1":
                        puzzle[channe_id]['home']['буфет'] = False
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        puzzle[channe_id]['players'][player_2]['item'].append("страница ?")
                        puzzle[channe_id]['players'][player_2]['item'].append("годиная стрелка")
                        await interaction.response.edit_message(content=f"Открыв буфет, я понял, что его давно никто не открывал: он весь был в пыли. Сквозь всю эту пыль я смог разглядеть какую-то страницу и стрелку от часов. Похоже, здесь больше ничего нет.", view=view_player2)

                    elif interaction.data['custom_id'] == "тумбочка1":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        if puzzle[channe_id]['home']['тумбочка1'] == False:
                            await interaction.response.edit_message(content=f"Вернувшись сюда снова, я ничего нового не заметил: та же шкатулка и всё то же.", view=view_player2)
                        else:
                            view_player2.add_item(button5)
                            await interaction.response.edit_message(content=f"Отодвинув первую шухляду на себя, я заметил странную шкатулку. Попытавшись взять её с собой, я понял, что она намертво приделана. На самой шкатулке были цифры — возможно, это код. Нужно разобраться.", view=view_player2)

                    elif interaction.data['custom_id'] == "тумбочка2":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        if puzzle[channe_id]['home']['тумбочка2'] == False:
                            await interaction.response.edit_message(content=f"Снова вернувшись сюда, я ничего нового не заметил: пустая шухляда и всё.", view=view_player2)
                        else:
                            if "ключ" in puzzle[channe_id]['players'][player_2]['item']:
                                puzzle[channe_id]['players'][player_2]['item'].remove("ключ")
                                puzzle[channe_id]['players'][player_2]['item'].append("изолента")
                                puzzle[channe_id]['home']['тумбочка2'] = False
                                await interaction.response.edit_message(content=f"Открыв её, я нашёл только изоленту. Ну ничего, может, пригодится где-то.", view=view_player2)
                            else:
                                await interaction.response.edit_message(content=f"Осмотрев другую шухляду, я обнаружил, что она закрыта на замок. Возможно, сначала нужно найти ключ от неё.", view=view_player2)

                    elif interaction.data['custom_id'] == "тумбочка3":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        await interaction.response.edit_message(content=f"Отодвинув третью шухляду на себя, я обнаружил какой-то знак, похожий на **V**. Что это может означать?", view=view_player2)

                    elif interaction.data['custom_id'] == "тумбочка11":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        view_player2.add_item(button_caskets1)
                        view_player2.add_item(button_caskets5)
                        view_player2.add_item(button_caskets2)
                        view_player2.add_item(button_caskets3)
                        view_player2.add_item(button_caskets4)
                        puzzle[channe_id]['kod']['kod'] = 1
                        await interaction.response.edit_message(content=f"""
|   ︿    ︿ {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] else " "} ︿   {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка3']] in ["2", "3", "4", "5"] else " "}︿
| {">" if puzzle[channe_id]['kod']['тумбочка'] == 1 else "  "} {caskets[puzzle[channe_id]['kod']['тумбочка1']]}   {">" if puzzle[channe_id]['kod']['тумбочка'] == 2 else "  "} {caskets[puzzle[channe_id]['kod']['тумбочка2']]}   {">" if puzzle[channe_id]['kod']['тумбочка'] == 3 else "  "} {caskets[puzzle[channe_id]['kod']['тумбочка3']]}   {">" if puzzle[channe_id]['kod']['тумбочка'] == 4 else "   "} {caskets[puzzle[channe_id]['kod']['тумбочка4']]}
|   ﹀    ﹀ {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] else " "} ﹀   {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка3']] in ["2", "3", "4", "5"] else " "}﹀                                                       
""", view=view_player2)

                    elif interaction.data['custom_id'] in ["caskets1", "caskets2", "caskets3", "caskets4", "caskets5"]:
                        if interaction.data['custom_id'] == "caskets1":
                            if puzzle[channe_id]['kod']['kod'] == 1:
                                if puzzle[channe_id]['kod'][f"тумбочка{puzzle[channe_id]['kod']['тумбочка']}"] == 9:
                                    puzzle[channe_id]['kod'][f"тумбочка{puzzle[channe_id]['kod']['тумбочка']}"] = 0
                                else:
                                    puzzle[channe_id]['kod'][f"тумбочка{puzzle[channe_id]['kod']['тумбочка']}"] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 2:
                                if puzzle[channe_id]['kod']['часи'] == 1:
                                    if puzzle[channe_id]['kod']["часи1"] == 2:
                                        puzzle[channe_id]['kod']["часи1"] = 0
                                    else:
                                        if puzzle[channe_id]['kod']["часи1"] == 1 and puzzle[channe_id]['kod']["часи2"] > 4:
                                            puzzle[channe_id]['kod']["часи1"] = 0
                                        else:
                                            puzzle[channe_id]['kod']["часи1"] += 1
                                
                                elif puzzle[channe_id]['kod']['часи'] == 2:
                                    if puzzle[channe_id]['kod']["часи2"] == 9:
                                        puzzle[channe_id]['kod']["часи2"] = 0
                                    else:
                                        if puzzle[channe_id]['kod']["часи1"] == 2 and puzzle[channe_id]['kod']["часи2"] == 4:
                                            puzzle[channe_id]['kod']["часи2"] = 0
                                        else:
                                            puzzle[channe_id]['kod']["часи2"] += 1

                                elif puzzle[channe_id]['kod']['часи'] == 3:
                                    if puzzle[channe_id]['kod']["часи3"] == 6:
                                        puzzle[channe_id]['kod']["часи3"] = 0
                                    else:
                                        if puzzle[channe_id]['kod']["часи3"] == 5 and puzzle[channe_id]['kod']["часи4"] > 0:
                                            puzzle[channe_id]['kod']["часи3"] = 0
                                        else:
                                            puzzle[channe_id]['kod']["часи3"] += 1

                                elif puzzle[channe_id]['kod']['часи'] == 4:
                                    if puzzle[channe_id]['kod']["часи4"] == 9:
                                        puzzle[channe_id]['kod']["часи4"] = 0
                                    else:
                                        if puzzle[channe_id]['kod']["часи3"] == 6:
                                            puzzle[channe_id]['kod']["часи3"] = 5
                                        puzzle[channe_id]['kod']["часи4"] += 1
                            
                            elif puzzle[channe_id]['kod']['kod'] == 3:
                                if puzzle[channe_id]['kod'][f"1ящик{puzzle[channe_id]['kod']['1ящик']}"] == 9:
                                    puzzle[channe_id]['kod'][f"1ящик{puzzle[channe_id]['kod']['1ящик']}"] = 0
                                else:
                                    puzzle[channe_id]['kod'][f"1ящик{puzzle[channe_id]['kod']['1ящик']}"] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 4:
                                if puzzle[channe_id]['kod'][f"2ящик{puzzle[channe_id]['kod']['2ящик']}"] == 9:
                                    puzzle[channe_id]['kod'][f"2ящик{puzzle[channe_id]['kod']['2ящик']}"] = 0
                                else:
                                    puzzle[channe_id]['kod'][f"2ящик{puzzle[channe_id]['kod']['2ящик']}"] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 5:
                                if puzzle[channe_id]['kod'][f"3ящик{puzzle[channe_id]['kod']['3ящик']}"] == 9:
                                    puzzle[channe_id]['kod'][f"3ящик{puzzle[channe_id]['kod']['3ящик']}"] = 0
                                else:
                                    puzzle[channe_id]['kod'][f"3ящик{puzzle[channe_id]['kod']['3ящик']}"] += 1

                        elif interaction.data['custom_id'] == "caskets3":
                            if puzzle[channe_id]['kod']['kod'] == 1:
                                if puzzle[channe_id]['kod'][f"тумбочка{puzzle[channe_id]['kod']['тумбочка']}"] == 0:
                                    puzzle[channe_id]['kod'][f"тумбочка{puzzle[channe_id]['kod']['тумбочка']}"] = 9
                                else:
                                    puzzle[channe_id]['kod'][f"тумбочка{puzzle[channe_id]['kod']['тумбочка']}"] -= 1

                            elif puzzle[channe_id]['kod']['kod'] == 2:
                                if puzzle[channe_id]['kod']['часи'] == 1:
                                    if puzzle[channe_id]['kod']["часи1"] == 0:
                                        if puzzle[channe_id]['kod']["часи2"] > 4:
                                            puzzle[channe_id]['kod']["часи1"] = 1
                                        else:
                                            puzzle[channe_id]['kod']["часи1"] = 2
                                    else:
                                        puzzle[channe_id]['kod']["часи1"] -= 1
                                
                                elif puzzle[channe_id]['kod']['часи'] == 2:
                                    if puzzle[channe_id]['kod']["часи2"] == 0:
                                        if puzzle[channe_id]['kod']["часи1"] == 2:
                                            puzzle[channe_id]['kod']["часи2"] = 4
                                        else:
                                            puzzle[channe_id]['kod']["часи2"] = 9
                                    else:
                                        puzzle[channe_id]['kod']["часи2"] -= 1

                                elif puzzle[channe_id]['kod']['часи'] == 3:
                                    if puzzle[channe_id]['kod']["часи3"] == 0:
                                        if puzzle[channe_id]['kod']["часи4"] > 0:
                                            puzzle[channe_id]['kod']["часи3"] = 5
                                        else:
                                            puzzle[channe_id]['kod']["часи3"] = 6
                                    else:
                                        puzzle[channe_id]['kod']["часи3"] -= 1

                                elif puzzle[channe_id]['kod']['часи'] == 4:
                                    if puzzle[channe_id]['kod']["часи4"] == 0:
                                        if puzzle[channe_id]['kod']["часи3"] == 6:
                                            puzzle[channe_id]['kod']["часи3"] = 5
                                        puzzle[channe_id]['kod']["часи4"] = 9
                                    else:
                                        puzzle[channe_id]['kod']["часи4"] -= 1
                            
                            elif puzzle[channe_id]['kod']['kod'] == 3:
                                if puzzle[channe_id]['kod'][f"1ящик{puzzle[channe_id]['kod']['1ящик']}"] == 0:
                                    puzzle[channe_id]['kod'][f"1ящик{puzzle[channe_id]['kod']['1ящик']}"] = 9
                                else:
                                    puzzle[channe_id]['kod'][f"1ящик{puzzle[channe_id]['kod']['1ящик']}"] -= 1

                            elif puzzle[channe_id]['kod']['kod'] == 4:
                                if puzzle[channe_id]['kod'][f"2ящик{puzzle[channe_id]['kod']['2ящик']}"] == 0:
                                    puzzle[channe_id]['kod'][f"2ящик{puzzle[channe_id]['kod']['2ящик']}"] = 9
                                else:
                                    puzzle[channe_id]['kod'][f"2ящик{puzzle[channe_id]['kod']['2ящик']}"] -= 1

                            elif puzzle[channe_id]['kod']['kod'] == 5:
                                if puzzle[channe_id]['kod'][f"3ящик{puzzle[channe_id]['kod']['3ящик']}"] == 0:
                                    puzzle[channe_id]['kod'][f"3ящик{puzzle[channe_id]['kod']['3ящик']}"] = 9
                                else:
                                    puzzle[channe_id]['kod'][f"3ящик{puzzle[channe_id]['kod']['3ящик']}"] -= 1

                        elif interaction.data['custom_id'] == "caskets2":
                            if puzzle[channe_id]['kod']['kod'] == 1:
                                if puzzle[channe_id]['kod']['тумбочка'] == 1:
                                    puzzle[channe_id]['kod']['тумбочка'] = 4
                                else:
                                    puzzle[channe_id]['kod']['тумбочка'] -= 1

                            elif puzzle[channe_id]['kod']['kod'] == 2:
                                if puzzle[channe_id]['kod']['часи'] == 1:
                                    puzzle[channe_id]['kod']['часи'] = 4
                                else:
                                    puzzle[channe_id]['kod']['часи'] -= 1
                            
                            elif puzzle[channe_id]['kod']['kod'] == 3:
                                if puzzle[channe_id]['kod']['1ящик'] == 1:
                                    puzzle[channe_id]['kod']['1ящик'] = 6
                                else:
                                    puzzle[channe_id]['kod']['1ящик'] -= 1

                            elif puzzle[channe_id]['kod']['kod'] == 4:
                                if puzzle[channe_id]['kod']['2ящик'] == 1:
                                    puzzle[channe_id]['kod']['2ящик'] = 6
                                else:
                                    puzzle[channe_id]['kod']['2ящик'] -= 1

                            elif puzzle[channe_id]['kod']['kod'] == 5:
                                if puzzle[channe_id]['kod']['3ящик'] == 1:
                                    puzzle[channe_id]['kod']['3ящик'] = 6
                                else:
                                    puzzle[channe_id]['kod']['3ящик'] -= 1
                        
                        elif interaction.data['custom_id'] == "caskets4":
                            if puzzle[channe_id]['kod']['kod'] == 1:
                                if puzzle[channe_id]['kod']['тумбочка'] == 4:
                                    puzzle[channe_id]['kod']['тумбочка'] = 1
                                else:
                                    puzzle[channe_id]['kod']['тумбочка'] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 2:
                                if puzzle[channe_id]['kod']['часи'] == 4:
                                    puzzle[channe_id]['kod']['часи'] = 1
                                else:
                                    puzzle[channe_id]['kod']['часи'] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 3:
                                if puzzle[channe_id]['kod']['1ящик'] == 6:
                                    puzzle[channe_id]['kod']['1ящик'] = 1
                                else:
                                    puzzle[channe_id]['kod']['1ящик'] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 4:
                                if puzzle[channe_id]['kod']['2ящик'] == 6:
                                    puzzle[channe_id]['kod']['2ящик'] = 1
                                else:
                                    puzzle[channe_id]['kod']['2ящик'] += 1

                            elif puzzle[channe_id]['kod']['kod'] == 5:
                                if puzzle[channe_id]['kod']['3ящик'] == 6:
                                    puzzle[channe_id]['kod']['3ящик'] = 1
                                else:
                                    puzzle[channe_id]['kod']['3ящик'] += 1

                        elif interaction.data['custom_id'] == "caskets5":
                            if puzzle[channe_id]['kod']['kod'] == 1:
                                if caskets[puzzle[channe_id]['kod']['тумбочка1']] == "3" and \
                                    caskets[puzzle[channe_id]['kod']['тумбочка2']] == "5" and \
                                    caskets[puzzle[channe_id]['kod']['тумбочка3']] == "1" and \
                                    caskets[puzzle[channe_id]['kod']['тумбочка4']] == "7":
                                    await interaction.response.send_message("gooot!!!", ephemeral=True)
                                    return
                                else:
                                    await interaction.response.send_message("цифры оказались в неправильном порядке.", ephemeral=True)
                                    return
                                
                            elif puzzle[channe_id]['kod']['kod'] == 2:
                                if puzzle[channe_id]['home']['старые час']:
                                    await interaction.response.send_message("Хммм... ничего не происходит.")
                                    return
                                else:
                                    if clock1[puzzle[channe_id]['kod']['часи1']] == "1" and \
                                        clock2[puzzle[channe_id]['kod']['часи2']] == "0" and \
                                        clock3[puzzle[channe_id]['kod']['часи3']] == "0" and \
                                        clock4[puzzle[channe_id]['kod']['часи4']] == "5":
                                        puzzle[channe_id]['home']['телевизор2'] == True
                                        puzzle[channe_id]['home']['старые час'] == True
                                        puzzle[channe_id]['players'][player_2]['item'].append("шештерня")
                                        await interaction.response.send_message("Поставив время на 10:05, часы открылись, и внутри я обнаружил шестерёнку. Взяв её, я закрыл часы обратно.")
                                        return
                                    else:
                                        await interaction.response.send_message(f"Я успешно поставил время на {clock1[puzzle[channe_id]['kod']['часи1']]}{clock2[puzzle[channe_id]['kod']['часи2']]}:{clock3[puzzle[channe_id]['kod']['часи3']]}{clock4[puzzle[channe_id]['kod']['часи4']]}.")
                                        return

                            elif puzzle[channe_id]['kod']['kod'] == 3:
                                if box1[puzzle[channe_id]['kod']['1ящик1']] == "5" and \
                                    box1[puzzle[channe_id]['kod']['1ящик2']] == "9" and \
                                    box1[puzzle[channe_id]['kod']['1ящик3']] == "7" and \
                                    box1[puzzle[channe_id]['kod']['1ящик4']] == "1" and \
                                    box1[puzzle[channe_id]['kod']['1ящик5']] == "8" and \
                                    box1[puzzle[channe_id]['kod']['1ящик6']] == "3":
                                    puzzle[channe_id]['home']['1ящик'] = False
                                    puzzle[channe_id]['players'][player_2]['item'].append("ключ")
                                    puzzle[channe_id]['players'][player_2]['item'].append("лист бумаги")
                                    await interaction.response.send_message("Открыв первый ящик, я обнаружил странный ключ и лист бумаги. Взяв всё с собой, я отошёл от ящика.", ephemeral=True)
                                    return
                                else:
                                    await interaction.response.send_message("цифры оказались в неправильном порядке.", ephemeral=True)
                                    return

                            elif puzzle[channe_id]['kod']['kod'] == 4:
                                if box2[puzzle[channe_id]['kod']['2ящик1']] == "1" and \
                                    box2[puzzle[channe_id]['kod']['2ящик2']] == "3" and \
                                    box2[puzzle[channe_id]['kod']['2ящик3']] == "5" and \
                                    box2[puzzle[channe_id]['kod']['2ящик4']] == "7" and \
                                    box2[puzzle[channe_id]['kod']['2ящик5']] == "8" and \
                                    box2[puzzle[channe_id]['kod']['2ящик6']] == "9":
                                    puzzle[channe_id]['home']['2ящик'] = False
                                    await interaction.response.send_message("Открыв другой ящик, я заметил странный символ на дне, похожий на **Х**. Что это может значить?", ephemeral=True)
                                    return                 
                                else:
                                    await interaction.response.send_message("цифры оказались в неправильном порядке.", ephemeral=True)
                                    return

                            elif puzzle[channe_id]['kod']['kod'] == 5:
                                puzzle[channe_id]['home']['3ящик'] = False
                                await interaction.response.send_message("gooot!!!", ephemeral=True)
                                return
                                
                            
                        if puzzle[channe_id]['kod']['kod'] == 1:
                            await interaction.response.edit_message(content=f"""
|   ︿    ︿ {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] else " "} ︿   {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка3']] in ["2", "3", "4", "5"] else " "}︿
| {">" if puzzle[channe_id]['kod']['тумбочка'] == 1 else "  "} {caskets[puzzle[channe_id]['kod']['тумбочка1']]}   {">" if puzzle[channe_id]['kod']['тумбочка'] == 2 else "  "} {caskets[puzzle[channe_id]['kod']['тумбочка2']]}   {">" if puzzle[channe_id]['kod']['тумбочка'] == 3 else "  "} {caskets[puzzle[channe_id]['kod']['тумбочка3']]}   {">" if puzzle[channe_id]['kod']['тумбочка'] == 4 else "   "} {caskets[puzzle[channe_id]['kod']['тумбочка4']]}
|   ﹀    ﹀ {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] else " "} ﹀   {"  " if caskets[puzzle[channe_id]['kod']['тумбочка1']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка2']] in ["2", "3", "4", "5"] and caskets[puzzle[channe_id]['kod']['тумбочка3']] in ["2", "3", "4", "5"] else " "}﹀                                                       
""")
                            return
                        
                        elif puzzle[channe_id]['kod']['kod'] == 2:
                            await interaction.response.edit_message(content=f"""
{f"__{clock1[puzzle[channe_id]['kod']['часи1']]}__" if puzzle[channe_id]['kod']['часи'] == 1 else clock1[puzzle[channe_id]['kod']['часи1']]}{f"__{clock2[puzzle[channe_id]['kod']['часи2']]}__" if puzzle[channe_id]['kod']['часи'] == 2 else clock2[puzzle[channe_id]['kod']['часи2']]}:{f"__{clock3[puzzle[channe_id]['kod']['часи3']]}__" if puzzle[channe_id]['kod']['часи'] == 3 else clock3[puzzle[channe_id]['kod']['часи3']]}{f"__{clock4[puzzle[channe_id]['kod']['часи4']]}__" if puzzle[channe_id]['kod']['часи'] == 4 else clock4[puzzle[channe_id]['kod']['часи4']]}
""")
                            return
                        
                        elif puzzle[channe_id]['kod']['kod'] == 3:
                            games3 = ""
                            for game3 in range(1, 7):
                                games3 += f"{f">{box1[puzzle[channe_id]['kod'][f'1ящик{game3}']]}<" if puzzle[channe_id]['kod']['1ящик'] == game3 else box1[puzzle[channe_id]['kod'][f'1ящик{game3}']]}"
                            await interaction.response.edit_message(content=f"""
)--{games3}--(
""")    
                            return

                        elif puzzle[channe_id]['kod']['kod'] == 4:
                            games4 = ""
                            for game4 in range(1, 7):
                                games4 += f"{f">{box2[puzzle[channe_id]['kod'][f'2ящик{game4}']]}<" if puzzle[channe_id]['kod']['2ящик'] == game4 else box2[puzzle[channe_id]['kod'][f'2ящик{game4}']]}"
                            await interaction.response.edit_message(content=f"""
)--{games4}--(
""") 
                            return

                        elif puzzle[channe_id]['kod']['kod'] == 5:
                            games5 = ""
                            for game5 in range(1, 7):
                                games5 += f"{f">{box3[puzzle[channe_id]['kod'][f'3ящик{game5}']]}<" if puzzle[channe_id]['kod']['3ящик'] == game5 else box3[puzzle[channe_id]['kod'][f'3ящик{game5}']]}"
                            await interaction.response.edit_message(content=f"""
)--{games5}--(
""")   
                            return
                            

                    elif interaction.data['custom_id'] == "телевизор1":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)                        
                        if "изолента" in puzzle[channe_id]['players'][player_2]['item']:
                            puzzle[channe_id]['players'][player_2]['item'].remove("изолента")
                            puzzle[channe_id]['home']['телевизор1'] = False
                            await interaction.response.edit_message(content=f"Обмотав кабель изолентой, мне удалось его починить, но телевизор всё равно не заработал. **Время и до него дойдёт,** — подумал я, отходя от него.", view=view_player2)
                        else:
                            await interaction.response.edit_message(content=f"Мне нужно найти изоленту. Где же начать искать? Хммм...", view=view_player2)


                    elif interaction.data['custom_id'] == "часи1":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        view_player2.add_item(button_caskets1)
                        view_player2.add_item(button_caskets5)
                        view_player2.add_item(button_caskets2)
                        view_player2.add_item(button_caskets3)
                        view_player2.add_item(button_caskets4)
                        puzzle[channe_id]['kod']['kod'] = 2
                        await interaction.response.edit_message(content=f"""
{f"__{clock1[puzzle[channe_id]['kod']['часи1']]}__" if puzzle[channe_id]['kod']['часи'] == 1 else clock1[puzzle[channe_id]['kod']['часи1']]}{f"__{clock2[puzzle[channe_id]['kod']['часи2']]}__" if puzzle[channe_id]['kod']['часи'] == 2 else clock2[puzzle[channe_id]['kod']['часи2']]}:{f"__{clock3[puzzle[channe_id]['kod']['часи3']]}__" if puzzle[channe_id]['kod']['часи'] == 3 else clock3[puzzle[channe_id]['kod']['часи3']]}{f"__{clock4[puzzle[channe_id]['kod']['часи4']]}__" if puzzle[channe_id]['kod']['часи'] == 4 else clock4[puzzle[channe_id]['kod']['часи4']]}
""", view=view_player2)

                    elif interaction.data['custom_id'] == "ящик1":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        if puzzle[channe_id]['home']['1ящик']:
                            view_player2.add_item(button_caskets1)
                            view_player2.add_item(button_caskets5)
                            view_player2.add_item(button_caskets2)
                            view_player2.add_item(button_caskets3)
                            view_player2.add_item(button_caskets4)
                            puzzle[channe_id]['kod']['kod'] = 3
                            games3 = ""
                            for game3 in range(1, 7):
                                games3 += f"{f">{box1[puzzle[channe_id]['kod'][f'1ящик{game3}']]}<" if box1[puzzle[channe_id]['kod']['1ящик']] == game3 else box1[puzzle[channe_id]['kod'][f'1ящик{game3}']]}"
                            await interaction.response.edit_message(content=f"""
)--{games3}--(
""", view=view_player2)
                        else:                      
                            await interaction.response.edit_message(content=f"Осмотрев открытый ящик, я ничего нового не заметил.", view=view_player2)                       

                    elif interaction.data['custom_id'] == "ящик2":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        if puzzle[channe_id]['home']['2ящик']:
                            view_player2.add_item(button_caskets1)
                            view_player2.add_item(button_caskets5)
                            view_player2.add_item(button_caskets2)
                            view_player2.add_item(button_caskets3)
                            view_player2.add_item(button_caskets4)
                            puzzle[channe_id]['kod']['kod'] = 4
                            games4 = ""
                            for game4 in range(1, 7):
                                games4 += f"{f">{box2[puzzle[channe_id]['kod'][f'2ящик{game4}']]}<" if box2[puzzle[channe_id]['kod']['2ящик']] == game4 else box2[puzzle[channe_id]['kod'][f'2ящик{game4}']]}"
                            await interaction.response.edit_message(content=f"""
)--{games4}--(
""", view=view_player2)
                        else:                      
                            await interaction.response.edit_message(content=f"Осматривая открытый ящик, я ничего нового не обнаружил: тот же символ **Х** и больше ничего.", view=view_player2)

                    elif interaction.data['custom_id'] == "ящик3":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        if puzzle[channe_id]['home']['3ящик']:
                            view_player2.add_item(button_caskets1)
                            view_player2.add_item(button_caskets5)
                            view_player2.add_item(button_caskets2)
                            view_player2.add_item(button_caskets3)
                            view_player2.add_item(button_caskets4)
                            puzzle[channe_id]['kod']['kod'] = 5
                            games5 = ""
                            for game5 in range(1, 7):
                                games5 += f"{f">{box3[puzzle[channe_id]['kod'][f'3ящик{game5}']]}<" if box3[puzzle[channe_id]['kod']['3ящик']] == game5 else box3[puzzle[channe_id]['kod'][f'3ящик{game5}']]}"
                            await interaction.response.edit_message(content=f"""
)--{games5}--(
""", view=view_player2)
                        else:                      
                            await interaction.response.edit_message(content=f"1", view=view_player2)

                    elif interaction.data['custom_id'] == "страница ?":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        await interaction.response.edit_message(content=f"1", view=view_player2)

                    elif interaction.data['custom_id'] == "лист бумаги":
                        view_player2.clear_items()
                        view_player2.add_item(button_N)
                        await interaction.response.edit_message(content=f"1", view=view_player2)

                    elif interaction.data['custom_id'] == "тgdgd":
                        puzzle[channe_id]['home']['буфет'] = False
                        view_player2.clear_items()
                        view_player2.add_item(button_N)


                async def Puzzle1(interaction: discord.Interaction):
                    
                    if 'values' not in interaction.data:
                        if interaction.data['custom_id'] == "R":
                            if puzzle[channe_id]['info']['player'] == 1:
                                puzzle[channe_id]['info']['player'] = 2
                                view_player2.remove_item(select1)
                                view_player2.add_item(select2)
                                await interaction.response.edit_message(content=f"Обернувшись, я увидел довольно похожую картину: старый телефон, по которому общаюсь с тобой, и какую-то странную дверь, видимо, закрытую.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 2:
                                puzzle[channe_id]['info']['player'] = 3
                                view_player2.remove_item(select2)
                                view_player2.add_item(select3)
                                await interaction.response.edit_message(content=f"В темноте была видна какая-то картина, старые часы, будто пришедшие из 50-х годов, и несколько ящиков, стоящих друг на друге.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 3:
                                puzzle[channe_id]['info']['player'] = 1
                                view_player2.remove_item(select3)
                                view_player2.add_item(select1)
                                await interaction.response.edit_message(content=f"В комнате не было ничего особенного: просто пустая комната с картиной на стене, огромным буфетом и телевизором на тумбочке в углу.", view=view_player2)

                        elif interaction.data['custom_id'] == "L":
                            if puzzle[channe_id]['info']['player'] == 1:
                                puzzle[channe_id]['info']['player'] = 3
                                view_player2.remove_item(select1)
                                view_player2.add_item(select3)
                                await interaction.response.edit_message(content=f"В темноте была видна какая-то картина, старые часы, будто пришедшие из 50-х годов, и несколько ящиков, стоящих друг на друге.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 2:
                                puzzle[channe_id]['info']['player'] = 1
                                view_player2.remove_item(select2)
                                view_player2.add_item(select1)
                                await interaction.response.edit_message(content=f"В комнате не было ничего особенного: просто пустая комната с картиной на стене, огромным буфетом и телевизором на тумбочке в углу.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 3:
                                puzzle[channe_id]['info']['player'] = 2
                                view_player2.remove_item(select3)
                                view_player2.add_item(select2)
                                await interaction.response.edit_message(content=f"Обернувшись, я увидел довольно похожую картину: старый телефон, по которому общаюсь с тобой, и какую-то странную дверь, видимо, закрытую.", view=view_player2)

                        elif interaction.data['custom_id'] == "item":
                            item = "" 
                            if puzzle[channe_id]['players'][player_2]['item'] == []:
                                item += "*пусто*\n" 
                            else:
                                for items in puzzle[channe_id]['players'][player_2]['item']:
                                    item += f"*{items}*\n"
                                
                            view_player2.clear_items()
                            view_player2.add_item(button_N)
                            if "страница ?" in puzzle[channe_id]['players'][player_2]['item']:
                                view_player2.add_item(button11)
                            elif "лист бумаги" in puzzle[channe_id]['players'][player_2]['item']:
                                view_player2.add_item(button12)
                            await interaction.response.edit_message(content=f"Ваши предметы:\n\n{item}.", view=view_player2)

                        elif interaction.data['custom_id'] == "N":
                            view_player2.clear_items()
                            view_player2.add_item(button_L)
                            view_player2.add_item(button_item)
                            view_player2.add_item(button_R)
                            
                            if puzzle[channe_id]['info']['player'] == 1:
                                view_player2.add_item(select1)
                                await interaction.response.edit_message(content=f"В комнате не было ничего особенного: просто пустая комната с картиной на стене, огромным буфетом и телевизором на тумбочке в углу.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 2:
                                view_player2.add_item(select2)
                                await interaction.response.edit_message(content=f"Обернувшись, я увидел довольно похожую картину: старый телефон, по которому общаюсь с тобой, и какую-то странную дверь, видимо, закрытую.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 3:
                                view_player2.add_item(select3)
                                await interaction.response.edit_message(content=f"В темноте была видна какая-то картина, старые часы, будто пришедшие из 50-х годов, и несколько ящиков, стоящих друг на друге.", view=view_player2)                    

                    else:
                        ##### обще
                        if interaction.data['values'][0] == "Картина":
                            if puzzle[channe_id]['info']['player'] == 1:
                                view_player2.clear_items()
                                view_player2.add_item(button_N)
                                await interaction.response.edit_message(content=f"Хм, интересная картина, но что-то казалось не так: какие-то (символи) символы вообще не вписывались в общую композицию.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 2:
                                view_player2.clear_items()
                                view_player2.add_item(button_N)                               
                                await interaction.response.edit_message(content=f"Эта картина точь-в-точь как первая, но здесь (символи) символы совершенно другие. Странно.", view=view_player2)

                            elif puzzle[channe_id]['info']['player'] == 3:
                                view_player2.clear_items()
                                view_player2.add_item(button_N)                                
                                await interaction.response.edit_message(content=f"А на этой вообще ничего нет, только белый лист бумаги. Что же это может означать? Хотя нет, в углу присутствуют два (символи) символа.", view=view_player2)
                    
                        ##### комната 1
                        elif interaction.data['values'][0] == "буфет":
                            view_player2.clear_items()
                            view_player2.add_item(button_N)
                            if puzzle[channe_id]['home']['буфет']:
                                view_player2.add_item(button1)
                                await interaction.response.edit_message(content=f"Приблизившись к огромному буфету, я даже не ожидал, что открою его, но желание узнать, что внутри, было сильнее.", view=view_player2)
                            else:
                                await interaction.response.edit_message(content=f"Снова вернувшись к буфету, я ничего нового не обнаружил — просто пыльный буфет, которому, вероятно, не меньше 100 лет. Думаю, нужно искать в другом месте.", view=view_player2)

                        elif interaction.data['values'][0] == "тумбочка":
                            view_player2.clear_items()
                            view_player2.add_item(button2)
                            view_player2.add_item(button3)
                            view_player2.add_item(button4)
                            view_player2.add_item(button_N)
                            await interaction.response.edit_message(content=f"Подойдя к тумбочке, я заметил телевизор, стоящий на ней. Но его я осмотрю позже; сначала нужно проверить саму тумбочку.", view=view_player2)
             
                        elif interaction.data['values'][0] == "телевизор":
                            view_player2.clear_items()
                            view_player2.add_item(button_N)
                            if puzzle[channe_id]['home']['телевизор1']:
                                view_player2.add_item(button6)
                                await interaction.response.edit_message(content=f"Подойдя ближе к телевизору, я попробовал его включить, но ничего не вышло. Видимо, что-то с ним случилось, подумал я. Осмотрев телевизор, я заметил, что кабель был повреждён. Нужно найти изоленту.", view=view_player2)
                            else:
                                if puzzle[channe_id]['home']['телевизор2']:
                                    await interaction.response.edit_message(content=f"2", view=view_player2)
                                else:
                                    await interaction.response.edit_message(content=f"Смотря на телевизор, я ничего не замечал: вроде работает, но ничего не показывает. Может, просто не его время.", view=view_player2)

                        
                        ##### комната 2
                        elif interaction.data['values'][0] == "Телефон":
                            view_player2.clear_items()
                            view_player2.add_item(button_N)
                            await interaction.response.edit_message(content=f"Подойдя к телефону, я решил поинтересоваться у друга о его успехах с расшифровкой символов. *Ну как успехи?* — спросил я. В ответ услышал: *Да нормально, всё ищу.*", view=view_player2)

                        elif interaction.data['values'][0] == "буфет11":
                            view_player2.clear_items()
                            view_player2.add_item(button_N)

                        ##### комната 3
                        elif interaction.data['values'][0] == "старые часи":
                            view_player2.clear_items()
                            view_player2.add_item(button_N)
                            if puzzle[channe_id]['home']['старые часи']:
                                view_player2.add_item(button7)
                                await interaction.response.edit_message(content=f"Хм... смотря на время {clock1[puzzle[channe_id]['kod']['часи1']]}{clock2[puzzle[channe_id]['kod']['часи2']]}:{clock3[puzzle[channe_id]['kod']['часи3']]}{clock4[puzzle[channe_id]['kod']['часи4']]}, я не могу понять, кто же всё это устроил?", view=view_player2)
                                return
                            if "годиная стрелка" in puzzle[channe_id]['players'][player_2]['item']:
                                puzzle[channe_id]['players'][player_2]['item'].remove("годиная стрелка")
                                view_player2.add_item(button7)
                                puzzle[channe_id]['home']['старые часи'] = True
                                await interaction.response.edit_message(content=f"Поставив часовую стрелку на своё место, я теперь имею доступ к часам. Но зачем мне это?", view=view_player2)
                            else:
                                await interaction.response.edit_message(content=f"Подойдя к старым часам, я посмотрел на время: 00:??. Видимо, часовая стрелка пропала. Нужно попытаться её найти — может, это ключ к выходу?", view=view_player2)
                        
                        elif interaction.data['values'][0] == "ящики":
                            view_player2.clear_items()
                            view_player2.add_item(button8)
                            view_player2.add_item(button9)
                            view_player2.add_item(button10)
                            view_player2.add_item(button_N)
                            await interaction.response.edit_message(content=f"Подойдя к ящикам, я заметил, что они все находятся под кодовым замком. Вопрос в том, с какого начать?", view=view_player2)

                ##### кнопки меню
                button_R = Button(emoji="➡️", style=discord.ButtonStyle.blurple, custom_id="R")
                button_item = Button(emoji="🎒", style=discord.ButtonStyle.blurple, custom_id="item")
                button_L = Button(emoji="⬅️", style=discord.ButtonStyle.blurple, custom_id="L")
                button_N = Button(emoji="⬇️", style=discord.ButtonStyle.blurple, custom_id="N")

                ##### кнопки действия
                button1 = Button(label="открыть буфет", style=discord.ButtonStyle.green, custom_id="буфет1")
                button2 = Button(emoji="1️⃣", style=discord.ButtonStyle.blurple, custom_id="тумбочка1")
                button3 = Button(emoji="2️⃣", style=discord.ButtonStyle.blurple, custom_id="тумбочка2")
                button4 = Button(emoji="3️⃣", style=discord.ButtonStyle.blurple, custom_id="тумбочка3")
                button5 = Button(label="осмотреть шкатулку", style=discord.ButtonStyle.green, custom_id="тумбочка11")
                button6 = Button(label="поченить телевизор", style=discord.ButtonStyle.green, custom_id="телевизор1")
                button7 = Button(label="посмотреть часи", style=discord.ButtonStyle.green, custom_id="часи1")
                button8 = Button(emoji="1️⃣", style=discord.ButtonStyle.blurple, custom_id="ящик1")
                button9 = Button(emoji="2️⃣", style=discord.ButtonStyle.blurple, custom_id="ящик2")
                button10 = Button(emoji="3️⃣", style=discord.ButtonStyle.blurple, custom_id="ящик3")
                button11 = Button(label="страница ?", style=discord.ButtonStyle.green, custom_id="страница ?")
                button12 = Button(label="лист бумаги", style=discord.ButtonStyle.green, custom_id="лист бумаги")
                # button = Button(emoji="", style= , custom_id="")

                ##### кнопки кода
                button_caskets1 = Button(emoji="⬆️", style=discord.ButtonStyle.blurple, custom_id="caskets1")
                button_caskets2 = Button(emoji="⬅️", style=discord.ButtonStyle.blurple, custom_id="caskets2", row=2)
                button_caskets3 = Button(emoji="⬇️", style=discord.ButtonStyle.blurple, custom_id="caskets3", row=2)
                button_caskets4 = Button(emoji="➡️", style=discord.ButtonStyle.blurple, custom_id="caskets4", row=2)
                button_caskets5 = Button(emoji="☑️", style=discord.ButtonStyle.green, custom_id="caskets5")
                
                ##### каталоги
                options1 = [
                    discord.SelectOption(label="Картина"),
                    discord.SelectOption(label="буфет"),
                    discord.SelectOption(label="тумбочка"),
                    discord.SelectOption(label="телевизор")
                    ] # 4/4
                options2 = [
                    discord.SelectOption(label="Картина"),
                    discord.SelectOption(label="Закрытая дверь"),
                    discord.SelectOption(label="Телефон")
                    ] # 2/3
                options3 = [
                    discord.SelectOption(label="Картина"),
                    discord.SelectOption(label="старые часи"),
                    discord.SelectOption(label="ящики")
                    ] # 3/3

                select1 = discord.ui.Select(
                        placeholder="выберите предмет",
                        min_values=1,
                        max_values=1,
                        options=options1
                                            )
                select2 = discord.ui.Select(
                        placeholder="выберите предмет",
                        min_values=1,
                        max_values=1,
                        options=options2
                                            )
                select3 = discord.ui.Select(
                        placeholder="выберите предмет",
                        min_values=1,
                        max_values=1,
                        options=options3
                                            )
                
                button_R.callback = Puzzle1
                button_item.callback = Puzzle1
                button_L.callback = Puzzle1
                button_N.callback = Puzzle1
                select1.callback = Puzzle1
                select2.callback = Puzzle1
                select3.callback = Puzzle1
                
                button1.callback = Puzzle2
                button2.callback = Puzzle2
                button3.callback = Puzzle2
                button4.callback = Puzzle2
                button5.callback = Puzzle2
                button6.callback = Puzzle2
                button7.callback = Puzzle2
                button8.callback = Puzzle2
                button9.callback = Puzzle2
                button10.callback = Puzzle2
                button11.callback = Puzzle2
                button12.callback = Puzzle2

                button_caskets1.callback = Puzzle2
                button_caskets2.callback = Puzzle2
                button_caskets3.callback = Puzzle2
                button_caskets4.callback = Puzzle2
                button_caskets5.callback = Puzzle2

                view_player2 = View(timeout=None)
                view_player2.add_item(button_L)
                view_player2.add_item(button_item)
                view_player2.add_item(button_R)
                
        
                if puzzle[channe_id]['info']['player'] == 1:
                    view_player2.add_item(select1)
                    if interaction.data['custom_id'] == "start":
                        await interaction.response.send_message(f"В комнате не было ничего особенного: просто пустая комната с картиной на стене, огромным буфетом и телевизором на тумбочке в углу.", ephemeral=True, view=view_player2)
                    else:
                        await interaction.response.edit_message(content=f"В комнате не было ничего особенного: просто пустая комната с картиной на стене, огромным буфетом и телевизором на тумбочке в углу.", view=view_player2)

                elif puzzle[channe_id]['info']['player'] == 2:
                    view_player2.add_item(select2)
                    if interaction.data['custom_id'] == "start":
                        await interaction.response.send_message(f"Обернувшись, я увидел довольно похожую картину: старый телефон, по которому общаюсь с тобой, и какую-то странную дверь, видимо, закрытую.", ephemeral=True, view=view_player2)
                    else:
                        await interaction.response.edit_message(content=f"Обернувшись, я увидел довольно похожую картину: старый телефон, по которому общаюсь с тобой, и какую-то странную дверь, видимо, закрытую.", view=view_player2)

                elif puzzle[channe_id]['info']['player'] == 3:
                    view_player2.add_item(select3)
                    if interaction.data['custom_id'] == "start":
                        await interaction.response.send_message(f"В темноте была видна какая-то картина, старые часы, будто пришедшие из 50-х годов, и несколько ящиков, стоящих друг на друге.", ephemeral=True, view=view_player2)
                    else:
                        await interaction.response.edit_message(content=f"В темноте была видна какая-то картина, старые часы, будто пришедшие из 50-х годов, и несколько ящиков, стоящих друг на друге.", view=view_player2)
                    
        
        button_start = Button(emoji=f"▶️", style=discord.ButtonStyle.blurple, custom_id="start")
        button_start.callback = chat
        
        view_start = View(timeout=None)
        view_start.add_item(button_start)

        await interaction.response.edit_message(content="игра началась!", view=view_start)
 
    async def add_player(interaction: discord.Interaction):
        interaction1 = interaction.message.id
        member = interaction.user.id

        if channe_id in puzzle:
            if member in puzzle[channe_id]['players']:
                await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
                return
            
            if len(puzzle[channe_id]['players']) > 1:
                await interaction.response.send_message("комната занята", ephemeral=True)
            else:
                puzzle[channe_id]['players'][member] = {"point": 0, "item": []}
                await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
                add_pley_button.disabled = True
                start_button.disabled = False
                await interaction.followup.edit_message(content=f"{tekst.Puzzle}\n2 Игроков в ожидании", message_id=interaction1, view=view)
        else:
            puzzle[channe_id] = {
                'players': {member: {"point": 0, "item": []}},
                "info": {"player": None, "id1": None, "id2": None},
                "home": {"буфет": True, "тумбочка1": True, "тумбочка2": True, "телевизор1": True, "телевизор2": True,
                         "старые часи": False, "старые час": False, "1ящик": True, "2ящик": True, "3ящик": True
                         },
                "kod": {"kod": 0,
                        "тумбочка1": 0, "тумбочка2": 0, "тумбочка3": 0, "тумбочка4": 0, "тумбочка": 1,
                        "часи1": 0, "часи2": 0, "часи3": 0, "часи4": 0, "часи": 1,
                        "1ящик1": 0, "1ящик2": 0, "1ящик3": 0, "1ящик4": 0, "1ящик5": 0, "1ящик6": 0, "1ящик": 1,
                        "2ящик1": 0, "2ящик2": 0, "2ящик3": 0, "2ящик4": 0, "2ящик5": 0, "2ящик6": 0, "2ящик": 1,
                        "3ящик1": 0, "3ящик2": 0, "3ящик3": 0, "3ящик4": 0, "3ящик5": 0, "3ящик6": 0, "3ящик": 1
                    }
                }
            
            await interaction.response.send_message("вы создали комнату", ephemeral=True)
            await interaction.followup.edit_message(content=f"{tekst.Puzzle}\n1 Игрок в ожидании", message_id=interaction1)


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
                del puzzle[channe_id]
            except:
                pass
            
    self.client.loop.create_task(timeout_callback()) 

    start_button.disabled = True
    await interaction.response.send_message(tekst.Puzzle, view=view)

##############################
    ########## ? ####################
#######################################################

#   @app_commands.command(name="test", description="test")
#   async def Hangman(self, interaction: discord.Interaction):

#     if interaction.guild is None:
#         await interaction.response.send_message(tekst.DM)
#         return
#     if config.Hangman == False:
#         await interaction.response.send_message(tekst.nots)
#         return
    
#     channe_id = interaction.channel_id

#     if channe_id in hangman:
#         await interaction.response.send_message(f":x: | комната занята", ephemeral=True)
#         return

#     async def game_start(interaction: discord.Interaction):
#         stop_event.set()
        
#         await interaction.response.edit_message(content="Загадиваю слово..", view=None)
#         await asyncio.sleep(5)

#         await interaction.delete_original_response()
#         id = await interaction.followup.send("Загадиваю слово...")
#         hangman[channe_id]['info']['id'] = id.id

#         keys = list(hangman[channe_id]['players'].keys())
#         player_1 = keys[0]
#         player_2 = keys[1]

#         text = random.choice(Hangman.text)

        
#     async def add_player(interaction: discord.Interaction):
#         interaction1 = interaction.message.id
#         member = interaction.user.id

#         if channe_id in hangman:
#             if member in hangman[channe_id]['players']:
#                 await interaction.response.send_message("вы уже вошли в комнату", ephemeral=True)
#                 return
            
#             if len(hangman[channe_id]['players']) > 1:
#                 await interaction.response.send_message("комната занята", ephemeral=True)
#             else:
#                 hangman[channe_id]['players'][member] = {"point": 0}
#                 await interaction.response.send_message("вы вошли в комнату", ephemeral=True)
#                 add_pley_button.disabled = True
#                 start_button.disabled = False
#                 await interaction.followup.edit_message(content=f"3\n2 Игроков в ожидании", message_id=interaction1, view=view)
#         else:
#             hangman[channe_id] = {'players': {member: {"point": 0}}, "info": {"player": None, "id": None}}
#             await interaction.response.send_message("вы создали комнату", ephemeral=True)
#             await interaction.followup.edit_message(content="2\n1 Игрок в ожидании", message_id=interaction1)


#     async def info(interaction: discord.Interaction):
#         await interaction.response.send_message("test", ephemeral=True)

#     start_button = Button(emoji=f"▶️", style=discord.ButtonStyle.green)
#     button_info = Button(emoji=f"❓", style=discord.ButtonStyle.green)
#     add_pley_button = Button(emoji=f"➕", style=discord.ButtonStyle.blurple)

#     start_button.callback = game_start
#     add_pley_button.callback = add_player
#     button_info.callback = info

#     view = View(timeout=180)
#     view.add_item(start_button)
#     view.add_item(add_pley_button)
#     view.add_item(button_info)
#     stop_event = asyncio.Event()

#     async def timeout_callback():
#         try:
#             await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
#         except asyncio.TimeoutError:
#             try:
#                 del hangman[channe_id]
#             except:
#                 pass
            
#     self.client.loop.create_task(timeout_callback()) 

#     start_button.disabled = True
#     await interaction.response.send_message("1", view=view)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(fun(client))
