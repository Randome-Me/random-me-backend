from pymongo import MongoClient
import os

def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host=os.environ.get('DATABASE_HOST'),
                      port=int(port),
                      username=username,
                      password=password
                     )
 db_handle = client['db_name']
 return db_handle, client