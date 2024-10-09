from app.models import Pago, db

def registrar_pago(usuario_id, monto, metodo_pago):
    nuevo_pago = Pago(usuario_id=usuario_id, monto=monto, metodo_pago=metodo_pago)
    db.session.add(nuevo_pago)
    db.session.commit()  # Guardamos el pago en la base de datos
    return {"status": "success", "pago": nuevo_pago}

def actualizar_estado_pago(pago_id, estado):
    pago = Pago.query.get(pago_id)
    if pago:
        pago.estado = estado
        db.session.commit()  # Actualizamos el estado del pago en la base de datos
        return {"status": "success", "pago": pago}
    else:
        return {"status": "error", "message": "Pago no encontrado"}
