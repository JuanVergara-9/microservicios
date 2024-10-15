from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Compra, db

from app.models import Producto, db

def obtener_todos_los_productos():
    # Retorna todos los productos de la base de datos
    return Producto.query.all()

def obtener_producto_por_id(producto_id):
    # Retorna un producto por su ID
    return Producto.query.get(producto_id)

def agregar_producto(nombre, descripcion, precio, stock):
    # Agrega un nuevo producto al catálogo
    nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
    db.session.add(nuevo_producto)
    db.session.commit()

    return nuevo_producto

def registrar_compra(datos_compra):
    from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.models import Compra, db

def registrar_compra(datos_compra):
    # Verifica que los datos sean válidos
    required_fields = ['producto_id', 'usuario_id']
    for field in required_fields:
        if field not in datos_compra:
            return {"status": "error", "message": f"Falta el campo requerido: {field}"}

    try:
        nueva_compra = Compra(
            producto_id=datos_compra['producto_id'],
            usuario_id=datos_compra['usuario_id'],
            cantidad=datos_compra.get('cantidad', 1)
        )
        db.session.add(nueva_compra)
        db.session.commit()
        return {"status": "success", "compra": nueva_compra.to_dict()}
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error al registrar la compra: {e}")
        db.session.rollback()
        return {"status": "error", "message": "Error al registrar la compra"}
