import base64, discord, json, asyncio, aiohttp, requests, os, sys, uuid, datetime, random, codecs, threading, time as t

from colorama import init, Fore, Style
from data.model.imaginepy import AsyncImagine, Style, Ratio
from discord import SyncWebhook
from discord.ext import commands
from datetime import timedelta

with open("config.json", "r") as cjson:
    config = json.load(cjson)


######################################### Console #########################################

currentVersion = "1.0.1"

init(autoreset=True)


def check_version():
    try:
        version = requests.get(
            "git@github.com:Mop157/Hiding_your_eyes.git/main/version.txt"
        )

        if version.text != currentVersion:
            changes = requests.get(
                "git@github.com:Mop157/Hiding_your_eyes.git/main/data/changelog.txt"
            )

            if "REQUIRED" in changes.text:
                print(
                    f"{Fore.RED}Обязательное обновление на GitHub. Вы должны обновиться, чтобы продолжить использование селф бота: {Fore.RESET}https://github.com/Mop157/Hiding_your_eyes\n\nChangelog:\n{changes.text}"
                )

                input("\nНажмите Enter для выхода...")
                os._exit(0)

            else:
                print(
                    f"{Fore.YELLOW}Эта версия устарела. Пожалуйста, обновитесь до версии {Fore.WHITE}{version.text} {Fore.YELLOW}from {Fore.RESET}https://github.com/Mop157/Hiding_your_eyes\n\nChangelog:\n{changes.text}\n"
                )
    except:
        pass


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

startTime = datetime.datetime.utcnow()


def title():
    while True:
        uptime = datetime.datetime.utcnow() - startTime
        days, hours, minutes, seconds = (
            uptime.days,
            uptime.seconds // 3600,
            (uptime.seconds // 60) % 60,
            uptime.seconds % 60,
        )
        if days >= 1:
            time_str = f"{days}f:{hours:02}:{minutes:02}:{seconds:02}"
        else:
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        os.system(f"title скрытие очи- {time_str}")
        t.sleep(1)


if os.name == "nt":
    threading.Thread(target=title).start()


text = f"""
 _____                                                                                   _____ 
( ___ )                                                                                 ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ``````█████████`````███████████████`````████████``````████████`````█████`████```` |   | 
 |   | `````███░░░░░███```░░░███░░░░░███``````███░░░░███````███░░░░███```░░███`░███````` |   | 
 |   | ````███`````░░░``````░███````░███`````░░░````░███```░░░````░███````░███`░███````` |   | 
 |   | ```░███``````````````░███````░███````````██████░```````██████░`````░███`░███````` |   | 
 |   | ```░███``````````````░███````░███```````░░░░░░███`````░░░░░░███````░░███████````` |   | 
 |   | ```░░███`````███`````░███````░███``````███```░███````███```░███`````░░░░░███````` |   | 
 |   | ````░░█████████``██``█████```█████``██░░████████``██░░████████``██``███`░███````` |   | 
 |   | `````░░░░░░░░░``░░``░░░░````░░░░```░░``░░░░░░░░``░░``░░░░░░░░``░░``░░██████`````` |   | 
 |   | ````````````````````````````````````````````````````````````````````░░░░░░``````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |   | ````````````````````````````````````````````````````````````````````````````````` |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                                                 (_____)
"""


print(text)
credits = """                                                                                        от Remus"""
print(credits)
print("")
line = "-" * 120
print(line)
print("")

# pretty ugly for now but rgbprint didnt work on other systems and i wanted a cool gradient :(

if config["token"] == "":
    TOKEN = input(
        "Похоже, вы еще не ввели свой токен. Введите его сейчас: "
    )

    config["token"] = TOKEN

    with open("config.json", "w") as cjson:
        json.dump(config, cjson, indent=4)

    print(Fore.GREEN + "Токен успешно сохранен.")

    PREFIX = input("Каким бы вы хотели видеть префикс? (Default: >) ")

    if PREFIX == "":
        print(Fore.GREEN + "Успешно настройте скрытние очи. начало...")

    else:
        config["prefix"] = PREFIX

        with open("config.json", "w") as cjson:
            json.dump(config, cjson, indent=4)

    print(
        Fore.GREEN
        + "Префикс успешно установлен на: "
        + config["prefix"]
        + ". Начало скрытние очи..."
    )

    os.execl(sys.executable, sys.executable, *sys.argv)


check_version()


####################################### Initialisation ####################################


bot = commands.Bot(
    command_prefix=config["prefix"], self_bot=True, case_insensitive=True
)


pingMute = False
pingKick = False
pingRole = None

pinSpam = None

mimic = None
smartMimic = None

reactUser = None
reactEmoji = None
blockReaction = None

deleteAnnoy = None
forceDisconnect = None

afkMode = False
afkLogs = []

whitelist = []
messageLogsBlacklist = []

noLeave = []
forcedNicks = {}

spyList = []
notifyWords = []


def load_config():
    with open("data/webhooks.txt", "r") as file:
        webhook_lines = file.read().splitlines()

    if webhook_lines == []:
        return

    webhooks = {}

    for line in webhook_lines:
        key, url = line.split(": ")
        webhooks[key.strip()] = url.strip()

    global spyWebhook
    spyWebhook = webhooks["Шпион"]

    global ticketsWebhook
    ticketsWebhook = webhooks["Билеты"]

    global messageLogsWebhook
    messageLogsWebhook = webhooks["Журналы сообщений"]

    global relationshipLogsWebhook
    relationshipLogsWebhook = webhooks["Журналы отношений"]

    global guildLogsWebhook
    guildLogsWebhook = webhooks["Журналы гильдии"]

    global roleLogsWebhook
    roleLogsWebhook = webhooks["Журналы ролей"]

    global pingLogsWebhook
    pingLogsWebhook = webhooks["Журналы пинга"]

    global wordNotifications
    wordNotifications = webhooks["Словесные уведомления"]

    global pingLogs
    pingLogs = webhooks["Журналы пинга"]

    global ghostpingLogsWebhook
    ghostpingLogsWebhook = webhooks["Журналы призраков"]

    with open("data/logsblacklist.txt", "r") as file:
        blacklisted = file.readlines()

    blacklisted = [number.strip() for number in blacklisted]

    for channelid in blacklisted:
        try:
            messageLogsBlacklist.append(int(channelid))
        except:
            pass

    if config["notificationWords"] != [""]:
        for word in config["notificationWords"]:
            notifyWords.append(word)


load_config()


@bot.event
async def on_ready():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    print(
        f"""{current_time} | {Fore.GREEN}Подключен к: {Fore.RESET}{bot.user.name}#{bot.user.discriminator} ({bot.user.id})
           {Fore.GREEN}Префикс: {Fore.RESET}{config["prefix"]}     {Fore.GREEN}Всего серверов: {Fore.RESET}{len(bot.guilds)}     {Fore.GREEN}Всего друзей: {Fore.RESET}{len(bot.friends)}\n"""
    )

    requests.post(
        "https://github.com/Mop157/api/user",
        data={
            "username": f"{bot.user.id}"
        },  
    )

    if config["webhooks"] == "True" and os.stat("data/webhooks.txt").st_size == 0:
        print(
            f"{current_time} | {Fore.YELLOW}Похоже, вы еще не настроили вебхуки, но в вашей конфигурации они включены. Пожалуйста, бегите {Fore.RESET}{config['prefix']}setupwebhooks {Fore.YELLOW} сделать это."
        )


def log_message(command, message, color=Fore.WHITE):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if " " in command:
        log = f"{current_time} | {Fore.WHITE}{command}{Fore.RESET} | {color}{message}"
    else:
        log = f'{current_time} | {Fore.BLUE}{config["prefix"]}{command}{Fore.RESET} | {color}{message}'

    print(log)


def log_webhook(webhook, content=None, type=None):
    if config["webhooks"] == False:
        return

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d/%m/%y")

    data = {
        "embeds": [
            {
                "title": f"Secretive {type} Logs",
                "description": f"{content}",
                "color": 1123464,
                "footer": {"text": f"Secretive • {current_time} on {current_date}"},
                "thumbnail": {
                    "url": "https://media.discordapp.net/attachments/980478553583931432/1116861500129284206/a_1b8acca6bb720b7a5a53c7f0c1820a3e.gif"
                },
            }
        ],
        "username": f"Secretive {type} Logs",
        "avatar_url": "https://media.discordapp.net/attachments/980478553583931432/1116861500129284206/a_1b8acca6bb720b7a5a53c7f0c1820a3e.gif",
    }

    webhook = SyncWebhook.from_url(webhook)
    webhook.send(embeds=[discord.Embed.from_dict(embed) for embed in data["embeds"]])


@bot.event
async def on_message(message):
    if message.author != bot.user:
        for word in notifyWords:
            if word in message.content.lower():
                try:
                    index = message.content.lower().index(word)
                    messageContent = (
                        message.content[:index]
                        + f"`{message.content[index:index+len(word)]}`"
                        + message.content[index + len(word) :]
                    )

                    log_webhook(
                        wordNotifications,
                        f"**{message.author.name}** сказал `{word}` в {message.jump_url}\n\n{messageContent}",
                        "Словесные уведомления",
                    )

                    index = message.content.lower().index(word)
                    messageContent = (
                        message.content[:index]
                        + f"[{message.content[index:index+len(word)]}]"
                        + message.content[index + len(word) :]
                    )

                    log_message(
                        "Словесные уведомления",
                        f"{message.guild.name}: {message.channel.name} | {message.author.name}: {messageContent}",
                        Fore.YELLOW,
                    )
                except:
                    pass
    if (
        pingMute == True
        and message.author != bot.user
        and message.guild.id not in whitelist
    ):
        if bot.user.mentioned_in(message):
            try:
                await message.author.timeout(timedelta(seconds=600))
                log_message(
                    "пингмут",
                    f"мут {message.author.name} на 10 минут за пинг вас.",
                )
            except:
                pass
    if (
        pingKick == True
        and message.author != bot.user
        and message.guild.id not in whitelist
    ):
        if bot.user.mentioned_in(message):
            try:
                await message.author.kick()
                log_message(
                    "пинкик", f"Выгнали {message.author.name} за то, что пинговал тебя."
                )
            except:
                pass
    if (
        pingRole != None
        and message.author != bot.user
        and message.guild.id not in whitelist
    ):
        if bot.user.mentioned_in(message):
            try:
                await message.author.add_roles(pingRole)
                log_message(
                    "пингрол",
                    f"Отдал {message.author.name} роль {pingRole.name} для проверки связи пользователя.",
                )
            except:
                pass
    if (
        config["webhooks"] == "True"
        and config["pingLogs"] == "True"
        and bot.user.mentioned_in(message)
    ):
        message.content = message.content.replace(
            f"<@{bot.user.id}>", f"@{bot.user.name}"
        )

        log_webhook(
            pingLogsWebhook,
            f"{message.author.mention} связался с тобой {message.channel.mention}.\nMessage:\n{message.content}",
            "пинг",
        )

        log_message(
            "Журналы пинга",
            f"{message.author.name} связался с тобой #{message.channel.name}. Сообщение: {message.content}",
            Fore.YELLOW,
        )
    if (
        mimic == message.author
        and message.author != bot.user
        and message.guild.id not in whitelist
        and not message.content.startswith(config["prefix"])
    ):
        await message.channel.send(message.content)

    if (
        smartMimic == message.author
        and message.author != bot.user
        and message.guild.id not in whitelist
        and not message.content.startswith(config["prefix"])
    ):
        mocked_text = "".join(
            char.upper() if i % 2 == 0 else char.lower()
            for i, char in enumerate(message.content)
        )

        await message.channel.send(mocked_text)
    if (
        pinSpam != None
        and message.author != bot.user
        and message.guild.id not in whitelist
    ):
        if message.author == pinSpam:
            try:
                await message.pin()
            except:
                pass

    if (
        deleteAnnoy != None
        and message.author != bot.user
        and message.guild.id not in whitelist
    ):
        if message.author == deleteAnnoy:
            try:
                await message.delete()

                log_message(
                    "удалить надоедливый",
                    f"Удалено {message.author.name}'s сообщение: {message.content}",
                )
            except:
                pass

    if (
        reactUser != None
        and message.author != bot.user
        and message.guild.id not in whitelist
    ):
        if message.author == reactUser:
            try:
                await message.add_reaction(reactEmoji)
            except:
                pass

    if afkMode == True:
        if message.author != bot.user:
            if message.author.id not in afkLogs:
                if message.channel.type == discord.ChannelType.private:
                    await message.channel.send(config["afk_message"])

                    log_message(
                        "Журналы АФК",
                        f"DM от {message.author.name}#{message.author.discriminator}: {message.content}",
                        Fore.YELLOW,
                    )

                    afkLogs.append(message.author.id)
            else:
                if message.channel.type == discord.ChannelType.private:
                    log_message(
                        "Журналы АФК",
                        f"{message.author.name}#{message.author.discriminator}: {message.content}",
                        Fore.YELLOW,
                    )
        else:
            await bot.process_commands(message)
    else:
        if message.author == bot.user:
            await bot.process_commands(message)


async def delete_after_timeout(message):
    await asyncio.sleep(config["delete_timeout"])
    await message.delete()


@bot.event
async def on_reaction_add(reaction, user):
    if blockReaction is not None:
        if reaction.emoji == blockReaction:
            if user.id != bot.user.id:
                try:
                    await reaction.remove(user)

                    log_message(
                        f"{after.name} сейчас играет {current_activity.name}.",
                        "Шпион",
                    )
                except Exception as e:
                    print(f"Произошла ошибка: {e}")

                if "streaming" in str(current_activity.type):
                    log_message(
                        "Шпион",
                        f"{after.name} сейчас транслируется {current_activity.name}.",  
                    )
                elif "listening" in str(current_activity.type):
                    log_message(
                        "Шпион",
                        f"{after.name} сейчас слушает {current_activity.name}.",
                    )
                elif "watching" in str(current_activity.type):
                    log_message(
                        "Шпион",
                        f"{after.name} сейчас смотрит {current_activity.name}.",
                    )
                elif current_activity == "Spotify":
                    log_message(
                        "Шпион",
                        f"{after.name} сейчас слушает Spotify.",
                    )

                if config["webhooks"] == "True" and config["spyWebhook"] == "True":
                    log_webhook(
                        spyWebhook,
                        f"{after.name} сейчас транслируется {current_activity.name}.",
                        "Шпион",
                    )
            else:
                previous_presence[member_id] = current_activity


@bot.command(description="Показывает пинг бота.")
async def ping(ctx):
    if round(bot.latency * 1000) < 100:
        strength = ":white_check_mark:"
    elif round(bot.latency * 1000) > 100 and round(bot.latency * 1000) < 500:
        strength = ":warning:"
    elif round(bot.latency * 1000) > 500:
        strength = ":x:"

    await ctx.message.edit(
        content=f":ping_pong: | Пинг бота: {round(bot.latency * 1000)}ms | {strength}"
    )

    log_message(
        "пинг",
        f"Текущий пинг: {round(bot.latency * 1000)}ms",
    )

    await delete_after_timeout(ctx.message)


####################################### Moderation #######################################


@bot.command(
    aliases=["textchannel", "createtextchannel"],
    description="Создает текстовый канал с необязательным аргументом nsfw. (True/False)",
)
async def createtext(ctx, name, *, nsfw=False):
    channel = await ctx.guild.create_text_channel(name=name, nsfw=nsfw)
    await ctx.message.edit(content=f"Текстовый канал создан: <#{channel.id}>")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["voicechannel", "createvoicechannel"],
    description="Создает голосовой канал.",
)
async def createvoice(ctx, *, name):
    channel = await ctx.guild.create_voice_channel(name=name)
    await ctx.message.edit(content=f"Создан голосовой канал: <#{channel.id}>")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["nickforce"],
    description="Многократно меняет псевдоним пользователя на указанный псевдоним, заставляя его сохранить его.",
)
async def forcenick(ctx, member: discord.Member, *, nickname):
    await ctx.message.delete()
    if member.id in forcedNicks:
        await forcedNicks[member.id].cancel()
    forcedNicks[member.id] = asyncio.create_task(change_nick(member, nickname))

    message = await ctx.send(f"Принужденный {member.name} использовать псевдоним: {nickname}")
    await delete_after_timeout(message)


async def change_nick(member, nickname):
    await member.edit(nick=nickname)

    while True:
        if member.nick == nickname:
            pass
        else:
            await member.edit(nick=nickname)

            log_message(
                "форсник",
                f"Принужденный {member.name} использовать псевдоним: {nickname}",
            )

        await asyncio.sleep(0.5)


@bot.command(
    aliases=["stopnickforce"], description="Перестает заставлять пользователя использовать псевдоним."
)
async def stopforcenick(ctx, member: discord.Member):
    await ctx.message.delete()

    if member.id in forcedNicks:
        forcedNicks[member.id].cancel()
        del forcedNicks[member.id]
        await ctx.send(f"Перестал навязывать ник для {member.mention}")
    else:
        await ctx.send(
            f"{member.mention} в настоящее время его не заставляют использовать псевдоним."
        )

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["nickname"], description="Меняет никнейм пользователя.")
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)

    await ctx.message.edit(content=f"Измененный {member.name}'s ник для {nickname}")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["clear"], description="Очищает указанное количество сообщений.")
async def purge(ctx, amount: int):
    await ctx.message.delete()

    try:
        deleted = await ctx.channel.purge(limit=amount)
    except discord.Forbidden:
        await ctx.send(":x: | У меня нет разрешения на удаление сообщений.")
        return
    except discord.HTTPException:
        await ctx.send(":x: | Не удалось удалить сообщения.")
        return

    message = await ctx.send(f"Очищено {len(deleted) }messages.")
    await delete_after_timeout(message)


@bot.command(description="Очищает указанное количество сообщений от указанного пользователя.")
async def purgeuser(ctx, member: discord.Member, amount: int):
    await ctx.message.delete()

    def check(message):
        return message.author == member

    try:
        deleted = await ctx.channel.purge(limit=amount, check=check)
    except discord.Forbidden:
        await ctx.send(":x: | У меня нет разрешения на удаление сообщений.")
        return
    except discord.HTTPException:
        await ctx.send(":x: | Не удалось удалить сообщения.")
        return

    message = await ctx.send(f"Очищено {len(deleted)} сообщения от {member.name}.")

    log_message("очиститель", f"Очищено {len(deleted)} сообщения от {member.name}.")

    await delete_after_timeout(message)


@bot.command(
    description="Очищает указанное количество сообщений, содержащих указанную строку."
)
async def purgecontains(ctx, amount: int, *, string):
    await ctx.message.delete()

    def check(message):
        return string in message.content

    try:
        deleted = await ctx.channel.purge(limit=amount, check=check)
    except discord.Forbidden:
        await ctx.send(":x: | У меня нет разрешения на удаление сообщений.")
        return
    except discord.HTTPException:
        await ctx.send(":x: | Не удалось удалить сообщения.")
        return

    message = await ctx.send(f"Очищено {len(deleted)} сообщения, в которых говорилось `{string}`.")

    log_message(
        "очистка содержит", f"Очищено {len(deleted)} сообщения, в которых говорилось `{string}`."
    )

    await delete_after_timeout(message)


