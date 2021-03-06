#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import logging
import time
from uuid import uuid4

from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from urlextract import URLExtract as extr

import dbutils
import execute
import memegen
import piazzolla

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
    else:
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id, text="Welcome home, Master. This shell is at your disposal.")


def memegen_tg(bot, update, direct=True):
    bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
    file_id = update.message.photo[-1]
    newImage = bot.get_file(file_id)
    newImage.download('./images/upload.png')
    if update.message.caption.find("SAVE"):
        save = True
        ncaption = {x.replace('SAVE', '').strip() for x in update.message.caption}
        templateName = ', '.join(ncaption).lower().replace(" ", "_")
        memegen.saveTemplate(templateName, "upload.png", update.message.from_user, dbfile)
    else:
        save = False
        caption = update.message.caption.split(',,')
        memegen.craft(caption, "upload.png")
        bot.send_photo(chat_id=update.message.chat_id, photo=open('images/temp.png', 'rb'), caption="Alan!",
                       parse_mode="Markdown")
        return True


def piazzollink_tg(bot, update, direct=True):
    ytlink = extr.find_urls(update.message)
    if ytlink is None:
        bot.sendMessage(chat_id=update.message.chat_id, text="Alan saving song. Something's wrong.")
    else:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if dbutils.addsong(ytlink, update.message.from_user.id):
            bot.sendMessage(chat_id=update.message.chat_id, text="Alan. Thanks for the link <3")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Alan saving link. Something's wrong.")


def piazzolla_tg(bot, update, direct=True):
    ytlink = extr.find_urls(update.message)
    if ytlink is None:
        if update.message.text.startswith("Tango"):
            piazzolla.tango(bot, update, dbfile)
        elif update.message.text.startswith("Meme"):
            memegen.meme(bot, update, dbfile)
    else:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if dbutils.addsong(ytlink, update.message.from_user.id):
            bot.sendMessage(chat_id=update.message.chat_id, text="Alan. Thanks for the link <3")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Alan saving link. Something's wrong.")


def inlinequery(bot, update):
    query = update.inline_query.query
    o = execute.bash(query, update, direct=False)
    results = list()
    results.append(InlineQueryResultArticle(id=uuid4(), title=query, description=o,
                                            input_message_content=InputTextMessageContent(
                                                '*{0}*\n\n{1}'.format(query, o), parse_mode="Markdown")))
    bot.answerInlineQuery(update.inline_query.id, results=results, cache_time=10)


if dbutils.check_file(dbfile) and dbutils.check_tables(dbfile):
    print('DB Alan and ready')
    pass
else:
    print('Something is Alan with the DB')
    pass

start_handler = CommandHandler('start', start)
execute_handler = MessageHandler(Filters.regex(r'^!'), execute.bash)
memegen_handler = MessageHandler(Filters.photo & (~ Filters.forwarded), memegen_tg)
# URLRegex = '^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
piazzollink_handler = MessageHandler(Filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'), piazzollink_tg)
piazzolla_handler = MessageHandler(Filters.text, piazzolla_tg)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(execute_handler)
dispatcher.add_handler(memegen_handler)
dispatcher.add_handler(piazzollink_tg)
dispatcher.add_handler(piazzolla_tg)
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_error_handler(error)
updater.start_polling()
updater.idle()
