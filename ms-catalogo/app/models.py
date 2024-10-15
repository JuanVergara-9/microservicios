from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "usuario_id": self.usuario_id,
            "cantidad": self.cantidad
        }
