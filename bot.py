#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import configparser
import PIL
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
from PIL import ImageFont, Image, ImageDraw
from uuid import uuid4
import subprocess
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

config = configparser.ConfigParser()
config.read('bot.ini')
updater = Updater(token=config['KEYS']['bot_api'])
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
        bot.sendMessage(chat_id=update.message.chat_id,text="Welcome home, Master. This shell is at your disposal.")

def memegen(topString, bottomString, filename):
    filename = "./images/" + filename
    img = Image.open(filename)
    imageSize = img.size
    fontSize = int(imageSize[1]/5)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
            fontSize = fontSize - 1
            #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
            font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", fontSize)
            topTextSize = font.getsize(topString)
            bottomTextSize = font.getsize(bottomString)
    topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)
    bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = ImageDraw.Draw(img)
    outlineRange = int(fontSize/15)
    #for x in range(-outlineRange, outlineRange+1):
    #        for y in range(-outlineRange, outlineRange+1):
    #                draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString.upper(), (0,0,0), font=font)
    #                draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString.upper(), (0,0,0), font=font)
    draw.text(topTextPosition, topString, (255,255,255), font=font)
    draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)
    img.save("./images/temp.png")
    return True

def memegen_tg(bot, update, direct=True):
    bot.send_chat_action(update.message.chat_id, ChatAction.UPLOAD_PHOTO)
    file_id = update.message.photo[-1]
    caption = update.message.caption.split(',')
    newImage = bot.get_file(file_id)
    newImage.download('./images/upload.png')
    memegen(caption[0],caption[1], "upload.png")
    #the above function writes the image with a new filename "temp.png"
    bot.send_photo(chat_id=update.message.chat_id, photo=open('images/temp.png', 'rb'), caption="Tomah", parse_mode="Markdown")
    return True

def inlinequery(bot, update):
    query = update.inline_query.query
    o = execute(query, update, direct=False)
    results = list()
    results.append(InlineQueryResultArticle(id=uuid4(),title=query,description=o,input_message_content=InputTextMessageContent('*{0}*\n\n{1}'.format(query, o), parse_mode="Markdown")))
    bot.answerInlineQuery(update.inline_query.id, results=results, cache_time=10)

def execute(bot, update, direct=True):
    print("Main")
        
    user_id = update.message.from_user.id
    inline = False

    if user_id == int(config['ADMIN']['id']) and update.message.text[0] == "!":
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        output = subprocess.Popen(update.message.text[1:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)
        bot.sendMessage(chat_id=update.message.chat_id, text=output, parse_mode="Markdown")
        return True

start_handler = CommandHandler('start', start)
execute_handler = MessageHandler(Filters.text, execute)
memegen_handler = MessageHandler(Filters.photo & (~ Filters.forwarded), memegen_tg)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(execute_handler)
dispatcher.add_handler(memegen_handler)
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_error_handler(error)
updater.start_polling()
updater.idle()
