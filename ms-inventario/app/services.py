from app.models import Producto, db

def actualizar_stock(producto_id, cantidad):
    producto = Producto.query.get(producto_id)
    if producto and producto.stock >= cantidad:
        producto.stock -= cantidad  # Reducimos el stock
        db.session.commit()
        return {"status": "success", "producto": producto}
    else:
        return {"status": "error", "message": "Stock insuficiente o producto no encontrado"}

def aumentar_stock(producto_id, cantidad):
    producto = Producto.query.get(producto_id)
    if producto:
        producto.stock += cantidad  # Aumentamos el stock
        db.session.commit()
        return {"status": "success", "producto": producto}
    else:
        return {"status": "error", "message": "Producto no encontrado"}
