import random
import cogs.text.Role_playing_text as text

buskshot = {}

def cartridg():
        buskshot["channe_id"] = {"info": {'cartridge': []}}
        cartridge = ["🔴", "🔵"]
        
        for _ in range(0, 3):
            buskshot['channe_id']['info']['cartridge'] += random.choice(cartridge)
        
        def are_all_cartridges_same(cartridge_list):
            # Проверяем, являются ли все элементы списка одинаковыми
            return all(item == cartridge_list[0] for item in cartridge_list)

        # Получаем список cartridges
        cartridges = buskshot['channe_id']['info']['cartridge']

        # Проверяем и выводим результат
        if are_all_cartridges_same(cartridges):
            if cartridges[0] == "🔴":
                print(buskshot['channe_id']['info']['cartridge'])
                print("Все картриджи красные")
                cartridges.remove("🔴")
                cartridges.append("🔵")
                
            elif cartridges[0] == "🔵":
                print(buskshot['channe_id']['info']['cartridge'])
                print("Все картриджи синие")
                cartridges.remove("🔵")
                cartridges.append("🔴")
            else:
                print("Ошибка: неизвестный цвет картриджей")
        else:
            print("Картриджи разных цветов")
        print(buskshot['channe_id']['info']['cartridge'])
# cartridg()
# if buskshot['channe_id']['info']['cartridge'] == []:
#      print(1)
# buskshot['channe_id']['info']['cartridge'].remove("🔴")
# buskshot['channe_id']['info']['cartridge'].remove("🔴")
# if buskshot['channe_id']['info']['cartridge'] == []:
#      print(1)
# buskshot['channe_id']['info']['cartridge'].remove("🔵")

# if buskshot['channe_id']['info']['cartridge'] == []:
#      print(1)

# lypa # лупа
# noz # нож
# energi # енергетик
# narycnik # нарушники
# cugara # сыгарета
# magaz # магазин

# async def menu_callback(interaction: discord.Interaction):
#     stop_event.set()

# options = []

# for opt in list_mafia[channel_id]['players']:
#     opts = guild.get_member(opt)
#     options.append(discord.SelectOption(label=f"{opts}"))

# select = discord.ui.Select(
#         placeholder="выберите игрока",
#         min_values=1,
#         max_values=1,
#         options=options
#                             )
# select.callback = menu_callback
                        
# view = discord.ui.View(timeout=20)
# view.add_item(select)

# stop_event = asyncio.Event()

# async def timeout_callback():
#     try:
#         await asyncio.wait_for(stop_event.wait(), timeout=view.timeout)
#     except asyncio.TimeoutError:
#         await don()

# self.client.loop.create_task(timeout_callback()) 
hello = {"he": {11: 1, 22: 0, 33: 0, 44: 0}}
yees = []
# for k in text.text1:

for p in range(1, 7):
     print(p)