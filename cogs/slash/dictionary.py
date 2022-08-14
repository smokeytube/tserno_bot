import random

from disnake import Option, OptionType
from disnake.ext import commands

from utils import decorations

class Dictionary(commands.Cog, name="dictionary"):
    def __init__(self, bot):
        self.bot = bot
        self.f = "refined_words.txt"
        self.uf = "words.txt"

    @commands.slash_command(
        name="word",
        description="Pull a random, unrefined word.",
    )
    async def word(self, interaction):
        l1 = []
        with open(self.uf, 'r', encoding="utf-8") as f:
            l1 = f.readlines()
            flen = len(l1)
            line = l1[random.randint(0,flen)]
            line = line.split(": ")[0]
        await interaction.send(line)

    @commands.slash_command(
        name="worddelete",
        description="Pull a random, unrefined word, then delete it.",
    )
    @decorations.is_owner()
    async def worddelete(self, interaction):
        l1 = []
        with open(self.uf, 'r', encoding="utf-8") as f:
            l1 = f.readlines()
            flen = len(l1)
            linen = random.randint(0,flen)
            line = l1[linen]
            line = line.split(": ")[0]
        with open(self.uf, 'w', encoding="utf-8") as fp:
            for number, l in enumerate(l1):
                if number != linen:
                    fp.write(l)
        await interaction.send(f"{line} : {linen}")


    @commands.slash_command(
        name="getword",
        description="Search an English word's translation, or vice versa.",
        options=[
            Option(
                name="word",
                description="The word to search for.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="e_or_t",
                description="English or Tšernoian. (Input 'E' or 'T'.)",
                type=OptionType.string,
                required=True
            )
        ],
    )
    async def getword(self, interaction):
        i = interaction.options
        word = i['word'].lower()
        eort = i['e_or_t'].lower()
        with open(self.f, 'r', encoding="utf-8") as f:
            definition = ""
            if eort == "e":
                for line in f:
                    linearr = line.split(" - ")
                    if word == linearr[1]:
                        definition = line
            elif eort == "t":
                for line in f:
                    linearr = line.split(" - ")
                    if word == linearr[0]:
                        definition = line
            else:
                await interaction.send("Please select 'E' or 'T' for the second option.")
            
            if definition == "":
                await interaction.send(f"'{word}' not found.")
            else:
                await interaction.send(definition)


    @commands.slash_command(
        name="addword",
        description="Add a word into the dictionary.",
        options=[
            Option(
                name="word",
                description="The Tšernoian word to add to the dictionary.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="translation",
                description="The English equivalent.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="pos",
                description="Part of speech.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @decorations.is_owner()
    async def addword(self, interaction):
        i = interaction.options
        word = i['word']
        translation = i['translation']
        pos = i['pos']
        f = open(self.f, 'r', encoding="utf-8")
        for line in f:
            line = line.strip('\n')
            if word in line.split(' ') and translation in line.split(' '):
                await interaction.send(f"The Tšernoian word `{word}` and the English translation `{translation}` was found in `{line}`")
                return
            elif word in line.split(' '):
                await interaction.send(f"The Tšernoian word `{word}` was found in `{line}`")
                return
            elif translation in line.split(' '):
                await interaction.send(f"The English translation `{translation}` was found in `{line}`")
                return
        f.close()

        f = open(self.f, 'a', encoding="utf-8")
        f.write(f"{word} - {translation} - {pos}\n")
        f.close()

        await interaction.send(f"Successfully added the Tšernoian word `{word}` as `{translation}` with the function `{pos}` to the dictionary.")

def setup(bot):
    bot.add_cog(Dictionary(bot))