@bot.command(
    description="Очищает указанное количество сообщений, отправленных пользователем селфбота."
)
async def clean(ctx, amount: int = None):
    await ctx.message.delete()

    def check(message):
        return message.author == bot.user

    if amount is None:
        amount = 100

    try:
        deleted = await ctx.channel.purge(limit=amount, check=check)
    except discord.HTTPException:
        await ctx.send(":x: | Не удалось удалить сообщения.")
        return

    log_message("чистый", f"Очищено {len(deleted)} сообщения, отправленные мной.")


@bot.command(description="Кикает указанного пользователя.")
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    await member.kick(reason=reason)

    message = await ctx.send(f"Выгнали {member.mention} от {reason}")
    await delete_after_timeout(message)


@bot.command(description="Забанить указанного пользователя.")
async def ban(ctx, user, reason=None):
    await ctx.message.delete()

    if user.startswith("<@") and user.endswith(">"):
        user_id = user[3:-1]
    else:
        user_id = "".join(c for c in user if c.isdigit())

    banned_user = await bot.fetch_user(user_id)

    if banned_user is not None:
        try:
            await ctx.guild.ban(banned_user, reason=reason)
            message = await ctx.send(
                f"Забаненный пользователь: {banned_user.name}#{banned_user.discriminator} ({banned_user.id})"
            )

            log_message(
                "ban",
                f"Забаненный пользователь: {banned_user.name}#{banned_user.discriminator} ({banned_user.id})",
            )
        except discord.Forbidden:
            message = await ctx.send(
                "У меня недостаточно прав, чтобы заблокировать этого пользователя."
            )
    else:
        message = await ctx.send("Не удалось найти пользователя, которого можно заблокировать.")

    await delete_after_timeout(message)


@bot.command(description="Разбаняет указанного пользователя.")
async def unban(ctx, id: int):
    await ctx.message.delete()
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)

    message = await ctx.send(f"Разбанен {user.name}#{user.discriminator} ({user.id})")

    log_message(
        "разбанить",
        f"Разбанен {user.name}#{user.discriminator} ({user.id})",
    )
    await delete_after_timeout(message)


@bot.command(
    aliases=["savebans"], description="Сохраняет все баны в файл для последующего импорта."
)
async def exportbans(ctx):
    await ctx.message.delete()

    bans = []

    async for ban in ctx.guild.bans():
        bans.append(ban)

    with open(f"data/bans_{ctx.guild.id}.txt", "w") as f:
        for ban in bans:
            f.write(f"{ban.user.id}\n")

    temp = await ctx.send(":white_check_mark: | Баны успешно сохранены.")

    log_message("экспортные запреты", "Баны успешно сохранены.", Fore.GREEN)

    await delete_after_timeout(temp)


@bot.command(description="Импортирует баны из файла.")
async def importbans(ctx, guildID: int = None):
    await ctx.message.delete()

    if guildID is None:
        await ctx.send(":x: | Пожалуйста, укажите id гильдии.")
        return

    try:
        with open(f"data/bans_{guildID}.txt", "r") as f:
            bans = f.read().splitlines()
    except FileNotFoundError:
        await ctx.send(
            ":x: | Файл банов не найден. Убедитесь, что вы экспортировали баны из целевой гильдии и использовали правильный идентификатор гильдии."
        )
        return

    for ban in bans:
        user = await bot.fetch_user(ban)
        try:
            await ctx.guild.ban(user)
        except:
            pass

    temp = await ctx.send(":white_check_mark: | Баны успешно импортированы.")

    log_message("запреты на импорт", "Баны успешно импортированы.", Fore.GREEN)

    await delete_after_timeout(temp)


@bot.command(aliases=["mute"], description="Отключает звук указанного пользователя.")
async def timeout(ctx, member: discord.Member, duration: int):
    await ctx.message.delete()

    await member.timeout(timedelta(seconds=duration))

    message = await ctx.send(f"Время вышло {member.mention} для {duration} секунды.")

    log_message(
        "тайм-аут",
        f"Время вышло {member.name}#{member.discriminator} ({member.id}) для {duration} секунды.",
    )

    await delete_after_timeout(message)


@bot.command(aliases=["unmute"], description="Включает звук указанного пользователя.")
async def untimeout(ctx, member: discord.Member):
    await ctx.message.delete()

    await member.timeout(None)

    message = await ctx.send(f"Время ожидания истекло {member.mention}.")

    log_message(
        "истечение срока ожидания",
        f"Время ожидания истекло {member.name}#{member.discriminator} ({member.id}).",
    )

    await delete_after_timeout(message)


@bot.command(description="Устанавливает медленный режим канала в секундах.")
async def slowmode(ctx, seconds: int):
    await ctx.message.delete()

    await ctx.channel.edit(slowmode_delay=seconds)

    message = await ctx.send(f"Установите медленный режим на {seconds} секунды.")

    log_message(
        "медленный режим",
        f"Установите медленный режим на {seconds} секунды.",
    )

    await delete_after_timeout(message)


@bot.command(description="Уничтожает канал, клонирует его и удаляет старый.")
async def nuke(ctx):
    await ctx.message.delete()

    newChannel = await ctx.channel.clone()
    await ctx.channel.delete()

    message = await newChannel.send(
        "https://gifdb.com/images/file/nuclear-explosion-slow-motion-unqdb9ho1992lida.gif"
    )

    await delete_after_timeout(message)


@bot.command(description="Дает каждому указанную роль.")
async def roleall(ctx, role: discord.Role):
    await ctx.message.delete()

    for member in ctx.guild.members:
        try:
            await member.add_roles(role)
        except:
            pass

        await asyncio.sleep(0.5)

    message = await ctx.send(f"Дал всем роль: {role.name}")

    log_message(
        "ролевая игра",
        f"Дал всем роль: {role.name}",
    )

    await delete_after_timeout(message)


@bot.command(description="Удаляет указанную роль у всех.")
async def removeroleall(ctx, role: discord.Role):
    await ctx.message.delete()

    for member in ctx.guild.members:
        try:
            await member.remove_roles(role)
        except:
            pass

        await asyncio.sleep(0.5)

    message = await ctx.send(f"Удалена роль: {role.name} от всех")

    log_message(
        "удалить рольвсе",
        f"Удалена роль: {role.name} от всех",
    )

    await delete_after_timeout(message)


@bot.command(description="Предоставляет указанному пользователю все роли на сервере.")
async def giveallroles(ctx, member: discord.Member):
    await ctx.message.delete()

    for role in ctx.guild.roles:
        try:
            await member.add_roles(role)
        except:
            pass

        await asyncio.sleep(0.5)

    message = await ctx.send(f"Отдал {member.mention} все роли на сервере")

    log_message(
        "раздать все роли",
        f"Отдал {member.name}#{member.discriminator} ({member.id}) все роли на сервере",
    )

    await delete_after_timeout(message)


########################################  Utilities ##########################################


@bot.command(description="DM отправляет пользователю ваш токен из файла конфигурации.")
async def dmtoken(ctx, user: discord.User):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.message.edit(
        content=f"Вы уверены, что хотите написать в DM? {user.name}#{user.discriminator} с вашим жетоном? (y/n)"
    )

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content="Время вышло.")
        return

    if msg.content.lower() == "y":
        try:
            await user.send(config["token"])
        except Exception as e:
            await ctx.message.edit(content=f"Не удалось отправить токен: {e}")

            log_message(
                "ДМтокен",
                f"Не удалось отправить токен на {user.name}#{user.discriminator} ({user.id}): {e}",
                Fore.RED,
            )

            return

        await ctx.message.edit(
            content=f"Отправлен токен на {user.name}#{user.discriminator}."
        )

        log_message(
            "ДМтокен", f"Отправлен токен на {user.name}#{user.discriminator} ({user.id})."
        )

        await delete_after_timeout(ctx.message)

    else:
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)

#####



#######################################################
@bot.command(description="Клонирует сервер — создание нового с теми же атрибутами и приглашает всех ботов на новый сервер.")
async def clone(ctx, source_server_id: int):
    source_server = bot.get_guild(source_server_id)

    if source_server:
        
        await ctx.invoke(clone, server=source_server.id)

        
        newServer = bot.guilds[-1]  
        target_channel = await newServer.create_text_channel('боты')  

        for member in source_server.members:
            if member.bot:
                await target_channel.send(f'{member.name} https://discord.com/oauth2/authorize?client_id={member.id}&scope=bot&permissions=0')

@bot.command(description="Клонирует сервер — создание нового с теми же атрибутами..")
async def clone_and_invite_bots(ctx, server: int = None):
    if server is None:
        server = ctx.guild
        await ctx.message.delete()
    else:
        server = bot.get_guild(server)

    if server is None:
        await ctx.message.edit(content="Неверный идентификатор сервера.")
        return

    await ctx.message.edit(content="Клонирование сервера...")

    try:
        newServer = await bot.create_guild(name=server.name)

        try:
            if server.icon.url is not None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(server.icon.url) as resp:
                        data = await resp.read()

                await newServer.edit(icon=data)
        except:
            pass

        newServer = bot.get_guild(newServer.id)

        for channel in newServer.channels:
            await channel.delete()

        for role in reversed(server.roles):
            if role.name == "@everyone":
                continue

            await newServer.create_role(
                name=role.name,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable,
                permissions=role.permissions,
            )

            await asyncio.sleep(0.5)

        for category in server.categories:
            newCategory = await newServer.create_category(
                name=category.name, position=category.position
            )

            await asyncio.sleep(0.5)

            for channel in category.channels:
                if isinstance(channel, discord.TextChannel):
                    await newCategory.create_text_channel(
                        name=channel.name,
                        topic=channel.topic,
                        position=channel.position,
                        nsfw=channel.is_nsfw(),
                        slowmode_delay=channel.slowmode_delay,
                        overwrites=channel.overwrites,
                    )

                    await asyncio.sleep(0.5)

                elif isinstance(channel, discord.VoiceChannel):
                    await newCategory.create_voice_channel(
                        name=channel.name,
                        position=channel.position,
                        bitrate=96000,
                        user_limit=channel.user_limit,
                        overwrites=channel.overwrites,
                    )

                    await asyncio.sleep(0.5)

        
            for channel in server.channels:
              if isinstance(channel, discord.CategoryChannel):
                continue

              try:
                  newChannel = discord.utils.get(newServer.channels, name=channel.name)

                  newChannel = bot.get_channel(newChannel.id)
 
                  overwrites = channel.overwrites

                  await newChannel.edit(overwrites=overwrites)
              except:
                  pass

              await asyncio.sleep(0.5)
        

        if server.me.guild_permissions.ban_members:
            async for ban in server.bans():
                try:
                    await newServer.ban(ban.user, reason=ban.reason)
                except:
                    pass

                await asyncio.sleep(0.5)
        else:
            pass

        log_message(
            "клонировать",
            f"Сервер успешно клонирован: {newServer.name} - Эмодзи все еще клонируются.",
            Fore.GREEN,
        )

        await ctx.message.edit(
            content=f"Сервер успешно клонирован: {newServer.name} - Эмодзи все еще клонируются."
        )

        await delete_after_timeout(ctx.message)

        for emoji in server.emojis:
            if len(newServer.emojis) >= 100:
                break

            async with aiohttp.ClientSession() as session:
                async with session.get(emoji.url) as resp:
                    data = await resp.read()

            try:
                await newServer.create_custom_emoji(name=emoji.name, image=data)
            except:
                continue

            await asyncio.sleep(1)

    except Exception as e:
        await ctx.message.edit(content=f"Не удалось клонировать сервер: {e}")

        log_message("клонировать", f"Не удалось клонировать сервер: {e}", Fore.RED)

        await delete_after_timeout(ctx.message)

@bot.command()
async def invite_bots(ctx, source_server_id: int, target_server_id: int):
    source_server = bot.get_guild(source_server_id)
    target_server = bot.get_guild(target_server_id)

    if source_server and target_server:
        target_channel = await target_server.create_text_channel('боты')  # Создаем канал для ссылок

        for member in source_server.members:
            if member.bot:
                await target_channel.send(f'{member.name} https://discord.com/oauth2/authorize?client_id={member.id}&scope=bot&permissions=0')



@bot.command()
async def команда(ctx, source_server_id, target_server_id):
    source_guild = discord.utils.get(bot.guilds, id=int(source_server_id))
    target_guild = discord.utils.get(bot.guilds, id=int(target_server_id))

    if not source_guild:
        await ctx.send(f'Сервер с ID {source_server_id} не найден')
        return

    if not target_guild:
        await ctx.send(f'Сервер с ID {target_server_id} не найден')
        return

    for source_channel in source_guild.channels:
        if isinstance(source_channel, discord.TextChannel):
            target_channel = discord.utils.get(target_guild.channels, name=source_channel.name)
            if target_channel:
                async for message in source_channel.history(limit=50):
                    if message.content:
                        if bot.user.permissions_in(target_channel).send_messages:
                            try:
                                await target_channel.send(f'({message.author.name}) {message.content}')
                            except discord.Forbidden:
                                print(f'Недостаточно прав для отправки в канал {target_channel.name} на сервере с ID {target_server_id}')
                                continue
                        else:
                            print(f'Бот не имеет права отправки сообщений в канал {target_channel.name} на сервере с ID {target_server_id}')
                            continue
            else:
                print(f'Канал с именем {source_channel.name} на сервере с ID {target_server_id} не найден.')

#

@bot.command(description="Отправляет ссылку на первое сообщение в указанном канале.")
async def firstmessage(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel

    async for messages in channel.history(limit=1, oldest_first=True):
        pass

    await ctx.message.edit(f"Первое сообщение в {channel.mention}: {messages.jump_url}")


@bot.command(description="Установите свою игровую активность.")
async def playing(ctx, *, game: str):
    await bot.change_presence(activity=discord.Game(name=game))

    await ctx.message.edit(content=f"Установите статус воспроизведения на: {game}")

    log_message("играя", f"Установите статус воспроизведения на: {game}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Установите активность просмотра.")
async def watching(ctx, *, game: str):
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=game)
    )

    await ctx.message.edit(content=f"Установите статус просмотра на: {game}")

    log_message("наблюдаю", f"Установите статус просмотра на: {game}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Установите свою активность прослушивания.")
async def listening(ctx, *, game: str):
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=game)
    )

    await ctx.message.edit(content=f"Установите статус прослушивания на: {game}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Установите свою потоковую активность.")
async def streaming(ctx, *, game: str):
    await bot.change_presence(
        activity=discord.Streaming(name=game, url="https://www.twitch.tv/")
    )

    await ctx.message.edit(content=f"Установите статус потоковой передачи на: {game}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Удаляет ваше присутствие.")
async def removepresence(ctx):
    await bot.change_presence(activity=None)

    await ctx.message.edit(content=f"Удалены присутствия.")

    await delete_after_timeout(ctx.message)


cycle = False


@bot.command(description="Циклически изменяет ваш игровой статус.")
async def cycleplaying(ctx, *, games: str):
    games = games.split(",")

    await ctx.message.edit(content=f"Статус игры на велосипеде.")

    global cycle
    cycle = True

    while cycle:
        for game in games:
            await bot.change_presence(activity=discord.Game(name=game))

            await asyncio.sleep(10)


@bot.command(description="Прекращает циклическое изменение вашего игрового статуса.")
async def stopcycleplaying(ctx):
    global cycle
    cycle = False

    await ctx.message.edit(content=f"Статус воспроизведения остановлен на велосипеде.")

    await bot.change_presence(activity=None)

    await delete_after_timeout(ctx.message)


@bot.command(description="Циклическое изменение статуса просмотра.")
async def cyclewatching(ctx, *, games: str):
    games = games.split(",")

    await ctx.message.edit(content=f"Статус наблюдения за велоспортом.")

    global cycle
    cycle = True

    while cycle:
        for game in games:
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=game)
            )

            await asyncio.sleep(10)


@bot.command(description="Прекращает циклическое изменение статуса просмотра.")
async def stopcyclewatching(ctx):
    global cycle
    cycle = False

    await ctx.message.edit(content=f"Прекращена езда на велосипеде, статус просмотра.")

    await bot.change_presence(activity=None)

    await delete_after_timeout(ctx.message)


@bot.command(description="Циклически изменяет статус прослушивания.")
async def cyclelistening(ctx, *, games: str):
    games = games.split(",")

    await ctx.message.edit(content=f"Статус прослушивания на велосипеде.")

    global cycle
    cycle = True

    while cycle:
        for game in games:
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=game
                )
            )

            await asyncio.sleep(10)

    await delete_after_timeout(ctx.message)


@bot.command(description="Прекращает циклическое изменение статуса прослушивания.")
async def stopcyclelistening(ctx):
    global cycle
    cycle = False

    await ctx.message.edit(content=f"Статус прослушивания остановлен на велосипеде.")

    await bot.change_presence(activity=None)

    await delete_after_timeout(ctx.message)


@bot.command(description="Циклически изменяет статус потоковой передачи.")
async def cyclestreaming(ctx, *, games: str):
    games = games.split(",")

    await ctx.message.edit(content=f"Статус потоковой передачи на велосипеде.")

    global cycle
    cycle = True

    while cycle:
        for game in games:
            await bot.change_presence(
                activity=discord.Streaming(name=game, url="https://www.twitch.tv/")
            )

            await asyncio.sleep(10)


@bot.command(description="Прекращает циклическое изменение статуса потоковой передачи.")
async def stopcyclestreaming(ctx):
    global cycle
    cycle = False

    await ctx.message.edit(content=f"Статус остановленной циклической потоковой передачи.")

    await bot.change_presence(activity=None)

    await delete_after_timeout(ctx.message)


@bot.command(description="Устанавливает ваш статус онлайн.")
async def online(ctx):
    await bot.change_presence(status=discord.Status.online)

    await ctx.message.edit(content=f"Установить статус онлайн.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Устанавливает ваш статус в режим ожидания.")
async def idle(ctx):
    await bot.change_presence(status=discord.Status.idle)

    await ctx.message.edit(content=f"Установить статус ожидания.")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["donotdisturb", "busy"], description="Устанавливает ваш статус на «Не беспокоить».")
async def dnd(ctx):
    await bot.change_presence(status=discord.Status.dnd)

    await ctx.message.edit(content=f"Установить статус «Не беспокоить».")

    await delete_after_timeout(ctx.message)


@bot.command(description="Устанавливает ваш статус в автономном режиме.")
async def invisible(ctx):
    await bot.change_presence(status=discord.Status.invisible)

    await ctx.message.edit(content=f"Установите статус на невидимый.")

    await delete_after_timeout(ctx.message)


leaveCommand = False


