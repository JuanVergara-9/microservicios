from flask import Blueprint, jsonify

catalogo_bp = Blueprint('catalogo', __name__)

productos = {
    1: {"nombre": "Producto 1", "precio": 100, "stock": 10},
    2: {"nombre": "Producto 2", "precio": 200, "stock": 5}
}

@catalogo_bp.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

@catalogo_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = productos.get(id)
    if producto:
        return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404
