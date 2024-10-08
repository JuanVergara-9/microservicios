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

    return {"status": "success", "compra": nueva_compra}
