from flask import Flask, request, jsonify
from user_data import insert_user_data

app = Flask(__name__)

@app.route('/api/register_user', methods=['POST'])
def register_user():
    data = request.json
    telefone = data.get('telefone')
    api_key = data.get('api_key')
    planta_id = data.get('planta_id')

    if not telefone or not api_key or not planta_id:
        return jsonify({"status": "error", "message": "Dados faltando"}), 400

    insert_user_data(telefone, api_key, planta_id)
    return jsonify({"status": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
