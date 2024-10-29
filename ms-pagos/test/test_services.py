import unittest
from unittest.mock import patch, MagicMock
from app.services import procesar_pago, obtener_pago_por_id, listar_pagos

class TestServices(unittest.TestCase):

    @patch('app.services.Pago.query.all')
    def test_listar_pagos(self, mock_query_all):
        mock_query_all.return_value = ['pago1', 'pago2']
        pagos = listar_pagos()
        self.assertEqual(pagos, ['pago1', 'pago2'])

    @patch('app.services.Pago.query.get')
    def test_obtener_pago_por_id(self, mock_query_get):
        mock_query_get.return_value = 'pago1'
        pago = obtener_pago_por_id(1)
        self.assertEqual(pago, 'pago1')

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.Pago')
    def test_procesar_pago(self, MockPago, mock_commit, mock_add):
        mock_pago = MockPago.return_value
        mock_pago.id = 1
        nuevo_pago = procesar_pago({'monto': 100.0, 'metodo': 'tarjeta'})
        mock_add.assert_called_once_with(mock_pago)
        mock_commit.assert_called_once()
        self.assertEqual(nuevo_pago.id, 1)

if __name__ == '__main__':
    unittest.main()