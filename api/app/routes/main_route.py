from flask import Blueprint, render_template
from app.controllers.personas_controller import PersonasController

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def main():
    controller = PersonasController()

    # Obtiene la respuesta del controlador (devuelve un objeto Response)
    response = controller.get_personas()

    # Extrae el JSON de la respuesta
    personas_data = response[0].get_json()  # Esto debería ser una lista de diccionarios

    # Ahora pasa los datos deserializados a la plantilla
    return render_template('crud.html', data=personas_data)


