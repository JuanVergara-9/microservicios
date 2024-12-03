from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Producto, db
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
def aumentar_stock(producto_id, cantidad):
    try:
        producto = Producto.query.get(producto_id)
        if producto:
            producto.stock += cantidad  # Aumentamos el stock
            db.session.commit()
            return {"status": "success", "producto": producto}
        else:
            return {"status": "error", "message": "Producto no encontrado"}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al aumentar el stock: {e}")
        db.session.rollback()
        return {"status": "error", "message": str(e)}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
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
