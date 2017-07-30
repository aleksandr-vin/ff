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
    filename = "foo.jpg"
    with PiCamera() as camera:
        camera.resolution = (3280, 2464)
        logger.info("Warming up camera...")
        # Camera warm-up time
        sleep(2)
        logger.info("Capturing picture to file")
        camera.capture(filename)
    logger.info("Reading file")
    file = open(filename, 'rb')
    logger.info("Sending pic")
    res = update.message.reply_photo(photo = file)
    logger.debug("result {}".format(res))

def video(bot, update):
    logger.debug("got {}".format(update))
    filename = "foo.mjpeg"
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        logger.info("Warming up camera...")
        # Camera warm-up time
        sleep(2)
        logger.info("Capturing video to file")
        camera.start_recording(filename)
        camera.wait_recording(10)
        camera.stop_recording()
    logger.info("Reading file")
    file = open(filename, 'rb')
    logger.info("Sending video")
    res = update.message.reply_video(video = file)
    logger.debug("result {}".format(res))

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
updater = Updater(TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pic', pic))
updater.dispatcher.add_handler(CommandHandler('video', video))

logger.info("Ready to start polling")
updater.start_polling()
logger.info("Going idle")
updater.idle()
