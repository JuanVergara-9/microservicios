from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)  # El ID del usuario que realiza el pago
    monto = db.Column(db.Float, nullable=False)  # Monto del pago
    metodo_pago = db.Column(db.String(50), nullable=False)  # Método de pago (e.g., tarjeta, PayPal, etc.)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # Estado del pago (e.g., pendiente, completado)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha y hora en que se realiza el pago

    def __repr__(self):
        return f"<Pago {self.id} de Usuario {self.usuario_id} - {self.estado}>"
