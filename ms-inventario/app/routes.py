from flask import Blueprint, jsonify, request
from app import cache
from app.services import actualizar_inventario, obtener_inventario, manejar_evento_actualizar_inventario_con_circuit_breaker

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['GET'])
@cache.cached(timeout=60, key_prefix='inventario')
def obtener_productos():
    return jsonify(obtener_inventario())

@inventario_bp.route('/inventario/<int:producto_id>', methods=['POST'])
def actualizar_stock(producto_id):
    datos = request.json
    resultado = manejar_evento_actualizar_inventario_con_circuit_breaker(producto_id, datos['cantidad'])

    if resultado['status'] == 'success':
        # Invalidar el caché relevante
        cache.delete('inventario')
        return jsonify({"message": "Inventario actualizado"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400