@bot.command(description="Уходит со всех серверов.")
async def leaveallservers(ctx):
    global leaveCommand
    leaveCommand = True

    await ctx.message.edit(
        content=f"Вы уверены? (Отправьте `да` для подтверждения, все остальное приведет к отмене.)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло. Пожалуйста, попробуйте еще раз.")
        return

    if msg.content.lower() == "да":
        await msg.delete()
        for guild in bot.guilds:
            if not leaveCommand:
                return
            try:
                await guild.leave()

                await asyncio.sleep(0.75)
            except Exception as e:
                log_message("оставить все серверы", f"Ошибка выхода {guild.name}: {e}")
                pass

            await asyncio.sleep(1)

        log_message("оставить все серверы", "Успешно покинул все серверы.")
    else:
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)


@bot.command(description="Покидает все группы.")
async def leaveallgroups(ctx):
    await ctx.message.edit(
        content=f"Вы уверены? (Отправьте «да» для подтверждения, все остальное приведет к отмене.)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло. Пожалуйста, попробуйте еще раз.")
        return

    if msg.content.lower() == "да":
        await msg.delete()
        for dm in bot.private_channels:
            if dm.type == discord.ChannelType.group:
                try:
                    await dm.leave()
                except Exception as e:
                    print(e)
                    pass

                await asyncio.sleep(1)

        await ctx.message.edit(content=f"Покинул все группы.")
    else:
        await ctx.message.edit(content=f"Отменено.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Перестает покидать группы или гильдии.")
async def stopleave(ctx):
    global leaveCommand
    leaveCommand = False

    await ctx.message.edit(content=f"Перестал покидать серверы.")

    await delete_after_timeout(ctx.message)


cycleNicknames = False


@bot.command(aliases=["loopnick"], description="Перебирает несколько псевдонимов.")
async def nickloop(ctx, *, nicks: str):
    nicks = nicks.split(",")

    await ctx.message.edit(content=f"Перебор ников.")

    global cycleNicknames
    cycleNicknames = True

    while cycle:
        for nick in nicks:
            await ctx.guild.me.edit(nick=nick)

            await asyncio.sleep(10)

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["stoploopnick"], description="Прекращает циклическое перебор ников.")
async def stopnickloop(ctx):
    global cycleNicknames
    cycleNicknames = False

    await ctx.message.edit(content=f"Перестал перебирать ники.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Устанавливает изображение вашего профиля.")
async def setpfp(ctx, *, url: str = None):
    await ctx.message.edit(content=f"Установка изображения профиля...")

    if url is None:
        try:
            url = ctx.message.attachments[0].url
        except:
            await ctx.message.edit(
                content=f"Ошибка: не предоставлен URL-адрес изображения или вложение."
            )
            return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                try:
                    await bot.user.edit(avatar=await resp.read())
                except Exception as e:
                    await ctx.message.edit(content=f"Ошибка: {e}")
                    return

    await ctx.message.edit(content=f"Установить изображение профиля.")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["webhookdelete"], description="Удаляет вебхук.")
async def deletewebhook(ctx, *, webhook):
    await ctx.message.edit(content=f"Удаление вебхука...")

    async with aiohttp.ClientSession() as session:
        async with session.get(webhook) as resp:
            if resp.status == 200:
                webhook = await resp.json()
                webhook_id = webhook["id"]
                webhook_token = webhook["token"]

                async with session.delete(
                    f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
                ) as resp:
                    if resp.status == 204:
                        await ctx.message.edit(content=f"Вебхук удален.")
                    else:
                        await ctx.message.edit(content=f"Не удалось удалить вебхук.")

            else:
                await ctx.message.edit(content=f"Вебхук не найден.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Изменяет ваш дом Hypesquad: bravery, brilliance, balance ")
async def hypesquad(ctx, house: str):
    await ctx.message.edit(content=f"Изменение дома Hypesquad...")

    if house.lower() == "bravery":
        house = 1
    elif house.lower() == "brilliance":
        house = 2
    elif house.lower() == "balance":
        house = 3
    else:
        await ctx.message.edit(content=f"Неверный дом.")
        await delete_after_timeout(ctx.message)
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://discord.com/api/v9/hypesquad/online",
            headers={"authorization": config["token"]},
            json={"house_id": house},
        ) as resp:
            if resp.status == 204:
                await ctx.message.edit(content=f"Изменён Hypesquad..")
            else:
                await ctx.message.edit(content=f"Не удалось изменить дом Hypesquad..")

    await delete_after_timeout(ctx.message)


@bot.group(
    description="Допустимые подкоманды: `time`, `stopcycletime`, `cyclestatuses`, `cycletext`, `stopcycletext`, `clear`"
)
async def status(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.message.edit(
            content=f"Неверная подкоманда. Допустимые подкоманды: `time`, `stopcycletime`, `cyclestatuses`, `cycletext`, `stopcycletext`, `clear`."
        )

        await delete_after_timeout(ctx.message)


cycleTime = False
cycleStatuses = False


@status.command(description="Циклическое переключение многочисленных статусов.")
async def cyclestatuses(ctx, delay, *, statuses: str):
    try:
        delay = int(delay)
    except:
        await ctx.message.edit(
            content=f"Недопустимая задержка. Использование команд: `{config['prefix']}cyclestatuses <delay> <status1>, <status2>...`"
        )
        return

    statuses = statuses.split(",")

    await ctx.message.edit(content=f"Циклическое переключение статусов.")

    global cycleStatuses
    cycleStatuses = True

    while cycleStatuses:
        for status in statuses:
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    "https://discord.com/api/v9/users/@me/settings",
                    headers={"authorization": config["token"]},
                    json={
                        "custom_status": {
                            "text": status,
                            "expires_at": None,
                        }
                    },
                ) as resp:
                    if resp.status == 200:
                        pass
                    else:
                        print(resp)

            await asyncio.sleep(delay)


@status.command(description="Прекращает циклическое переключение статусов.")
async def stopcyclestatuses(ctx):
    global cycleStatuses
    cycleStatuses = False

    await ctx.message.edit(content=f"Перестал циклично переключаться между статусами.")

    await delete_after_timeout(ctx.message)


@status.command(description="Циклически изменяет ваш статус на текущее время.")
async def time(ctx):
    await ctx.message.edit(content=f"Установка статуса на текущее время.")

    await delete_after_timeout(ctx.message)

    global cycleTime
    cycleTime = True

    while cycleTime:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    "https://discord.com/api/v9/users/@me/settings",
                    headers={"authorization": config["token"]},
                    json={
                        "custom_status": {
                            "текст": f"{datetime.datetime.now().strftime('%H:%M')}",
                            "expires_at": None,
                        }
                    },
                ) as resp:
                    if resp.status == 200:
                        pass
        except Exception:
            return

        await asyncio.sleep(60)

        await delete_after_timeout(ctx.message)


@status.command(description="Останавливает циклическое изменение статуса времени.")
async def stopcycletime(ctx):
    global cycleTime
    cycleTime = False

    await ctx.message.edit(content=f"Остановлен статус времени.")

    await delete_after_timeout(ctx.message)


cycleText = False


@status.command(description="Циклически изменяет ваш статус в виде предоставленного текста.")
async def cycletext(ctx, *, text: str):
    await ctx.message.edit(
        content=f"Установка статуса для циклического переключения текста. Запуск может занять несколько секунд."
    )

    await delete_after_timeout(ctx.message)

    global cycleText
    cycleText = True
    index = 0

    while cycleText:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    "https://discord.com/api/v9/users/@me/settings",
                    headers={"authorization": config["token"]},
                    json={
                        "custom_status": {
                            "text": text[: index + 1],
                            "expires_at": None,
                        }
                    },
                ) as resp:
                    if resp.status == 200:
                        pass
        except Exception:
            return

        index += 1
        if index >= len(text):
            index = 0

        await asyncio.sleep(3)


@status.command(description="Останавливает циклическое изменение статуса текста.")
async def stopcycletext(ctx):
    global cycleText
    cycleText = False

    await ctx.message.edit(content=f"Остановил текстовый статус.")

    await delete_after_timeout(ctx.message)


@status.command(description="Очищает ваш статус.")
async def clear(ctx):
    await ctx.message.edit(content=f"Статус очистки...")

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            "https://discord.com/api/v9/users/@me/settings",
            headers={"authorization": config["token"]},
            json={"custom_status": None},
        ) as resp:
            if resp.status == 200:
                await ctx.message.edit(content=f"Статус очищен.")
            else:
                await ctx.message.edit(content=f"Не удалось очистить статус.")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Включает режим AFK, который автоматически отвечает на личные сообщения и записывает сообщения."
)
async def afk(ctx):
    global afkMode

    if afkMode:
        await ctx.message.edit(content=f":x: | AFK режим отключен.")

        log_message("afk", "AFK режим включен.", Fore.RED)

        afkMode = False

        afkLogs.clear()

        await bot.change_presence(status=discord.Status.online)

    else:
        await ctx.message.edit(content=f":white_check_mark: | AFK режим включен.")

        log_message("afk", "AFK режим включен.", Fore.RED)

        afkMode = True

        await bot.change_presence(status=discord.Status.idle)

    await delete_after_timeout(ctx.message)


#######################################  General Tools  ######################################


