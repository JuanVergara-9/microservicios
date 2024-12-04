from flask import Blueprint, jsonify, request
from app.services import obtener_inventario, aumentar_stock, manejar_evento_reservar_inventario
from app import cache

inventario_bp = Blueprint('inventario', __name__, url_prefix='/api/v1')

@inventario_bp.route('/inventario', methods=['GET'])
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
    compra_id = datos.get('compra_id')
    producto_id = datos.get('producto_id')
    cantidad = datos.get('cantidad')

    if not compra_id or not producto_id or not cantidad:
        return jsonify({"error": "Datos incompletos"}), 400

    resultado = manejar_evento_reservar_inventario(compra_id, producto_id, cantidad)

    if resultado['status'] == 'success':
        # Invalidar el caché relevante
        cache.delete('inventario')
        return jsonify({"message": "Inventario reservado"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400