from telegram.ext import Updater
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

updater = Updater(token=config['APP']['TELEGRAM_TOKEN'], use_context=True)