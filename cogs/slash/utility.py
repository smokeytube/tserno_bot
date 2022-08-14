import disnake
from disnake.ui import Button
from disnake.ext import commands

from utils import decorations

class Utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot
        self.f = "refined_words.txt"

    @commands.slash_command(
        name="backup",
        description="Backup the refined words text file.",
    )
    @decorations.is_owner()
    async def backup(self, interaction):
        # Backup channel
        channel = self.bot.get_channel(1008509065997078538)
        l1 = []
        with open(self.f, 'r', encoding="utf-8") as f:
            l1 = f.readlines()
            number_of_words = len(l1)
            await interaction.send(f"Successful. Backup in channel <#1008509065997078538>")
        with open(self.f, 'rb') as f:
            await channel.send(f"Number of entries: {number_of_words}")
            await channel.send(file=disnake.File(f, 'чуккäмид.txt'))

def setup(bot):
    bot.add_cog(Utility(bot))
