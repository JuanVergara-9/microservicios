import unittest
from app import create_app, db
from app.models import Item

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

    def test_agregar_y_obtener_item(self):
        response = self.client.post('/items', json={
            'nombre': 'Item Test',
            'descripcion': 'Descripción Test',
            'precio': 100.0,
            'stock': 10
        })
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'Item Test')

    def test_actualizar_stock(self):
        self.client.post('/items', json={
            'nombre': 'Item Test',
            'descripcion': 'Descripción Test',
            'precio': 100.0,
            'stock': 10
        })
        response = self.client.put('/items/1/stock', json={'cantidad': 5})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['stock'], 15)

if __name__ == '__main__':
    unittest.main()