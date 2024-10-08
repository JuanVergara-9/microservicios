from flask import Blueprint, jsonify, request
from app.services import procesar_pago

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/pagos', methods=['POST'])
def realizar_pago():
    datos_pago = request.json
    resultado = procesar_pago(datos_pago)

    if resultado['status'] == 'success':
        return jsonify({"message": "Pago procesado con éxito"}), 200
    else:
        return jsonify({"error": resultado['message']}), 400
