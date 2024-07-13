

nots = f':x: | извените эта игра на даный момент отключена'
DM = f':x: | команда отключена в лс'

################### Камень, ножницы, бумага #############

rps_error_user1 = f":x: | вы уже присоединились к игре"
rps_error_user2 = f":x: | к этой игре нельзя больше присоединиться"
rps_error_user3 = f":x: | вы уже сделали свой выбор, ожидайте другого игрока"
rps_error_user4 = f":x: | время вышло, игра окончена"

rps_info = """
Камень, ножницы, бумага (Rock, Paper, Scissors) - это простая и популярная игра, в которой два игрока выбирают один из трех предметов: камень, ножницы или бумагу. Результаты игры определяются следующим образом:

- Камень побеждает ножницы (камень применяет ножницы).
- Ножницы побеждают бумагу (ножницы разрезают бумагу).
- Бумага побеждает камень (бумага накрывает камень).

Если оба игрока выбирают одинаковый предмет, игра считается ничьей.
создано - mop157
"""

rps_play = """
С кем бы вы хотели сыграть?
"""

rps_play_bot = "нажмите одно из (камень, ножницы, бумага)"


rps_play_user = """
С кем бы вы хотели сыграть?\nигроков 
"""

######################## mafia #############

mafia_game = "Добро пожаловать в игру Мафия!\n\nНажмите ▶️, чтобы начать игру, или ➕, чтобы присоединиться к игре."
mafia_start = "Игра началась! Ожидание игроков..."
mafia_add_player = "Вы добавлены в команду!"

mafia_error_1 = ":x: | к этой игре нельзя больше присоединиться"
mafia_error_2 = ":x: | вы уже присоединились к игре"

mafia_info = """
### Мафия через Discord Бота: Короткое Описание Игры

**Мафия** — это увлекательная ролевая игра, проводимая через Discord бота. Игроки разделяются на две команды: мафию и мирных жителей. Цель мафии — устранить всех мирных жителей, а цель мирных жителей — найти и обезвредить всех членов мафии.

**Как играть:**
1. **Начало игры:**
   - Команда вводит команду для начала игры.
   - Бот раздает роли случайным образом и отправляет их в личные сообщения игрокам.
   
2. **Ночь:**
   - Все игроки получают сообщение от бота "наступает ночь".
   - Мафия выбирает жертву через приватные сообщения бота.
   - Комиссар (если есть) проверяет игрока через приватные сообщения боту.

3. **День:**
   - Бот сообщает о жертвах ночи.
   - Игроки обсуждают, кто может быть мафией, и голосуют за исключение одного из игроков.
   - Голосование проводится с помощью (хз).

4. **Циклы:**
   - Игра продолжается, чередуя ночи и дни, пока одна из команд не достигнет своей цели.

**Команды:**
- **/mafia** — начать новую игру.

Игра требует внимательности, стратегического мышления и умения убеждать. Приятной игры!
создано - mop157"""

############################################### buckshot_roulette 

buckshot_roulette = """

"Buckshot Roulette" - это захватывающая многопользовательская текстовая игра, основанная на принципах русской рулетки, но с использованием дробовика и патронов. В этой игре участники по очереди делают ходы, стреляя из дробовика и активируя предметы. Цель игры - сохранить своё здоровье и остаться последним выжившим игроком.

Основные элементы игры:

    Патроны: В игре используются два типа патронов:

        🔴 Красный (опасный)
        🔵 Синий (безопасный)

    Предметы: У игроков есть возможность использовать различные предметы, которые могут повлиять на ход игры.
       
    Очередь ходов: Игроки по очереди делают ходы, стреляя из дробовика в себя/другого пользователя  или активируя предметы.

    Режимы сложности: Игра поддерживает несколько режимов сложности, которые влияют на следующие параметры:
        Здоровье (HP): Количество единиц здоровья у каждого игрока.
        Получение предметов: Количество предметов, которые игроки могут получать.
        Количество патронов в дробовике: Количество патронов, которое участвует в каждом раунде.

    Режимы сложности:
        Легкий: 2 HP, 3 патрона, 1 предмета.
        Средний: 4 HP, 5 патронов, 2 предмета.
        Тяжелый: 6 HP, 7 патронов, 3 предмет.

    Победа: Игрок, который теряет все единицы здоровья, выбывает из игры. Побеждает тот, кто остаётся последним выжившим с хотя бы одной единицей здоровья.

Пример игрового процесса:

    Начинается раунд, и игра предлагает игрокам сделать выбор: выбрать дробовик или активировать предмет.
    Игрок выбирает дробовик или активирует предмет.
    Если выпал синий патрон, игрок остается в игре и продолжает с тем же количеством HP.
    Если выпал красный патрон, игрок теряет одну единицу HP или забывает у другого игрока
    Игра продолжается до тех пор, пока не останется один игрок.


"Buckshot Roulette" сочетает в себе элементы удачи, стратегического мышления и тактики, создавая напряжённую и увлекательную атмосферу для всех участников.
создано - mop157"""

