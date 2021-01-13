from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import json
import discord
import utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author.bot: # ignore messages from bots
        return

    if message.channel.name == 'stock-news' and message.content.startswith('$'):
        rtn_message = utils.handle_message(message)

        if rtn_message == 'post_graph':
            await message.channel.send(file=discord.File('shot.png'))
        else:
            if rtn_message:
                if len(rtn_message) >= 2000:
                    split_strings = rtn_message.split("52WeekHigh")
                    second_half = split_strings[1]
                    split_strings[1] = '52WeekHigh' + second_half

                    for sub_string in split_strings:
                        if len(sub_string) >= 2000:
                            n = 1990
                            split_strings = [sub_string[index : index + n] for index in range(0, len(sub_string), n)]
                            for sub_string2 in split_strings:
                                await message.channel.send(utils.code_embed(sub_string))
                        await message.channel.send(utils.code_embed(sub_string))
                    
                else:
                    await message.channel.send(utils.code_embed(rtn_message))
            else: 
                await message.channel.send('Command not recognized')

client.run(TOKEN)