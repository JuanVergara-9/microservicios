from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Pago, db
from app.saga import SagaEvent, SagaState
from tenacity import retry, stop_after_attempt, wait_fixed
import time

class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=60):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.failures >= self.max_failures:
            if time.time() - self.last_failure_time < self.reset_timeout:
                raise Exception("Circuit breaker is open")
            else:
                self.failures = 0

        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            raise e
        
        
circuit_breaker = CircuitBreaker(max_failures=3, reset_timeout=60)

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
    
def registrar_pago_con_circuit_breaker(usuario_id, monto, metodo_pago):
    return circuit_breaker.call(registrar_pago, usuario_id, monto, metodo_pago)

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
    
def actualizar_estado_pago_con_circuit_breaker(pago_id, estado):
    return circuit_breaker.call(actualizar_estado_pago, pago_id, estado)

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
    

def manejar_evento_procesar_pago_con_circuit_breaker(compra_id, usuario_id, monto, metodo_pago):
    return circuit_breaker.call(manejar_evento_procesar_pago, compra_id, usuario_id, monto, metodo_pago)

def emitir_evento(evento, data):
    # Implementar la lógica para emitir eventos
    current_app.logger.info(f"Evento emitido: {evento} con datos: {data}")

def obtener_todos_los_pagos():
    pagos = Pago.query.all()
    return [{"id": pago.id, "monto": pago.monto, "estado": pago.estado} for pago in pagos]

