from flask import Blueprint, jsonify, request
from compras_app import cache
from compras_app.services import registrar_compra

compras_bp = Blueprint('compras', __name__)

compras = []

@compras_bp.route('/compras', methods=['POST'])
def nueva_compra():
    datos_compra = request.json
    resultado = registrar_compra(datos_compra)

    if resultado['status'] == 'success':
        # Invalidar el caché relevante
        cache.delete('compras')
        return jsonify({"message": "Compra registrada con éxito"}), 201
    else:
        return jsonify({"error": "Error al registrar la compra"}), 400

@compras_bp.route('/compras', methods=['GET'])
@cache.cached(timeout=60, key_prefix='compras')
def obtener_compras():
    return jsonify(compras)