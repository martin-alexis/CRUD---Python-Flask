from app.models.personas_model import Personas
from app import db
from flask import jsonify, url_for, redirect, request

class PersonasController:

    def __init__(self):
        pass


    def get_personas(self):
        try:
            # Obtiene todos los registros de la tabla Personas
            personas = Personas.query.all()

            # Si hay resultados, los convierte a un formato JSON serializable
            if personas:
                personas_list = [persona.to_dict() for persona in personas]

                # Verificar si la solicitud acepta JSON
                if request.is_json or request.accept_mimetypes['application/json']:
                    return jsonify(personas_list), 200  # Devuelve una lista de personas como JSON

                # Si no es una solicitud JSON, renderizar una página HTML con los datos
                return redirect(url_for('main.main'))

            # Devolver JSON si la solicitud lo requiere
            if request.is_json or request.accept_mimetypes['application/json']:
                return jsonify({'message': 'No hay registros en la base de datos.'}), 200

            return redirect(url_for('main.main'))
        except Exception as e:
            print(f'Error: {e}')

            if request.is_json or request.accept_mimetypes['application/json']:
                return jsonify({'error': 'Ocurrió un error al obtener las personas.'}), 500

            return redirect(url_for('main.main'))

    def insert_personas(self, nombre, apellido, email):
        try:
            # Verificar si alguno de los campos está vacío
            if not nombre or not apellido or not email:
                return jsonify({'message': 'Todos los campos son obligatorios'}), 400

            # Verificar si el email ya está registrado
            existing_persona = Personas.query.filter_by(email=email).first()

            if existing_persona:
                return jsonify({'message': 'Email ya registrado'}), 400

            nueva_persona = Personas(nombre=nombre, apellido=apellido, email=email)
            db.session.add(nueva_persona)
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'Persona insertada correctamente'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()


    def delete_personas(self, id_personas):
        try:
            # Buscar la persona por id
            persona = Personas.query.get(id_personas)

            # Comprobar si la persona existe
            if not persona:
                return jsonify({'status': 'error', 'message': 'Persona no encontrada'}), 404

            # Eliminar la persona
            db.session.delete(persona)
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'Persona eliminada correctamente'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'Error al eliminar la persona: {e}'}), 400

        finally:
            db.session.close()

    def update_persona(self, id_personas, nombre, apellido, email):
        try:
            persona = Personas.query.get(id_personas)

            if not persona:
                return jsonify({"error": "Persona no encontrada"}), 404

            # Obtener los datos del cuerpo de la solicitud en formato JSON
            data = request.json
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            email = data.get('email')

            # Verificar si el email ya está registrado por otra persona
            if email:
                existing_persona = Personas.query.filter(Personas.email == email, Personas.id_personas != id_personas).first()
                if existing_persona:
                    return jsonify({'error': 'El email ya está registrado'}), 400

            # Actualizar solo los campos proporcionados
            if nombre:
                persona.nombre = nombre
            if apellido:
                persona.apellido = apellido
            if email:
                persona.email = email

            # Guardar cambios en la base de datos
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el registro: {e}")
            return jsonify({"error": "Error al actualizar el registro"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Persona actualizada exitosamente"}), 200






