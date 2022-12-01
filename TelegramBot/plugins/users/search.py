from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TelegramBot.config import *
from datetime import datetime
import requests as r
import os
import requests
prefixes = COMMAND_PREFIXES
commands = ["search", f"search@{BOT_USERNAME}"]

@Client.on_message(filters.command(commands, **prefixes))
async def search(_, message: Message):
    # search for the query
    if len(message.command) == 1:
        await message.reply_text("Please provide a query!")
        return
    query = message.text.split(None, 1)[1]
    # fetch the json
    url = f"https://nhentai.net/api/galleries/search?query={query}"
    r = requests.get(url)
    if r.status_code != 200:
        await message.reply_text("Please provide a valid query!")
        return
    # get the json
    json = r.json()
    # paginate the results
    data = requests.get(url).json()
    results = data["result"]
    i = 0
    text = ""
    while i < 5:
        try:
            text += f"""
**Title:** {results[i]["title"]["english"]}
**ID:** {results[i]["id"]}
**Pages:** {results[i]["num_pages"]}
**Link:** https://nhentai.net/g/{results[i]["id"]}
"""
            i += 1
        
        except IndexError:
            break
    # button for each result
    buttons = []
    for i in range(5):
        try:
            buttons.append([InlineKeyboardButton(text=f"{results[i]['title']['english']}", callback_data=f"kode_{results[i]['id']}")])
        except IndexError:
            break
    # send the results
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    # send the results

        
    