from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Producto, db
from app.saga import SagaEvent, SagaState

def manejar_evento_reservar_inventario(compra_id, producto_id, cantidad):
    try:
        producto = Producto.query.get(producto_id)
        if producto and producto.stock >= cantidad:
            producto.stock -= cantidad
            db.session.commit()

            # Emitir evento para procesar el pago
            emitir_evento(SagaEvent.PROCESS_PAYMENT, compra_id)
            return {"status": "success"}
        else:
            # Emitir evento para cancelar la orden
            emitir_evento(SagaEvent.CANCEL_ORDER, compra_id)
            return {"status": "error", "message": "Stock insuficiente"}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al reservar inventario: {e}")
        db.session.rollback()
        return {"status": "error", "message": "Error al reservar inventario"}

def emitir_evento(evento, compra_id):
    # Emitir evento (puedes usar una cola de mensajes como RabbitMQ o Kafka)
    current_app.logger.info(f"Emitir evento {evento} para la compra {compra_id}")
