from flask import request, jsonify
from app.models.user_data import (
    insert_user_data, get_user_data, get_user_by_email, update_user_data, delete_user_data
)

def register_user():
    data = request.json
    telefone = data.get('telefone')
    api_key = data.get('api_key')
    planta_id = data.get('planta_id')
    email = data.get('email')
    senha = data.get('senha')
    nome = data.get('nome')

    if not telefone or not api_key or not planta_id or not email or not senha or not nome:
        return jsonify({"status": "error", "message": "Dados faltando"}), 400

    insert_user_data(telefone, api_key, planta_id, email, senha, nome)
    return jsonify({"status": "Usuario cadastrado"}), 201

def get_users():
    users = get_user_data()
    return jsonify(users), 200

def get_user(email):
    user = get_user_by_email(email)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"status": "error", "message": "Passe um email valido"}), 404

def update_user(user_id):
    data = request.json
    telefone = data.get('telefone')
    api_key = data.get('api_key')
    
    if not telefone and not api_key:
        return jsonify({"status": "error", "message": "Nenhum dado para atualizar"}), 400

    result = update_user_data(user_id, telefone, api_key)
    if result:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Falha"}), 400

def delete_user(user_id):
    result = delete_user_data(user_id)
    if result:
        return jsonify({"status": "usuario deletado"}), 200
    else:
        return jsonify({"status": "error", "message": "Falha"}), 400
