from dotenv import load_dotenv
import os
from pymongo import MongoClient
from .exceptions import ImpervaError

load_dotenv()

class DBClient:
    ''' Class which abstracts the connection to mongo db '''
    def db_client(self):
        mongo_uri = os.getenv("MONGO_URI", None)
        if mongo_uri == None:
            raise ImpervaError('Failed to get MONGO_URI env variable')
        return MongoClient(mongo_uri)
        