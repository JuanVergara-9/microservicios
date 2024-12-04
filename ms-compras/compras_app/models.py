from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Compra(db.Model):
    __tablename__ = 'compras'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    productos = db.Column(db.String, nullable=False)  

    def __repr__(self):
        return f"<Compra {self.id} de Usuario {self.usuario_id}>"
