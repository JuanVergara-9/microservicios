def obtener_inventario():
    # Retorna el inventario completo (puedes conectar a base de datos si es necesario)
    return inventario

def actualizar_inventario(producto_id, cantidad):
    # Verifica si el producto existe en el inventario
    if producto_id not in inventario:
        return {"status": "error", "message": "Producto no encontrado"}

    # Verifica si hay suficiente stock
    stock_actual = inventario[producto_id]["stock"]
    if stock_actual + cantidad < 0:
        return {"status": "error", "message": "Stock insuficiente"}

    # Actualiza el stock
    inventario[producto_id]["stock"] += cantidad
    return {"status": "success", "producto_id": producto_id, "nuevo_stock": inventario[producto_id]["stock"]}
