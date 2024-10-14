from sqlalchemy import Column, Integer, String
from app import db
from werkzeug.security import generate_password_hash


class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id_usuarios = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    rol = Column(String(45), nullable=True)

    def __init__(self, username, password, rol="usuario"):
        self.username = username
        self.password = generate_password_hash(password)
        self.rol = rol

