#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import configparser
import sqlite3
import PIL
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
from PIL import ImageFont, Image, ImageDraw
from uuid import uuid4
import subprocess
from urlextract import URLExtract as extr
import time
import memegen
import execute
import dbutils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


config = configparser.ConfigParser()
config.read('bot.ini')
updater = Updater(token=config['KEYS']['bot_api'])
dbfile = Updater(token=config['FILES']['db'])
dispatcher = updater.dispatcher


def start(bot, update):
    if update.message.from_user.id != int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id, text="Welcome, guest!")
        bot.sendMessage(chat_id=update.message.chat_id, text=update.message.from_user.id)
    else:
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id, text="Welcome home, Master. This shell is at your disposal.")


def memegen_tg(bot, update, direct=True):
    bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
    file_id = update.message.photo[-1]
    caption = update.message.caption.split(',,')
    newImage = bot.get_file(file_id)
    newImage.download('./images/upload.png')
    memegen.craft(caption[0], caption[1], "upload.png")
    # the above function writes the image with a new filename "temp.png", we then get it and use it as "upload.png"
    bot.send_photo(chat_id=update.message.chat_id, photo=open('images/temp.png', 'rb'), caption="Tomah",
                   parse_mode="Markdown")
    return True


def piazzolla_tg(bot, update, direct=True):
    ytlink = extr.find_urls(update.message)
    if ytlink is None:
        pass
    else:
        dbutils.addsong(ytlink, update.message.from_user.id)


def inlinequery(bot, update):
    query = update.inline_query.query
    o = execute.bash(query, update, direct=False)
    results = list()
    results.append(InlineQueryResultArticle(id=uuid4(), title=query, description=o,
                                            input_message_content=InputTextMessageContent(
                                                '*{0}*\n\n{1}'.format(query, o), parse_mode="Markdown")))
    bot.answerInlineQuery(update.inline_query.id, results=results, cache_time=10)


if dbutils.check_file(dbfile) and dbutils.check_tables(dbfile):
    print('DB present and ready')
    pass
else:
    print('Something is wrong with the DB')
    pass


start_handler = CommandHandler('start', start)
execute_handler = MessageHandler(Filters.regex(r'^!'), execute.bash)
memegen_handler = MessageHandler(Filters.photo & (~ Filters.forwarded), memegen_tg)
# URLRegex = '^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
piazzolla_handler = MessageHandler(Filters.text ,piazzolla_tg)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(execute_handler)
dispatcher.add_handler(memegen_handler)
dispatcher.add_handler(piazzolla_tg)
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_error_handler(error)
updater.start_polling()
updater.idle()
