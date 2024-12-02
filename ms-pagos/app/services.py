from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Pago, db
from app.saga import SagaEvent, SagaState
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def registrar_pago(usuario_id, monto, metodo_pago):
    try:
        nuevo_pago = Pago(usuario_id=usuario_id, monto=monto, metodo_pago=metodo_pago)
        db.session.add(nuevo_pago)
        db.session.commit()  # Guardamos el pago en la base de datos
        return {"status": "success", "pago": nuevo_pago}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al registrar el pago: {e}")
        db.session.rollback()
        return {"status": "error", "message": str(e)}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def actualizar_estado_pago(pago_id, estado):
    try:
        pago = Pago.query.get(pago_id)
        if pago:
            pago.estado = estado
            db.session.commit()  # Actualizamos el estado del pago en la base de datos
            return {"status": "success", "pago": pago}
        else:
            return {"status": "error", "message": "Pago no encontrado"}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al actualizar el estado del pago: {e}")
        db.session.rollback()
        return {"status": "error", "message": str(e)}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
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
        return {"status": "error", "message": str(e)}

def emitir_evento(evento, data):
    # Implementar la lógica para emitir eventos
    current_app.logger.info(f"Evento emitido: {evento} con datos: {data}")

def obtener_todos_los_pagos():
    pagos = Pago.query.all()
    return [{"id": pago.id, "monto": pago.monto, "estado": pago.estado} for pago in pagos]