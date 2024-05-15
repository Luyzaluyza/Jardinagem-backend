from flask import request, jsonify
from app.services.whatsapp_service import enviar_mensagem_whatsapp
from app.models.sensor_data import insert_sensor_data
from app import db

def receive_data():
    data = request.json
    planta_id = data.get('planta_id')
    temperatura = data.get('temperatura_ambiente')
    umidade_solo = data.get('umidade_solo')
    umidade_ar = data.get('umidade_ar')
    alerta = False
    rega = False

    user_collection = db.users
    user = user_collection.find_one({"planta_id": planta_id})

    if user:
        telefone = user.get('telefone')
        api_key = user.get('api_key')

        if umidade_solo < 60:
            alerta = True
            enviar_mensagem_whatsapp(telefone, api_key, "Sua plantinha está com sede, regue-a o mais rápido possível.")
        elif umidade_solo >= 60:
            rega = True
            enviar_mensagem_whatsapp(telefone, api_key, "Muito obrigado por regar sua plantinha!")

    insert_sensor_data(planta_id, temperatura, umidade_solo, umidade_ar, alerta, rega)
    return jsonify({"status": "success"}), 201
