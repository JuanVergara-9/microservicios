import unittest
from app import create_app, db
from app.models import Producto, Compra

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_agregar_y_obtener_producto(self):
        response = self.client.post('/productos', json={
            'nombre': 'Producto Test',
            'descripcion': 'Descripción Test',
            'precio': 100.0,
            'stock': 10
        })
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/productos')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'Producto Test')

    def test_registrar_compra(self):
        self.client.post('/productos', json={
            'nombre': 'Producto Test',
            'descripcion': 'Descripción Test',
            'precio': 100.0,
            'stock': 10
        })
        response = self.client.post('/compras', json={
            'producto_id': 1,
            'usuario_id': 1,
            'cantidad': 1
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()