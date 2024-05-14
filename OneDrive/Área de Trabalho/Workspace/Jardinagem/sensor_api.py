from flask import Flask, request, jsonify
import datetime
import requests
from database import db
from sensor_data import insert_sensor_data

app = Flask(__name__)

# Função para enviar mensagem no WhatsApp
def enviar_mensagem_whatsapp(telefone, api_key, mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?phone={telefone}&text={mensagem}&apikey={api_key}"
    response = requests.get(url)
    return response.status_code

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    planta_id = data.get('planta_id')
    temperatura = data.get('temperatura_ambiente')
    umidade_solo = data.get('umidade_solo')
    umidade_ar = data.get('umidade_ar')
    timestamp = data.get('timestamp')
    alerta = False
    rega = False

    user_collection = db.users
    user = user_collection.find_one({"planta_id": planta_id})
    
    if user:
        telefone = user.get('telefone')
        api_key = user.get('api_key')

        # Verifique se a umidade do solo é menor que 60 e envie uma mensagem se necessário
        if umidade_solo < 60:
            alerta = True
            enviar_mensagem_whatsapp(telefone, api_key, "Sua plantinha está com sede, regue-a o mais rápido possível.")
        elif umidade_solo >= 60:
            rega = True
            enviar_mensagem_whatsapp(telefone, api_key, "Muito obrigado por regar sua plantinha!")

    insert_sensor_data(planta_id, temperatura, umidade_solo, umidade_ar, alerta, rega)
    return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
