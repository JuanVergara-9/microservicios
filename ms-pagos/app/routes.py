from flask import Blueprint, jsonify, request
from app import cache
from app.models import db, Pago
from app.services import procesar_pago

pagos_bp = Blueprint('pagos', __name__)

def obtener_todos_los_pagos():
    pagos = Pago.query.all()
    return [{"id": pago.id, "monto": pago.monto, "estado": pago.estado} for pago in pagos]

@pagos_bp.route('/pagos', methods=['POST'])
def realizar_pago():
    datos_pago = request.json
    resultado = procesar_pago(datos_pago)

    if resultado['status'] == 'success':
        # Invalidar el caché relevante si es necesario
        cache.delete('pagos')
        return jsonify({"message": "Pago procesado con éxito"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400

@pagos_bp.route('/pagos', methods=['GET'])
@cache.cached(timeout=60, key_prefix='pagos')
def obtener_pagos():
    return jsonify(obtener_todos_los_pagos())