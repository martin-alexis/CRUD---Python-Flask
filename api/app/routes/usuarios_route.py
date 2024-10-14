from flask import Blueprint, request
from api.app.controllers.usuarios_controller import UsuariosController


usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['POST'])
def insert_usuario():
    username = request.json['username']
    password = request.json['password']

    controller = UsuariosController()
    return controller.insert_usuarios(username, password)