buckshot_roulette_1 = "Увеличительное стекло — это, вероятно, тот предмет, который вам захочется потянуть больше всего ; это полезный инструмент, который покажет текущий снаряд, загруженный в патронник, не удаляя его и не заканчивая ход. Если вы не знаете, каким может быть текущий снаряд, стоит воспользоваться увеличительным стеклом, чтобы убедиться, что вы не выстрелите холостым или, что еще хуже, не поранитесь боевым патроном. "
buckshot_roulette_2 = "Ручная пила — отличный выбор для максимального ущерба, при условии, что вы правильно ее используете. После использования ручной пилы ваш следующий выстрел нанесет урон на два заряда вместо одного. "
buckshot_roulette_3 = "Выпив банку енергетика, вы выбросите текущий патрон из патронника дробовика. Вы также можете использовать несколько бутылок енергетика подряд, чтобы опорожнить камеру и попытаться быстрее перейти к более выгодному порядку. "
buckshot_roulette_4 = "Этот предмет заставляет противника пропустить следующий ход, и его можно использовать, чтобы дать себе передышку, если вы не уверены в текущем снаряде или когда патронник израсходован равномерно между живыми и пустыми патронами. "
buckshot_roulette_5 = "Сигарета — один из немногих предметов, восстанавливающих заряд вашего дефибриллятора."
buckshot_roulette_6 = "магазин воспользуйтесь им чтобы зарядить дробовик допольнительним патроном"
buckshot_roulette_7 = "Более опасная версия сигареты, лекарство с истекшим сроком годности, может дать вам еще два заряда дефибриллятора, но также может стоить вам заряда. Если у вас меньше двух зарядов, лучше отказаться от этого, чтобы не поставить себя в смертельную ситуацию. Однако если у вас есть сигареты, они «покроют» стоимость лекарств, если вы потеряете заряд. "
buckshot_roulette_8 = "Инвертор переключает текущие холостые и боевые патроны в патроннике; если, например, заряжены два холостых и четыре боевых патрона, то вместо этого в дробовике будет четыре холостых и два боевых патрона."

################################################

witch = """
**Карточная игра "Ведьма"** - это простая и увлекательная игра, которая идеально подходит для небольшой компании. Вот краткое описание правил:

1. **Количество игроков**: От 3 до 5 человек.
2. **Цель игры**: Избавиться от всех своих карт и не остаться с картой "Ведьма" на руках.
3. **Колода**: Стандартная колода из 32/52 карт плюс одна специальная карта "Ведьма".

### Правила игры:

1. **Раздача карт**: Все карты, включая "Ведьму", раздаются ботом поровну. У некоторых игроков может оказаться на одну карту больше.
2. **Начало игры**: Игру начинает игрок создавший комнату. Ход переходит от 1 до последнего.
3. **Ход игрока**: Игрок берет одну карту из руки соседа слева, не видя её.
4. **Пары**: Если у игрока образуется пара (две карты одного ранга), пары убираются из игры.
5. **Ведьма**: Карта "Ведьма" не образует пар с другими картами.
6. **Конец игры**: Игра продолжается до тех пор, пока у всех игроков не закончатся карты, кроме одного. Игрок, у которого остается карта "Ведьма", проигрывает.

### Дополнительные правила:

- **Избавление от карт**: Пары образуются и сбрасываются сразу же, как только игрок их обнаруживает.
- **Проигравший**: Игрок, у которого в конце игры остаётся карта "Ведьма", считается проигравшим.

### Задача игры:

Игроки стремятся избавиться от своих карт, формируя пары и избегая удерживания карты "Ведьма". Простые правила и элемент неожиданности делают эту игру интересной и захватывающей.
создано - mop157 и haiko_uwu
"""

