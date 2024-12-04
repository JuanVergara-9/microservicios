from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from compras_app.models import Compra, db
from compras_app.saga import SagaState, SagaEvent, Saga
import time

compras = []  # Inicializamos la lista de compras

# Retry Decorator
def retry(retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
            raise last_exception
        return wrapper
    return decorator

@retry(retries=3, delay=2)
def registrar_compra(datos_compra):
    # Verifica que los datos sean válidos
    if 'producto_id' not in datos_compra or 'usuario_id' not in datos_compra:
        return {"status": "error", "message": "Datos incompletos"}

    # Simulación de guardar la compra en la base de datos o lista en memoria
    nueva_compra = {
        "producto_id": datos_compra['producto_id'],
        "usuario_id": datos_compra['usuario_id'],
        "cantidad": datos_compra.get('cantidad', 1),
    }
    compras.append(nueva_compra)

    # Iniciar la saga de compra
    try:
        nueva_compra_db = Compra(
            producto_id=datos_compra['producto_id'],
            usuario_id=datos_compra['usuario_id'],
            cantidad=datos_compra.get('cantidad', 1),
            estado=SagaState.PENDING
        )
        db.session.add(nueva_compra_db)
        db.session.commit()

        # Emitir evento para reservar inventario
        emitir_evento(SagaEvent.RESERVE_INVENTORY, nueva_compra_db.id)
        return {"status": "success", "compra": nueva_compra}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al iniciar la saga de compra: {e}")
        db.session.rollback()
        return {"status": "error", "message": "Error al iniciar la saga de compra"}

def emitir_evento(evento, compra_id):
    current_app.logger.info(f"Emitir evento {evento} para la compra {compra_id}")

# Ejemplo de implementación del patrón Circuit Breaker
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

# Ejemplo de uso del Circuit Breaker
circuit_breaker = CircuitBreaker(max_failures=3, reset_timeout=60)

def registrar_compra_con_circuit_breaker(datos_compra):
    return circuit_breaker.call(registrar_compra, datos_compra)