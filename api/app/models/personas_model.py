from app import db
from sqlalchemy import Column, Integer, String

class Personas(db.Model):
    __tablename__ = 'personas'

    id_personas = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    apellido = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)

    def __init__(self, nombre, apellido, email):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def to_dict(self):
        return {
            'id_personas': self.id_personas,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email
        }