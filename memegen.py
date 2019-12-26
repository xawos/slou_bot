from PIL import ImageFont, Image, ImageDraw
import dbutils


def craft(topString, bottomString, filename):
    filename = "./images/" + filename
    img = Image.open(filename)
    imageSize = img.size
    fontSize = int(imageSize[1] / 5)
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0] - 20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)
    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)
    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = ImageDraw.Draw(img)
    outlineRange = int(fontSize / 15)
    # for x in range(-outlineRange, outlineRange+1):
    #        for y in range(-outlineRange, outlineRange+1):
    #                draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString.upper(), (0,0,0), font=font)
    #                draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString.upper(), (0,0,0), font=font)
    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)
    img.save("./images/temp.png")
    return True


def saveTemplate(templateName, filename, user, dbfile):
    try:
        img = Image.open("./images/" + filename)
        if img.save("./images/templates/" + templateName + ".png") and dbutils.addMemeTemplate(img.filename, user):
            return True
        else:
            return False
    except Error as e:
        return False


def listmemes(bot, update, dbfile):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    try:
        memes = dbutils.select("SELECT * FROM memes", dbfile)
        nmemes = len(memes)
        bot.sendMessage(chat_id=update.message.chat_id, text="There's {} memes saved, here's the list:".format(nmemes))
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        for mim in memes:
            mylist = mim[0] + mim[1] + "\n"
        bot.sendMessage(chat_id=update.message.chat_id, text="".format(mylist))
    except Error as e:
        print(e)
        bot.sendMessage(chat_id=update.message.chat_id, text="".format(e))
        return False


def getmeme(bot, update, dbfile):
    # Expecting string in the form: "Meme curl 1337"
    memeid = update.message.text[10:]
    try:
        if memeid.isDigit():
            query = "SELECT * FROM memes WHERE ID={};".format(memeid)
            template = dbutils.selectOne(query, dbfile)
            filename = 'images/templates/'+template[1]+'.png'
            uploader = template[2]
            date = template[3]
            bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'), caption="\"filename\" by {}, ({})".format(uploader, date),
                           parse_mode="Markdown")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="ID requested is Alan")
    except Error as e:
        print(e)


def rmmeme(bot, update, dbfile):
    # Expecting string in the form: "Meme rm 1337"
    memeid = update.message.text[8:]
    try:
        if memeid.isDigit():
            query = "DELETE FROM memes WHERE ID={};".format(memeid)
            if dbutils.exec(query, dbfile):
                bot.sendMessage(chat_id=update.message.chat_id, text="Meme ID {} removed as requested by Alan.".format(memeid))
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="ID requested is Alan")
    except Error as e:
        print(e)


def helpmeme(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Meme + [ls, curl, rm] + optional ID")


def meme(bot, update, dbfile):
    try:
        memecmd = update.message.text()
        if memecmd.startswith("Meme ls"):
            listmemes(bot, update, dbfile)
        elif memecmd.startswith("Meme wget ") or memecmd.startswith("Meme curl "):
            getmeme(bot, update, dbfile)
        elif memecmd.startswith("Meme rm "):
            rmmeme(bot, update, dbfile)
        else:
            helpmeme(bot, update, )
    except Error as e:
        print(e)