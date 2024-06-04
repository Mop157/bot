import asyncio
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import json
import random
import functools
import os
import datetime
from typing import Union  
import time
import schedule
import aioschedule



        
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.reactions = True

user_behavior = {}

last_command_usage = {}

allowed_user_ids = [670163392979271710, 943154656014659595]

# Каналы, в которых бот НЕ будет работать (репутауия)
IGNORED_CHANNELS = [123456789012345678, 987654321098765432]

def is_allowed_user(ctx):
    return ctx.author.id in allowed_user_ids


current_directory = os.path.dirname(os.path.abspath(__file__))

GOOD_FILE_PATH = os.path.join(current_directory, "config", "Good.py")
BAD_FILE_PATH = os.path.join(current_directory, "config", "bad.py")
values_file_path_1 = os.path.join(current_directory, "config", "text.py")

with open(values_file_path_1, "r", encoding="utf-8") as file:
    exec(file.read())



bot = commands.Bot(command_prefix="!", intents=intents)



async def setup_views():
    await bot.wait_until_ready()
    
    global view1
    view1 = View()



@bot.event
async def on_ready():
    print(f'Бот вошёл как {bot.user.name}')
    await setup_views()
    check_behavior.start()
    daily_reset.start()
    


    
@bot.command(name='test_point', help='Тестирование обработки событий')
async def process_test_command(ctx):
    print("Запуск тестовой команды !test_point:")
    await process_users()
    


@bot.command(name='test_events', help='Тестирование обработки событий')
async def test_events(ctx):
    print("Тестирование обработки событий:")
    await process_events()
    print("Тестирование завершено.")

    
@bot.command(name='test_user')
async def check_user_behavior(ctx, user: discord.User = None):
    user = user or ctx.author
    user_id = str(user.id)
    behavior_data = user_behavior.get(user_id, {'good_points': 0, 'bad_points': 0, 'message_count': 0, 'reaction_count': 0})
    await ctx.send(f'{user.mention}, ваш поведенческий счет: Хороших поинтов - {behavior_data["good_points"]}, Плохих поинтов - {behavior_data["bad_points"]}, Количество сообщений - {behavior_data["message_count"]}, Количество реакций - {behavior_data["reaction_count"]}')

    

POINTS_FILE_PATH = 'Good.json'



# Лимит поинтов в день
DAILY_POINTS_LIMIT_GOOD = 10
DAILY_POINTS_LIMIT_BAD = 15

# Лимит реакций в сообщении для выдачи плохого поинта
REACTION_LIMIT = 10









    


@tasks.loop(hours=1)
async def check_behavior():
    for user_id, data in user_behavior.items():
        user_behavior[user_id]['message_count'] = 0  # Обнуляем счетчик сообщений
        user_behavior[user_id]['reaction_count'] = 0  # Обнуляем счетчик реакций
        if data['good_points'] >= DAILY_POINTS_LIMIT_GOOD:
            user_behavior[user_id]['good_points'] = DAILY_POINTS_LIMIT_GOOD
        if data['bad_points'] >= DAILY_POINTS_LIMIT_BAD:
            user_behavior[user_id]['bad_points'] = DAILY_POINTS_LIMIT_BAD
        check_message_count(user_id)  # Добавлен вызов функции проверки message_count
        check_reaction_count(user_id)  # Добавлен вызов функции проверки reaction_count
    save_to_file()

@tasks.loop(hours=24)
async def daily_reset():
    for user_id, data in user_behavior.items():
        if data['bad_points'] > 0 and data['good_points'] > 0:
            diff = min(data['good_points'], data['bad_points'])
            user_behavior[user_id]['good_points'] -= diff
            user_behavior[user_id]['bad_points'] -= diff
    save_to_file()

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id in IGNORED_CHANNELS:
        return

    user_id = str(message.author.id)

    if user_id not in user_behavior:
        user_behavior[user_id] = {'good_points': 0, 'bad_points': 0, 'message_count': 0, 'reaction_count': 0, 'last_points_reset': datetime.datetime.utcnow()}  # Заменено

    # Проверка лимита хороших поинтов
    current_time = datetime.datetime.utcnow()  # Заменено
    time_since_reset = current_time - user_behavior[user_id]['last_points_reset']
    if time_since_reset.days >= 1:
        user_behavior[user_id]['good_points'] = 0  # Обнуляем хорошие поинты
        user_behavior[user_id]['last_points_reset'] = current_time  # Обновляем время последнего сброса

    # Проверка лимита плохих поинтов
    if user_behavior[user_id]['bad_points'] < DAILY_POINTS_LIMIT_BAD:
        # Поиск хороших слов в файле Good.py
        with open(GOOD_FILE_PATH, 'r') as good_file:
            good_words = [line.strip() for line in good_file]

        for word in good_words:
            if word.lower() in message.content.lower():
                user_behavior[user_id]['good_points'] += 1
                

    # Проверка лимита плохих поинтов
    if user_behavior[user_id]['bad_points'] < DAILY_POINTS_LIMIT_BAD:
        # Поиск плохих слов в файле bad.py
        with open(BAD_FILE_PATH, 'r') as bad_file:
            bad_words = [line.strip() for line in bad_file]

        for word in bad_words:
            if word.lower() in message.content.lower():
                user_behavior[user_id]['bad_points'] += 1
                

    user_behavior[user_id]['message_count'] += 1

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user or reaction.message.channel.id in IGNORED_CHANNELS:
        return

    user_id = str(user.id)

    # Добавление плохого поведения при множественных реакциях
    if reaction.count >= 5 and user_behavior[user_id]['bad_points'] < DAILY_POINTS_LIMIT_BAD:
        user_behavior[user_id]['bad_points'] += 1
        user_behavior[user_id]['message_count'] = 0  # Обнуляем счетчик сообщений
        

    # Счетчик реакций под сообщением
    user_behavior[user_id]['reaction_count'] += 1
    check_reaction_count(user_id)  # Добавлен вызов функции проверки reaction_count


def save_to_file():
    with open(POINTS_FILE_PATH, 'w') as file:
        user_behavior_serializable = {
            user_id: {
                key: value.strftime('%Y-%m-%d %H:%M:%S.%f') if isinstance(value, datetime.datetime) else value
                for key, value in data.items()
            }
            for user_id, data in user_behavior.items()
        }
        json.dump(user_behavior_serializable, file)

def load_from_file():
    try:
        with open(POINTS_FILE_PATH, 'r') as file:
            user_behavior_loaded = json.load(file)
            for user_id, data in user_behavior_loaded.items():
                data['last_points_reset'] = datetime.datetime.strptime(data['last_points_reset'], '%Y-%m-%d %H:%M:%S.%f')
            return user_behavior_loaded
    except FileNotFoundError:
        return {}

def check_message_count(user_id):
    if user_behavior[user_id]['message_count'] >= 1500 and user_behavior[user_id]['bad_points'] < DAILY_POINTS_LIMIT_BAD:
        user_behavior[user_id]['bad_points'] += 1
        user_behavior[user_id]['message_count'] = 0  # Обнуляем счетчик сообщений

def check_reaction_count(user_id):
    if user_behavior[user_id]['reaction_count'] >= REACTION_LIMIT and user_behavior[user_id]['bad_points'] < DAILY_POINTS_LIMIT_BAD:
        user_behavior[user_id]['bad_points'] += 1
        user_behavior[user_id]['reaction_count'] = 0  # Обнуляем счетчик реакций




