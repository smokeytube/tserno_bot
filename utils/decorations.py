import json

from disnake.ext import commands


def is_owner():

    async def predicate(context: commands.Context) -> bool:
        with open("settings.json") as file:
            data = json.load(file)
        if context.author.id not in data["owners"]:
            return False
        return True

    return commands.check(predicate)