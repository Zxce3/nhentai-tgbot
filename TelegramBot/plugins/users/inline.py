# inline search nhentai
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InlineQueryResultCachedPhoto, InputMediaPhoto
from TelegramBot.config import *
from datetime import datetime
import requests as r
import os
import requests

# inline search nhentai
@Client.on_inline_query()
async def inline_query_handler(client: Client, query: InlineQuery):
    # check if user already listed or not
    if query.query == "":
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    title="Nhentai",
                    input_message_content=InputTextMessageContent(
                        "Search nhentai"
                    ),
                    description="Search nhentai",
                    thumb_url="https://telegra.ph/file/69043a0dac3789fea967d.png",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Search", switch_inline_query_current_chat=""
                                )
                            ]
                        ]
                    ),
                )
            ],
            cache_time=0,
        )
    else:
        try:
            results = []
            search = query.query
            url = f"https://nhentai.net/api/galleries/search?query={search}"
            data = r.get(url).json()
            for i in data["result"]:
                code = i["id"]
                title = i["title"]["english"]
                media_id = i["media_id"]
                if title is None:
                    title = i["title"]["japanese"]
                if title is None:
                    title = i["title"]["pretty"]
                # parse the date
                date = datetime.fromtimestamp(i["upload_date"])
                # get scanlator
                scanlator = i["scanlator"]
                # get pages
                pages = i["num_pages"]
                url = f"https://nhentai.net/g/{code}/"
                thumb = f"https://t.nhentai.net/galleries/{media_id}/cover.jpg"
                # append the result with image and title
                results.append(
                    InlineQueryResultArticle(
                        title=title,
                        input_message_content=InputTextMessageContent(
                            f"**Title:** {title} \n**Code:** {code} \n**Date:** {date} \n**Scanlator:** {scanlator} \n**Link:** {url}"
                        ),
                        description=f"{code} | {pages} pages",
                        thumb_url=thumb,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("Read", url=url)],
                                # creat url to /kode {code}
                                [InlineKeyboardButton("Full Info", callback_data=f"kode_{code}")],
                                
                            ]
                        ),
                    )
                )
            await query.answer(
                results=results,
                cache_time=0,
            )
        except Exception as e:
            print(e)
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title="Error",
                        input_message_content=InputTextMessageContent(
                            f"Error: {e}"
                        ),
                        description="Error",
                        thumb_url="https://telegra.ph/file/69043a0dac3789fea967d.png",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Search", switch_inline_query_current_chat=""
                                    )
                                ]
                            ]
                        ),
                    )
                ],
                cache_time=0,
            )
# callback for kode_{number}
from TelegramBot import bot
@Client.on_callback_query(filters.regex(pattern=r"^kode_(.*)"))
async def kode_callback(_, query):
    # send message to user who request the callback
    # check if user is subscribed to bot
    
    # get user id
    user_id = query.from_user.id
    # get code
    code = query.matches[0].group(1)
    # get data
    url = f"https://nhentai.net/api/gallery/{code}"
    data = r.get(url).json()
    # get title
    title = data["title"]["english"]
    if title is None:
        title = data["title"]["japanese"]
    if title is None:
        title = data["title"]["pretty"]
    # get date
    date = datetime.fromtimestamp(data["upload_date"])
    # get scanlator
    scanlator = data["scanlator"]
    # get pages
    pages = data["num_pages"]
    # get tags
    tags = data["tags"]
    # parse tags
    tag = ""
    for i in tags:
        tag += f"{i['name']} ".join(i["name"])
    # get media id
    media_id = data["media_id"]
    # get images
    images = data["images"]
    # get url
    url = f"https://nhentai.net/g/{code}/"
    # get thumbnail
    thumb = f"https://t.nhentai.net/galleries/{media_id}/cover.jpg"
    caption = f"""
**Title:** {title}
**Code:** {code}
**Date:** {date}
**Scanlator:** {scanlator}
**Pages:** {pages}
**Link:** {url}
"""
    # send message to user with caption and image
    await bot.send_photo(
        chat_id=user_id,
        photo=thumb,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Read", url=url)],
                [InlineKeyboardButton("Read Now", callback_data=f"next_{code}_1")],
            ]
        ),
    )

