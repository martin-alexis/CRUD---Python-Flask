from flask import jsonify, Blueprint, request
from api.app.controllers.personas_controller import PersonasController
from api.app.utils.security import Security

personas_bp = Blueprint('personas', __name__)


@personas_bp.route('/personas', methods=['GET'])
def get_personas():
    has_access = Security.verify_token(request.headers)

    if has_access:
        controller = PersonasController()
        return controller.get_personas()
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@personas_bp.route('/personas', methods=['POST'])
def insert_personas():
    has_access = Security.verify_token(request.headers)

    if has_access:
        # Verifica si la solicitud tiene datos en formato JSON
        if request.is_json:
            data = request.get_json()
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            email = data.get('email')
        else:
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            email = request.form.get('email')

        controller = PersonasController()
        return controller.insert_personas(nombre, apellido, email)
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@personas_bp.route('/personas/<int:id_personas>', methods=['DELETE'])
def delete_persona(id_personas):
    has_access = Security.verify_token(request.headers)

    if has_access:
        controller = PersonasController()
        personas = controller.delete_personas(id_personas)
        return personas
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@personas_bp.route('/personas/<int:id_personas>', methods=['PATCH'])
def update_persona(id_personas):
    has_access = Security.verify_token(request.headers)

    if has_access:
        data = request.json
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')

        controller = PersonasController()
        return controller.update_persona(id_personas, nombre, apellido, email)

    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

