from flask import Blueprint, jsonify, request
from app.services import actualizar_inventario, obtener_inventario

inventario_bp = Blueprint('inventario', __name__)

inventario = {
    1: {"producto": "Producto 1", "stock": 10},
    2: {"producto": "Producto 2", "stock": 5}
}

@inventario_bp.route('/inventario', methods=['GET'])
def obtener_productos():
    return jsonify(obtener_inventario())

@inventario_bp.route('/inventario/<int:producto_id>', methods=['POST'])
def actualizar_stock(producto_id):
    datos = request.json
    resultado = actualizar_inventario(producto_id, datos['cantidad'])

    if resultado['status'] == 'success':
        return jsonify({"message": "Inventario actualizado"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400
