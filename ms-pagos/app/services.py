from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Pago, db
from app.saga import SagaEvent, SagaState


def registrar_pago(usuario_id, monto, metodo_pago):
    nuevo_pago = Pago(usuario_id=usuario_id, monto=monto, metodo_pago=metodo_pago)
    db.session.add(nuevo_pago)
    db.session.commit()  # Guardamos el pago en la base de datos
    return {"status": "success", "pago": nuevo_pago}

def actualizar_estado_pago(pago_id, estado):
    pago = Pago.query.get(pago_id)
    if pago:
        pago.estado = estado
        db.session.commit()  # Actualizamos el estado del pago en la base de datos
        return {"status": "success", "pago": pago}
    else:
        return {"status": "error", "message": "Pago no encontrado"}

def manejar_evento_procesar_pago(compra_id, usuario_id, monto, metodo_pago):
    try:
        nuevo_pago = Pago(usuario_id=usuario_id, monto=monto, metodo_pago=metodo_pago)
        db.session.add(nuevo_pago)
        db.session.commit()

        # Emitir evento para completar la orden
        emitir_evento(SagaEvent.COMPLETE_ORDER, compra_id)
        return {"status": "success"}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al procesar el pago: {e}")
        db.session.rollback()
        return {"status": "error", "message": "Error al procesar el pago"}

def emitir_evento(evento, compra_id):
    # Emitir evento (puedes usar una cola de mensajes como RabbitMQ o Kafka)
    current_app.logger.info(f"Emitir evento {evento} para la compra {compra_id}")
