from pymongo import MongoClient
import os

def get_db_handle(db_name, host, port, username, password):

    client = MongoClient(   
                            host=os.getenv('MONGODB_URI'),
                            port=int(port),
                        )
    db_handle = client['db_name']
    return db_handle, client