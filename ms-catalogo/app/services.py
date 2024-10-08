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
