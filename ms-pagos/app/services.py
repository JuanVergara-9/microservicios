import random

def procesar_pago(datos_pago):
    # Verifica que los datos de pago sean válidos
    if 'usuario_id' not in datos_pago or 'monto' not in datos_pago:
        return {"status": "error", "message": "Datos incompletos"}

    # Simulación de procesamiento de pago
    metodo_pago = datos_pago.get('metodo_pago', 'tarjeta')

    # Simulamos un error aleatorio en el proceso de pago
    if random.choice([True, False]):
        return {"status": "error", "message": "Error en el procesamiento del pago"}

    # Aquí se podría integrar un sistema real de pagos, como Stripe, PayPal, etc.
    return {"status": "success", "monto": datos_pago['monto'], "metodo_pago": metodo_pago}
