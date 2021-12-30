from pymongo import MongoClient
import os

def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host=os.environ.get('DATABASE_HOST'),
                      port=int(port),
                      username=os.environ.get('DATABASE_USERNAME'),
                      password=os.environ.get('DATABASE_PASSWORD')
                     )
 db_handle = client['db_name']
 return db_handle, client