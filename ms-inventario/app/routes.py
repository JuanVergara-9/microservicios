from flask import Blueprint, jsonify, request
from app import cache
from app.services import manejar_evento_reservar_inventario, aumentar_stock, obtener_inventario

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['GET'])
@cache.cached(timeout=60, key_prefix='inventario')
def obtener_productos():
    return jsonify(obtener_inventario())

@inventario_bp.route('/inventario/<int:producto_id>', methods=['POST'])
def actualizar_stock(producto_id):
    datos = request.json
    resultado = aumentar_stock(producto_id, datos['cantidad'])

    if resultado['status'] == 'success':
        # Invalidar el caché relevante
        cache.delete('inventario')
        return jsonify({"message": "Inventario actualizado"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400

@inventario_bp.route('/reservar', methods=['POST'])
def reservar_inventario():
    datos = request.json
    compra_id = datos['compra_id']
    producto_id = datos['producto_id']
    cantidad = datos['cantidad']

    resultado = manejar_evento_reservar_inventario(compra_id, producto_id, cantidad)

    if resultado['status'] == 'success':
        # Invalidar el caché relevante
        cache.delete('inventario')
        return jsonify({"message": "Inventario reservado"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400
