from flask import Blueprint, request, jsonify

from api.app.controllers.usuarios_controller import UsuariosController
from api.app.utils import security
from api.app.utils.security import Security

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/generate_token', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    authenticated_user = UsuariosController.verify_user(username, password)

    if (authenticated_user != None):
        if authenticated_user.rol == 'administrador':
            encoded_token = Security.generate_token(authenticated_user)
            return jsonify({'success': True, 'token': encoded_token})
        else:
            return jsonify({'message': 'Unauthorized: Solo administradores pueden generar tokens'}), 403
    else:
        return jsonify({'message': 'Unauthorized'}), 401
