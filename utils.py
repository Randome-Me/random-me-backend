from pymongo import MongoClient
import os

def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host=host,
                      port=int(port) | os.environ.get('DATABASE_PORT'),
                      username=username,
                      password=password
                     )
 db_handle = client['db_name']
 return db_handle, client