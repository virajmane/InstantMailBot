import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Welcome to InstantMail Bot. \nHit /generate to get an email.\nOr use an existing/customized mail with the following domains '@wwjmp.com', '@1secmail.com', '@esiix.com' after /get_msg. \nExample: '/get_msg yourusername@esiix.com'")

def help_command(update, context):
    update.message.reply_text("Hit /generate to get an email.\nOr use an existing/customized mail with the following domains '@wwjmp.com', '@1secmail.com', '@esiix.com' along with /get_msg. \nExample: '/get_msg yourusername@esiix.com'")

def gen_command(update, context):
    r = requests.get("https://virajapi.herokuapp.com/mail/gen/").json()
    global email
    email = r["mail"]
    update.message.reply_text("Your instant mail is: " +email)

def get_msg(update, context):
    if len(update.message.text)>9:
        new = update.message.text[9:]
        url2 = requests.get(f"https://virajapi.herokuapp.com/mail/msg/?email={new}").json()
        if len(url2) == 0:
            update.message.reply_text("No Messages Yet")
        else:
            update.message.reply_text("Date: " +url2["msg1"]["date"]+"\n"+
                                      "From: " +url2["msg1"]["from"]+"\n"+
                                      "Subject: " +url2["msg1"]["subject"]+"\n"+
                                      "Message: " +url2["msg1"]["textBody"])
    elif email != None:
        url = requests.get(f"https://virajapi.herokuapp.com/mail/msg/?email={email}").json()
        if len(url) == 0:
            update.message.reply_text("No Messages Yet")
        else:
            update.message.reply_text("Date: " +url["msg1"]["date"]+"\n"+
                                      "From: " +url["msg1"]["from"]+"\n"+
                                      "Subject: " +url["msg1"]["subject"]+"\n"+
                                      "Message: " +url["msg1"]["textBody"])

def main():
    updater = Updater("1148611466:AAHO4vaKdJaEdTCLircNTChAK4cm6zQX7wI", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("generate", gen_command))
    dp.add_handler(CommandHandler("get_msg", get_msg))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