# callback for back
@Client.on_callback_query(filters.regex(pattern=r"^back$"))
async def back_callback(_, query):
    # edit message
    await query.edit_message_text(
        text="Search nhentai",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Search", switch_inline_query_current_chat=""
                    )
                ]
            ]
        ),
    )
# callback for next_{code}_{number}
@Client.on_callback_query(filters.regex(pattern=r"^next_(.*)_(.*)"))
async def next_callback(_, query):
    # get code
    code = query.matches[0].group(1)
    # get number
    number = int(query.matches[0].group(2))
    # get data
    url = f"https://nhentai.net/api/gallery/{code}"
    data = r.get(url).json()
    # get title
    title = data["title"]["english"]
    if title is None:
        title = data["title"]["japanese"]
    if title is None:
        title = data["title"]["pretty"]
    # get date
    date = datetime.fromtimestamp(data["upload_date"])
    # get scanlator
    scanlator = data["scanlator"]
    # get pages
    pages = data["num_pages"]
    # get tags
    tags = data["tags"]
    # parse tags
    tag = ""
    for i in tags:
        tag += f"{i['name']} ".join(i["name"])
    # get media id
    media_id = data["media_id"]
    # get images
    images = data["images"]
    # get url
    url = f"https://nhentai.net/g/{code}/"
    # get thumbnail
    thumb = f"https://t.nhentai.net/galleries/{media_id}/cover.jpg"
    # get image
    image = f"https://i.nhentai.net/galleries/{media_id}/{number}.jpg"
    # if the image is not compitable
    if number > pages:
        image = thumb

    # get caption
    caption = f"""
**Title:** {title}
**Date:** {date}
**Pages:** {number} - {pages}
**Link:** {url}
"""
    # check if number is less than pages
    if number < pages:
        # send image
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=image,
                caption=caption,
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Read", url=url)],
                    [
                        InlineKeyboardButton("Prev", callback_data=f"prev_{code}_{number-1}"),
                        InlineKeyboardButton("Next", callback_data=f"next_{code}_{number+1}"),
                    ],
                ]
            ),
        )
    else:
        # send image
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=image,
                caption=caption,
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Read", url=url)],
                    [InlineKeyboardButton("Prev", callback_data=f"prev_{code}_{number-1}"),],
                ]
            ),
        )

# callback for prev_{code}_{number}
@Client.on_callback_query(filters.regex(pattern=r"^prev_(.*)_(.*)"))
async def prev_callback(_, query):
    # get code
    code = query.matches[0].group(1)
    # get number
    number = int(query.matches[0].group(2))
    # get data
    url = f"https://nhentai.net/api/gallery/{code}"
    data = r.get(url).json()
    # get title
    title = data["title"]["english"]
    if title is None:
        title = data["title"]["japanese"]
    if title is None:
        title = data["title"]["pretty"]
    # get date
    date = datetime.fromtimestamp(data["upload_date"])
    # get scanlator
    scanlator = data["scanlator"]
    # get pages
    pages = data["num_pages"]
    # get tags
    tags = data["tags"]
    # parse tags
    tag = ""
    for i in tags:
        tag += f"{i['name']} ".join(i["name"])
    # get media id
    media_id = data["media_id"]
    # get images
    images = data["images"]
    # get url
    url = f"https://nhentai.net/g/{code}/"
    # get thumbnail
    thumb = f"https://t.nhentai.net/galleries/{media_id}/cover.jpg"
    # get image
    image = f"https://i.nhentai.net/galleries/{media_id}/{number}.jpg"
    # get caption
    caption = f"""
**Title:** {title}
**Date:** {date}
**Pages:** {number} - {pages}
**Link:** {url}
"""
    # check if number is greater than 1
    if number > 1:
        # send image
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=image,
                caption=caption,
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Read", url=url)],
                    [
                        InlineKeyboardButton("Prev", callback_data=f"prev_{code}_{number-1}"),
                        InlineKeyboardButton("Next", callback_data=f"next_{code}_{number+1}"),
                    ],
                ]
            ),
        )
    else:
        # send image
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=image,
                caption=caption,
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Read", url=url)],
                    [InlineKeyboardButton("Next", callback_data=f"next_{code}_{number+1}"),]
                ]
            ),
        )

