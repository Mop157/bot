import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class MemberDatabase(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.bot = client
        self.db_conn = sqlite3.connect('cogs.SQLite.members.db')
        self.init_database()

    def init_database(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                user_id INTEGER PRIMARY KEY,
                points INTEGER DEFAULT 0
            )
        ''')
        self.db_conn.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Добавляем нового участника в базу данных при входе на сервер
        cursor = self.db_conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO members (user_id) VALUES (?)', (member.id,))
        self.db_conn.commit()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Удаляем участника из базы данных при выходе из сервера
        cursor = self.db_conn.cursor()
        cursor.execute('DELETE FROM members WHERE user_id = ?', (member.id,))
        self.db_conn.commit()

    @commands.command(name='points')
    async def get_points(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT points FROM members WHERE user_id = ?', (member.id,))
        result = cursor.fetchone()
        points = result[0] if result else 0
        await ctx.send(f'{member.display_name} имеет {points} очков.')

    def cog_unload(self):
        self.db_conn.close()

async def setup(client:commands.Bot) -> None:
  await client.add_cog(MemberDatabase(client))