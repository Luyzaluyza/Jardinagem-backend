from flask import Blueprint
from app.controllers.user_controller import register_user, get_users, get_user, update_user, delete_user

routes = Blueprint('routes', __name__)

routes.route('/api/register_user', methods=['POST'])(register_user)
routes.route('/api/users', methods=['GET'])(get_users)
routes.route('/api/user/<email>', methods=['GET'])(get_user)
routes.route('/api/users/<user_id>', methods=['PUT'])(update_user)
routes.route('/api/users/<user_id>', methods=['DELETE'])(delete_user)
