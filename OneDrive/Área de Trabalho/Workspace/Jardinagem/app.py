from flask import Flask, request, jsonify
from pymongo import MongoClient
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
    data['timestamp'] = datetime.datetime.now()
    collection = db.sensor_data
    collection.insert_one(data)
    
    # Verifique se a umidade do solo é menor que 60 e envie uma mensagem se necessário
    if data['umidade_solo'] < 60:
        telefone = data.get('telefone')
        api_key = data.get('api_key')
        if telefone and api_key:
            enviar_mensagem_whatsapp(telefone, api_key, "Sua plantinha está com sede, regue-a o mais rápido possível.")
    
    return jsonify({"status": "success"}), 201

@app.route('/check_watered', methods=['POST'])
def check_watered():
    data = request.json
    telefone = data.get('telefone')
    api_key = data.get('api_key')

    if not telefone or not api_key:
        return jsonify({"status": "error", "message": "Telefone ou API Key faltando"}), 400

    # Verifique o último estado da umidade do solo
    collection = db.sensor_data
    last_entry = collection.find_one(sort=[("timestamp", -1)])
    if last_entry and last_entry.get('umidade_solo') >= 60:
        enviar_mensagem_whatsapp(telefone, api_key, "Muito obrigado por regar sua plantinha!")
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
