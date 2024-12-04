from app import create_app, db
from app.models import Inventario

def add_products():
    app = create_app()
    with app.app_context():
        # Añadir productos a la base de datos
        producto1 = Inventario(nombre="Producto 1", descripcion="Descripción del Producto 1", precio=10.0, stock=100)
        producto2 = Inventario(nombre="Producto 2", descripcion="Descripción del Producto 2", precio=20.0, stock=200)
        
        db.session.add(producto1)
        db.session.add(producto2)
        db.session.commit()

if __name__ == "__main__":
    add_products()