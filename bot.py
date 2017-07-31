import logging
import logging.config
import os
from time import sleep
from picamera import PiCamera
from telegram.ext import Updater, CommandHandler
from threading import Timer
import string
import random

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('bot')

jobs = {}

def rand_name():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))

def delayed_job(job_name, update):
    jobs[job_name] = Timer(5, delayed_job, [job_name, update])
    jobs[job_name].start()
    logger.debug("Restarted delayed job {}".format(job_name))

def list_jobs(bot, update):
    logger.debug("got {}".format(update))
    if len(jobs) > 0:
        jobs_list = "\n- ".join([""] + list(jobs.keys()))
        res = update.message.reply_text('Jobs running: {}'.format(jobs_list))
        logger.debug("result {}".format(res))
    else:
        res = update.message.reply_text('No jobs are running')
        logger.debug("result {}".format(res))
    
def start(bot, update):
    logger.debug("got {}".format(update))
    name = rand_name()
    jobs[name] = Timer(5, delayed_job, [name, update])
    jobs[name].start()
    logger.debug("Started delayed job {}".format(name))
    res = update.message.reply_text('Started job: {}'.format(name))
    logger.debug("result {}".format(res))

def stop(bot, update, args):
    logger.debug("got {}".format(update))
    logger.debug("jobs: {}".format(jobs))
    for arg in args:
        logger.debug("job: %s", arg)
        timer = jobs.get(arg)
        if timer:
            timer.cancel()
            del jobs[arg]
            res = update.message.reply_text('Job {} stopped'.format(arg))
            logger.debug("result {}".format(res))
        else:
            res = update.message.reply_text('Job {} not found'.format(arg))
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
updater.dispatcher.add_handler(CommandHandler('stop', stop, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('jobs', list_jobs))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('pic', pic))
updater.dispatcher.add_handler(CommandHandler('video', video))

logger.info("Ready to start polling")
updater.start_polling()
logger.info("Going idle")
updater.idle()
