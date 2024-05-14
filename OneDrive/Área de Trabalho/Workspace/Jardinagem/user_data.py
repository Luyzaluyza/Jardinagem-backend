from database import db
from datetime import datetime

def insert_user_data(telefone, api_key, planta_id):
    user_collection = db.users
    user_collection.insert_one({
        "telefone": telefone,
        "api_key": api_key,
        "planta_id": planta_id,
        "data_hora": datetime.now()
    })
