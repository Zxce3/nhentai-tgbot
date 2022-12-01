from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
# import InlineKeyboardMarkup from pyrogram.types import InlineKeyboardMarkup
from TelegramBot.config import *
from datetime import datetime
import requests as r
import os
import requests
prefixes = COMMAND_PREFIXES
commands = ["kode", f"kode@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
async def kode(_, message: Message):
    # fetch the number from nhentai
    if len(message.command) == 1:
        await message.reply_text("Please provide a number!")
        return
    number = message.command[1]
    if not number.isdigit():
        await message.reply_text("Please provide a valid number!")
        return
    # fetch the json
    url = f"https://nhentai.net/api/gallery/{number}"
    r = requests.get(url)
    if r.status_code != 200:
        await message.reply_text("Please provide a valid number!")
        return
    # get the json
    json = r.json()
    # get the title
    title = json["title"]["english"]
    jtitle = json["title"]["japanese"]
    ptitles = json["title"]["pretty"]
    # if the title is None, use the japanese title or the pretty title
    if title is None:
        if jtitle is None:
            title = ptitles
        else:
            title = jtitle
    # get tags
    tags = json["tags"]
    # get pages
    pages = json["images"]["pages"]
    # get cover
    cover = json["images"]["cover"]["t"]
    # get thumbnail
    thumbnail = json["images"]["thumbnail"]["t"]
    # get number of pages
    num_pages = json["num_pages"]
    # get upload date
    upload_date = json["upload_date"]
    # parse the date
    date = datetime.fromtimestamp(upload_date)
    # get scanlator
    scanlator = json["scanlator"]
    # get link
    link = f"https://nhentai.net/g/{number}"
    # get media id
    media_id = json["media_id"]
    # get favorites
    favorites = json["num_favorites"]
    # get id
    id = json["id"]
    # get images
    images = []
    for page in pages:
        images.append(page["t"])
    # get tags
    tags = []
    for tag in tags:
        tags.append(tag["name"])
    # parse the tags
    tags = ", ".join(tags)
    # get the text
    text = f"""
**Title:** `{title}`
**Number of pages:** `{num_pages}`
**Upload date:** `{date}`
**Scanlator:** `{scanlator}`
**Link:** `{link}`
**Media id:** `{media_id}`
**Favorites:** `{favorites}`
**Id:** `{id}`
**Tags:** `{tags}`
"""
    cover = f"https://t.nhentai.net/galleries/{media_id}/cover.jpg"
    # if cover .jpg not found then use .png
    if requests.get(cover).status_code != 200:
        cover = f"https://t.nhentai.net/galleries/{media_id}/cover.png"
    # download and save the cover
    cover = requests.get(cover) # get the cover
    with open(f"{number}.jpg", "wb") as file: # save the cover
        file.write(cover.content)
    # send the message
    await message.reply_photo(
        photo=f"{number}.jpg",
        caption=text,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Read", url=link)]
            ]
        )
    )
    # then delete the cover from the server
    os.remove(f"{number}.jpg")