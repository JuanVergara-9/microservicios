from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Compra, db
from app.saga import SagaState, SagaEvent

compras = []  # Inicializamos la lista de compras

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
    # Emitir evento (puedes usar una cola de mensajes como RabbitMQ o Kafka)
    current_app.logger.info(f"Emitir evento {evento} para la compra {compra_id}")
