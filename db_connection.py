import pymongo
import configparser
import ssl
import certifi

# config is used to extract remote mongo instance
config = configparser.ConfigParser()
config.read('config.ini')

mongo_client = pymongo.MongoClient(config['DATABASE']['URL'])
db = mongo_client.motiwaste_bot