trivia = """
**Описание игры "Викторина"**

Добро пожаловать в захватывающую игру "Викторина"! В этой интеллектуальной дуэли участвуют два игрока, стремящихся первыми набрать 3 очка. Игра предлагает более 260 разнообразных вопросов, охватывающих самые разные темы и уровни сложности.

Игровой процесс уникален: вместо привычного поочерёдного ответа, оба игрока отвечают на вопросы одновременно, что добавляет динамики и азарт. Побеждает тот, кто первым набирает 3 очка.

Проверьте свои знания и скорость реакции в этой увлекательной и напряжённой игре!
"""

Hangman = """"
Игра "Виселица" предлагает классическое испытание на знание слов, но с уникальными особенностями. Цель участников - угадать загаданное слово, называя буквы. У игроков есть бесконечное количество попыток, чтобы отгадать слово, что позволяет сосредоточиться на стратегии и анализе. Победить можно двумя способами: набрать наибольшее количество очков или угадать само слово. Эта игра отлично подходит для вечеринок и дружеских встреч, предлагая увлекательное и интеллектуальное развлечение, в котором каждый раунд приносит новые вызовы и эмоции.
"""

Truth_or_lie = """
Игра "Правда или Ложь" предлагает игрокам проверить свои знания и интуицию, решая, являются ли предложенные утверждения правдой или вымыслом. Цель участников - как можно быстрее набрать 5 баллов, чтобы одержать победу. В игре представлено более 300 кратких историй и фактов, что гарантирует увлекательные и познавательные раунды. Игра идеально подходит для вечеринок и дружеских встреч, предлагая веселое и познавательное времяпрепровождение.
"""

anagrams = """
Игра "Расшифруй слово" предлагает увлекательное испытание, в котором игроки соревнуются в расшифровке загаданого слова. Цель каждого участника - угадать слово за ограниченное количество попыток. У каждого игрока есть 5 попыток, чтобы найти правильное слово, что добавляет элемент напряжения и стратегии. Эта игра отлично подходит для вечеринок и дружеских встреч, предлагая интеллектуальные и развлекательные испытания. Благодаря разнообразию слов и ограниченному числу попыток, каждый раунд приносит новые эмоции и азарт.
"""

role_playing = """
### Ролевые диалоги

**Описание**:
Игра "Ролевые диалоги" позволяет игрокам разыгрывать различные сценарии, принимая на себя определенные роли. Бот предоставляет сценарии и назначает роли, а игроки по очереди отправляют свои реплики, развивая сюжет.

**Цель игры**:
Развивать креативность, навыки импровизации и умение взаимодействовать с другими участниками.

**Как играть**:
1. Бот предлагает сценарий и распределяет роли между игроками.
2. Бот отправляет начальные реплики для каждой роли, чтобы задать направление диалога.
3. Игроки по очереди разыгрывают свои реплики, придерживаясь своих ролей.
4. Бот может добавлять неожиданные повороты сюжета.
5. После завершения диалога игроки голосуют за лучшего импровизатора.

**Пример сценария**:
**Сценарий**: Встреча в кафе
**Роли**: Официант, Посетитель 1, Посетитель 2
**Начальный диалог**:
- **Официант**: "Добрый день! Добро пожаловать в наше кафе. Что будете заказывать?"
- **Посетитель 1**: "Привет! Мне, пожалуйста, кофе и кусочек яблочного пирога."
- **Посетитель 2**: "А мне чай и круассан."

**Неожиданный поворот**:
- Бот сообщает, что в кафе внезапно пропало электричество.

Эта игра проста в реализации и увлекательна, поскольку позволяет игрокам проявить креативность и участвовать в веселых и неожиданных диалогах.
"""

##############################################################

Puzzle = "Два человека пришли в заброшенный отель. Первый вошёл через главный вход, а второй через запасной выход. Когда второй человек вошёл, дверь за ним захлопнулась. Тем временем первый человек прошел дальше и обнаружил телефон сотрудников отеля и странную книгу. Открыв книгу на первой странице, он увидел какой-то номер. Несмотря на странность ситуации, он решил набрать этот номер и услышал в ответ голос второго человека: *Дверь закрылась...* Положив телефон, он поспешил на помощь другу, но обнаружил, что и входная дверь тоже закрылась. Позвонив ему второй раз, он спросил, что тот видит и есть ли там что-то, например, генератор или что-то подобное, чтобы выбраться."