@bot.command(name='shop')
async def shop_command(ctx, *args):
    allowed_channel_id = 1188195686374703214
    if ctx.channel.id == allowed_channel_id:
        # Ваш код для выполнения команды "shop" здесь
        channel = bot.get_channel(allowed_channel_id)
    else:
        await ctx.send("Эта команда доступна только в определенном канале.")




    
        
    async def menu1_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '1':
                await interaction.response.send_message(content=s1, ephemeral=True, view=view1_1)
            elif selected_option == '2':
                await interaction.response.send_message(content=s2, ephemeral=True, view=view1_2)
                
    
    async def button_callback1(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя необходимая валюта
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        if user_id not in balances or balances[user_id] < 10000:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты.", ephemeral=True)
            return
    
        # Проверяем, есть ли у пользователя роль
        for role in ctx.author.roles:
            if role.name == "Охотник":  # Замените "Название роли" на имя роли, которую вы хотите предоставить
                await interaction.response.send_message("Извиняюсь, вы уже купили роль.", ephemeral=True)
                return
    
        # Забираем у пользователя валюту
        balances[user_id] -= 10000
    
        # Выдаем пользователю роль
        role_to_add = discord.utils.get(ctx.guild.roles, name="Охотник")  # Замените "Название роли" на имя роли, которую вы хотите предоставить
        await ctx.author.add_roles(role_to_add)
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message("Вы успешно приобрели роль за 10000<:emoji_16:1185972508655095928> тенелитов.", ephemeral=True)


    async def button_callback2(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя одна из 5 ролей
        roles_to_currency = {
            "Запретник": 1200,
            "запретная тьма": 1200,
            "одержимый тенями": 1100,
            "повелитель теней": 900,
            "исследователь теней": 850,
            "лесной вестник": 750,
        }
    
        user_roles = [role.name for role in interaction.user.roles]
        eligible_roles = [role for role in user_roles if role in roles_to_currency]
    
        if not eligible_roles:
            await interaction.response.send_message("Извиняюсь, вы на 0 этапе", ephemeral=True)
            return
    
        # Сортируем роли от высшей к низшей
        sorted_roles = sorted(eligible_roles, key=lambda x: list(roles_to_currency.keys()).index(x))
    
        # Проверяем, есть ли у пользователя достаточно валюты
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        role_found = None
        for role_name in sorted_roles:
            if user_id in last_command_usage and user_id in balances and balances[user_id] >= roles_to_currency[role_name]:
                role_found = role_name
                break
    
        if role_found is None:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты или вы можете использовать охоту или работу", ephemeral=True)
            return
    
        # Удаляем пользователя из last_command_usage
        last_command_usage.pop(user_id)
    
        # Забираем у пользователя валюту
        balances[user_id] -= roles_to_currency[role_found]
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message(f"Вы успешно получили ключ от врат, можете использовать охоту или работу", ephemeral=True)


                
    async def menu2_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '01':
                await interaction.response.send_message(content=o1, ephemeral=True, view=view2_1)
            elif selected_option == '02':
                await interaction.response.send_message(content=o2, ephemeral=True, view=view2_2)
                
    async def button_callback01(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя валюта для обмена
        with open('Boll.json', 'r') as f1, open('Boll2.json', 'r') as f2:
            balances_boll = json.load(f1)
            balances_boll2 = json.load(f2)
    
        if user_id not in balances_boll2 or balances_boll2[user_id] < 1:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно леннефира для обмена.", ephemeral=True)
            return
    
        # Забираем у пользователя 1 валюту из Boll2.json
        balances_boll2[user_id] -= 1
    
        # Даем пользователю 3000 валют в Boll.json
        if user_id not in balances_boll:
            balances_boll[user_id] = 1500
        balances_boll[user_id] += 3000
    
        # Сохраняем обновленные балансы в файлах
        with open('Boll.json', 'w') as f1, open('Boll2.json', 'w') as f2:
            json.dump(balances_boll, f1)
            json.dump(balances_boll2, f2)
    
        await interaction.response.send_message("Обмен прошел успешно. Вы получили 3000<:emoji_16:1185972508655095928> тенелитов", ephemeral=True)

            
    async def button_callback02(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя одна из 5 ролей
        roles_to_currency = {
            "запретная тьма": 1200,
            "одержимый тенями": 1100,
            "повелитель теней": 900,
            "исследователь теней": 850,
            "лесной вестник": 750,
        }
    
        user_roles = [role.name for role in interaction.user.roles]
        eligible_roles = [role for role in user_roles if role in roles_to_currency]
    
        if not eligible_roles:
            await interaction.response.send_message("Извиняюсь, вы на 0 этапе", ephemeral=True)
            return
    
        # Сортируем роли от высшей к низшей
        sorted_roles = sorted(eligible_roles, key=lambda x: list(roles_to_currency.keys()).index(x))
    
        # Проверяем, есть ли у пользователя достаточно валюты
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        role_found = None
        for role_name in sorted_roles:
            if user_id in last_command_usage and user_id in balances and balances[user_id] >= roles_to_currency[role_name]:
                role_found = role_name
                break
    
        if role_found is None:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты или вы можете использовать охоту или работу", ephemeral=True)
            return
    
        # Удаляем пользователя из last_command_usage
        last_command_usage.pop(user_id)
    
        # Забираем у пользователя валюту
        balances[user_id] -= roles_to_currency[role_found]
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message(f"Вы успешно получили ключ от врат, можете использовать охоту или работу", ephemeral=True)


                
    async def menu3_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '001':
                await interaction.response.send_message(content=h1, ephemeral=True, view=view3_1)
            elif selected_option == '002':
                await interaction.response.send_message(content=h2, ephemeral=True, view=view3_2)
            elif selected_option == '003':
                await interaction.response.send_message(content=h3, ephemeral=True, view=view3_3)
                
    async def button_callback001(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя необходимая валюта
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        if user_id not in balances or balances[user_id] < 30000:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты.", ephemeral=True)
            return
    
        # Проверяем, есть ли у пользователя роль
        for role in ctx.author.roles:
            if role.name == "Фантом Охоты":  # Замените "Название роли" на имя роли, которую вы хотите предоставить
                await interaction.response.send_message("Извиняюсь, вы уже купили роль.", ephemeral=True)
                return
    
        # Забираем у пользователя валюту
        balances[user_id] -= 30000
    
        # Выдаем пользователю роль
        role_to_add = discord.utils.get(ctx.guild.roles, name="Фантом Охоты")  # Замените "Название роли" на имя роли, которую вы хотите предоставить
        await ctx.author.add_roles(role_to_add)
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message("Вы успешно приобрели роль за 30000<:emoji_16:1185972508655095928> тенелитов.", ephemeral=True)

    async def button_callback002(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя достаточно валюты для операции
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        if user_id not in balances or balances[user_id] < 30000:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты", ephemeral=True)
            return
    
        # Снимаем у пользователя 30000 валют из Boll.json
        balances[user_id] -= 30000
    
        # Проверяем, есть ли пользователь уже в файле rule.json
        with open('rule.json', 'r') as f_rule:
            rule_data = json.load(f_rule)
    
        if user_id in rule_data:
            await interaction.response.send_message("Вы уже имеете роль свою роль", ephemeral=True)
            return
    
        # Добавляем пользователя с ролью 'rule' в rule.json
        rule_data[user_id] = "rule"
    
        # Сохраняем обновленные балансы и данные ролей в файлах
        with open('Boll.json', 'w') as f1, open('rule.json', 'w') as f_rule:
            json.dump(balances, f1)
            json.dump(rule_data, f_rule)
    
        await interaction.response.send_message("вы успешно купили свою роль, пожалуйста используйте команду !rol в канале спим команд.", ephemeral=True)

    async def button_callback003(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя одна из 5 ролей
        roles_to_currency = {
            "запретная тьма": 1200,
            "одержимый тенями": 1100,
            "повелитель теней": 900,
            "исследователь теней": 850,
            "лесной вестник": 750,
        }
    
        user_roles = [role.name for role in interaction.user.roles]
        eligible_roles = [role for role in user_roles if role in roles_to_currency]
    
        if not eligible_roles:
            await interaction.response.send_message("Извиняюсь, вы на 0 этапе", ephemeral=True)
            return
    
        # Сортируем роли от высшей к низшей
        sorted_roles = sorted(eligible_roles, key=lambda x: list(roles_to_currency.keys()).index(x))
    
        # Проверяем, есть ли у пользователя достаточно валюты
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        role_found = None
        for role_name in sorted_roles:
            if user_id in last_command_usage and user_id in balances and balances[user_id] >= roles_to_currency[role_name]:
                role_found = role_name
                break
    
        if role_found is None:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты или вы можете использовать охоту или работу", ephemeral=True)
            return
    
        # Удаляем пользователя из last_command_usage
        last_command_usage.pop(user_id)
    
        # Забираем у пользователя валюту
        balances[user_id] -= roles_to_currency[role_found]
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message(f"Вы успешно получили ключ от врат, можете использовать охоту или работу", ephemeral=True)


                
    async def menu4_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '0001':
                await interaction.response.send_message(content=p1, ephemeral=True, view=view4_1)
            elif selected_option == '0002':
                await interaction.response.send_message(content=p2, ephemeral=True, view=view4_2)
                
    async def button_callback0001(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя необходимая валюта
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        if user_id not in balances or balances[user_id] < 20000:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты.", ephemeral=True)
            return
    
        # Проверяем, есть ли у пользователя роль
        for role in ctx.author.roles:
            if role.name == "Теневой Охотник":  # Замените "Название роли" на имя роли, которую вы хотите предоставить
                await interaction.response.send_message("Извиняюсь, вы уже купили роль.", ephemeral=True)
                return
    
        # Забираем у пользователя валюту
        balances[user_id] -= 20000
    
        # Выдаем пользователю роль
        role_to_add = discord.utils.get(ctx.guild.roles, name="Теневой Охотник")  # Замените "Название роли" на имя роли, которую вы хотите предоставить
        await ctx.author.add_roles(role_to_add)
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message("Вы успешно приобрели роль за 20000<:emoji_16:1185972508655095928> тенелитов.", ephemeral=True)

            
    async def button_callback0002(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя валюта для обмена
        with open('Boll.json', 'r') as f1, open('Boll2.json', 'r') as f2:
            balances_boll = json.load(f1)
            balances_boll2 = json.load(f2)
    
        if user_id not in balances_boll2 or balances_boll2[user_id] < 1:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно леннефира для обмена.", ephemeral=True)
            return
    
        # Забираем у пользователя 1 валюту из Boll2.json
        balances_boll2[user_id] -= 1
    
        # Даем пользователю 3000 валют в Boll.json
        if user_id not in balances_boll:
            balances_boll[user_id] = 1500
        balances_boll[user_id] += 3500
    
        # Сохраняем обновленные балансы в файлах
        with open('Boll.json', 'w') as f1, open('Boll2.json', 'w') as f2:
            json.dump(balances_boll, f1)
            json.dump(balances_boll2, f2)
    
        await interaction.response.send_message("Обмен прошел успешно. Вы получили 3500<:emoji_16:1185972508655095928> тенелитов", ephemeral=True)

                
    async def menu5_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '00001':
                await interaction.response.send_message(content=l1, ephemeral=True, view=view5_1)
            elif selected_option == '00002':
                await interaction.response.send_message(content=l2, ephemeral=True, view=view5_2)
                
    async def button_callback00001(interaction):
            await interaction.response.edit_message(content=WoodlandSentinel)
            
    async def button_callback00002(interaction):
            await interaction.response.edit_message(content=WoodlandSentinel)
                
    async def menu6_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '000001':
                await interaction.response.send_message(content=i1, ephemeral=True, view=view6_1)
            elif selected_option == '000002':
                await interaction.response.send_message(content=i2, ephemeral=True)
                await interaction.followup.send(content=i2_1, ephemeral=True, view=view6_2)
                    
    async def button_callback000001(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя необходимая валюта
        with open('Boll2.json', 'r') as f:
            balances = json.load(f)
    
        if user_id not in balances or balances[user_id] < 30:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты.", ephemeral=True)
            return
    
        # Проверяем, есть ли у пользователя роль
        for role in ctx.author.roles:
            if role.name == "Запретник":  # Замените "Название роли" на имя роли, которую вы хотите предоставить
                await interaction.response.send_message("Извиняюсь, вы уже купили роль.", ephemeral=True)
                return
    
        # Забираем у пользователя валюту
        balances[user_id] -= 30
    
        # Выдаем пользователю роль
        role_to_add = discord.utils.get(ctx.guild.roles, name="Запретник")  # Замените "Название роли" на имя роли, которую вы хотите предоставить
        await ctx.author.add_roles(role_to_add)
    
        # Сохраняем обновленный баланс в файл
        with open('Boll2.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message("Вы успешно приобрели роль за 30<:emoji_17:1186095454488903821> валюты.", ephemeral=True)
            

    async def button_callback000002(interaction):
        user_id = str(interaction.user.id)
        
        # Загружаем данные из файлов
        with open('jod.json', 'r') as f_jod, open('Boll.json', 'r') as f_boll, open('Boll2.json', 'r') as f_boll2:
            jod_data = json.load(f_jod)
            boll_data = json.load(f_boll)
            boll2_data = json.load(f_boll2)
        
        # Проверяем, есть ли пользователь в файле jod.json, и если нет, добавляем его
        if user_id not in jod_data:
            jod_data[user_id] = {"points": 0, "price_index": 0}
        
        # Список цен для каждого этапа
        prices = [10000, 2500, 3000, 3500, 4000, 8000, 6000, 7000, 8000, 9000, 16000, 10500,
                  13000, 14500, 16000, 20000, 17000, 19000, 21000, 25000]
    
        # Список цен для валюты2
        prices_boll2 = [13, 11, 13, 15, 17, 25]
    
        # Определение валюты и текущей цены
        current_price_index = jod_data[user_id]["price_index"]
    
        if current_price_index < len(prices):
            current_currency = boll_data
            current_prices_list = prices
        elif current_price_index < len(prices) + len(prices_boll2):
            current_currency = boll2_data
            current_prices_list = prices_boll2
            current_price_index -= len(prices)
        else:
            await interaction.response.send_message("Извините, вы уже купили все %.", ephemeral=True)
            return
        
        current_price = current_prices_list[current_price_index]
        
        # Проверяем, хватает ли у пользователя валюты
        if current_currency[user_id] < current_price:
            await interaction.response.send_message(f"Извините, у вас недостаточно валюты ({current_currency[user_id]}), чтобы купить этот предмет за {current_price}.", ephemeral=True)
            return
            

        # Списываем валюту
        current_currency[user_id] -= current_price
        
        # Добавляем очко и обновляем индекс цены
        jod_data[user_id]["points"] += 1
        jod_data[user_id]["price_index"] += 1
        
        # Сохраняем изменения в файлах
        with open('jod.json', 'w') as f_jod, open('Boll.json', 'w') as f_boll, open('Boll2.json', 'w') as f_boll2:
            json.dump(jod_data, f_jod)
            json.dump(boll_data, f_boll)
            json.dump(boll2_data, f_boll2)
        
        # Отправляем сообщение о покупке и получении очка
        if current_price_index == len(prices) + len(prices_boll2) - 1:
            await interaction.response.send_message("Извините, вы уже купили все товары.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Вы купили этот предмет за {current_price} валюты и получили +1% от рынка!\nвас баланс: {current_currency[user_id]}.", ephemeral=True)




    async def menu7_callback(interaction):
            selected_option = interaction.data['values'][0]
            if selected_option == '0000001':
                await interaction.response.send_message(content=k1, ephemeral=True, view=view7_1)
            elif selected_option == '0000002':
                await interaction.response.send_message(content=k2, ephemeral=True, view=view7_2)
                
    async def button_callback0000001(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя валюта для обмена
        with open('Boll.json', 'r') as f1, open('Boll2.json', 'r') as f2:
            balances_boll = json.load(f1)
            balances_boll2 = json.load(f2)
    
        if user_id not in balances_boll2 or balances_boll2[user_id] < 1:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно леннефира для обмена.", ephemeral=True)
            return
    
        # Забираем у пользователя 1 валюту из Boll2.json
        balances_boll2[user_id] -= 1
    
        # Даем пользователю 3000 валют в Boll.json
        if user_id not in balances_boll:
            balances_boll[user_id] = 1500
        balances_boll[user_id] += 2500
    
        # Сохраняем обновленные балансы в файлах
        with open('Boll.json', 'w') as f1, open('Boll2.json', 'w') as f2:
            json.dump(balances_boll, f1)
            json.dump(balances_boll2, f2)
    
        await interaction.response.send_message("Обмен прошел успешно. Вы получили 2500<:emoji_16:1185972508655095928> тенелитов", ephemeral=True)

            
    async def button_callback0000002(interaction):
        user_id = str(interaction.user.id)
    
        # Проверяем, есть ли у пользователя одна из 5 ролей
        roles_to_currency = {
            "запретная тьма": 1200,
            "одержимый тенями": 1100,
            "повелитель теней": 900,
            "исследователь теней": 850,
            "лесной вестник": 750,
        }
    
        user_roles = [role.name for role in interaction.user.roles]
        eligible_roles = [role for role in user_roles if role in roles_to_currency]
    
        if not eligible_roles:
            await interaction.response.send_message("Извиняюсь, вы на 0 этапе", ephemeral=True)
            return
    
        # Сортируем роли от высшей к низшей
        sorted_roles = sorted(eligible_roles, key=lambda x: list(roles_to_currency.keys()).index(x))
    
        # Проверяем, есть ли у пользователя достаточно валюты
        with open('Boll.json', 'r') as f:
            balances = json.load(f)
    
        role_found = None
        for role_name in sorted_roles:
            if user_id in last_command_usage and user_id in balances and balances[user_id] >= roles_to_currency[role_name]:
                role_found = role_name
                break
    
        if role_found is None:
            await interaction.response.send_message("Извиняюсь, у вас недостаточно валюты или вы можете использовать охоту или работу", ephemeral=True)
            return
    
        # Удаляем пользователя из last_command_usage
        last_command_usage.pop(user_id)
    
        # Забираем у пользователя валюту
        balances[user_id] -= roles_to_currency[role_found]
    
        # Сохраняем обновленный баланс в файл
        with open('Boll.json', 'w') as f:
            json.dump(balances, f)
    
        await interaction.response.send_message(f"Вы успешно получили ключ от врат, можете использовать охоту или работу", ephemeral=True)


            
    button1 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button1")
    button2 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button2")
    button01 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button01")
    button02 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button02")
    button001 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button001")
    button002 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button002")
    button003 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button002")
    button0001 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button0001")
    button0002 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button0002")
    button00001 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button00001")
    button00002 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button00002")
    button000001 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button000001")
    button000002 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button000002")
    button0000001 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button0000001")
    button0000002 = Button(label=f"купить", style=discord.ButtonStyle.blurple, custom_id="button0000002")
    
    button1.callback = button_callback1
    button2.callback = button_callback2
    button01.callback = button_callback01
    button02.callback = button_callback02
    button001.callback = button_callback001
    button002.callback = button_callback002
    button003.callback = button_callback003
    button0001.callback = button_callback0001
    button0002.callback = button_callback0002
    button00001.callback = button_callback00001
    button00002.callback = button_callback00002
    button000001.callback = button_callback000001
    button000002.callback = button_callback000002
    button0000001.callback = button_callback0000001
    button0000002.callback = button_callback0000002
        
    menu1.callback = menu1_callback
    menu2.callback = menu2_callback
    menu3.callback = menu3_callback
    menu4.callback = menu4_callback
    menu5.callback = menu5_callback
    menu6.callback = menu6_callback
    menu7.callback = menu7_callback
        
    view1 = View()
    view1.add_item(menu1) 
    
    view1_1 = View()
    view1_1.add_item(button1)
    
    view1_2 = View()
    view1_2.add_item(button2)
    
    view2 = View()
    view2.add_item(menu2) 
    
    view2_1 = View()
    view2_1.add_item(button01) 
    
    view2_2 = View()
    view2_2.add_item(button02) 
    
    view3 = View()
    view3.add_item(menu3) 
    
    view3_1 = View()
    view3_1.add_item(button001) 
    
    view3_2 = View()
    view3_2.add_item(button002) 
    
    view3_3 = View()
    view3_3.add_item(button003) 
    
    view4 = View()
    view4.add_item(menu4) 
    
    view4_1 = View()
    view4_1.add_item(button0001) 
    
    view4_2 = View()
    view4_2.add_item(button0002) 
    
    view5 = View()
    view5.add_item(menu5) 
    
    view5_1 = View()
    view5_1.add_item(button00001) 
    
    view5_2 = View()
    view5_2.add_item(button00002) 
    
    view6 = View()
    view6.add_item(menu6) 
    
    view6_1 = View()
    view6_1.add_item(button000001) 
    
    view6_2 = View()
    view6_2.add_item(button000002) 
    
    view7 = View()
    view7.add_item(menu7) 
    
    view7_1 = View()
    view7_1.add_item(button0000001) 
    
    view7_2 = View()
    view7_2.add_item(button0000002) 
    
    
    current_day = datetime.datetime.utcnow().weekday()
    if current_day == 0:
        await channel.send(content=shop1, view=view1)
    elif current_day == 1:
        await channel.send(content=shop2, view=view6)
    elif current_day == 2:
        await channel.send(content=shop3, view=view3)
    elif current_day == 3:
        await channel.send(content=shop4, view=view4)
    elif current_day == 4:
        await channel.send(content=shop5, view=view5)
    elif current_day == 5:
        await channel.send(content=shop6, view=view6)
    elif current_day == 6:
        await channel.send(content=shop7, view=view7)













async def process_users():
    jod_file_path = "jod.json"
    boll_file_path = "Boll.json"

    try:
        with open(jod_file_path, 'r') as f:
            jod_data = json.load(f)
    except FileNotFoundError:
        jod_data = {}

    try:
        with open(boll_file_path, 'r') as f:
            boll_data = json.load(f)
    except FileNotFoundError:
        boll_data = {}

    for user_id, user_info in jod_data.items():
        points = user_info.get("points", 0)
        price_index = user_info.get("price_index", 0)

        if points > 0:
            daily_reward = calculate_daily_reward(points, price_index)
            boll_data[user_id] = boll_data.get(user_id, 0) + daily_reward

    with open(boll_file_path, 'w') as f:
        json.dump(boll_data, f)

def calculate_daily_reward(points, price_index):
    rewards = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
               600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100,
               1200, 1300, 1400, 1500, 1700, 2000]

    if 1 <= points <= len(rewards):
        return rewards[points - 1]
    else:
        return 0



async def main():
    try:
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    # Расписание для запуска событий каждый день в полночь
    aioschedule.every().day.at("00:00").do(process_users)
    
    # Запуск основной программы
    asyncio.run(main())












async def process_events():
    control_file = "control.json"

    with open(control_file, 'r') as f:
        control_data = json.load(f)

    for user_id, points in control_data.items():
        await process_event(user_id, points)

async def process_event(user_id, points):
    balance_file_path = "Boll.json"
    backup_balance_file_path = "Boll3.json"

    try:
        with open(balance_file_path, 'r') as f:
            balance_data = json.load(f)
    except FileNotFoundError:
        balance_data = {}

    try:
        with open(backup_balance_file_path, 'r') as f:
            backup_balance_data = json.load(f)
    except FileNotFoundError:
        backup_balance_data = {}

    if points > 0:
        with open("control.json", 'r') as f:
            control_data = json.load(f)

        # Переменная, чтобы узнать, сможем ли снять баланс из файлов
        can_deduct_balance = True

        if 1 <= points <= 5:
            can_deduct_balance = await deduct_balance(user_id, balance_data, 250)
        elif 6 <= points <= 10:
            can_deduct_balance = await deduct_balance(user_id, balance_data, 300)
            if not can_deduct_balance:
                can_deduct_balance = await deduct_balance(user_id, backup_balance_data, 300)
        elif 11 <= points <= 25:
            can_deduct_balance = await deduct_balance(user_id, balance_data, 600)
            if not can_deduct_balance:
                can_deduct_balance = await deduct_balance(user_id, backup_balance_data, 600)
            if can_deduct_balance:  # Исправлено на уменьшение на 2, а не 1
                control_data[user_id] -= 1
        elif 26 <= points <= 50:
            can_deduct_balance = await deduct_balance(user_id, balance_data, 800)
            if not can_deduct_balance:
                can_deduct_balance = await deduct_balance(user_id, backup_balance_data, 800)
            if can_deduct_balance:  # Исправлено на уменьшение на 2, а не 1
                control_data[user_id] -= 1
        elif points >= 51:
            can_deduct_balance = await deduct_balance(user_id, balance_data, 400)
            if can_deduct_balance:
                try:
                    with open("Boll2.json", 'r') as f:
                        boll2_data = json.load(f)

                    boll2_data[user_id] -= 1
                    with open("Boll2.json", 'w') as f:
                        json.dump(boll2_data, f)
                except FileNotFoundError:
                    pass
                control_data[user_id] -= 5

        if can_deduct_balance:
            control_data[user_id] -= 1
            with open("control.json", 'w') as f:
                json.dump(control_data, f)

async def deduct_balance(user_id, balance_data, amount):
    if user_id in balance_data and balance_data[user_id] >= amount:
        balance_data[user_id] -= amount
        with open("Boll.json", 'w') as f:
            json.dump(balance_data, f)
        return True
    elif user_id in balance_data and balance_data[user_id] < amount:
        backup_balance_file_path = "Boll3.json"
        try:
            with open(backup_balance_file_path, 'r') as f:
                backup_balance_data = json.load(f)
            
            if user_id in backup_balance_data and backup_balance_data[user_id] >= amount:
                backup_balance_data[user_id] -= amount
                with open(backup_balance_file_path, 'w') as f:
                    json.dump(backup_balance_data, f)
                return True
        except FileNotFoundError:
            pass

    return False

async def main():
    try:
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    # Расписание для запуска событий каждый день в полночь
    aioschedule.every().day.at("00:00").do(process_events)
    
    # Запуск основной программы
    asyncio.run(main())


################ роль 1

async def code_role1(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 2000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)


async def code_role2(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text2)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)





async def code_role3(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text3)
    else:
        await message.channel.send(content=qtext3)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)




        
async def code_role4(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 200
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text4)
    else:
        await message.channel.send(content=qtext4)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role5(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text5)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 400

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role6(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 250
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text6)
    else:
        await message.channel.send(content=qtext6)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role7(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text7)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role8(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text8)
    else:
        await message.channel.send(content=qtext8)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role9(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text9)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 750

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role10(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 750
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text101)
    else:
        await message.channel.send(content=qtext101)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

async def code_role11(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text11)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role12(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 750
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text12)
    else:
        await message.channel.send(content=qtext12)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role13(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text13)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role14(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text14)
    else:
        await message.channel.send(content=qtext14)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role15(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text15)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 750

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role16(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 250
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text16)
    else:
        await message.channel.send(content=qtext16)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role17(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text17)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role18(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 100
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text18)
    else:
        await message.channel.send(content=qtext18)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role19(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text19)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 200

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role20(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text201)
    else:
        await message.channel.send(content=qtext201)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role21(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text21)
    else:
        await message.channel.send(content=qtext21)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role22(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text22)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role23(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text23)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

#########################

###################### роль 2
   
async def code_role01(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text10)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 2500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role02(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text20)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role03(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 750
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text30)
    else:
        await message.channel.send(content=qtext30)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role04(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 350
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text40)
    else:
        await message.channel.send(content=qtext40)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role05(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text50)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 600

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role06(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 400
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text60)
    else:
        await message.channel.send(content=qtext60)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

        
async def code_role07(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text70)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 700

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role08(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text80)
    else:
        await message.channel.send(content=qtext80)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role09(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text90)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 900

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
        
async def code_role010(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 850
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text1002)
    else:
        await message.channel.send(content=qtext1002)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

async def code_role011(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text110)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1150

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role012(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 850
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text120)
    else:
        await message.channel.send(content=qtext120)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role013(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text130)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1100

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role014(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text140)
    else:
        await message.channel.send(content=qtext140)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role015(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text150)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 900

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role016(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 400
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text160)
    else:
        await message.channel.send(content=qtext160)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role017(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text170)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 700

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role018(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 250
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text180)
    else:
        await message.channel.send(content=qtext180)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role019(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text190)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role020(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1750
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text2002)
    else:
        await message.channel.send(content=qtext2002)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role021(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text210)
    else:
        await message.channel.send(content=qtext210)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role022(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text220)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 750

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

############################

############################ роль 3

async def code_role0001(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text100)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 3000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role0002(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text200)
    else:
        await message.channel.send(content=qtext200)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0003(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text300)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)

async def code_role0004(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 350
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text400)
    else:
        await message.channel.send(content=qtext400)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0005(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text500)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 600

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role0006(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 400
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text600)
    else:
        await message.channel.send(content=qtext600)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

async def code_role0007(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text700)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 700

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role0008(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text800)
    else:
        await message.channel.send(content=qtext800)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0009(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text900)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 900

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role00010(message):
    await message.channel.send(content=text10003)

async def code_role00011(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 850
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text1100)
    else:
        await message.channel.send(content=qtext1100)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role00012(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1200)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1200

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role00013(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1300)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role00014(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 850
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text1400)
    else:
        await message.channel.send(content=qtext1400)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role00015(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1500)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1150

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role00016(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1600)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role00017(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text1700)
    else:
        await message.channel.send(content=qtext1700)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role00018(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1800)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 900

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role00019(message):
    await message.channel.send(content=text1900)
    
async def code_role00020(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 400
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text20003)
    else:
        await message.channel.send(content=qtext20003)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role00021(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text2100)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 700

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role00022(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 250
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text2200)
    else:
        await message.channel.send(content=qtext2200)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role00023(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text2300)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role00024(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 2000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text2400)
    else:
        await message.channel.send(content=qtext2400)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role00025(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text2500)
    else:
        await message.channel.send(content=qtext2500)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role00026(message):
    await message.channel.send(content=text2600)


##################################

############################ роль 4

async def code_role00001(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text1000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 4000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role00002(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text2000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)

async def code_role00003(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text3000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 2000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role00004(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text4000)
    else:
        await message.channel.send(content=qtext4000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role00005(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text5000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 800

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role00006(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text6000)
    else:
        await message.channel.send(content=qtext6000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role00007(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text7000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role00008(message):
    await message.channel.send(content=text8000)

async def code_role00009(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 800
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text9000)
    else:
        await message.channel.send(content=qtext9000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role000010(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text100004)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role000011(message):
    await message.channel.send(content=text11000) 

async def code_role000012(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text12000)
    else:
        await message.channel.send(content=qtext12000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role000013(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text13000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1600

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role000014(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text14000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role000015(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text15000)
    else:
        await message.channel.send(content=qtext15000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role000016(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text16000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role000017(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text17000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role000018(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 800
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text18000)
    else:
        await message.channel.send(content=qtext18000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role000019(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text19000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role000020(message):
    await message.channel.send(content=text200004)
    
async def code_role000021(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text21000)
    else:
        await message.channel.send(content=qtext21000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role000022(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text22000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role000023(message):
    await message.channel.send(content=text23000)

async def code_role000024(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 400
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text2400)
    else:
        await message.channel.send(content=qtext2400)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role000025(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text25000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 700

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role000026(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 3000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text26000)
    else:
        await message.channel.send(content=qtext26000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role000027(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 2000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text27000)
    else:
        await message.channel.send(content=text27000)
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role000028(message):
    await message.channel.send(content=text28000)

###############################

############################# роль 5

async def code_role000001(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text10000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 4000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role000002(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text20000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 3

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)

async def code_role000003(message):
    await message.channel.send(content=text30000)

async def code_role000004(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 500
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text40000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role000005(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text50000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 800

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role000006(message):
    await message.channel.send(content=text60000)

async def code_role000007(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text70000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role000008(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text80000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role000009(message):
    await message.channel.send(content=text90000)

async def code_role0000010(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 800
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text1000005)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0000011(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text110000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f) 

async def code_role0000012(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text120000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000013(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text130000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role0000014(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text140000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1600

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000015(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text150000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000016(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 1000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text160000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role0000017(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text170000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1500

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000018(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text180000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 2

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000019(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 800
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text190000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role0000020(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text2000005)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1250

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000021(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text210000)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 1

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)
    
async def code_role0000022(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 600
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text220000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0000023(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text230000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 1000

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role0000024(message):
    await message.channel.send(content=text240000)

async def code_role0000025(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 400
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text250000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0000026(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text260000)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += 700

    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

async def code_role0000027(message):
    await message.channel.send(content=text270000)

async def code_role0000028(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 3000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text280000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)

    
async def code_role0000029(message):
    user_id = str(message.author.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    with open('control.json', 'r') as control_file:
        control_data = json.load(control_file)

    if user_id not in balances:
        balances[user_id] = 1500

    amount_to_deduct = 2000
    percentage_of_balance = (balances[user_id] / amount_to_deduct) * 100

    if balances[user_id] >= amount_to_deduct:
        balances[user_id] -= amount_to_deduct
        await message.channel.send(content=text290000)
    else:
        await message.channel.send(content='У вас недостаточно средств. Команда заблокирована на 3 дня.')
        balances[user_id] = 0

        if 1 <= percentage_of_balance <= 25:
            control_data[user_id] = control_data.get(user_id, 0) + 3
        elif 26 <= percentage_of_balance <= 50:
            control_data[user_id] = control_data.get(user_id, 0) + 2
        elif percentage_of_balance >= 51:
            control_data[user_id] = control_data.get(user_id, 0) + 10

        
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    with open('control.json', 'w') as control_file:
        json.dump(control_data, control_file)


async def code_role0000030(message):
    user_id = str(message.author.id)
    await message.channel.send(content=text3000005)

    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 0

    balances[user_id] += 2

    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)

############################

role_functions = {

    "лесной вестник": {"functions": [code_role1, code_role2, code_role3, code_role4, code_role5, code_role6, code_role7, code_role8, code_role9, code_role10, code_role11, code_role12, code_role13, code_role14, code_role15, code_role16, code_role17, code_role18, code_role19, code_role20, code_role21, code_role22, code_role23], "chances": [10,50, 80, 800, 850, 700, 750, 300, 350, 80, 100, 80, 100, 300, 350, 850, 900, 950, 1000, 50, 80, 100, 10]},

    "исследователь теней": {"functions": [code_role01, code_role02, code_role03, code_role04, code_role05, code_role06, code_role07, code_role08, code_role09, code_role010, code_role011, code_role012, code_role013, code_role014, code_role015, code_role016, code_role017, code_role018, code_role019, code_role020, code_role021, code_role022], "chances": [10,50, 80, 800, 850, 700, 750, 300, 350, 80, 90, 80, 100, 300, 350, 850, 900, 950, 1000, 50, 80, 100]},
    "повелитель теней": {"functions": [code_role0001, code_role0002, code_role0003, code_role0004, code_role0005, code_role0006, code_role0007, code_role0008, code_role0009, code_role00010, code_role00011, code_role00012, code_role00013, code_role00014, code_role00015, code_role00016, code_role00017, code_role00018, code_role00019, code_role00020, code_role00021, code_role00022, code_role00023, code_role00024, code_role00025, code_role00026], "chances": [10,50, 10, 800, 850, 700, 750, 300, 350, 200, 80, 90, 5, 80, 100, 5, 300, 350, 200, 850, 900, 950, 1000, 50, 80, 100]},
    "одержимый тенями": {"functions": [code_role00001, code_role00002, code_role00003, code_role00004, code_role00005, code_role00006, code_role00007, code_role00008, code_role00009, code_role000010, code_role000011, code_role000012, code_role000013, code_role000014, code_role000015, code_role000016, code_role000017, code_role000018, code_role000019, code_role000020, code_role000021, code_role000022, code_role000023, code_role000024, code_role000025, code_role000026, code_role000027, code_role000028], "chances": [15,20, 50, 800, 850, 700, 750, 200, 300, 350, 200, 80, 90, 5, 80, 100, 5, 300, 350, 200, 850, 900, 200, 950, 1000, 50, 80, 100]},
    "запретная тьма": {"functions": [code_role000001, code_role000002, code_role000003, code_role000004, code_role000005, code_role000006, code_role000007, code_role000008, code_role000009, code_role0000010, code_role0000011, code_role0000012, code_role0000013, code_role0000014, code_role0000015, code_role0000016, code_role0000017, code_role0000018, code_role0000019, code_role0000020, code_role0000021, code_role0000022, code_role0000023, code_role0000024, code_role0000025, code_role0000026, code_role0000027, code_role0000028, code_role0000029, code_role0000030], "chances": [15,25, 50, 800, 850, 200, 700, 750, 200, 300, 350, 50, 80, 90, 50, 80, 100, 30, 300, 350, 50, 850, 900, 200, 950, 1000, 200, 50, 80, 30]},
    "Запретник": {"functions": [code_role000001, code_role000002, code_role000003, code_role000004, code_role000005, code_role000006, code_role000007, code_role000008, code_role000009, code_role0000010, code_role0000011, code_role0000012, code_role0000013, code_role0000014, code_role0000015, code_role0000016, code_role0000017, code_role0000018, code_role0000019, code_role0000020, code_role0000021, code_role0000022, code_role0000023, code_role0000024, code_role0000025, code_role0000026, code_role0000027, code_role0000028, code_role0000029, code_role0000030], "chances": [65,75, 100, 800, 850, 200, 700, 750, 200, 300, 350, 50, 80, 140, 50, 80, 150, 30, 300, 350, 50, 850, 900, 200, 950, 1000, 200, 50, 80, 30]},
}
   
role_values = {
    1: ["лесной вестник"],
    2: ["исследователь теней"],
    3: ["повелитель теней"],
    4: ["одержимый тенями"],
    5: ["запретная тьма"],
    6: ["Запретник"],
}


async def send_code(ctx, selected_function):
    await selected_function(ctx.message)



@bot.command()
async def Hunting(ctx):
    allowed_channel_id = 1188195784810844220  # Замените на ID разрешенного канала
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("Вы можете использовать эту команду только в <#1188195784810844220> ")
        return
    
    user_id = str(ctx.author.id)
    user_roles = [role.name for role in ctx.author.roles]  

    # Проверяем, прошло ли более 24 часов с последнего использования команды
    if user_id in last_command_usage:
        last_usage_time = last_command_usage[user_id]
        elapsed_time = datetime.datetime.now() - last_usage_time
        if elapsed_time < datetime.timedelta(hours=24):
            remaining_time = datetime.timedelta(hours=24) - elapsed_time
            remaining_time_str = str(remaining_time).split(".")[0]  # Форматируем время
            await ctx.send(f"Вы можете отправиться на охоту или работу только раз в сутки.\n(Время до окончания срока: {remaining_time_str})")
            return
        
    # Сортируем роли по убыванию
    sorted_roles = sorted(role_values.keys(), reverse=True)

    for value in sorted_roles:
        if value in role_values and any(role in user_roles for role in role_values[value]):
            selected_function = random.choice(role_functions[role_values[value][0]]["functions"])
            await send_code(ctx, selected_function)

            # Обновите время последнего использования команды
            last_command_usage[user_id] = datetime.datetime.now()

            remaining_time = datetime.timedelta(hours=24)
            
            break



@bot.command()
async def random_reward(ctx):
    allowed_channel_id = 1188195784810844220  # Замените на ID разрешенного канала
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("Вы можете использовать эту команду только в <#1188195784810844220> ")
        return
    
    user_id = str(ctx.author.id)

    # Проверяем, прошло ли более 24 часов с последнего использования команды
    if user_id in last_command_usage:
        last_usage_time = last_command_usage[user_id]
        elapsed_time = datetime.datetime.now() - last_usage_time
        if elapsed_time < datetime.timedelta(hours=24):
            remaining_time = datetime.timedelta(hours=24) - elapsed_time
            remaining_time_str = str(remaining_time).split(".")[0]  # Форматируем время
            await ctx.send(f"Вы можете отправиться на работу или охоту только раз в сутки.\n(Время до окончания срока: {remaining_time_str})")
            return

    # Выбираем роль пользователя
    user_roles = [role.name for role in ctx.author.roles]

    # Определение диапазона для каждой роли
    role_ranges = {
        "лесной вестник": (300, 500),
        "исследователь теней": (400, 700),
        "повелитель теней": (500, 750),
        "одержимый тенями": (700, 1000),
        "запретная тьма": (800, 1200),
    }

    reward_amount = 0

    for role, reward_range in role_ranges.items():
        if role in user_roles:
            reward_amount = random.randint(*reward_range)
            break

    # Если роль не определена, используем диапазон по умолчанию
    if reward_amount == 0:
        default_range = (0, 200)
        reward_amount = random.randint(*default_range)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances:
        balances[user_id] = 1500

    balances[user_id] += reward_amount

    # Сохраняем обновленный баланс в файл
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    # Устанавливаем блок на 24 часа
    last_command_usage[user_id] = datetime.datetime.now()

    remaining_time = datetime.timedelta(hours=24)
    await ctx.send(f"Вы получили {reward_amount} валюты.\nБаланс: {balances[user_id]}.\n(Время до окончания срока: {remaining_time})")

# minutes=10 control

######################################

@bot.command()
@commands.check(is_allowed_user)
async def coin_balance(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    member = member or ctx.author  # Если пользователь не указан, используем автора сообщения
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    # Получение баланса пользователя или отправка сообщения, если баланса нет
    user_balance = balances.get(user_id, "нет баланса")

    # Отправка сообщения с балансом
    await ctx.send(f'Баланс пользователя {member.mention}: {user_balance} единиц валюты.')
    
@bot.command()
@commands.check(is_allowed_user)
async def coin2_balance(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    member = member or ctx.author  # Если пользователь не указан, используем автора сообщения
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    # Получение баланса пользователя или отправка сообщения, если баланса нет
    user_balance = balances.get(user_id, "нет баланса")

    # Отправка сообщения с балансом
    await ctx.send(f'Баланс пользователя {member.mention}: {user_balance} единиц валюты.')

@bot.command()
@commands.check(is_allowed_user)
async def coin3_balance(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    member = member or ctx.author  # Если пользователь не указан, используем автора сообщения
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('Boll3.json', 'r') as f:
        balances = json.load(f)

    # Получение баланса пользователя или отправка сообщения, если баланса нет
    user_balance = balances.get(user_id, "нет баланса")

    # Отправка сообщения с балансом
    await ctx.send(f'Баланс пользователя {member.mention}: {user_balance} единиц валюты.')

@bot.command()
@commands.check(is_allowed_user)
async def coin4_balance(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    member = member or ctx.author  # Если пользователь не указан, используем автора сообщения
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('control.json', 'r') as f:
        balances = json.load(f)

    # Получение баланса пользователя или отправка сообщения, если баланса нет
    user_balance = balances.get(user_id, "нет очков")

    # Отправка сообщения с балансом
    await ctx.send(f'очки пользователя {member.mention}: {user_balance} единиц очков.')


@bot.command()
@commands.check(is_allowed_user)
async def coin(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    # Проверка, есть ли пользователь в данных
    if user_id not in balances:
        # Создание нового пользователя с балансом 0
        balances[user_id] = 1500

    # Выполнение операции
    if operation == '+':
        balances[user_id] += amount
        await ctx.send(f'{amount} единиц валюты добавлены пользователю {member.mention}.')
    elif operation == '-':
        if balances[user_id] >= amount:
            balances[user_id] -= amount
            await ctx.send(f'{amount} единиц валюты убавлены у пользователя {member.mention}.')
        else:
            await ctx.send(f'У пользователя {member.mention} недостаточно средств.')
    else:
        await ctx.send('Некорректная операция. Используйте "+" для добавления, "-" для уменьшения.')

    # Сохранение обновленных данных в файл
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

@bot.command()
@commands.check(is_allowed_user)
async def coin_2(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('Boll2.json', 'r') as f:
        balances = json.load(f)

    # Проверка, есть ли пользователь в данных
    if user_id not in balances:
        # Создание нового пользователя с балансом 0
        balances[user_id] = 1500

    # Выполнение операции
    if operation == '+':
        balances[user_id] += amount
        await ctx.send(f'{amount} единиц валюты добавлены пользователю {member.mention}.')
    elif operation == '-':
        if balances[user_id] >= amount:
            balances[user_id] -= amount
            await ctx.send(f'{amount} единиц валюты убавлены у пользователя {member.mention}.')
        else:
            await ctx.send(f'У пользователя {member.mention} недостаточно средств.')
    else:
        await ctx.send('Некорректная операция. Используйте "+" для добавления, "-" для уменьшения.')

    # Сохранение обновленных данных в файл
    with open('Boll2.json', 'w') as f:
        json.dump(balances, f)

@bot.command()
@commands.check(is_allowed_user)
async def coin_3(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('Boll3.json', 'r') as f:
        balances = json.load(f)

    # Проверка, есть ли пользователь в данных
    if user_id not in balances:
        # Создание нового пользователя с балансом 0
        balances[user_id] = 1500

    # Выполнение операции
    if operation == '+':
        balances[user_id] += amount
        await ctx.send(f'{amount} единиц валюты добавлены пользователю {member.mention}.')
    elif operation == '-':
        if balances[user_id] >= amount:
            balances[user_id] -= amount
            await ctx.send(f'{amount} единиц валюты убавлены у пользователя {member.mention}.')
        else:
            await ctx.send(f'У пользователя {member.mention} недостаточно средств.')
    else:
        await ctx.send('Некорректная операция. Используйте "+" для добавления, "-" для уменьшения.')

    # Сохранение обновленных данных в файл
    with open('Boll3.json', 'w') as f:
        json.dump(balances, f)
        
@bot.command()
@commands.check(is_allowed_user)
async def coin_4(ctx, member: commands.MemberConverter = None, operation: str = None, amount: int = 0):
    user_id = str(member.id)

    # Загрузка данных из файла
    with open('control.json', 'r') as f:
        balances = json.load(f)

    # Проверка, есть ли пользователь в данных
    if user_id not in balances:
        # Создание нового пользователя с балансом 0
        balances[user_id] = 1500

    # Выполнение операции
    if operation == '+':
        balances[user_id] += amount
        await ctx.send(f'{amount} единиц валюты добавлены пользователю {member.mention}.')
    elif operation == '-':
        if balances[user_id] >= amount:
            balances[user_id] -= amount
            await ctx.send(f'{amount} единиц валюты убавлены у пользователя {member.mention}.')
        else:
            await ctx.send(f'У пользователя {member.mention} недостаточно средств.')
    else:
        await ctx.send('Некорректная операция. Используйте "+" для добавления, "-" для уменьшения.')

    # Сохранение обновленных данных в файл
    with open('control.json', 'w') as f:
        json.dump(balances, f)        
        
######################################

@bot.command()
async def balance(ctx, member: commands.MemberConverter = None):
    # Если участник не указан, использовать автора команды
    if member is None:
        member = ctx.author

    user_id = str(member.id)

    # Загрузка данных из файла для первой валюты
    with open('Boll.json', 'r') as f1:
        balances_currency1 = json.load(f1)

    # Загрузка данных из файла для второй валюты
    with open('Boll2.json', 'r') as f2:
        balances_currency2 = json.load(f2)

    # Загрузка данных из файла для третьей валюты
    with open('Boll3.json', 'r') as f3:
        balances_currency3 = json.load(f3)

    # Проверка, есть ли пользователь в данных для первой валюты
    if user_id not in balances_currency1:
        balance_currency1 = 0
    else:
        balance_currency1 = balances_currency1[user_id]

    # Проверка, есть ли пользователь в данных для второй валюты
    if user_id not in balances_currency2:
        balance_currency2 = 0
    else:
        balance_currency2 = balances_currency2[user_id]

    # Проверка, есть ли пользователь в данных для третьей валюты
    if user_id not in balances_currency3:
        balance_currency3 = 0
    else:
        balance_currency3 = balances_currency3[user_id]

    # Показывает баланс всех трех валют или только той, которая есть
    if balance_currency1 > 0 and balance_currency2 > 0 and balance_currency3 > 0:
        await ctx.send(f'{member.mention} имеет <:emoji_16:1185972508655095928>{balance_currency1} тенелитов,  🏦{balance_currency3} в банку и <:emoji_17:1186095454488903821>{balance_currency2} леннефира')
    elif balance_currency1 > 0 and balance_currency2 > 0:
        await ctx.send(f'{member.mention} имеет <:emoji_16:1185972508655095928>{balance_currency1} тенелита и <:emoji_17:1186095454488903821>{balance_currency2} леннефира.')
    elif balance_currency1 > 0 and balance_currency3 > 0:
        await ctx.send(f'{member.mention} имеет <:emoji_16:1185972508655095928>{balance_currency1} тенелита и 🏦{balance_currency3} в банку')
    elif balance_currency2 > 0 and balance_currency3 > 0:
        await ctx.send(f'{member.mention} имеет <:emoji_17:1186095454488903821>{balance_currency2} леннефира и 🏦{balance_currency3} тенелита в банке.')
    elif balance_currency1 > 0:
        await ctx.send(f'{member.mention} имеет <:emoji_16:1185972508655095928>{balance_currency1} тенелита.')
    elif balance_currency2 > 0:
        await ctx.send(f'{member.mention} имеет <:emoji_17:1186095454488903821>{balance_currency2} леннефира.')
    elif balance_currency3 > 0:
        await ctx.send(f'{member.mention} имеет 🏦{balance_currency3} в банку')
    else:
        await ctx.send(f'{member.mention} не имеет баланса.')





@bot.command()
async def top(ctx):
    # Загрузка данных из файла для первой валюты
    with open('Boll.json', 'r') as f1:
        balances_currency1 = json.load(f1)

    # Загрузка данных из файла для второй валюты
    with open('Boll2.json', 'r') as f2:
        balances_currency2 = json.load(f2)

    # Сортировка пользователей по балансу валюты 1
    sorted_users = sorted(balances_currency1.items(), key=lambda x: x[1], reverse=True)

    # Ограничение вывода первыми 10 участниками
    sorted_users = sorted_users[:10]

    # Поиск места пользователя в общем рейтинге
    user_place = None
    for i, (user, _) in enumerate(sorted_users, start=1):
        if user == str(ctx.author.id):
            user_place = i
            break

    # Подготовка сообщения с таблицей лидеров
    leaderboard_message = f"""
        Топ 10 пользователей:
╭─━━━━───━──━━━⊱⋆⊰━━━─────━━━━━─╮\n"""

    for i, (user_id, balance_currency1) in enumerate(sorted_users, start=1):
        # Проверка, есть ли баланс валюты 2
        balance_currency2 = balances_currency2.get(user_id, None)

        # Загрузка данных из файла для третьей валюты
        with open('Boll3.json', 'r') as f3:
            balances_currency3 = json.load(f3)

        # Получение баланса валюты 3
        balance_currency3 = balances_currency3.get(user_id, None)

        if balance_currency2 is not None:
            leaderboard_message += (
                f"{i}. <@{user_id}> - <:emoji_16:1185972508655095928>+🏦{balance_currency1 + balance_currency3 if balance_currency1 is not None and balance_currency3 is not None else 0}, "

                f"<:emoji_16:1185972508655095928>{balance_currency1}, 🏦{balance_currency3}, <:emoji_17:1186095454488903821>{balance_currency2}\n"
            )
        else:
            leaderboard_message += (
                f"{i}. <@{user_id}> - <:emoji_16:1185972508655095928>+🏦{balance_currency1 + balance_currency3 if balance_currency1 is not None and balance_currency3 is not None else 0}, "

                f"<:emoji_16:1185972508655095928>{balance_currency1}, 🏦{balance_currency3}\n"
            )

    # Если пользователь не в топе, добавляем его информацию в конец топа
    if user_place is None:
        leaderboard_message += (
            f"{ctx.author.mention} -"
            f"<:emoji_16:1185972508655095928>+🏦{balances_currency1.get(str(ctx.author.id), 0) + balances_currency3.get(str(ctx.author.id), 0)}, "
            f"<:emoji_16:1185972508655095928>{balances_currency1.get(str(ctx.author.id), 0)}, "
            f"🏦{balances_currency3.get(str(ctx.author.id), 0)}, "
            f"<:emoji_17:1186095454488903821>{balances_currency2.get(str(ctx.author.id), 0)}\n"
        )

    # Если нет пользователей
    if not sorted_users:
        leaderboard_message += "Пока что пусто."

    leaderboard_message += "╰─━━━━━━━━────━⊱⋆⊰━━━──━───━━━━─╯"
    
        
    
    
    
    async def button_callback1(interaction):
        # Загрузка данных из файла для второй валюты
        with open('Boll2.json', 'r') as f2:
            balances_currency2 = json.load(f2)
    
        # Сортировка пользователей по балансу валюты 2
        sorted_users = sorted(balances_currency2.items(), key=lambda x: x[1], reverse=True)
    
        # Ограничение вывода первыми 10 участниками
        sorted_users = sorted_users[:10]
    
        # Поиск места пользователя в общем рейтинге
        user_place = None
        for i, (user, _) in enumerate(sorted_users, start=1):
            if user == str(ctx.author.id):
                user_place = i
                break
    
        # Подготовка сообщения с таблицей лидеров
        leaderboard_message = f"""
        Топ 10 пользователей:
╭─━━━━───━──━━━⊱⋆⊰━━━─────━━━━━─╮\n"""
        
        
        for i, (user_id, balance) in enumerate(sorted_users, start=1):
            leaderboard_message += f"{i}. <@{user_id}> - <:emoji_17:1186095454488903821>{balance}\n"
    
        # Если пользователь вызвавший команду не в топе, добавляем его информацию в конец топа
        if user_place is None:
            leaderboard_message += (
                f"{user_place}. {ctx.author.mention} - <:emoji_17:1186095454488903821>{balances_currency2.get(str(ctx.author.id), 0)}\n"
            )
    
        # Если нет пользователей
        if not sorted_users:
            leaderboard_message += "Пока что пусто."
    
        leaderboard_message += "╰─━━━━━━━━────━⊱⋆⊰━━━──━───━━━━─╯"
    
        
    
        
        await interaction.response.edit_message(content=leaderboard_message, view=view6)
        
    async def button_callback2(interaction):
        # Загрузка данных из файла для первой валюты
        with open('Boll.json', 'r') as f1:
            balances_currency1 = json.load(f1)
    
        # Загрузка данных из файла для второй валюты
        with open('Boll2.json', 'r') as f2:
            balances_currency2 = json.load(f2)
    
        # Сортировка пользователей по балансу валюты 1
        sorted_users = sorted(balances_currency1.items(), key=lambda x: x[1], reverse=True)
    
        # Ограничение вывода первыми 10 участниками
        sorted_users = sorted_users[:10]
    
        # Поиск места пользователя в общем рейтинге
        user_place = None
        for i, (user, _) in enumerate(sorted_users, start=1):
            if user == str(ctx.author.id):
                user_place = i
                break
    
        # Подготовка сообщения с таблицей лидеров
        leaderboard_message = f"""

        Топ 10 пользователей:
╭─━━━━───━──━━━⊱⋆⊰━━━─────━━━━━─╮\n"""
    
        for i, (user_id, balance_currency1) in enumerate(sorted_users, start=1):
            # Проверка, есть ли баланс валюты 2
            balance_currency2 = balances_currency2.get(user_id, None)
    
            # Загрузка данных из файла для третьей валюты
            with open('Boll3.json', 'r') as f3:
                balances_currency3 = json.load(f3)
    
            # Получение баланса валюты 3
            balance_currency3 = balances_currency3.get(user_id, None)
    
            if balance_currency2 is not None:
                leaderboard_message += (
                    f"{i}. <@{user_id}> - <:emoji_16:1185972508655095928>+🏦{balance_currency1 + balance_currency3 if balance_currency1 is not None and balance_currency3 is not None else 0}, "

                    f"<:emoji_16:1185972508655095928>{balance_currency1}, 🏦{balance_currency3}, <:emoji_17:1186095454488903821>{balance_currency2}\n"
                )
            else:
                leaderboard_message += (
                    f"{i}. <@{user_id}> - <:emoji_16:1185972508655095928>+🏦{balance_currency1 + balance_currency3 if balance_currency1 is not None and balance_currency3 is not None else 0}, "

                    f"<:emoji_16:1185972508655095928>{balance_currency1}, 🏦{balance_currency3}\n"
                )
    
        # Если пользователь не в топе, добавляем его информацию в конец топа
        if user_place is None:
            leaderboard_message += (
                f"{ctx.author.mention} - "
                f"<:emoji_16:1185972508655095928>+🏦{balances_currency1.get(str(ctx.author.id), 0) + balances_currency3.get(str(ctx.author.id), 0)}, "
                f"<:emoji_16:1185972508655095928>{balances_currency1.get(str(ctx.author.id), 0)}, "
                f"🏦{balances_currency3.get(str(ctx.author.id), 0)}, "
                f"<:emoji_17:1186095454488903821>{balances_currency2.get(str(ctx.author.id), 0)}\n"
            )
    
        # Если нет пользователей
        if not sorted_users:
            leaderboard_message += "Пока что пусто."
    
        leaderboard_message += "╰─━━━━━━━━────━⊱⋆⊰━━━──━───━━━━─╯"
    
        await interaction.response.edit_message(content=leaderboard_message, view=view5)


    
    button1 = Button(label=f"--›", style=discord.ButtonStyle.blurple, custom_id="button1")
    button2 = Button(label=f"‹--", style=discord.ButtonStyle.blurple, custom_id="button2")
    
    
    button1.callback = button_callback1
    button2.callback = button_callback2
    
    view5 = View()
    view5.add_item(button1)
    
    view6 = View()
    view6.add_item(button2)
    
    
    
    await ctx.send(content=leaderboard_message, view=view5)






#@bot.command()
#async def leaderboard2(ctx):
#    # Загрузка данных из файла для второй валюты
#    with open('Boll2.json', 'r') as f2:
#        balances_currency2 = json.load(f2)

#    # Сортировка пользователей по балансу валюты 2
#    sorted_users = sorted(balances_currency2.items(), key=lambda x: x[1], reverse=True)

#    # Ограничение вывода первыми 10 участниками
#    sorted_users = sorted_users[:10]

    # Поиск места пользователя в общем рейтинге
#    user_place = None
#    for i, (user, _) in enumerate(sorted_users, start=1):
#        if user == str(ctx.author.id):
#            user_place = i
#            break

    # Подготовка сообщения с таблицей лидеров
#    leaderboard_message = "Таблица лидеров:\n"
#    for i, (user_id, balance) in enumerate(sorted_users, start=1):
#        leaderboard_message += f"{i}. <@{user_id}> - <:emoji_17:1186095454488903821>{balance}\n"

    # Если пользователь вызвавший команду не в топе, добавляем его информацию в конец топа
#    if user_place is None:
#        leaderboard_message += (
#            f"{user_place}. {ctx.author.mention} - <:emoji_17:1186095454488903821>{balances_currency2.get(str(ctx.author.id), 0)}\n"
#        )

    # Если нет пользователей
#    if not sorted_users:
#        leaderboard_message += "Пока что пусто."

#    leaderboard_message += "╰─━━━━━━───━⊱⋆⊰━━━───━━━─╯"
    
#    await ctx.send(leaderboard_message)







@bot.command()
async def pay(ctx, user: discord.User = None, amount: Union[int, str] = None):
    if user is None or amount is None:
        # Отправляем сообщение с инструкцией, если не указан пользователь или сумма
        await ctx.send("Пожалуйста, укажите пользователя и количество валюты. Пример: `!pay @Пользователь 100`.")
        return

    sender_id = str(ctx.author.id)
    receiver_id = str(user.id)

    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if sender_id not in balances:
        balances[sender_id] = 0

    # Проверяем, если ключевое слово "all" в amount, передаем все доступные средства
    if isinstance(amount, str) and amount.lower() == 'all':
        amount = balances[sender_id]

    # Проверяем, достаточно ли средств у отправителя
    if balances[sender_id] < amount:
        await ctx.send("У вас недостаточно средств для выполнения этой операции.")
        return

    # Переводим валюту от отправителя к получателю
    balances[sender_id] -= amount
    if receiver_id not in balances:
        balances[receiver_id] = 0
    balances[receiver_id] += amount

    # Сохраняем обновленные балансы в файл
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    await ctx.send(f"""
Перевод <:emoji_16:1185972508655095928>{amount} тенелита выполнен. 

Баланс {ctx.author.mention}: <:emoji_16:1185972508655095928>{balances[sender_id]}

Баланс {user.mention}: <:emoji_16:1185972508655095928>{balances[receiver_id]}""")

@bot.command()
async def bank(ctx, operation: str = None, amount: Union[int, str] = None):
    if operation not in ('+', '-'):
        await ctx.send("Некорректная операция. Используйте '+' для перемещения тенелита в банк, '-' для перемещения из банка.")
        return

    sender_id = str(ctx.author.id)

    with open('Boll.json', 'r') as f1:
        balances_currency1 = json.load(f1)

    with open('Boll3.json', 'r') as f3:
        balances_currency3 = json.load(f3)

    # Проверяем, если ключевое слово "all" в amount, перемещаем всю доступную валюту
    if isinstance(amount, str) and amount.lower() == 'all':
        amount = balances_currency1.get(sender_id, 0) if operation == '+' else balances_currency3.get(sender_id, 0)

    # Проверяем, достаточно ли средств у отправителя для операции
    if operation == '+':
        if balances_currency1.get(sender_id, 0) < amount:
            await ctx.send("У вас недостаточно тенелита для выполнения этой операции.")
            return
    elif operation == '-':
        if balances_currency3.get(sender_id, 0) < amount:
            await ctx.send("У вас недостаточно тенелита для выполнения этой операции.")
            return

    # Выполняем перемещение валюты
    if operation == '+':
        balances_currency1[sender_id] -= amount
        balances_currency3[sender_id] += amount
    elif operation == '-':
        balances_currency3[sender_id] -= amount
        balances_currency1[sender_id] += amount

    # Сохраняем обновленные балансы в файл
    with open('Boll.json', 'w') as f1:
        json.dump(balances_currency1, f1)

    with open('Boll3.json', 'w') as f3:
        json.dump(balances_currency3, f3)

    await ctx.send(f"""
Перемещение <:emoji_16:1185972508655095928>{amount} тенелитов выполнено.

Баланс {ctx.author.mention}:
тенелитов: <:emoji_16:1185972508655095928>{balances_currency1[sender_id]}
Банк: 🏦{balances_currency3[sender_id]}
""")

@bot.command()
async def rol(ctx, *args):
    user_id = str(ctx.author.id)
    
    with open('rule.json', 'r') as f:
        rule_data = json.load(f)
    
    if user_id not in rule_data:
        await ctx.send("что-бы получить доступ пожалуйста купите себе свою роль")
        return

    if not args:
        await ctx.send("Пример использования команды:\n`!rol (название роли)\n!rol edit (другое название роли)`")
        return

    # Обработка случая, если пользователь хочет создать или изменить роль
    if args[0].lower() == "edit" and len(args) >= 2:
        await edit_role(ctx, args[1])
    else:
        # Добавим проверку названия роли в файле rule.json только для создания
        expected_role_name = rule_data[user_id]
        if args[0].lower() == expected_role_name.lower() or expected_role_name.lower() == "rule":
            await create_role(ctx, args[0])
        else:
            await ctx.send("Извините, вы уже создали свою роль, используйте \n!rol edit (новое название роли)")

async def create_role(ctx, role_name):
    # Проверка, достаточно ли у пользователя валюты
    user_id = str(ctx.author.id)
    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances or balances[user_id] < 5000:
        await ctx.send("Извините, у вас недостаточно валюты для этой операции, потребуеться 5000<:emoji_16:1185972508655095928>")
        return

    # Проверка, существует ли роль с таким же названием на сервере
    existing_role = discord.utils.get(ctx.guild.roles, name=role_name)
    if existing_role:
        await ctx.send(f"Извините, роль с названием '{role_name}' уже существует на сервере.")
        return

    # Создание роли на сервере
    try:
        role = await ctx.guild.create_role(name=role_name, reason="Создание роли пользователем")
    except discord.Forbidden:
        await ctx.send("Бот не имеет достаточных прав для создания ролей.")
        return
    except discord.HTTPException:
        await ctx.send("Произошла ошибка при создании роли.")
        return

    # Добавление роли пользователю
    await ctx.author.add_roles(role)

    # Перемещение созданной роли под разработчиком
    developer_role = discord.utils.get(ctx.guild.roles, name="разработчик")
    if developer_role:
        await role.edit(position=developer_role.position - 1)
    else:
        await ctx.send("Не удалось найти роль 'разработчик' на сервере.")

    # Обновление значения rule в файле
    with open('rule.json', 'r') as f_rule:
        rule_data = json.load(f_rule)

    rule_data[user_id] = role.name

    with open('rule.json', 'w') as f_rule:
        json.dump(rule_data, f_rule)

    # Списание валюты
    balances[user_id] -= 5000
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    await ctx.send(f"Роль '{role_name}' успешно создана и добавлена вам, для изменения используйте команду\n!rol edit (новое название)")

async def edit_role(ctx, new_role_name):
    # Проверка, достаточно ли у пользователя валюты
    user_id = str(ctx.author.id)
    with open('Boll.json', 'r') as f:
        balances = json.load(f)

    if user_id not in balances or balances[user_id] < 5000:
        await ctx.send("Извините, у вас недостаточно валюты для этой операции, потребуеться 5000<:emoji_16:1185972508655095928>")
        return

    # Поиск роли пользователя в файле rule.json
    with open('rule.json', 'r') as f_rule:
        rule_data = json.load(f_rule)

    if user_id not in rule_data:
        await ctx.send("У вас нет роли для изменения.")
        return

    # Поиск роли на сервере
    role = discord.utils.get(ctx.guild.roles, name=rule_data[user_id])
    if not role:
        await ctx.send("Не удалось найти роль для изменения на сервере.")
        return

    # Проверка, существует ли роль с таким же названием на сервере
    existing_role = discord.utils.get(ctx.guild.roles, name=new_role_name)
    if existing_role:
        await ctx.send(f"Извините, роль с названием '{new_role_name}' уже существует на сервере.")
        return

    # Попытка изменить название роли
    try:
        await role.edit(name=new_role_name)
    except discord.Forbidden:
        await ctx.send("Бот не имеет достаточных прав для изменения роли.")
        return
    except discord.HTTPException:
        await ctx.send("Произошла ошибка при изменении названия роли.")
        return

    # Обновление значения rule в файле
    rule_data[user_id] = role.name
    with open('rule.json', 'w') as f_rule:
        json.dump(rule_data, f_rule)

    # Списание валюты
    balances[user_id] -= 5000
    with open('Boll.json', 'w') as f:
        json.dump(balances, f)

    await ctx.send(f"Роль успешно изменена на '{new_role_name}'.")

    
bot.run('MTE2OTc3NDUxOTc4Nzk4NzAxNQ.GxEbbD.MKJFudUBtEjSv5ngmK9RNSLGuY9b_0uD5Ht4HY')
