import json
import os
import sys

import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot


if not os.path.isfile("settings.json"):
    sys.exit("'settings.json' not found! Please add it and try again.")
else:
    with open("settings.json") as file:
        settings = json.load(file)

intents = disnake.Intents.default()

bot = Bot(command_prefix=commands.when_mentioned_or(settings["prefix"]), intents=intents, help_command=None)
bot.settings = settings


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

def load_commands(command_type):
    for f in os.listdir(f"./cogs/{command_type}"):
        if f.endswith(".py"):
            extension = f[:-3]
            bot.load_extension(f"cogs.{command_type}.{extension}")


if __name__ == "__main__":
    load_commands("slash")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)

bot.run(settings["token"])
