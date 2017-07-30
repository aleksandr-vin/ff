import logging
import logging.config
import os
from time import sleep
from picamera import PiCamera
from telegram.ext import Updater, CommandHandler

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('bot')

def start(bot, update):
    logger.debug("got {}".format(update))
    res = update.message.reply_text('Hello World!')
    logger.debug("result {}".format(res))

def hello(bot, update):
    logger.debug("got {}".format(update))
    res = update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    logger.debug("result {}".format(res))

def pic(bot, update):
    logger.debug("got {}".format(update))
    camera = PiCamera()
    camera.resolution = (3280, 2464)
    logger.info("Warming up camera...")
    # Camera warm-up time
    sleep(2)
    logger.info("Capturing picture to file")
    camera.capture('foo.jpg')
    logger.info("Reading file")
    file = open('foo.jpg', 'rb')
    logger.info("Sending pic")
    res = update.message.reply_photo(photo = file)
    logger.debug("result {}".format(res))

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
updater = Updater(TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pic', pic))

logger.info("Ready to start polling")
updater.start_polling()
logger.info("Going idle")
updater.idle()
