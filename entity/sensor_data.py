from database import db
from datetime import datetime

def insert_sensor_data(temperatura, umidade_solo, umidade_ar, alerta, rega):
    collection = db.sensor_data
    collection.insert_one({
        "temperatura_ambiente": temperatura,
        "umidade_solo": umidade_solo,
        "umidade_ar": umidade_ar,
        "alerta": alerta,
        "rega": rega,
        "data_hora": datetime.now()
    })