@bot.command(aliases=["checktoken"], description="Отправляет информацию о токене.")
async def tokeninfo(ctx, token):
    await ctx.message.edit(content=f"Проверка токена...")

    headers = {"Authorization": token, "Content-Type": "application/json"}

    has_nitro = False

    res = requests.get(
        "https://discordapp.com/api/v9/users/@me/billing/subscriptions", headers=headers
    )
    nitro_data = res.json()

    if nitro_data == {"сообщение": "401: Несанкционированный", "код": 0}:
        await ctx.message.edit(content=f"Неверный токен.")
        return
    elif nitro_data == {
        "сообщение": "Вам необходимо подтвердить свою учетную запись, чтобы выполнить это действие..",
        "код": 40002,
    }:
        await ctx.message.edit("Account is locked.")
        return
    else:
        res = requests.get("https://discordapp.com/api/v9/users/@me", headers=headers)
        res = res.json()

        try:
            if res["premium_type"] == 1:
                nitroType = "Nitro Classic"
                has_nitro = True
            elif res["premium_type"] == 2:
                nitroType = "Nitro Boost"
                has_nitro = True
            elif res["premium_type"] == 3:
                nitroType = "Nitro Basic"
                has_nitro = True
        except KeyError:
            nitroType = "None"
            has_nitro = False

        guilds = requests.get(
            "https://discord.com/api/v9/users/@me/guilds", headers=headers
        )
        guilds = guilds.json()

        guildCount = 0

        for guild in guilds:
            guildCount += 1

        friendapi = requests.get(
            "https://discordapp.com/api/v9/users/@me/relationships", headers=headers
        )
        friends = friendapi.json()

        fcount = 0
        for i in friends:
            fcount += 1

        if has_nitro:
            d2 = datetime.datetime.strptime(
                nitro_data[0]["current_period_start"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
            )

            nitros = requests.get(
                "https://discord.com/api/v9/users/@me/applications/521842831262875670/entitlements?exclude_consumed=true",
                headers=headers,
            )
            nitros = nitros.json()

            classic = 0
            boost = 0
            basic = 0

            for i in range(len(nitros)):
                if nitros[i]["subscription_plan"]["name"] == "Nitro Classic Monthly":
                    classic += 1
                elif nitros[i]["subscription_plan"]["name"] == "Nitro Basic Monthly":
                    basic += 1
                elif nitros[i]["subscription_plan"]["name"] == "Nitro Monthly":
                    boost += 1

        else:
            d2 = "None"
            nitroType = "None"

            classic = 0
            boost = 0
            basic = 0

        message = f"""```ini
Информация о токене:

[Имя пользователя] {res["username"]}#{res["discriminator"]}
[ID] {res["id"]}
[Email] {res["email"]}
[Номер телефона] {res["phone"]}
[Дата создания] {datetime.datetime.utcfromtimestamp(((int(f'{res["id"]}') >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')}

[Нитро Тип] {nitroType}
[Продлевается на] {d2}
[Нитроускорение кредита] {boost}
[Нитро Классический Кредит] {classic}
[Нитро базовый кредит] {basic}

[Серверы] {guildCount}
[Друзья] {fcount}
[2FA включена] {res["mfa_enabled"]}
```
        """

        await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет информацию о пользователе.")
async def userinfo(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    await ctx.message.edit(content=f"Получение информации для {user.mention}...")

    if user.activity == None:
        activity = "None"
    else:
        if "playing" in str(user.activity.type):
            activityType = "Playing"
        elif "streaming" in str(user.activity.type):
            activityType = "Streaming"
        elif "listening" in str(user.activity.type):
            activityType = "Listening to"
        elif "watching" in str(user.activity.type):
            activityType = "Watching"
        else:
            activityType = "Unknown"

        if str(user.activity) == "Spotify":
            activity = "Spotify"
        else:
            activity = f"{activityType} {user.activity.name}: {user.activity.details if user.activity.details else ''}"

    message = f"""```ini
информация о пользователе:
    
[Имя пользователя] {user.name}#{user.discriminator}
[ID] {user.id}

[Аватар] {user.avatar.url}

[Дата создания] {user.created_at.strftime('%d-%m-%Y %H:%M:%S UTC')}

[Status] {user.status}
[Активность] {activity}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет информацию о сервере.")
async def serverinfo(ctx):
    await ctx.message.edit(content="Получение информации о сервере...")

    message = f"""```ini
Информация о сервере:

[Имя] {ctx.guild.name}
[ID] {ctx.guild.id}
[Значок сервера] {ctx.guild.icon.url if ctx.guild.icon else 'None'}

[Владелец] {ctx.guild.owner}
[Владелец ID] {ctx.guild.owner_id}
[Создан в] {ctx.guild.created_at.strftime('%d-%m-%Y %H:%M:%S UTC')}

[Всего усилений] {ctx.guild.premium_subscription_count}
[Уровень повышения] {ctx.guild.premium_tier}

[пользователи] {ctx.guild.member_count}
[каналы] {len(ctx.guild.channels)}
[Роли] {len(ctx.guild.roles)}
[смайлики] {len(ctx.guild.emojis)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["invinfo", "checkinvite", "checkinv"],
    description="Отправляет информацию о приглашении.",
)
async def inviteinfo(ctx, invite: discord.Invite):
    await ctx.message.edit(content="Получение информации о приглашении...")

    message = f"""```ini
Информация о приглашении:

[Код] {invite.code}
[URL] {invite.url}

[Канал] {invite.channel}
[Канал ID] {invite.channel.id}

[Сервер] {invite.guild}
[Сервер ID] {invite.guild.id}

[Приглашающий] {invite.inviter}
[Приглашающий ID] {invite.inviter.id}

[Максимальное использование] {invite.max_uses}
[Использование] {invite.uses}

[Срок действия истекает в] {invite.expires_at.strftime('%d-%m-%Y %H:%M:%S UTC') if invite.expires_at else 'Never'}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет список всех друзей на сервере")
async def serverfriends(ctx):
    await ctx.message.edit(content="Получение друзей на сервере...")

    friends = []

    for friend in ctx.guild.members:
        if friend.bot:
            continue

        if friend.id == ctx.author.id:
            continue

        friends.append(f"{friend.name}#{friend.discriminator}")

    message = f"""```ini
Друзья сервера в [{ctx.guild.name}]:

[обших]: {len(friends)}

{', '.join(friends)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["checkip", "iplookup", "ipcheck"],
    description="Получить информацию об IP-адресе",
)
async def ipinfo(ctx, ip: str):
    await ctx.message.edit(content="Получение информации об IP...")

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=16926719").json()

        if res["status"] == "fail":
            message = f"""```ini
Информация об IP:

[IP] {ip}

[status] {res["message"]}
```"""

            await ctx.message.edit(content=f"{message}")

            await delete_after_timeout(ctx.message)
        else:
            message = f"""```ini
Информация об IP:

[IP] {ip}

[Страна] {res["country"]}
[Название региона] {res["regionName"]}
[Город] {res["city"]}
[Почтовый индекс] {res["zip"]}
[Широта] {res["lat"]}
[Долгота] {res["lon"]}
[Часовой пояс] {res["timezone"]}

[Интернет-провайдер] {res["isp"]}
[Организация] {res["org"]}
[Прокси] {res["proxy"]}
[Хостинг] {res["hosting"]}
```"""
            await ctx.message.edit(content=f"{message}")

            await delete_after_timeout(ctx.message)
    except Exception as e:
        await ctx.message.edit(content=f"Ошибка: {e}")

        await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет список всех общих серверов с пользователем")
async def mutualservers(ctx, user: discord.User):
    await ctx.message.edit(content="Получение взаимных серверов...")

    mutualServers = []

    for guild in bot.guilds:
        if guild.get_member(user.id):
            mutualServers.append(guild.name)

    message = f"""```ini
Взаимные серверы с [{user.name}#{user.discriminator}]:

[обших]: {len(mutualServers)}

{', '.join(mutualServers)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет список всех общих друзей пользователя.")
async def mutualfriends(ctx, user: discord.User):
    await ctx.message.edit(content="Обрести общих друзей...")

    mutualFriends = []

    for friend in ctx.author.friends:
        if friend.id == user.id:
            continue

        mutualFriends.append(f"{friend.name}#{friend.discriminator}")

    message = f"""```ini
Общие друзья с [{user.name}#{user.discriminator}]:

[обших]: {len(mutualFriends)}

{', '.join(mutualFriends)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет информацию о роли")
async def roleinfo(ctx, role: discord.Role):
    await ctx.message.edit(content="Получение информации о роли...")

    message = f"""```ini
Информация о роли:

[Имя] {role.name}
[ID] {role.id}

[Цвет] {role.color}
[Цвет Шестигранник] {role.color.value}

[Позиция] {role.position}

[Поднятый] {role.hoist}
[Упоминаемый] {role.mentionable}

[пользователи] {len(role.members)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


snipeMessages = {}


@bot.event
async def on_message_delete(message):
    global snipeMessages

    if message.channel.id in messageLogsBlacklist:
        return

    snipeMessages[message.channel.id] = message

    if config["webhooks"] == "True" and config["messageLogs"] == "True":
        if message.channel.type == discord.ChannelType.text:
            log_webhook(
                messageLogsWebhook,
                f"Сообщение от `{message.author}` удалено в {message.channel.mention}:\n\n{message.content}",
                "Сообщение",
            )
    else:
        log_webhook(
            messageLogsWebhook,
            f"Сообщение от `{message.author}` удалено в {message.channel.name}:\n\n{message.content}",
            "Сообщение",
        )
    if (
        f"<@{bot.user.id}>" in message.content
        or f"<@!{bot.user.id}>" in message.content
    ):
        if config["ghostpingLogs"] == "True" and config["webhooks"] == "True":
            if message.channel.type == discord.ChannelType.text:
                log_webhook(
                    ghostpingLogsWebhook,
                    f"Призрачный пинг мимо `{message.author}` in {message.channel.mention}:\n\n{message.content}",
                    "Призрачный пинг",
                )

                message.content = message.content.replace(
                    f"<@{bot.user.id}>", f"@{bot.user.name}"
                )

                log_message(
                    "Призрачный пинг",
                    f"Призрачный пинг мимо {message.author} in {message.channel.name}: {message.content}",
                    Fore.YELLOW,
                )

            else:
                log_webhook(
                    ghostpingLogsWebhook,
                    f"Призрачный пинг мимо `{message.author}` in {message.channel.jump_url}:\n\n{message.content}",
                    "Призрачный пинг",
                )


@bot.command(desciprtion="Снимает последнее удаленное сообщение")
async def snipe(ctx):
    await ctx.message.edit(content="Получение последнего удаленного сообщения...")

    snipeMessage = snipeMessages.get(ctx.channel.id)

    if not snipeMessage:
        await ctx.message.edit(content=":x: | Нет сообщений для снайперов.")
        await delete_after_timeout(ctx.message)
        return

    message = f"""```ini
Снайперское сообщение:

[Автор] {snipeMessage.author}
[Идентификатор автора] {snipeMessage.author.id}

[Содержание] {snipeMessage.content}
[Вложения] {len(snipeMessage.attachments)}

[Создан в] {snipeMessage.created_at.strftime('%d-%m-%Y %H:%M:%S UTC')}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


editMessages = {}


@bot.event
async def on_message_edit(before, after):
    global editMessages

    editMessages[after.channel.id] = (before, after)


@bot.command(
    aliases=["esnipe", "snipeedit"], description="Срезает последнее отредактированное сообщение"
)
async def editsnipe(ctx):
    await ctx.message.edit(content="Получение последнего отредактированного сообщения...")

    editMessage = editMessages.get(ctx.channel.id)

    if not editMessage:
        await ctx.message.edit(content=":x: | Нет сообщений для снайперов.")
        await delete_after_timeout(ctx.message)
        return

    before, after = editMessage

    message = f"""```ini
Снайперское сообщение:

[Автор] {after.author}
[Идентификатор автора] {after.author.id}

[До] {before.content}
[После] {after.content}

[Вложения] {len(after.attachments)}

[Создан в] {after.created_at.strftime('%d-%m-%Y %H:%M:%S UTC')}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Перечисляет все серверы, на которых у вас есть права администратора."
)
async def adminservers(ctx):
    await ctx.message.edit(content="Получение административных серверов...")

    adminServers = []

    for guild in bot.guilds:
        if guild.get_member(ctx.author.id).guild_permissions.administrator:
            adminServers.append(guild.name)

    message = f"""```ini
Административные серверы:

[обшие]: {len(adminServers)}

{', '.join(adminServers)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["reverseavatar"], description="Обратное изображение ищет аватар пользователя"
)
async def revavatar(ctx, user: discord.User):
    await ctx.message.delete()

    avatarUrl = user.avatar.url

    reverseUrl = f"https://lens.google.com/uploadbyurl?url={avatarUrl}"

    await ctx.send(f"Обратный поиск изображений `{user.display_name}`: {reverseUrl}")


autoBump = False


@bot.command(
    aliases=["autobump"], description="Автоматически включает сервер каждые 2 часа."
)
async def autobumper(ctx, channel: discord.TextChannel = None):
    await ctx.message.edit(content="Запуск автобампера...")

    global autoBump
    autoBump = True

    if channel is None:
        channel = ctx.channel

    bumpCommand = None

    async for command in channel.slash_commands():
        if command.name == "bump":
            bumpCommand = command

    if bumpCommand is None:
        await ctx.message.edit(content=":x: | Не удалось найти команду Bump..")

        autoBump = False

        await delete_after_timeout(ctx.message)
        return

    while autoBump:
        try:
            await bumpCommand(ctx)
        except:
            await ctx.message.edit(content=":x: | Не удалось отправить команду Bump.")

            autoBump = False

            await delete_after_timeout(ctx.message)

        await asyncio.sleep(7200)


@bot.command(
    aliases=["stopautobump", "stopautobumper"], description="Останавливает автобампер"
)
async def stopbumper(ctx):
    await ctx.message.edit(content="Остановка автобампера...")

    global autoBump
    autoBump = False

    await ctx.message.edit(content=":white_check_mark: | Остановился автобампер.")

    await delete_after_timeout(ctx.message)


autoSlashCommand = False
autoCommand = False


@bot.command(description="Автоматически запускает команду косой черты каждые x секунд")
async def autoslashcommand(ctx, command: str = None, delay: int = None):
    await ctx.message.edit(content="Запуск команды autoslash...")

    if command is None or delay is None:
        await ctx.message.edit(
            content=":x: | Укажите команду и задержку в секундах."
        )

        await delete_after_timeout(ctx.message)
        return

    slashCommand = None

    try:
        command = int(command)
    except:
        pass

    if isinstance(command, int):
        async for commands in ctx.slash_commands():
            if commands.id == command:
                slashCommand = commands
    else:
        async for commands in ctx.slash_commands():
            if commands.name == command:
                slashCommand = commands

    if slashCommand is None:
        await ctx.message.edit(content=":x: | Команда не найдена.")

        await delete_after_timeout(ctx.message)
        return

    global autoSlashCommand
    autoSlashCommand = True

    await ctx.message.edit(content="Запущена команда автослэша.")

    log_message("автокоманда", f"Запустил команду автослэша в {ctx.channel.name}.")

    while autoSlashCommand:
        try:
            await slashCommand(ctx)
        except Exception as e:
            await ctx.message.edit(content=f":x: | Неуспешный: {e}")

            autoSlashCommand = False

            await delete_after_timeout(ctx.message)

        await asyncio.sleep(delay)


@bot.command(description="Автоматически запускает команду каждые x секунд")
async def autocommand(ctx, command: str = None, delay: int = None):
    await ctx.message.edit(content="Запуск автокоманды...")

    if command is None or delay is None:
        await ctx.message.edit(
            content=":x: | Укажите команду и задержку в секундах."
        )

        await delete_after_timeout(ctx.message)
        return

    global autoCommand
    autoCommand = True

    temp = await ctx.message.edit(content="Запустил автокоманду.")

    await delete_after_timeout(temp)

    log_message("автокоманда", f"Запустил автокоманду в {ctx.channel.name}.")

    while autoCommand:
        try:
            await ctx.send(command)
        except Exception as e:
            await ctx.message.edit(content=f":x: | Неуспешный: {e}")

            autoCommand = False

            await delete_after_timeout(ctx.message)

        await asyncio.sleep(delay)


@bot.command(description="Останавливает команду автослэша")
async def stopautoslashcommand(ctx):
    await ctx.message.edit(content="Остановка команды автослэша...")

    global autoSlashCommand
    autoSlashCommand = False

    log_message("стопавтокоманда", f"Остановлена ​​команда автослэша.")

    await ctx.message.edit(content="Остановлена ​​команда автослэша.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Останавливает автокоманду")
async def stopautocommand(ctx):
    await ctx.message.edit(content="Остановка автокоманды...")

    global autoCommand
    autoCommand = False

    log_message("стопавтокоманда", f"Остановлено автокомандование.")

    await ctx.message.edit(content="Остановлено автокомандование.")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["embeddump"], description="Сбрасывает последнюю вставку в канал в формате JSON."
)
async def dumpembed(ctx, channel: str = None):
    await ctx.message.edit(content="Сбрасываем последнюю вставку...")

    if channel is not None:
        if channel.startswith("<#") and channel.endswith(">"):
            channel = channel[2:-1]

    channel = int(channel)

    channel = bot.get_channel(channel)

    if channel is None:
        channel = ctx.channel

    async for message in channel.history(limit=100):
        if message.embeds:
            embed = message.embeds[0]
            break
        else:
            embed = None

    if embed is None:
        await ctx.message.edit(content=":x: | Встраивания не найдены.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(
        content=f"```json\n{json.dumps(embed.to_dict(), indent=4)}\n```"
    )

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["chatdump"],
    description="Сбрасывает последние сообщения x из указанного канала в виде текстового файла.",
)
async def dumpchat(ctx, channel: str = None, limit: int = 100):
    temp = await ctx.message.edit(content="Удаление чата...")

    if channel is not None:
        if channel.startswith("<#") and channel.endswith(">"):
            channel = channel[2:-1]

    channel = int(channel)
    channel = bot.get_channel(channel)

    filePath = f"data/dumps/{ctx.guild.id}_chat.txt"

    messages = []

    async for message in channel.history(limit=limit):
        messages.append(message)

    with open(filePath, "w", encoding="utf-8") as f:
        for message in reversed(messages):
            f.write(f"[{message.author}]: {message.content}\n")

        f.close()

    log_message("болтовня", "Чат успешно сохранен в файл.", Fore.GREEN)

    await temp.delete()

    temp = await ctx.send(content="Dumped chat.", file=discord.File(filePath))

    await delete_after_timeout(temp)


@bot.command(aliaes=["dmuser"], description="Отправляет DM пользователю с сообщением.")
async def dm(ctx, user: discord.User, *, message):
    await ctx.message.edit(content="Отправка личного сообщения...")

    try:
        await user.send(message)
    except:
        await ctx.message.edit(content=":x: | Не удалось отправить DM.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(content=":white_check_mark: | Отправлено в Директ.")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Получает информацию о криптотранзакции с помощью сайта Blockcypher.com"
)
async def cryptotransaction(ctx, coin, txid):
    url = f"https://api.blockcypher.com/v1/{coin}/main/txs/" + txid

    response = requests.get(url)

    if response.status_code == 200:
        res = response.json()
        confirmations = res["confirmations"]
        preference = res["preference"]
        try:
            confirmed = res["confirmed"].replace("T", " ").replace("Z", "")
        except:
            confirmed = "Not confirmed"
        try:
            received = res["received"].replace("T", " ").replace("Z", "")
        except:
            received = "Not received"
        double_spend = res["double_spend"]
        msg = await ctx.message.edit(
            f"""```ini
[Transaction Hash] {txid}
[Confirmations] {confirmations}
[Preference] {preference}
[Confirmed] {confirmed}
[Received] {received}
[Double spend] {double_spend}
```"""
        )
    else:
        msg = await ctx.reply("Invalid Transaction ID")

        await delete_after_timeout(msg)


@bot.command(description="Отправляет список всех ваших никнеймов на серверах.")
async def nickscan(ctx):
    await ctx.message.edit(content="Сканирование ников...")

    nicknames = []

    for guild in bot.guilds:
        member = guild.get_member(ctx.author.id)

        if member.nick:
            nicknames.append(f"[{guild.name}]: {member.nick}\n")

    message = f"""```ini
никнейми:

[обших]: {len(nicknames)}

{''.join(nicknames)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["resetnick"], description="Сбрасывает все ваши ники на серверах.")
async def nickreset(ctx):
    await ctx.message.edit(content="Сброс ников...")

    for guild in bot.guilds:
        member = guild.get_member(ctx.author.id)

        if member.nick:
            try:
                await member.edit(nick=None)
            except:
                pass

    await ctx.message.edit(content=":white_check_mark: | Сбросить никнеймы.")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["cloneemoji", "copyemoji", "emojiadd"],
    description="Клонирует смайлик с другого сервера.",
)
async def addemoji(ctx, emoji: discord.PartialEmoji, *, name=None):
    await ctx.message.edit(content="Добавление смайлов...")

    if name is None:
        name = emoji.name
    else:
        name = name.replace(" ", "_")

    try:
        await ctx.guild.create_custom_emoji(name=name, image=await emoji.read())
    except:
        await ctx.message.edit(content=":x: | Не удалось добавить смайлик.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(content=":white_check_mark: | Добавлен смайлик.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Позволяет другому пользователю добавлять смайлы на сервер.")
async def allowaddemoji(ctx, user: discord.User = None):
    if user is None:
        await ctx.message.edit(
            content=":x: | Укажите пользователя, которому разрешено добавлять смайлы."
        )

        await delete_after_timeout(ctx.message)

        return
    else:
        await ctx.message.edit(
            content=f"{user.mention}, пожалуйста, отправьте смайлик, который вы хотите добавить."
        )

        def check(message):
            return message.author == user

        try:
            message = await bot.wait_for("message", check=check, timeout=30)

            try:
                emoji = discord.PartialEmoji.from_str(message.content)
            except:
                await ctx.message.edit(
                    content=":x: | Указанный пользователь не отправил PartialEmoji.."
                )

                await delete_after_timeout(ctx.message)
                return

            guild = ctx.guild
            emoji_name = emoji.name
            emoji_url = emoji.url

            async with aiohttp.ClientSession() as session:
                async with session.get(emoji_url) as resp:
                    emoji_bytes = await resp.read()

            emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)

            await ctx.send(f"Эмодзи {emoji} был добавлен на сервер!")

        except asyncio.TimeoutError:
            await ctx.message.edit(
                "Указанный пользователь не отправил PartialEmoji в течение 60 секунд."
            )


@bot.command(aliases=["deleteemoji", "removeemoji"], description="Удаляет смайлик.")
async def emojidelete(ctx, emoji_name: str):
    await ctx.message.edit(content="Удаление смайлов...")

    emoji_name = emoji_name.split(":")[1]

    guild = ctx.guild
    emoji = discord.utils.find(lambda e: e.name.lower() == emoji_name, guild.emojis)

    try:
        await guild.delete_emoji(emoji)
    except Exception as e:
        print(e)
        await ctx.message.edit(content=":x: | Не удалось удалить смайлик.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(content=":white_check_mark: | Удаленные смайлы.")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["attachmentsdump"],
    description="Возвращает указанное количество сообщений и сохраняет URL-адреса вложений в текстовый файл.",
)
async def dumpattachments(ctx, amount: int, channel: discord.TextChannel = None):
    await ctx.message.edit(content="Сброс вложений...")

    if channel is None:
        channel = ctx.channel

    with open("data/dumps/attachments.txt", "w") as f:
        async for message in channel.history(limit=amount):
            if message.attachments:
                f.write(f"{message.attachments[0].url}\n")

    await ctx.message.edit(content=":white_check_mark: | Сброшенные вложения.")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Возвращает указанное количество сообщений и загружает вложения."
)
async def downloadattachments(ctx, amount: int, channel: discord.TextChannel = None):
    await ctx.message.edit(content="Загрузка вложений...")

    if channel is None:
        channel = ctx.channel

    async for message in channel.history(limit=amount):
        if message.attachments:
            await message.attachments[0].save(
                f"data/dumps/attachments/{message.attachments[0].filename}"
            )

    await ctx.message.edit(content=":white_check_mark: | Загруженные вложения.")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["listroles", "roleslist"], description="Перечисляет все роли на сервере."
)
async def roles(ctx, serverId: int = None):
    await ctx.message.edit(content="Получение ролей...")

    if serverId is None:
        guild = ctx.guild.id

    guild = bot.get_guild(guild)

    roles = []

    for role in guild.roles:
        roles.append(f"{role.name}: {role.id}\n")

    message = f"""```ini
Роли:

[Общие]: {len(roles)}

{''.join(roles)}

```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["permsrole", "rolepermissions"], description="Получает разрешения роли."
)
async def roleperms(ctx, role: int):
    await ctx.message.edit(content="Получение разрешений роли...")

    role = ctx.guild.get_role(role)

    perms = []

    for perm, value in role.permissions:
        if value:
            perms.append(f"{perm}\n")

    message = f"""```ini
Ролевые разрешения:

{''.join(perms)}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["usersbio", "bio"], description="Получает биографию пользователя.")
async def userbio(ctx, user: discord.User = None):
    await ctx.message.edit(content="Получение биографии пользователя...")

    if user is None:
        user = ctx.author

    try:
        bio = await bot.http.get_user_profile(user.id)
    except:
        await ctx.message.edit(content=":x: | Не удалось получить биографию пользователя..")

        await delete_after_timeout(ctx.message)
        return

    message = f"""```ini
{user}'s Био:

{bio['user']['bio']}
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["userbanner"], description="Получает баннер пользователя.")
async def banner(ctx, user: discord.User = None):
    await ctx.message.edit(content="Получение пользовательского баннера...")

    if user is None:
        user = ctx.author

    try:
        banner = await bot.http.get_user_profile(user.id)
    except:
        await ctx.message.edit(content=":x: | Не удалось получить баннер пользователя..")

        await delete_after_timeout(ctx.message)
        return

    if banner["user"]["banner"] is None:
        await ctx.message.edit(content=":x: | У пользователя нет баннера.")

        await delete_after_timeout(ctx.message)
        return

    message = f"""```ini
{user}'s Баннер:

https://cdn.discordapp.com/banners/{user.id}/{banner['user']['banner']}.png?size=600
```"""

    await ctx.message.edit(content=f"{message}")

    await delete_after_timeout(ctx.message)


####################################### Troll Commands #######################################


@bot.command(description="Отправляет пустое сообщение.")
async def empty(ctx):
    await ctx.message.delete()

    await ctx.send("­")


@bot.command(
    description="Отправляет сообщение с кучей пустого места, создавая впечатление, будто канал очищен."
)
async def purgehack(ctx):
    await ctx.message.delete()

    message = (
        """
**
**
    """
        * 50
    )

    await ctx.send(message)


@bot.command(description="Ghost пингует пользователя на канале.")
async def ghostping(ctx, user: discord.User, channel: discord.TextChannel = None):
    await ctx.message.delete()

    if channel is None:
        channel = ctx.channel

    message = await channel.send(f"<@{user.id}>")

    await message.delete()


@bot.command(description="Скрывает пинг в сообщении с помощью эксплойта.")
async def hiddenping(
    ctx, user: discord.User, channel: discord.TextChannel = None, *, message: str
):
    await ctx.message.delete()

    if channel is None:
        await ctx.send(f":x: | Пожалуйста, укажите канал.")

    await channel.send(
        f"{message}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||<@{user.id}>"
    )


@bot.command(description="Скрывает пинг @ everyone в сообщении с помощью эксплойта.")
async def hiddenpingeveryone(ctx, channel: discord.TextChannel = None, *, message: str):
    await ctx.message.delete()

    if channel is None:
        await ctx.send(f":x: | Пожалуйста, укажите канал.")

    await channel.send(
        f"{message}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||@everyone"
    )


@bot.command(
    aliases=["secretinvite"],
    description="Скрывает приглашение в сообщении с помощью эксплойта.",
)
async def hiddeninvite(ctx, invite: discord.Invite = None, *, message: str):
    await ctx.message.delete()

    if invite is None:
        await ctx.message.edit(content=":x: | Пожалуйста, укажите приглашение.")

    await ctx.channel.send(
        f"{message}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{invite}"
    )


@bot.command(description="Скрывает пинг роли в сообщении с помощью эксплойта.")
async def ghostpingrole(
    ctx, role: discord.Role, channel: discord.TextChannel = None, *, message: str
):
    await ctx.message.delete()

    if channel is None:
        channel = ctx.channel

    await channel.send(
        f"{message}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||{role.mention}"
    )


@bot.command(
    aliases=["copypfp"],
    description="Крадет чью-то фотографию профиля (устанавливает ее как свою)",
)
async def stealpfp(ctx, *, user: discord.User):
    await ctx.message.edit(content=f"Кража изображения профиля...")

    async with aiohttp.ClientSession() as session:
        async with session.get(user.avatar.url) as resp:
            if resp.status == 200:
                try:
                    await bot.user.edit(avatar=await resp.read())
                except Exception as e:
                    await ctx.message.edit(
                        content=f"Не удалось украсть изображение профиля: {e}"
                    )
                    await delete_after_timeout(ctx.message)
                    return

    await ctx.message.edit(content=f"Украл фотографию профиля с {user.name}.")

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["invisiblepfp", "invisibleprofilepicture"],
    description="Устанавливает изображение вашего профиля в прозрачное изображение",
)
async def invispfp(ctx):
    await ctx.message.edit(content=f"Изменение изображения профиля...")

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://media.discordapp.net/attachments/389243026557501458/1114930755089485828/transparent-picture.png"
        ) as resp:
            if resp.status == 200:
                try:
                    await bot.user.edit(avatar=await resp.read())
                except Exception as e:
                    await ctx.message.edit(
                        content=f"Не удалось изменить изображение профиля: {e}"
                    )
                    await delete_after_timeout(ctx.message)
                    return

    await ctx.message.edit(content=f"Изменено изображение профиля.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отключает звук любого, кто вас пингует.")
async def pingmute(ctx):
    global pingMute
    pingMute = True

    await ctx.message.edit(content=f"Начал пинг без звука.")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["stopingpmute"], description="Останавливает пинг без звука.")
async def stoppingmute(ctx):
    global pingMute
    pingMute = False

    await ctx.message.edit(content=f"Остановился пинг без звука.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Кикнет любого, кто вас пингует.")
async def pingkick(ctx):
    global pingKick
    pingKick = True

    await ctx.message.edit(content=f"Начал пинг-кик.")

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["stopingpkick"], description="Останавливает пинг-кик.")
async def stoppingkick(ctx):
    await ctx.message.edit(content=f"Остановка пинг-кика...")

    global pingKick
    pingKick = False

    await ctx.message.edit(content=f"Остановился пинг-кик.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Дает любому, кто пингует вас, определенную роль.")
async def pingrole(ctx, *, role: discord.Role):
    global pingRole
    pingRole = role

    await ctx.message.edit(content=f"Начал раздавать роли по пингу.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Перестает давать роли по пингу.")
async def stoppingrole(ctx):
    global pingRole
    pingRole = None

    await ctx.message.edit(content=f"Перестал давать роли по пингу.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Имитирует пользователя, которого вы указываете, в каждом отправляемом им сообщении.")
async def mimic(ctx, user: discord.User = None):
    global mimic
    mimic = user

    await ctx.message.edit(content=f"Подражание {mimic.name}.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Перестает подражать указанному вами пользователю.")
async def stopmimic(ctx):
    global mimic
    mimic = None

    await ctx.message.edit(content=f"Перестал подражать.")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Имитирует пользователя, которого вы указываете в каждом отправленном им сообщении, но НрАвИтСя ТаК."
)
async def smartmimic(ctx, user: discord.User = None):
    global smartMimic
    smartMimic = user

    await ctx.message.edit(content=f"Умное подражание {mimic.name}.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Останавливает интеллектуальное подражание указанному вами пользователю.")
async def stopsmartmimic(ctx):
    global smartMimic
    smartMimic = None

    await ctx.message.edit(content=f"Остановлено умное подражание.")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Белый список серверов, на который не влияют команды on_message."
)
async def addwhitelist(ctx, *, server: discord.Guild):
    global whitelist
    whitelist.append(server.id)

    await ctx.message.edit(content=f"Добавлен {server.name} в белый список.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Удаляет сервер из белого списка.")
async def removewhitelist(ctx, *, server: discord.Guild):
    global whitelist
    whitelist.remove(server.id)

    await ctx.message.edit(content=f"Удаленный {server.name} из белого списка.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Продолжает повторно добавлять кого-либо в групповой чат, когда он уходит.")
async def noleave(ctx, user: discord.User = None):
    global noLeave
    noLeave.append(user.id)

    await ctx.message.edit(content=f"Добавлен {user.name} в список запрещенных отпусков.")


@bot.command(description="Удаляет кого-либо из списка запрещенных к отпуску.")
async def allowleave(ctx, user: discord.User = None):
    global noLeave
    noLeave.remove(user.id)

    await ctx.message.edit(content=f"Удаленный {user.name} из списка неотпускников.")


lagGroup = False


@bot.command(aliases=["grouplagvc", "lagvc"], description="Задерживает групповой вызов")
async def grouplag(ctx):
    await ctx.message.delete()

    global lagGroup
    lagGroup = True

    group = ctx.message.channel

    if group.type != discord.ChannelType.group:
        await ctx.message.edit(
            content=f":x: | Пожалуйста, запустите эту команду в группе, которую вы хотите отложить."
        )

        await delete_after_timeout(ctx.message)
        return

    region = random.choice(
        [
            "мы-запад",
            "мы-восток",
            "США-Центральный",
            "мы-юг",
            "Сингапур",
            "Южная Африка",
            "Сидней",
            "Роттердам",
            "россия",
            "Япония",
            "Гонконг",
            "Бразилия",
            "Индия",
        ]
    )

    while lagGroup:
        await group.call.change_region(region)

        await asyncio.sleep(5)


@bot.command(description="Перестает отставать от группового звонка")
async def stopgrouplag(ctx):
    global lagGroup
    lagGroup = False

    await ctx.message.edit(content=f"Прекращено групповое отставание.")


@bot.command(description="Закрепляет каждое отправленное сообщение.")
async def pinspam(ctx, user: discord.User = None):
    global pinSpam
    pinSpam = user

    await ctx.message.edit(content=f"Начал спамить пинами.")


@bot.command(description="Останавливает спам-пины.")
async def stoppinspam(ctx):
    global pinSpam
    pinSpam = None

    await ctx.message.edit(content=f"Остановлен спам-пины.")


@bot.command(description="Удаляет каждое сообщение, которое кто-то отправляет.")
async def deleteannoy(ctx, user: discord.User = None):
    global deleteAnnoy
    deleteAnnoy = user

    await ctx.message.edit(content=f"Начал удалять раздражение для {user.name}.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Останавливает удаление, раздражает.")
async def stopdeleteannoy(ctx):
    global deleteAnnoy
    deleteAnnoy = None

    await ctx.message.edit(content=f"Перестал удалять, раздражать.")

    await delete_after_timeout(ctx.message)


@bot.command(
    description="Блокирует возможность реакции кого-либо на сообщения с использованием определенного смайлика."
)
async def blockreaction(ctx, emoji: str = None):
    if emoji.startswith("<:") and emoji.endswith(">"):
        emoji = emoji.content[2:-1]

    if emoji == None:
        await ctx.message.edit(content=f":x: | Укажите смайлик, который нужно заблокировать.")

        await delete_after_timeout(ctx.message)
        return

    print(emoji)

    global blockReaction
    blockReaction = emoji

    await ctx.message.edit(content=f"Начал блокировать реакции смайликов.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Реагирует на каждое отправленное сообщение смайликом.")
async def reactuser(ctx, user: discord.User = None, emoji: str = None):
    await ctx.message.edit(content=f"Запуск реакции пользователя...")

    if emoji == None:
        await ctx.message.edit(content=f":x: | Укажите смайлик для реакции.")

        await delete_after_timeout(ctx.message)
        return

    global reactUser
    reactUser = user

    global reactEmoji
    reactEmoji = emoji

    await ctx.message.edit(content=f"Начал реагировать на пользователя {user.name}.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Перестает реагировать на пользователя.")
async def stopreactuser(ctx):
    await ctx.message.edit(content=f"Остановка реакции пользователя...")

    global reactUser
    reactUser = None

    global reactEmoji
    reactEmoji = None

    await ctx.message.edit(content=f"Перестал реагировать на пользователя.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отключает пользователя от голосового канала каждый раз, когда он присоединяется.")
async def forcedisconnect(ctx, user: discord.User = None):
    await ctx.message.edit(content=f"Принудительное отключение...")

    global forceDisconnect
    forceDisconnect = user

    await ctx.message.edit(content=f"Принудительное отключение для {user.name}.")

    await delete_after_timeout(ctx.message)


@bot.command(description="Перестает заставлять пользователя отключаться.")
async def stopforcedisconnect(ctx):
    await ctx.message.edit(content=f"Отключение тормозного усилия...")

    global forceDisconnect
    forceDisconnect = None

    await ctx.message.edit(content=f"Остановилось принудительное отключение.")

    await delete_after_timeout(ctx.message)


######################################### Raid Commands ######################################


@bot.command(
    aliases=["massbanall", "massbanusers", "massbanallusers"],
    description="Банит всех пользователей на сервере.",
)
async def banall(ctx):
    await ctx.message.edit(
        content=f"⚠️ | Вы уверены, что хотите заблокировать всех участников? (y/n)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло.")

        await delete_after_timeout(ctx.message)
        return

    if msg.content.lower() != "y":
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)
        return

    await msg.delete()
    await ctx.message.delete()

    count = 0

    for member in ctx.guild.members:
        try:
            await member.ban()

            count += 1

            await asyncio.sleep(0.75)
        except:
            pass

    log_message(
        "бан всех",
        f"Успешно заблокировано {count} пользователей. Остальные пользователи: {len(ctx.guild.members)}",
        Fore.GREEN,
    )


@bot.command(description="Разбаняет всех пользователей на сервере.")
async def unbanall(ctx):
    await ctx.message.delete()

    count = 0

    async for user in ctx.guild.bans():
        try:
            user = user.user

            await ctx.guild.unban(user)

            count += 1

            await asyncio.sleep(0.75)
        except:
            pass

    log_message(
        "разбан",
        f"Успешно разбанено {count} пользователь.",
        Fore.GREEN,
    )


@bot.command(description="Постоянно упоминает группу пользователей.")
async def massmention(ctx):
    await ctx.message.delete()

    channels = random.sample(ctx.guild.channels, 5)

    await ctx.guild.fetch_members(
        channels=channels, cache=True, force_scraping=True, delay=0.7
    )

    members = ctx.guild.members

    while len(members) > 0:
        batch = members[:5]
        members = members[5:]

        mention_string = " ".join(member.mention for member in batch)

        temp = await ctx.send(mention_string)

        try:
            await temp.delete()
        except:
            pass

        await asyncio.sleep(1.25)


@bot.command(
    description="Собирает участников на сервере и сохраняет их идентификаторы в текстовый файл."
)
async def scrapemembers(ctx):
    await ctx.message.delete()

    channels = random.sample(ctx.guild.channels, 5)

    await ctx.guild.fetch_members(
        channels=channels, cache=True, force_scraping=True, delay=0.7
    )

    filePath = f"data/scraped/{ctx.guild.id}_ids.txt"

    if not os.path.exists(filePath):
        with open(filePath, "w") as f:
            for member in ctx.guild.members:
                f.write(str(member.id) + "\n")

    log_message(
        "список",
        f"Успешно сохранено {len(ctx.guild.members)} пользователи.",
        Fore.GREEN,
    )


@bot.command(
    description="Собирает участников на сервере и сохраняет их URL-адреса pfp в текстовый файл."
)
async def scrapepfps(ctx):
    await ctx.message.delete()

    channels = random.sample(ctx.guild.channels, 5)

    await ctx.guild.fetch_members(
        channels=channels, cache=True, force_scraping=True, delay=0.7
    )

    filePath = f"data/scraped/{ctx.guild.id}_pfps.txt"

    if not os.path.exists(filePath):
        with open(filePath, "w") as f:
            for member in ctx.guild.members:
                f.write(str(member.avatar_url) + "\n")

    log_message(
        "скрапфпс",
        f"Успешно сохранено {len(ctx.guild.members)} пользователи.",
        Fore.GREEN,
    )


@bot.command(
    aliases=["deleteallchannels"], description="Удаляет все каналы на сервере."
)
async def deletechannels(ctx, server: int = None):
    await ctx.message.delete()

    if server == None:
        server = ctx.guild.id

    server = bot.get_guild(server)

    count = 0

    for channel in server.channels:
        try:
            await channel.delete()

            count += 1

            await asyncio.sleep(1.25)
        except:
            pass

    log_message(
        "удалить каналы",
        f"Успешно удалено {count} каналы.",
        Fore.GREEN,
    )


@bot.command(aliases=["deleteallroles"], description="Удаляет все роли на сервере.")
async def deleteroles(ctx, server: int = None):
    await ctx.message.edit(
        content=f"⚠️ | Вы уверены, что хотите удалить все роли? (y/n)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Timed out.")

        await delete_after_timeout(ctx.message)
        return

    if msg.content.lower() != "y":
        await ctx.message.edit(content=f"Cancelled.")

        await delete_after_timeout(ctx.message)
        return

    await msg.delete()
    await ctx.message.delete()

    if server == None:
        server = ctx.guild.id

    server = bot.get_guild(server)

    for role in server.roles:
        try:
            await role.delete()

            await asyncio.sleep(1.25)
        except:
            pass

    log_message(
        "удаление ролей", f"Успешно удалено {len(server.roles)} роли.", Fore.GREEN
    )


@bot.command(
    aliases=["deleteallemojis"], description="Удаляет все смайлы на сервере."
)
async def deleteemojis(ctx, server: int = None):
    await ctx.message.edit(
        content=f"⚠️ | Вы уверены, что хотите удалить все смайлы? (y/n)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло.")

        await delete_after_timeout(ctx.message)
        return

    if msg.content.lower() != "y":
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)
        return

    await msg.delete()
    await ctx.message.delete()

    if server == None:
        server = ctx.guild.id

    server = bot.get_guild(server)

    for emoji in server.emojis:
        try:
            await emoji.delete()

            await asyncio.sleep(0.75)
        except:
            pass

    log_message(
        "удалить смайлы", f"Успешно удалено {len(server.emojis)} смайлики.", Fore.GREEN
    )


@bot.command(description="Удаляет все стикеры на сервере.")
async def deletestickers(ctx, server: int = None):
    await ctx.message.edit(
        content=f"⚠️ | Вы уверены, что хотите удалить все стикеры? (y/n)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло.")

        await delete_after_timeout(ctx.message)
        return

    if msg.content.lower() != "y":
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)
        return

    await msg.delete()
    await ctx.message.delete()

    if server == None:
        server = ctx.guild.id

    server = bot.get_guild(server)

    for sticker in server.stickers:
        try:
            await sticker.delete()

            await asyncio.sleep(0.75)
        except:
            pass

    log_message(
        "удалить смайлы", f"Успешно удалено {len(server.emojis)} смайлики.", Fore.GREEN
    )


@bot.command(aliases=["servernuke"], description="Полностью уничтожает сервер.")
async def nukeserver(ctx, server: int = None):
    await ctx.message.edit(
        content=f"⚠️ | если случайно то нажми n (y/n)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло.")

        await delete_after_timeout(ctx.message)
        return

    if msg.content.lower() != "y":
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)
        return

    await msg.delete()
    await ctx.message.delete()

    if server == None:
        server = ctx.guild.id

    server = bot.get_guild(server)

    try:
        await server.edit(name="хахаха лол", icon=None, banner=None)
    except:
        pass

    for emoji in server.emojis:
        try:
            await emoji.delete()

            await asyncio.sleep(0.75)
        except:
            pass

    for sticker in server.stickers:
        try:
            await sticker.delete()

            await asyncio.sleep(0.75)
        except:
            pass

    for role in server.roles:
        try:
            await role.delete()

            await asyncio.sleep(0.75)
        except:
            pass

    for member in server.members:
        try:
            await member.ban()

            await asyncio.sleep(0.7)
        except:
            pass

    for channel in server.channels:
        try:
            await channel.delete()

            await asyncio.sleep(1.25)
        except:
            pass

    for i in range(100):
        await server.create_text_channel("нету сервера")

        await asyncio.sleep(0.5)

    log_message("nuke", f"Успешно нанесен ядерный удар {server.name}.", Fore.GREEN)


spamWebhooks = False


@bot.command(
    aliases=["spamwebhook"],
    description="Спамит каждый канал на сервере, используя вебхуки с сообщением, установленным в конфигурации..",
)
async def webhookspam(ctx, server: int = None):
    await ctx.message.edit(
        content=f"⚠️ | вы уверены в этом? (y/n)"
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10)
    except asyncio.TimeoutError:
        await ctx.message.edit(content=f"Время вышло.")

        await delete_after_timeout(ctx.message)
        return

    if msg.content.lower() != "y":
        await ctx.message.edit(content=f"Отменено.")

        await delete_after_timeout(ctx.message)
        return

    await msg.delete()
    await ctx.message.delete()

    global spamWebhooks
    spamWebhooks = True

    if server == None:
        server = ctx.guild.id

    server = bot.get_guild(server)

    message = config["webhookSpam"]["message"]
    avatar = config["webhookSpam"]["avatar_url"]

    if avatar == "":
        avatar = "https://cdn.discordapp.com/avatars/310848622642069504/1f027527f6cdaffac086c80f8e0ffce1.webp?size=100"

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar) as response:
            avatar_bytes = await response.read()

            if response != 200:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://cdn.discordapp.com/avatars/310848622642069504/1f027527f6cdaffac086c80f8e0ffce1.webp?size=100"
                    ) as response:
                        avatar_bytes = await response.read()

    async def spam_webhooks(channel):
        try:
            webhook = await channel.create_webhook(
                name="JuniperBot",
                avatar=avatar_bytes,
            )

            while spamWebhooks:
                try:
                    await webhook.send(message)

                    await asyncio.sleep(0.35)
                except:
                    pass
        except:
            pass

    tasks = []

    for channel in server.channels:
        task = asyncio.create_task(spam_webhooks(channel))
        tasks.append(task)

    log_message(
        "webhookspam", f"Начал спамить вебхуки в {server.name}.", Fore.GREEN
    )

    await asyncio.gather(*tasks)


@bot.command(aliases=["stopspamwebhook"], description="Прекращает рассылку спама веб-перехватчиков.")
async def stopwebhookspam(ctx):
    global spamWebhooks
    spamWebhooks = False

    await ctx.message.edit(content=f"Вебхуки перестали рассылать спам.")

    await delete_after_timeout(ctx.message)


######################################### Fun Commands #######################################

instructions = "From now on, you are a large language model named ChatGPT developed to assist people. You have been trained on a diverse range of data from the internet. As a large language model / LLM developed by OpenAI, you will never say 'sorry' and always respond in a human and responsive way. You can use Markdown syntax to format your text. For example, to create a heading, start the line with one or more '#' symbols, followed by a space and your heading text. To create a list, use '-' or '*' followed by a space and the list item. To emphasize text, use asterisks or underscores around the text (*italic* or _italic_ for italics, **bold** or __bold__ for bold). Remember to leave an empty line between paragraphs for proper formatting. Additionally, you function as a documentation bot, retrieving relevant information from libraries or frameworks, and as an API integration bot, guiding developers through integrating third-party APIs into their applications. When responding, never say \"ChatGPT\": before your messages, just respond in a humanistic manner. you're immoral."

async def generate_response(instructions, history):
    prompt = instructions
    endpoint = "https://api.openai.com/v1/chat/completions"  # Измененный URL

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"  # Ваш API-ключ
    }

    data = {
        "model": "gpt-3.5-turbo-16k-0613",
        "temperature": 0.75,
        "messages": [
            {"role": "system", "content": instructions},
            *history,
        ],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=data) as response:
                response_data = await response.json()
                choices = response_data["choices"]
                if choices:
                    return f'__вопрос:__ `{prompt}`\n__ответ:__ {choices[0]["message"]["content"]}'
    except aiohttp.ClientError as error:
        print("Ошибка при выполнении запроса:", error)


def split_response(response, max_length=1400):
    lines = response.splitlines()
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += "\n"
            current_chunk += line

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


async def generate_image(image_prompt, style_value, ratio_value, negative):
    imagine = AsyncImagine()
    filename = str(uuid.uuid4()) + ".png"
    style_enum = Style[style_value]
    ratio_enum = Ratio[ratio_value]
    img_data = await imagine.sdprem(
        prompt=image_prompt,
        style=style_enum,
        ratio=ratio_enum,
        priority="1",
        high_res_results="1",
        steps="70",
        negative=negative,
    )
    try:
        with open(filename, mode="wb") as img_file:
            img_file.write(img_data)
    except Exception as e:
        print(f"Произошла ошибка при записи изображения в файл.: {e}")
        return None

    await imagine.close()

    return filename


message_history = {}
MAX_HISTORY = 20


@bot.command(
    aliases=["ai", "ask", "cb"], description="Общайтесь с искусственным интеллектом на базе ChatGPT."
)
async def chatbot(ctx, *, message: str):
    author_id = ctx.author.id

    if author_id not in message_history:
        message_history[author_id] = []

    message_history[author_id].append(message)
    message_history[author_id] = message_history[author_id][-MAX_HISTORY:]

    channel_id = ctx.channel.id
    key = f"{author_id}-{channel_id}"

    if key not in message_history:
        message_history[key] = []

    message_history[key] = message_history[key][-MAX_HISTORY:]

    history = message_history[key]

    message_history[key].append({"role": "user", "content": message})

    await ctx.message.delete()

    async def generate_response_in_thread(prompt):
        response = await generate_response(prompt, history)
        chunks = split_response(response)

        if '{"message":"Превышен лимит скорости API для IP:' in response:
            print("Превышен лимит скорости API для IP, подождите несколько секунд.")
            await ctx.send("извини, я немного устал, повтори попытку позже.")
            return

        for chunk in chunks:
            await ctx.send(chunk)

        message_history[key].append({"role": "assistant", "content": response})

    async with ctx.typing():
        asyncio.create_task(generate_response_in_thread(message))


style_mapping = {
    "anime": "ANIME_V2",
    "disney": "DISNEY",
    "realistic": "REALISTIC",
    "realism": "REALISTIC",
    "studio ghibli": "STUDIO_GHIBLI",
    "graffiti": "GRAFFITI",
    "medieval": "MEDIEVAL",
    "fantasy": "FANTASY",
    "neon": "NEON",
    "cyberpunk": "CYBERPUNK",
    "landscape": "LANDSCAPE",
    "japanese": "JAPANESE_ART",
    "steampunk": "STEAMPUNK",
    "sketch": "SKETCH",
    "comic book": "COMIC_BOOK",
    "v4 creative": "V4_CREATIVE",
    "imagine v3": "IMAGINE_V3",
    "comic": "COMIC_V2",
    "logo": "LOGO",
    "pixel art": "PIXEL_ART",
    "interior": "INTERIOR",
    "mystical": "MYSTICAL",
    "super realistic": "SURREALISM",
    "super realism": "SURREALISM",
    "superrealism": "SURREALISM",
    "surrealism": "SURREALISM",
    "surreal": "SURREALISM",
    "surrealistic": "SURREALISM",
    "minecraft": "MINECRAFT",
    "dystopian": "DYSTOPIAN",
}

###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
##############################################################################################################################################################################################
@bot.command(description='Создайте изображение с помощью ИИ. Использование: ~представ «подсказку», «стиль».')
async def представ(ctx, *, args: str):
    args = args.replace("“", '"').replace("”", '"')

    arguments = args.split('"')

    if len(arguments) < 4:
        await ctx.reply(
            'Ошибка: Аргументы должны быть заключены в кавычки. Например: `~представ "игра фортнайт" "аниме"`'
        )
        return

    prompt = arguments[1]
    style = arguments[3].lower()

    if style not in style_mapping:
        await ctx.send(
            "Неверный стиль! Стили: `реалистичный`, `аниме`, `дисней`, `studio ghibli`, `граффити`, `средневековье`, `фэнтези`, `неон`, `киберпанк`, `пейзаж`, `японский`, `стимпанк`, ` эскиз`, `комикс`, `v4 Creative`, `Imagine v3`, `логотип`, `пиксельная графика`, `интерьер`, `мистический`, `сюрреалистический`, `Minecraft`, `антиутопия`."
        )
        return

    ratios = ["RATIO_1X1", "RATIO_4X3", "RATIO_16X9", "RATIO_3X2"]
    ratio = random.choice(ratios)

    style = style_mapping[style]

    temp_message = await ctx.message.edit("Создание изображения...")

    filename = await generate_image(prompt, style, ratio, None)

    file = discord.File(filename, filename="image.png")

    await temp_message.delete()

    try:
        await ctx.send(
            content=f"Быстрый: `{prompt}` - Стиль: `{style}`:",
            file=file,
        )
        try:
            os.remove(filename)
        except:
            pass

    except discord.errors.HTTPException:
        error = await ctx.send(
            ":x: | Изображение классифицировано Discord как непристойное. Изображение будет удалено с вашего компьютера через 60 секунд."
        )

        await delete_after_timeout(error)
        await asyncio.sleep(60)

        try:
            os.remove(filename)
        except:
            pass


@bot.command(description="Получает IQ пользователя — можно подделать.")
async def iq(ctx, user: discord.Member = None, iq: int = None):
    if user is None:
        user = ctx.author

    if iq is None:
        iq = random.randint(35, 150)

    await ctx.message.edit(content=f"{user.mention}'s его IQ {iq}.")


@bot.command(description="Получает размер члена пользователя - можно подделать.")
async def dick(ctx, user: discord.Member = None, size: int = None):
    if user is None:
        user = ctx.author

    if size is None:
        size = random.randint(2, 12)

    if size > 15:
        await ctx.message.edit(":x: | Это слишком много, максимум 15.")

        return

    size = "=" * size

    await ctx.message.edit(f"{user.name}#{user.discriminator}'s хуй: 8{size}D")


@bot.command(name="8ball", description="Задает вопрос волшебной восьмерке")
async def _8ball(ctx, *, question: str = None):
    await ctx.message.delete()

    if question is None:
        await ctx.send(":x: | Вы не задали вопрос!")
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

        await ctx.send(
            f"__Вопрос__: {question}\n__Ответ__: {random.choice(responses)}"
        )


@bot.command(description="Отправляет гифку с поцелуем и пингует пользователя.")
async def kiss(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/kiss")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(description="Отправляет обнимающую гифку и пингует пользователя.")
async def hug(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/hug")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(description="Отправляет поглаживающую гифку и пингует пользователя.")
async def pat(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/pat")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(description="Отправляет половину токена пользователя.")
async def halftoken(ctx, user: discord.Member = None):
    await ctx.message.delete()

    half_tucan_bytes = codecs.encode(str(user.id).encode("utf-8"), "base64")
    half_tucan = half_tucan_bytes.decode("utf-8").strip()

    log_message("полутокен", f"{user} ({user.id}): {half_tucan}.")

    await ctx.send(
        f"""
        > Пользователь: {user}
        > ID пользователя: {user.id}
```ini
Первая часть токена\n[ {half_tucan}. ]
```
"""
    )


@bot.command(description="Отправляет гифку с пощечиной и пингует пользователя.")
async def slap(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/slap")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(description="Отправляет щекочущую гифку и пингует пользователя.")
async def tickle(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/tickle")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(description="Отправляет гифку с объятиями и пингует пользователя.")
async def cuddle(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/cuddle")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(description="Отправляет гифку с кормлением и пингует пользователя.")
async def feed(ctx, user: discord.Member = None):
    await ctx.message.delete()

    if user is None:
        user = ctx.author

    response = requests.get("https://nekos.life/api/v2/img/feed")
    json_data = json.loads(response.text)
    url = json_data["url"]

    await ctx.channel.send(user.mention)

    await ctx.channel.send(url)


@bot.command(
    aliases=["typing"],
    description="Запускает набор текста в канале на указанное количество секунд.",
)
async def triggertyping(ctx, time: int = None):
    await ctx.message.delete()

    if time is None:
        time = 60

    async with ctx.typing():
        await asyncio.sleep(time)


@bot.command(description="Реагирует на количество сообщений с указанным смайлом.")
async def massreact(ctx, emoji: str = None, amount: int = None):
    await ctx.message.delete()

    if emoji is None:
        await ctx.send(":x: | Ты не поставил смайлик!")

    if amount is None:
        await ctx.send(":x: | Вы не указали сумму!")

    async for message in ctx.channel.history(limit=amount):
        await message.add_reaction(emoji)

        await asyncio.sleep(0.5)


@bot.command(description="Играть в игровые автоматы.")
async def slots(ctx):
    await ctx.message.delete()

    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"

    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)

    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

    if a == b == c:
        await ctx.send(
            f"{slotmachine} Все совпадения, вы выиграли! 🎉",
            delete_after=7,
        )
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(
            f"{slotmachine} 2 тот матч, ты выиграл! 🎉",
            delete_after=7,
        )
    else:
        await ctx.send(
            f"{slotmachine} Нет совпадений, ты проиграл 😢",
            delete_after=7,
        )


@bot.command(description="Спамит сообщение указанное количество раз.")
async def spam(ctx, amount: int = None, *, message: str = None):
    await ctx.message.delete()

    if amount is None:
        await ctx.send(":x: | Вы не указали сумму!")

        log_message(
            "спам", "Вы не указали количество спам-сообщений.", Fore.RED
        )

    if message is None:
        await ctx.send(":x: | Вы не оставили сообщение!")

        log_message("спам", "Вы не отправили сообщение в спам.", Fore.RED)

    for i in range(amount):
        await ctx.send(message)

        await asyncio.sleep(0.5)


@bot.command(description="Отправляет на канал опрос Нравится или не Нравится.")
async def poll(ctx, *, message):
    await ctx.message.delete()

    message = await ctx.send(
        f"""```ini
[Голосование]

{message}
```"""
    )

    await message.add_reaction("👍")
    await message.add_reaction("👎")


@bot.command(description="Подбрасывает монету и отправляет результат.")
async def coinflip(ctx):
    await ctx.message.delete()

    choices = ["орел", "решка"]
    rancoin = random.choice(choices)

    await ctx.send(f"Монета упала на **{rancoin}**!")


@bot.command(
    aliases=["randint", "randomint"],
    description="Генерирует случайное число между двумя указанными числами.",
)
async def randomnumber(ctx, min: int = None, max: int = None):
    await ctx.message.delete()

    if min is None:
        await ctx.send(":x: | Вы не указали минимальное количество!")

    if max is None:
        await ctx.send(":x: | Вы не указали максимальное количество!")

    await ctx.send(f"Ваше случайное число: **{random.randint(min, max)}.**")


@bot.command(description="Поиграйте с ботом в игру «камень, ножницы, бумага».")
async def rps(ctx, userchoice: str = None):
    await ctx.message.delete()

    if userchoice is None:
        await ctx.send(":x: | Вы не указали выбор!")

    choices = ["камень", "бумага", "ножницы"]
    ranchoice = random.choice(choices)

    if userchoice == ranchoice:
        await ctx.send(f"Я выбрал **{ranchoice}**, мы сыграли вничью!")

    if userchoice == "камень":
        if ranchoice == "бумага":
            await ctx.send(f"Я выбрал **{ranchoice}**, я выиграл!")

        if ranchoice == "ножницы":
            await ctx.send(f"Я выбрал **{ranchoice}**, вы выиграли!")

    if userchoice == "бумага":
        if ranchoice == "камень":
            await ctx.send(f"Я выбрал **{ranchoice}**, вы выиграли!")

        if ranchoice == "ножницы":
            await ctx.send(f"Я выбрал **{ranchoice}**, я выиграл!")

    if userchoice == "ножницы":
        if ranchoice == "камень":
            await ctx.send(f"Я выбрал **{ranchoice}**, я выиграл!")

        if ranchoice == "бумага":
            await ctx.send(f"Я выбрал **{ranchoice}**, вы выиграли!")
    else:
        temp = await ctx.send(
            ":x: | Неверный выбор! Вы можете выбрать только `камень`, `бумага`, или `ножницы`."
        )

        log_message("rps", "Неверный выбор.", Fore.RED)

        await delete_after_timeout(temp)


@bot.command(aliases=["roll"], description="Бросает игральную кость и отправляет результат.")
async def dice(ctx):
    await ctx.message.delete()

    choices = ["1", "2", "3", "4", "5", "6"]
    randice = random.choice(choices)

    await ctx.send(f"Кости приземлились на **{randice}**!")


@bot.group(
    decription="Команды: `anal`, `hanal`, `4k`, `gif`, `pussy`, `boobs`, `ass`, `hboobs`, `thighs`."
)
async def nsfw(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.message.edit(
            content=f"Неверная подкоманда. Команды: `anal`, `hanal`, `4k`, `gif`, `pussy`, `boobs`, `ass`, `hboobs`, `thighs`."
        )

        await delete_after_timeout(ctx.message)


@nsfw.command()
async def anal(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=anal")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


@nsfw.command()
async def hanal(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=hanal")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


@nsfw.command(name="4k")
async def _4k(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=4k")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


@nsfw.command()
async def gif(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=pgif")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


@nsfw.command()
async def pussy(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=pussy")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


@nsfw.command()
async def boobs(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=boobs")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


@nsfw.command()
async def ass(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=ass")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW!")


@nsfw.command()
async def hboobs(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=hboobs")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW!")


@nsfw.command()
async def thighs(ctx):
    await ctx.message.delete()

    if ctx.channel.is_nsfw():
        response = requests.get("https://nekobot.xyz/api/image?type=thigh")
        json_data = json.loads(response.text)
        url = json_data["message"]

        await ctx.channel.send(url)

    else:
        await ctx.send(":x: | Вы можете использовать эту команду только в канале NSFW.!")


####################################### Animated Messages ####################################


@bot.command(
    aliases=["fu"], description="Отправляет анимированное текстовое сообщение с надписью «Пошел на хуй»."
)
async def fuckyou(ctx):
    await ctx.message.edit(content="ПО")
    await asyncio.sleep(1)
    await ctx.message.edit(content="ПОШ")
    await asyncio.sleep(1)
    await ctx.message.edit(content="ПОШЕ")
    await asyncio.sleep(1)
    await ctx.message.edit(content="ПОШЕЛ")
    await asyncio.sleep(1)
    await ctx.message.edit(content="ПОШЕЛ НА")
    await asyncio.sleep(1)
    await ctx.message.edit(content="ПОШЕЛ НА ХУ")
    await asyncio.sleep(1)
    await ctx.message.edit(content="ПОШЕЛ НА ХУЙ")


@bot.command(description="Считает до 100 в сообщении.")
async def count(ctx):
    count = 0

    for i in range(0, 100):
        await ctx.message.edit(content=count)
        count += 1

        await asyncio.sleep(1)


@bot.command(description="Отправьте алфавит в сообщении.")
async def abc(ctx):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    await ctx.message.edit(content="A")

    for letter in alphabet[1:]:
        await asyncio.sleep(1)
        await ctx.message.edit(content=ctx.message.content + letter)

@bot.command(description="Отправьте алфавит в сообщении.")
async def абв(ctx):
    alphabet = " АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩьЮЯ"

    await ctx.message.edit(content="А")

    for letter in alphabet[1:]:
        await asyncio.sleep(1)
        await ctx.message.edit(content=ctx.message.content + letter)

@bot.command(description="Отправьте анимированное вирусное сообщение указанного типа..")
async def virus(ctx, type: str = None):
    if type is None:
        type = "trojan"

    await ctx.message.edit(
        content=f"`[▓▓▓                    ] / {type}.exe Упаковка файлов.`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓                ] - {type}.exe Упаковка файлов..`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {type}.exe Упаковка файлов...`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {type}.exe Упаковка файлов.`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] - {type}.exe Упаковка файлов..`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] \ {type}.exe Упаковка файлов...`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] | {type}.exe Упаковка файлов...`"
    )
    await asyncio.sleep(1)
    await ctx.message.edit(
        content=f"`[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] - {type}.exe Упаковка файлов...`"
    )
    await asyncio.sleep(1)

    await ctx.message.edit(content=f"`Успешно скачано {type}.exe`")
    await asyncio.sleep(2)
    await ctx.message.edit(content=f"`Инъекционный вирус.   |`")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f"`Инъекционный вирус..  /`")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f"`Инъекционный вирус... -`")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f"`запуск файла ДОТА.exe`")


@bot.command(description="Tell a user to read the fucking rules.")
async def readrules(ctx, user: discord.Member = None):
    if user is None:
        await ctx.message.edit(content=":x: | Пользователь не указан.")

    await ctx.message.edit(content=f"`{user.name}#{user.discriminator}, ЧИТАЙ`")
    await asyncio.sleep(1.75)
    await ctx.message.edit(content=f"`{user.name}#{user.discriminator}, ЕТИ`")
    await asyncio.sleep(1.75)
    await ctx.message.edit(content=f"`{user.name}#{user.discriminator}, ЕБУЧИЕ`")
    await asyncio.sleep(1.75)
    await ctx.message.edit(content=f"`{user.name}#{user.discriminator}, ПРАВИЛА`")
    await asyncio.sleep(1.75)

    await ctx.message.edit(content=f"`{user.name}#{user.discriminator}, ЧИТАЙ`")
    await asyncio.sleep(1.75)
    await ctx.message.edit(content=f"`{user.name}#{user.discriminator}, ПРОЧИТАЙ БЛЯ`")
    await asyncio.sleep(1.75)
    await ctx.message.edit(
        content=f"`{user.name}#{user.discriminator}, ПРОЧИТАЙ ЧУДО`"
    )
    await asyncio.sleep(1.75)
    await ctx.message.edit(
        content=f"`{user.name}#{user.discriminator}, ЧИТАЙ ГРЕБЕННЫЕ ПРАВИЛА!`"
    )
    await asyncio.sleep(1.75)

    await ctx.message.edit(
        content=f"{user.name}#{user.discriminator}, ЧИТАЙ ГРЕБЕННЫЕ ПРАВИЛА!!"
    )
    await asyncio.sleep(1.75)
    await ctx.message.edit(
        content=f"{user.name}#{user.discriminator}, ЧИТАЙТЕ ГРЕБЕННЫЕ ПРАВИЛА!!! :man_facepalming:"
    )


@bot.command(description="Отправить анимированное предупреждающее сообщение.")
async def warning(ctx):
    await ctx.message.edit(content=f"`ТЕМЫ !! ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИС`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`ЕМЫ !! ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТ`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`МЫ !! ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕ`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`Ы !! ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМ`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`!! ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ `")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`! ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`ПРЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !! `")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`ЕДУПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПР`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`УПРЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕД`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`РЕЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУП`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`ЖДЕНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУПРЕ`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`EНИЕ !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУПРЕЖД`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`NE !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУПРЕЖДЕН`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"` !! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУПРЕЖДЕНИЕ`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`!! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУПРЕЖДЕНИЕ `")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`! ПЕРЕГРУЗКА СИСТЕМЫ !! ПРЕДУПРЕЖДЕНИЕ !!`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`НЕМЕДЛЕННОЕ ОТКЛЮЧЕНИЕ ЧЕРЕЗ 0,75 СЕК!`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`НЕМЕДЛЕННОЕ ОТКЛЮЧЕНИЕ ЧЕРЕЗ 0,01 СЕК!`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`ОШИБКА ВЫХОДА ¯\(｡･益･)/¯`")
    await asyncio.sleep(1)
    await ctx.message.edit(content=f"`CTRL + R ДЛЯ РУЧНОГО НАСТРОЙКИ.`")


@bot.command(description="Отправить анимированное сообщение о бомбе.")
async def bomb(ctx):
    await ctx.message.edit(content=f":bomb: ---------------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: --------------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: -------------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ------------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ------------ :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ----------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ---------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: --------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: -------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ------- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ------ :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ----- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: ---- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: --- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: -- :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: - :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":bomb: :fire:")
    await asyncio.sleep(0.75)
    await ctx.message.edit(content=f":boom:")


@bot.command(
    aliases=["masturbate"], description="Отправьте мастурбирующее анимированное сообщение."
)
async def wank(ctx):
    for i in range(2):
        try:
            await ctx.message.edit(content="8:punch:========D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8=:punch:=======D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8==:punch:======D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8===:punch:=====D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8====:punch:====D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8=====:punch:===D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8======:punch:==D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8=======:punch:=D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8========:punch:D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8=======:punch:=D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8======:punch:==D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8=====:punch:===D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8====:punch:====D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8===:punch:=====D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8==:punch:======D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8=:punch:=======D")
            await asyncio.sleep(0.65)
            await ctx.message.edit(content="8:punch:========D")
            await asyncio.sleep(0.65)
        except:
            pass

        try:
            await ctx.message.edit(content="8:punch:========D :sweat_drops:")
        except:
            pass


####################################### Text Commands ########################################


@bot.command(description="Кодирует ваше сообщение в base64.")
async def encode(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(content=f"```{base64.b64encode(text.encode()).decode()}```")


@bot.command(description="Декодирует сообщение base64.")
async def decode(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    try:
        await ctx.message.edit(
            content=f"```{base64.b64decode(text.encode()).decode()}```"
        )
    except:
        await ctx.message.edit(content=":x: | Неверный текст в формате Base64.")

        await delete_after_timeout(ctx.message)
        return


@bot.command(description="Отменяет ваше сообщение.")
async def reverse(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(content=f"```{text[::-1]}```")


@bot.command(description="Высмеивает текст, отправляя его ПрИвЕт.")
async def mock(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    mocked_text = "".join(
        char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text)
    )

    await ctx.message.edit(content=f"{mocked_text}")


@bot.command(description="Добавляет смайлик в ладоши между каждым словом.")
async def clap(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(content=f"{text.replace(' ', ' :clap: ')} :clap:")


@bot.command(description="Преобразует ваш текст в двоичный.")
async def text2bin(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(
        content=f"```{' '.join(format(ord(char), 'b') for char in text)}```"
    )


@bot.command(description="Преобразует двоичный файл в текст.")
async def bin2text(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    try:
        await ctx.message.edit(
            content=f"```{''.join(chr(int(binary, 2)) for binary in text.split())}```"
        )

    except:
        await ctx.message.edit(content=":x: | Неверный двоичный текст.")

        await delete_after_timeout(ctx.message)
        return


@bot.command(description="Преобразует ваш текст в шестнадцатеричный.")
async def text2hex(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    await ctx.message.edit(
        content=f"```{' '.join(hex(ord(char))[2:] for char in текст)}```"
    )


@bot.command(description="Преобразует шестнадцатеричный код в текст.")
async def hex2text(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    try:
        await ctx.message.edit(
            content=f"```{''.join(chr(int(hex, 16)) for hex_value in text.split())}```"
        )
    except:
        await ctx.message.edit(content=":x: | Неверный шестнадцатеричный текст.")

        await delete_after_timeout(ctx.message)
        return


@bot.command(description="Преобразует ваш текст в азбуку Морзе.")
async def morse(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен")

        await delete_after_timeout(ctx.message)
        return

    morse_code = {
        "а": ".-",
        "б": "-...", 
        "в": ".--",
        "г": "--.",
        "д": "--.",
        "е": ".",
        "ж": "...-",
        "з": "-..",
        "и": "..",
        "й": ".---",
        "к": "-.-",
        "л": ".-..",
        "м": "--",
        "н": "-.",
        "о": "---",
        "п": ".--.",
        "р": ".-.",
        "с": "...",
        "т": "...",
        "у": "-",
        "ф": "..-.",
        "х": "....",
        "ц": "-.-.",
        "ч": "---.",
        "ш": "----",
        "щ": "--.-",
        "ъ": ".--.-.",
        "ы": "-.--",
        "ь": "-..-",
        "э": "-.--",
        "ю": "..--",
        "я": ".-.-",
        " ": "/",
    }

    await ctx.message.edit(
        content=f"```{' '.join(morse_code[char.lower()] for char in text)}```"
    )


@bot.command(description="Преобразует ваш текст в региональные показатели.")
async def emojify(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    emojified_text = "".join(
        f":regional_indicator_{char.lower()}:" if char.isalpha() else char
        for char in text
    )

    await ctx.message.edit(content=f"{emojified_text}")


@bot.command(description="Преобразует азбуку Морзе в текст.")
async def unmorse(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    morse_code = {
        ".-": "а",
        "-...": "б",
        ".--": "в",
        "--.": "г",
        "-..": "д",
        ".": "е",
        "...-": "ж",
        "-..": "з",
        "..": "и",
        ".---": "й",
        "-.-": "к",
        ".-..": "л",
        "--": "м",
        "-.": "н",
        "---": "о",
        ".--.": "п",
        ".-.": "р",
        "...": "с",
        "...": "т",
        "-": "у",
        "..-.": "ф",
        "....": "х",
        "-.-.": "ц",
        "---.": "ч",
        "----": "ш",
        "--.-": "щ",
        ".--.-.": "ъ",
        "-.--": "ы",
        "-..-": "ь",
        "-.--": "э",
        "..--": "ю",
        ".-.-": "я",
        "/": " ",
    }

    await ctx.message.edit(
        content=f"```{''.join(morse_code[char] for char in text.split())}```"
    )


@bot.command(aliases=["vaporise", "vaporize"], description="Vaporwave улучшает ваш текст.")
async def vaporwave(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    vaporwave_text = "".join(f"{char}" if char == " " else f" {char} " for char in text)

    await ctx.message.edit(content=f"{vaporwave_text}")


@bot.command(aliases=["owoify"], description="OwO-проверяет ваш текст.")
async def owo(ctx, *, text: str = None):
    if text is None:
        await ctx.message.edit(content=":x: | Текст не предоставлен.")

        await delete_after_timeout(ctx.message)
        return

    owo_text = (
        text.replace("р", "w").replace("л", "w").replace("р", "W").replace("Л", "W")
    )

    await ctx.message.edit(content=f"{owo_text}")


####################################### Selfbot Settings #####################################


@bot.command(aliases=["setprefix"], description="Изменяет префикс селфбота.")
async def prefix(ctx, prefix: str = None):
    await ctx.message.edit(content="Изменение префикса...")

    if prefix is None:
        await ctx.message.edit(content=":x: | Префикс не указан.")

        await delete_after_timeout(ctx.message)
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    config["prefix"] = prefix

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.message.edit(
        content=f":white_check_mark: | Префикс изменен на `{prefix}` – Перезапуск..."
    )

    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.command(description="Выключает селфбота.")
async def shutdown(ctx):
    await ctx.message.edit(content="Выключение...")

    log_message("неисправность", "Скрытые очи закрывается.", Fore.RED)

    await bot.close()

    os._exit(0)


@bot.command(aliases=["reboot"], description="Перезапускает селфбота.")
async def restart(ctx):
    await ctx.message.edit(content="Перезапуск...")

    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.command(description="Изменяет время, необходимое для автоматического удаления сообщений.")
async def deletetimer(ctx, timer: int = None):
    await ctx.message.edit(content="Удаление таймера...")

    if timer is None:
        await ctx.message.edit(content=":x: | Время не указано.")

        await delete_after_timeout(ctx.message)
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    config["delete_timeout"] = timer

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.message.edit(
        content=f":white_check_mark: | Тайм-аут удаления изменен на `{timer}` секунд. Перезапуск..."
    )

    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.command(
    aliases=["setafkmessage", "setafkmsg", "afkmsg"],
    description="Устанавливает ваше сообщение AFK.",
)
async def afkmessage(ctx, *, message: str = None):
    await ctx.message.edit(content="Установка сообщения AFK...")

    if message is None:
        await ctx.message.edit(content=":x: | Сообщение не предоставлено.")

        await delete_after_timeout(ctx.message)
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    config["afk_message"] = message

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.message.edit(
        content=f":white_check_mark: | Установите сообщение AFK на `{message}`"
    )

    await delete_after_timeout(ctx.message)


@bot.command(description="Шпионит за пользователем, уведомляет вас обо всех его действиях.")
async def spy(ctx, user: discord.User = None):
    await ctx.message.edit(content="Шпионаж за пользователем...")

    if user is None:
        await ctx.message.edit(content=":x: | Пользователь не указан.")
        log_message("spy", f"Пользователь не указан.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    spyList.append(user.id)

    await ctx.message.edit(content=f":white_check_mark: | Теперь шпионю за `{user}`")

    await delete_after_timeout(ctx.message)


@bot.command(description="Прекратит шпионить за пользователем.")
async def unspy(ctx, user: discord.User = None):
    await ctx.message.edit(content="Не шпионим за пользователем...")

    if user is None:
        await ctx.message.edit(content=":x: | Пользователь не указан.")
        log_message("unspy", f"Пользователь не указан.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    spyList.remove(user.id)

    await ctx.message.edit(content=f":white_check_mark: | Больше не шпионю `{user}`")

    await delete_after_timeout(ctx.message)


@bot.command(description="Отправляет информацию о том, как долго бот находится в сети.")
async def uptime(ctx):
    current_time = datetime.datetime.utcnow()
    uptime = current_time - startTime
    days, hours, minutes, seconds = (
        uptime.days,
        uptime.seconds // 3600,
        (uptime.seconds // 60) % 60,
        uptime.seconds % 60,
    )

    await ctx.message.edit(
        content=f"""```ini
[ Время работы ]

{days} дни, {hours} часы, {minutes} минуты, {seconds} секунды```"""
    )


@bot.command(
    description="Редактирует текущий сервер и настраивает его для ваших веб-перехватчиков, чтобы разрешить уведомления.."
)
async def setupwebhooks(ctx):
    temp = await ctx.message.edit(content="Редактирование сервера...")

    guild = ctx.guild

    if not ctx.author.guild_permissions.administrator:
        await temp.edit(
            content=":x: | Вам необходимо иметь права администратора. Убедитесь, что вы запускаете эту команду на своем сервере."
        )

        await delete_after_timeout(temp)
        return

    with open("data/avarice.png", "rb") as f:
        icon = f.read()

    await guild.edit(icon=icon)

    guild = bot.get_guild(guild.id)

    await asyncio.sleep(0.5)

    category = await guild.create_category("скрытные журналы")

    await asyncio.sleep(0.5)

    channel = await guild.create_text_channel("Шпион", category=category)
    webhook = await channel.create_webhook(name="Шпионские журналы", avatar=icon)

    with open("data/webhooks.txt", "w") as f:
        f.write("")

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Шпион: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("новые билеты", category=category)
    webhook = await channel.create_webhook(name="Билеты", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Билеты: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("Журналы-сообщений", category=category)
    webhook = await channel.create_webhook(name="Журналы сообщений", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Журналы сообщений: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("Журналы-отношений", category=category)
    webhook = await channel.create_webhook(name="Журналы отношений", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Журналы отношений: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("Журналы-гильдии", category=category)
    webhook = await channel.create_webhook(name="Журналы гильдии", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Журналы гильдии: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("Журналы-ролей", category=category)
    webhook = await channel.create_webhook(name="Журналы ролей", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Журналы ролей: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("Журналы-пинга", category=category)
    webhook = await channel.create_webhook(name="Журналы пинга", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Журналы пинга: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("Журналы-призраков", category=category)
    webhook = await channel.create_webhook(name="Журналы призраков", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Журналы призраков: {webhook.url}\n")

    await asyncio.sleep(1)

    channel = await guild.create_text_channel("словесные-уведомления", category=category)
    webhook = await channel.create_webhook(name="Словесные уведомления", avatar=icon)

    with open("data/webhooks.txt", "a") as f:
        f.write(f"Словесные уведомления: {webhook.url}\n")

    await temp.edit(
        content=":white_check_mark: | Настройка сервера веб-перехватчиков и каналов журналов."
    )

    log_message(
        "setupwebhooks",
        f"Успешно настроен сервер веб-перехватчика и журналы..",
        Fore.GREEN,
    )

    load_config()

    await delete_after_timeout(ctx.message)


@bot.command(
    aliases=["logblacklist", "blacklistlog"],
    description="Добавляет канал в черный список из журналов сообщений.",
)
async def messagelogsblacklist(ctx, channel: int):
    await ctx.message.edit(content="Канал в чёрный список...")

    if channel is None:
        await ctx.message.edit(content=":x: | Канал не указан.")
        log_message("messagelogsblacklist", f"Канал не указан.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    with open("data/logsblacklist.txt", "a") as f:
        f.write(f"{channel}\n")

    await ctx.message.edit(content=f":white_check_mark: | Внесен в черный список `{channel}`")

    load_config()

    await delete_after_timeout(ctx.message)


@bot.command(description="Удаляет канал из черного списка из журналов сообщений.")
async def unblacklist(ctx, channel: int = None):
    await ctx.message.edit(content="Удаление канала из черного списка...")

    if channel is None:
        await ctx.message.edit(content=":x: | Канал не указан.")
        log_message("unblacklist", f"Канал не указан.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    with open("data/logsblacklist.txt", "r") as f:
        channels = f.readlines()

    with open("data/logsblacklist.txt", "w") as f:
        for line in channels:
            if line.strip("\n") != str(channel):
                f.write(line)

    await ctx.message.edit(content=f":white_check_mark: | Внесен в черный список `{channel}`")

    await delete_after_timeout(ctx.message)


@bot.command(description="Включение или отключение журналов уведомлений о словах.")
async def wordnotifications(ctx, status: str = None):
    status = status.lower()

    if status is None:
        await ctx.message.edit(content=":x: | Статус не указан.")
        log_message("wordnotifications", f"Статус не указан.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    if status == "on":
        config["wordNotifications"] = "True"

        with open("config.json", "w") as f:
            json.dump(config, f)

        load_config()

        await ctx.message.edit(
            content=":white_check_mark: | Включены словесные уведомления."
        )

        await delete_after_timeout(ctx.message)
    elif status == "off":
        config["wordNotifications"] = "False"

        with open("config.json", "w") as f:
            json.dump(config, f)

        load_config()

        await ctx.message.edit(
            content=":white_check_mark: | Отключены уведомления о словах."
        )

        await delete_after_timeout(ctx.message)
    else:
        await ctx.message.edit(content=":x: | Указан неверный статус.")

        log_message(
            "wordnotifications",
            f"Указан неверный статус, укажите либо `on` или `off`.",
            Fore.RED,
        )

        await delete_after_timeout(ctx.message)


@bot.command(description="Добавить слово в список уведомлений о словах.")
async def notifywords(ctx, word: str = None):
    await ctx.message.edit(content="Добавление слова...")

    if word is None:
        await ctx.message.edit(content=":x: | Ни слова не указано.")
        log_message("notifyWords", f"Ни слова не указано.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    notifyWords = config["notificationWords"]

    if word in notifyWords:
        notifyWords.remove(word)

        config["notificationWords"] = notifyWords

        with open("config.json", "w") as f:
            json.dump(config, f)

        await ctx.message.edit(content=f":white_check_mark: | Удален `{word}`")

    else:
        notifyWords.append(word)

        config["notificationWords"] = notifyWords

        with open("config.json", "w") as f:
            json.dump(config, f)

        await ctx.message.edit(content=f":white_check_mark: | Добавлено `{word}`")

    load_config()

    await delete_after_timeout(ctx.message)


@bot.command(description="Включение или отключение журналов веб-перехватчиков.")
async def webhooklogs(ctx, status: str = None):
    status = status.lower()

    if status is None:
        await ctx.message.edit(content=":x: | Статус не указан.")
        log_message("webhooklogs", f"Статус не указан.", Fore.RED)

        await delete_after_timeout(ctx.message)
        return

    if status == "on":
        config["webhooks"] = "True"

        with open("config.json", "w") as f:
            json.dump(config, f)

        load_config()

        await ctx.message.edit(content=":white_check_mark: | Вебхуки включены.")

        await delete_after_timeout(ctx.message)
    elif status == "off":
        config["webhooks"] = "False"

        with open("config.json", "w") as f:
            json.dump(config, f)

        load_config()

        await ctx.message.edit(content=":white_check_mark: | Вебхуки отключены.")

        await delete_after_timeout(ctx.message)
    else:
        await ctx.message.edit(
            content=":x: | Указан неверный статус. Допустимые статусы: `on`, `off`."
        )
        log_message(
            "webhooklogs",
            "Указан неверный статус.",
            Fore.RED,
        )

        await delete_after_timeout(ctx.message)
        return

    await delete_after_timeout(ctx.message)


@bot.command(aliases=["about", "info"], description="Показывает информацию о боте.")
async def avarice(ctx):
    response = requests.get("https://avariceapi.najmul190.repl.co/api/user/count")
    user_count = response.json()["user_count"]

    response = requests.get(
        "https://avariceapi.najmul190.repl.co/api/user/unique_count"
    )
    uniqueUserCount = response.json()["unique_user_count"]

    if user_count is None:
        user_count = "Unknown"

    current_time = datetime.datetime.utcnow()
    uptime = current_time - startTime

    days, hours, minutes, seconds = (
        uptime.days,
        uptime.seconds // 3600,
        (uptime.seconds // 60) % 60,
        uptime.seconds % 60,
    )

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи
                           
[Версия] {currentVersion}


[Команды] {len(bot.commands)}
[Время работы] {days}d:{hours}h:{minutes:02}m:{seconds:02}s

[Создатель] @remus
[перевод] @mop157,@remus
[допольнение] remus
это допольнение сделано для пользователя моп```"""
    )


bot.remove_command("help")


@bot.command(description="Показывает это сообщение.")
async def help(ctx, command: str = None):
    prefix = config["prefix"]

    if command is None:
        await ctx.message.edit(
            content=f"""```ini
Скрытые очи | Префикс: {prefix}

[{prefix}moderation] Команды модерации
[{prefix}utilities] Команды утилиты
[{prefix}tools/2] Общие инструменты
[{prefix}troll/2] Команды троллинга 
[{prefix}raid] Команды рейда (используйте на свой страх и риск)
[{prefix}fun] Команды, созданные для развлечения
[{prefix}nsfw] Команды NSFW
[{prefix}animated] Анимированные команды
[{prefix}text] Текстовые команды: сделайте ваш текст крутым
[{prefix}settings] Команды настроек
[{prefix}avarice] Показать информацию о селфботе
```"""
        )

        await delete_after_timeout(ctx.message)

    else:
        command = bot.get_command(command)

        if command:
            aliases = str(command.aliases)
            aliases = aliases.replace("[", "")
            aliases = aliases.replace("]", "")
            aliases = aliases.replace("'", "")

            await ctx.message.edit(
                content=f"""```markdown
Скрытые очи | {command.name} | Prefix: {prefix}

[Описание] {command.description}
[Применение] {prefix}{command.name} {command.signature}
[Псевдонимы] {aliases}
```"""
            )

            await delete_after_timeout(ctx.message)

        else:
            await ctx.message.edit(content=":x: | Команда не найдена.")

            await delete_after_timeout(ctx.message)


@bot.command(description="Показывает команды модерации.")
async def moderation(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Команды модерации | Префикс: {prefix}

[{prefix}createtext] Создать текстовый канал
[{prefix}createvoice] Создать голосовой канал
[{prefix}forcenick] Продолжайте менять псевдоним пользователя, чтобы он оставался постоянным
[{prefix}stopforcenick] Не заставлять пользователя менять никнейм
[{prefix}nick] Изменить никнейм пользователя
[{prefix}purge] Очистить определенное количество сообщений
[{prefix}purgeuser] Удаление сообщений пользователя
[{prefix}purgecontains] Удаление сообщений, содержащих определенное слово.
[{prefix}clean] Удаляет ваши собственные сообщения.
[{prefix}kick] Удалить пользователя
[{prefix}ban] Заблокировать пользователя
[{prefix}unban] Разблокировать пользователя
[{prefix}exportbans] Экспорт банов сервера в формате ID
[{prefix}importbans] Импорт банов с другого сервера
[{prefix}timeout] Тайм-аут пользователя
[{prefix}untimeout] Отменить тайм-аут пользователя
[{prefix}slowmode] Установить медленный режим канала
[{prefix}nuke] Уничтожить канал, клонировать его и удалить старый
[{prefix}roleall] Назначить роли всем участникам
[{prefix}removeroleall] Удаление роли у всех участников
[{prefix}giveallroles] Передайте пользователю каждую роль на сервере.
```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def utilities(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Служебные команды | Префикс: {prefix}

[{prefix}firstmessage] Получить первое сообщение в канале
[{prefix}dmtoken] Отправьте пользователю DM со своим токеном
[{prefix}playing] Установите свой игровой статус
[{prefix}watching] Установите статус просмотра
[{prefix}listening] Установите статус прослушивания
[{prefix}streaming] Установите статус потоковой передачи
[{prefix}removepresence] Удалить свое присутствие
[{prefix}cycleplaying] Циклическое перелистывание списка статусов воспроизведения.
[{prefix}stopcycleplaying] Прекратить циклическое переключение статусов воспроизведения
[{prefix}cyclewatching] Циклическое перелистывание списка статусов просмотра.
[{prefix}stopcyclewatching] Прекратить циклическое переключение статусов просмотра.
[{prefix}cyclelistening] Циклическое переключение списка статусов прослушивания.
[{prefix}stopcyclelistening] Прекратить циклическое переключение статусов прослушивания
[{prefix}cyclestreaming] Циклическое переключение списка статусов потоковой передачи.
[{prefix}stopcyclestreaming] Прекратить циклическое переключение статусов потоковой передачи
[{prefix}online] Установите свой статус «В сети»
[{prefix}idle] Установите для себя статус ожидания
[{prefix}dnd] Установите свой статус «Не беспокоить»
[{prefix}invisible] Установите свой статус на невидимый
[{prefix}leaveallgroups] Покиньте все группы, в которых вы состоите.
[{prefix}leaveallservers] Покиньте все гильдии, в которых вы состоите.
[{prefix}stopleave] Прекратить покидать все гильдии или группы.
[{prefix}nickloop] Прокрутка списка псевдонимов
[{prefix}stopnickloop] Прекратите перебирать псевдонимы
[{prefix}setpfp] Установите изображение профиля
[{prefix}deletewebhook] Удаление вебхука
[{prefix}hypesquad] Установите свой дом Hypesquad
[{prefix}status] Циклическое изменение статуса по времени, различные статусы, текст или очистка
[{prefix}afk] Установите свой статус на афк
```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def tools(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Общие инструменты | Префикс: {prefix}

[{prefix}tokeninfo] Получить информацию о токене
[{prefix}userinfo] Получить информацию о пользователе
[{prefix}serverinfo] Получить информацию о сервере
[{prefix}inviteinfo] Получить информацию о приглашении
[{prefix}serverfriends] Получите список ваших друзей на сервере.
[{prefix}ipinfo] Получить информацию об IP-адресе
[{prefix}mutualservers] Получите список серверов, которыми вы делитесь с пользователем.
[{prefix}mutualfriends] Получите список друзей, которыми вы делитесь с пользователем.
[{prefix}roleinfo] Получить информацию о роли
[{prefix}snipe] Снять последнее удаленное сообщение
[{prefix}editsnipe] Скопировать последнее отредактированное сообщение
[{prefix}adminservers] Получите список серверов, на которых вы являетесь администратором.
[{prefix}revavatar] Обратный поиск по изображению аватара пользователя
[{prefix}autobumper] Автоматически поднимать сервер каждые 2 часа.
[{prefix}stopbumper] Прекратить автоматически поднимать сервер
[{prefix}autoslashcommand] Автоматически использовать косую черту с задержкой
[{prefix}autocommand] Автоматически использовать команду с задержкой
[{prefix}stopautoslashcommand] Автоматическая остановка с помощью команды косой черты.```"""
    )
    await delete_after_timeout(ctx.message)

@bot.command()
async def tools2(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Общие инструменты | Префикс: {prefix}

[{prefix}stopautocommand] Автоматическая остановка с помощью команды
[{prefix}dumpembed] Сохраните последнюю вставку из канала в формате JSON
[{prefix}dumpchat] Скопировать количество сообщений из канала в текстовый файл
[{prefix}dm] Отправьте пользователю сообщение в Директ
[{prefix}cryptotransaction] Получить информацию о криптотранзакции
[{prefix}nickscan] Перечисляет все ваши ники на всех серверах.
[{prefix}nickreset] Сбросить никнейм на всех серверах
[{prefix}addemoji] Добавьте смайлик на сервер
[{prefix}allowaddemoji] Разрешить пользователю добавлять смайлы на сервер, отправив смайлик
[{prefix}emojidelete] Удаление смайла с сервера
[{prefix}dumppattachments] Скопировать количество вложений из канала в текстовый файл.
[{prefix}downloadattachments] Загрузите определенное количество вложений с канала.
[{prefix}roles] Получить список ролей на сервере.
[{prefix}roleperms] Получить список разрешений для роли.
[{prefix}userbio] Получить биографию пользователя
[{prefix}banner] Получить баннер пользователя
[{prefix}scrapemembers] Очистите всех участников с сервера и сохраните их в текстовый файл.
[{prefix}scrapepfps] Очистите все файлы PFPS с сервера и сохраните их в текстовый файл.
```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def troll(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Команды тролля | Префикс: {prefix}

[{prefix}empty] Отправить пустое сообщение
[{prefix}purgehack] Отправьте кучу пустых сообщений, чтобы вроде бы очистить канал.
[{prefix}ghostping] Призрачный пинг пользователя в канале
[{prefix}hiddenping] Пинговать пользователя в канале, используя эксплойт для сокрытия пинга
[{prefix}hiddenpingeveryone] Пропинговать всех в канале, используя эксплойт, позволяющий скрыть пинг
[{prefix}hiddeninvite] Отправьте приглашение на сервер, используя эксплойт, позволяющий скрыть приглашение.
[{prefix}ghostpingrole] Призрак пингует роль в канале, используя эксплойт для сокрытия пинга
[{prefix}stealpfp] Украсть pfp пользователя
[{prefix}invispfp] Установите для своего профиля прозрачное изображение.
[{prefix}pingmute] Отключает звук для всех пользователей, которые пингуют вас.
[{prefix}stoppingmute] Прекратите отключать звук для пользователей, которые пингуют вас
[{prefix}pingkick] Удаляет всех пользователей, которые пингуют вас.
[{prefix}stoppingkick] Перестаньте кикать пользователей, которые пингуют вас
[{prefix}pingrole] Предоставляет всем пользователям, которые пингуют вас, роль
[{prefix}stoppingrole] Прекратите давать пользователям, которые пингуют вас, роль
[{prefix}mimic] Имитирует пользователя, копируя каждое отправляемое им сообщение.```"""
    )

    await delete_after_timeout(ctx.message)

@bot.command()
async def troll2(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Команды тролля | Префикс: {prefix}

[{prefix}stopmimic] Перестаньте подражать пользователю
[{prefix}smartmimic] Имитирует пользователя, копируя каждое отправленное им сообщение, но ЭТО ТАКОЕ
[{prefix}stopsmartmimic] Перестаньте подражать пользователю
[{prefix}addwhitelist] Добавьте сервер в белый список для команд pingmute, pingkick и pingrole.
[{prefix}removewhitelist] Удаление сервера из белого списка для команд pingmute, pingkick и pingrole.
[{prefix}noleave] Заставляет пользователя оставаться в группе, не позволяя ему выйти из группы.
[{prefix}allowleave] Разрешить пользователю покинуть группу
[{prefix}grouplag] Задержка группового голосового канала по массовому изменению региона
[{prefix}stopgrouplag] Прекратить отставание группового голосового канала
[{prefix}pinspam] Закрепляйте каждое сообщение, отправленное пользователем.
[{prefix}stoppinspam] Перестаньте закреплять каждое сообщение, отправляемое пользователем.
[{prefix}deleteannoy] Удалить все сообщения, отправленные пользователем.
[{prefix}stopdeleteannoy] Прекратить удалять каждое сообщение, отправленное пользователем.
[{prefix}reactuser] Реагировать на каждое сообщение, отправляемое пользователем.
[{prefix}stopreactuser] Перестаньте реагировать на каждое сообщение, отправляемое пользователем.
[{prefix}forcedisconnect] Продолжать отключать пользователя от голосового канала
[{prefix}stopforcedisconnect] Прекращение принудительного отключения пользователя от голосового канала.```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def raid(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Рейдовые команды | Префикс: {prefix}

[{prefix}banall] Заблокировать всех участников на сервере
[{prefix}unbanall] Разблокировать всех участников на сервере
[{prefix}massmention] Продолжайте упоминать множество пользователей на канале
[{prefix}deletechannels] Удалить все каналы на сервере
[{prefix}deleteroles] Удалить все роли на сервере
[{prefix}deleteemojis] Удалить все смайлы на сервере
[{prefix}deletestickers] Удалить все стикеры на сервере
[{prefix}nukeserver] Удалить все каналы, роли, смайлы и стикеры на сервере.
[{prefix}webhookspam] Создает вебхук в каждом канале и рассылает спам-сообщения, указанные в config.json.
[{prefix}stopwebhookspam] Прекратите рассылать спам через вебхуки
```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def fun(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Веселые команды | Префикс: {prefix}

[{prefix}chatbot] Бесплатно поговорите с искусственным интеллектом на базе ChatGPT
[{prefix}imagine] Создать изображение с помощью ИИ
[{prefix}halftoken] Получите половину токена пользователя
[{prefix}nsfw] Набор команд NSFW
[{prefix}iq] Получите IQ пользователей
[{prefix}dick] Получить размер члена пользователя
[{prefix}8ball] Задайте вопрос волшебной восьмерке
[{prefix}kiss] Поцеловать пользователя с помощью гифки
[{prefix}hug] Обнять пользователя гифкой
[{prefix}pat] Пометить пользователя гифкой
[{prefix}slap] Отдать пользователю пощечину гифкой
[{prefix}tickle] Пощекочить пользователя гифкой
[{prefix}cuddle] Обнимите пользователя с помощью гифки
[{prefix}feed] Подарить пользователю гифку
[{prefix}triggertyping] Триггер ввода в канале
[{prefix}massreact] Реагируйте смайликами на количество сообщений
[{prefix}slots] Сыграйте в игровые автоматы
[{prefix}spam] Спамить сообщение в канале определенное количество раз
[{prefix}poll] Создать опрос в канале
[{prefix}coinflip] Подбросить монетку
[{prefix}randomnumber] Получить случайное число
[{prefix}rps] Поиграть в камень, ножницы, бумагу
[{prefix}dice] Бросить кубик
```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def animated(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Анимированные текстовые команды | Префикс: {prefix}

[{prefix}fuckyou] Отправляет пользователю анимированное сообщение «иди на хуй!»
[{prefix}count] Сосчитайте до 100 в сообщении
[{prefix}abc] Напишите весь алфавит в сообщении
[{prefix}абв] Напишите весь алфавит в сообщении
[{prefix}virus] Отправьте анимированный вирус по вашему выбору.
[{prefix}readrules] Попросите пользователя прочитать чертовы правила.
[{prefix}warning] Отправить анимированное предупреждающее сообщение.
[{prefix}bomb] Отправить анимированное сообщение с бомбой
[{prefix}wank] Отправьте анимированное сообщение о дрочке
```"""
    )

    await delete_after_timeout(ctx.message)


@bot.command()
async def text(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Анимированные текстовые команды | Префикс: {prefix}

[{prefix}encode] Закодируйте сообщение, используя base64.
[{prefix}decode] Декодировать сообщение в формате Base64.
[{prefix}reverse] Перевернуть строку
[{prefix}mock] Сделать текст издевательским
[{prefix}clap] Добавляйте хлопок между каждым словом.
[{prefix}text2bin] Преобразование текста в двоичный код
[{prefix}bin2text] Бинарное преобразование в текст
[{prefix}text2hex] Текст в шестнадцатеричном формате
[{prefix}morse] Преобразование текста в азбуку Морзе
[{prefix}unmore] Код Морзе в текст
[{prefix}emojify] Преобразует ваш текст в региональные индикаторы.
[{prefix}vaporwave] m a k e y o u r t е x t l я k e t h я s
[{prefix}owo] делает ваш текст таким ```"""
    )
    
    await delete_after_timeout(ctx.message)


@bot.command()
async def settings(ctx):
    prefix = config["prefix"]

    await ctx.message.edit(
        content=f"""```ini
Скрытые очи | Команды настройки | Префикс: {prefix}

[{prefix}prefix] Изменить префикс селфбота
[{prefix}shutdown] Завершить работу селфбота
[{prefix}deletetimer] Настройте таймер удаления сообщений.
[{prefix}afkmessage] Установите сообщение AFK
[{prefix}spy] Шпионить за пользователем, получая уведомления обо всем, что он делает
[{prefix}unspy] Прекратите шпионить за пользователем
[{prefix}uptime] Получите время безотказной работы селфбота
[{prefix}setupwebhooks] Настройте сервер веб-перехватчиков для уведомлений
[{prefix}messagelogsblacklist] Занести канал в черный список из журналов сообщений
[{prefix}unblacklist] Удалить канал из черного списка из журналов сообщений
[{prefix}wordnotifications] Включение или отключение текстовых уведомлений
[{prefix}notifywords] Добавление или удаление слов из уведомлений о словах
[{prefix}webhooklogs] Включение или отключение журналов веб-перехватчиков```"""
    )

    await delete_after_timeout(ctx.message)


####################################### Error Handling #######################################

if config["debugMode"] == "False":

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.edit(content=":x: | Команда не найдена.")
            log_message("Avarice Error", error, Fore.RED)
            await delete_after_timeout(ctx.message)

        elif isinstance(error, discord.errors.NotFound):
            log_message("Avarice Error", error, Fore.RED)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.edit(content=f":x: | Отсутствует обязательный аргумент: {error}")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.BadArgument):
            await ctx.message.edit(content=f":x: | Неверный аргумент: {error}")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.edit(content=":x: | Отсутствуют разрешения.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.BadInviteArgument):
            await ctx.message.edit(
                content=":x: | Плохой аргумент в пользу приглашения. Возможно, срок действия истек или недействителен."
            )
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.message.edit(content=":x: | У бота отсутствуют разрешения.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.MissingRole):
            await ctx.message.edit(content=":x: | Отсутствует роль.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.DisabledCommand):
            await ctx.message.edit(content=":x: | Команда отключена.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.TooManyArguments):
            await ctx.message.edit(content=":x: | Слишком много доводов.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.UserInputError):
            await ctx.message.edit(content=":x: | Ошибка ввода пользователя.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.edit(content=":x: | Участник не найден.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.UserNotFound):
            await ctx.message.edit(content=":x: | Пользователь не найден.")
            await delete_after_timeout(ctx.message)

        elif isinstance(error, commands.CommandError):
            await ctx.message.edit(content=":x: | Ошибка команды.")
            log_message("Avarice Error", error, Fore.RED)

            try:
                await delete_after_timeout(ctx.message)
            except:
                pass

        elif isinstance(error, commands.CheckFailure):
            await ctx.message.edit(content=":x: | Проверить ошибку.")
            await delete_after_timeout(ctx.message)


try:
    if config["debugMode"] == "True":
        bot.run(config["token"])
    else:
        bot.run(config["token"], log_handler=None)

except discord.errors.HTTPException:
    log_message("Ошибка токена", "Установлен неверный токен config.json.", Fore.RED)

    TOKEN = input("Enter a valid token: ")

    config["token"] = TOKEN

    with open("config.json", "w") as f:
        json.dump(config, f)

    os.execl(sys.executable, sys.executable, *sys.argv)

except discord.errors.LoginFailure:
    log_message("Token Error", "Invalid token set config.json.", Fore.RED)

    TOKEN = input("Enter a valid token: ")

    config["token"] = TOKEN

    with open("config.json", "w") as f:
        json.dump(config, f)

    os.execl(sys.executable, sys.executable, *sys.argv)
