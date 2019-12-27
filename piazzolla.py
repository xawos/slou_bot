import dbutils
import re


def listsongs(bot, update, dbfile):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    try:
        songs = dbutils.select("SELECT * FROM songs", dbfile)
        nsongs = len(songs)
        bot.sendMessage(chat_id=update.message.chat_id, text="There's {} songs saved, here's the list:".format(nsongs))
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        for mim in songs:
            mylist = mim[0] + mim[1] + "\n"
        bot.sendMessage(chat_id=update.message.chat_id, text="".format(mylist))
    except Error as e:
        print(e)
        bot.sendMessage(chat_id=update.message.chat_id, text="".format(e))
        return False


def gettango(bot, update, dbfile):
    # Expecting string in the form: "Tango curl 1337"
    mail = update.message.text[11:]
    try:
        if mail.isdigit():
            bot.sendMessage(chat_id=update.message.chat_id, text="Alan! Not implemented yet! Only full list for now :)")
        else
            query = "SELECT * FROM songs;"
            tangolist = dbutils.select(query, dbfile)
            with open("./wubbalubbadubdub.csv", "wb") as tangofile:
                for row in tangolist:
                    wrow = " ".join(row)
                    tangofile.write(wrow)
            bot.send_document(chat_id=update.message.chat_id, document=open('./wubbalubbadubdub.csv', 'rb'))
    except Error as e:
        print(e)
        bot.sendMessage(chat_id=update.message.chat_id, text="Action requested is Alan \n{}".format(e))


def rmtango(bot, update, dbfile):
    # Expecting string in the form: "Tango rm 1337"
    songid = update.message.text[9:]
    try:
        if songid.isDigit():
            query = "DELETE FROM songs WHERE ID={};".format(songid)
            if dbutils.exec(query, dbfile):
                bot.sendMessage(chat_id=update.message.chat_id, text="Song ID {} removed as requested by Alan.".format(songid))
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="ID requested is Alan")
    except Error as e:
        print(e)


def helptango(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Tango + [ls, curl, rm] + optional ID")


def tango(bot, update, dbfile):
    try:
        tangocmd = update.message.text()
        if tangocmd.startswith("Tango ls"):
            listsongs(bot, update, dbfile)
        elif tangocmd.startswith("Tango wget ") or tangocmd.startswith("Tango curl "):
            gettango(bot, update, dbfile)
        elif tangocmd.startswith("Tango rm "):
            rmtango(bot, update, dbfile)
        else:
            helptango(bot, update, )
    except Error as e:
        print(e)