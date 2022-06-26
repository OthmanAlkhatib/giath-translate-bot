from telegram.ext import CommandHandler, Updater, CallbackContext
from telegram import Update
from googletrans import Translator
import os
import logging
import sys

TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if MODE == "dev":
    def run():
        logger.info("Start in DEV mode")
        updater.start_polling()
elif MODE == "prod":
    def run():
        logger.info("Start in PROD mode")
        updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), url_path=TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format("giath-translate-bot", TOKEN))
else:
    logger.error("No mode specified")
    sys.exit(1)

def voice_hanlder(update: Update, context: CallbackContext):
    try:
        text = update.message.text.split(" ", 1)
        comm = text[0]
        sentence = text[1].replace(" ", "+")
        if comm == "/say":
            url = "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q={0}".format(sentence)
        elif comm == "/kol":
            url = "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=ar&q={0}".format(sentence)
        update.message.bot.send_audio(update.message.chat_id, url)
    except Exception as error:
        update.message.reply_text("انقلع ذاكر")
        print(error)


def translate_hanlder(update: Update, context: CallbackContext):
    text = update.message.text.split(" ", 1)[1]
    translator = Translator()
    translation = translator.translate(text, dest="ar")
    update.message.reply_text(translation.text)


if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("say", voice_hanlder))
    updater.dispatcher.add_handler(CommandHandler("kol", voice_hanlder))
    updater.dispatcher.add_handler(CommandHandler("trans", translate_hanlder))

    run()