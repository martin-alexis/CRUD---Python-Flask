from app.models.usuarios_model import Usuarios
from app import db
from flask import jsonify
from werkzeug.security import check_password_hash


class UsuariosController:

    def __init__(self):
        pass

    def insert_usuarios(self, username, password):

        if not username or not password:
            return jsonify({"error": "Falta nombre de usuario o contraseña"}), 400

            # Verificar si el username ya está registrado
            existing_usuario = Personas.query.filter_by(username=username).first()

            if existing_usuario:
                return jsonify({'message': 'Usuario ya registrado'}), 400

        # Crear el usuario con la contraseña hasheada
        new_user = Usuarios(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario creado exitosamente!"}), 201

    @staticmethod
    def verify_user(username, password):
        # Busca el usuario en la base de datos por su nombre de usuario
        existing_usuario = Usuarios.query.filter_by(username=username).first()

        # Verifica si el usuario existe y si la contraseña coincide
        if existing_usuario and check_password_hash(existing_usuario.password, password):
            return existing_usuario
        else:
            return None  # Usuario no encontrado o contraseña incorrecta

