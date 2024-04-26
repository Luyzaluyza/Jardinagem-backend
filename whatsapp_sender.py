from flask import Flask, request, jsonify
import requests
from entity.sensor_data import insert_sensor_data, setup_database

app = Flask(__name__)

@app.route('/register_sensor_data', methods=['POST'])
def register_sensor_data():
    data = request.get_json()
    temperatura = data['temperatura_ambiente']
    umidade_solo = data['umidade_solo']
    umidade_ar = data['umidade_ar']
    alerta = data['alerta'] if 'alerta' in data else False
    rega = data['rega'] if 'rega' in data else False

    if umidade_solo < 60:
        alerta = True
        enviar_mensagem_whatsapp(data['telefone'], data['api_key'], "Sua plantinha está com sede, regue-a o mais rápido possível.")

    insert_sensor_data(temperatura, umidade_solo, umidade_ar, alerta, rega)
    return jsonify({"status": "Dados de sensor registrados com sucesso", "alerta": alerta}), 201

def enviar_mensagem_whatsapp(telefone, api_key, mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?phone={telefone}&text={mensagem}&apikey={api_key}"
    response = requests.get(url)
    return response.status_code

if __name__ == '__main__':
    setup_database()  
    app.run(debug=True, port=5001)
