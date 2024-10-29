import unittest
from app import create_app, db
from app.models import Pago

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

    def test_procesar_y_obtener_pago(self):
        response = self.client.post('/pagos', json={
            'monto': 100.0,
            'metodo': 'tarjeta'
        })
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/pagos/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['monto'], 100.0)

    def test_listar_pagos(self):
        self.client.post('/pagos', json={
            'monto': 100.0,
            'metodo': 'tarjeta'
        })
        response = self.client.get('/pagos')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['monto'], 100.0)

if __name__ == '__main__':
    unittest.main()