from app import db  # Asegúrate de usar la instancia correcta
from app.models import Inventario
from flask import current_app
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

def obtener_inventario():
    # Implementación para obtener el inventario
    inventario = Inventario.query.all()
    return [item.to_dict() for item in inventario]

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def aumentar_stock(producto_id, cantidad):
    try:
        producto = Inventario.query.get(producto_id)
        if producto:
            producto.cantidad += cantidad  # Aumentamos el stock
            db.session.commit()
            return {"status": "success", "producto": producto}
        else:
            return {"status": "error", "message": "Producto no encontrado"}
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def manejar_evento_reservar_inventario(compra_id, producto_id, cantidad):
    # Implementación para manejar el evento de reservar inventario
    try:
        producto = Inventario.query.get(producto_id)
        if producto and producto.cantidad >= cantidad:
            producto.cantidad -= cantidad
            db.session.commit()
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Stock insuficiente o producto no encontrado"}
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}

def emitir_evento(evento, compra_id):
    # Emitir evento 
    current_app.logger.info(f"Emitir evento {evento} para la compra {compra_id}")