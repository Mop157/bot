# button2 = Button(label=f"‹--", style=discord.ButtonStyle.blurple, custom_id="button2")
    
# button2.callback = button_callback2
    
# view6 = View()
# view6.add_item(button2)
    
# await ctx.send(content=leaderboard_message, view=view5)

import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord import app_commands

import json, random
import config
import cogs.text.tekst as tekst
import cogs.command.fun as fun



#######################################################
########## камень, ножничи, бумага ####################
#######################################################

user = None
bot_choice = None

class button(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # async def button_callback_rps_bot(interaction: discord.Interaction):
    #     await interaction.response.send_message(content=tekst.rps_play_bot, view=view_bot)
    #     async def paper(interaction: discord.Interaction):
    #         choices = ['камень', 'ножницы', 'бумага']
    #         user = 'бумага'

    #         bot_choice = random.choice(choices)


    #         if user == bot_choice:                    
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_00, view=None)
    #         elif bot_choice == 'ножницы':
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_0_1, view=None)
    #         elif bot_choice == 'камень':
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_1_0, view=None)
                    
                          

    #     async def kamen(interaction: discord.Interaction):
    #         user = 'камень'
    #         choices = ['камень', 'ножницы', 'бумага']

    #         bot_choice = random.choice(choices)

    #         if user == bot_choice:                    
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_00, view=None)
    #         elif bot_choice == 'ножницы':
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_1_0, view=None)
    #         elif bot_choice == 'бумага':
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_0_1, view=None)
        
    #     async def noznuci(interaction: discord.Interaction):
    #         user = 'ножницы'
    #         choices = ['камень', 'ножницы', 'бумага']

    #         bot_choice = random.choice(choices)

    #         if user == bot_choice:                    
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_00, view=None)
    #         elif bot_choice == 'бумага':
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_1_0, view=None)
    #         elif bot_choice == 'камень':
    #             await interaction.response.edit_message(content=tekst.rps_play_bot_0_1, view=None)

    #     button_rps_paper.callback = paper
    #     button_rps_kamen.callback = kamen
    #     button_rps_noznuci.callback = noznuci

    # async def button_callback_rps_user(interaction: discord.Interaction):
    #     await interaction.response.send_message("helo")

    # async def button_callback_rps_info(interaction: discord.Interaction):
    #     await interaction.response.send_message(content=tekst.rps_info, ephemeral=True)


    #######################################################

async def setup(client:commands.Bot) -> None:
  await client.add_cog(button(client))