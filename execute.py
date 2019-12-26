import subprocess

def bash(bot, update, direct=True):
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