import unittest
from unittest.mock import patch, MagicMock
from app.services import registrar_compra

class TestRegistrarCompra(unittest.TestCase):

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.db.session.rollback')
    @patch('app.services.Compra')
    def test_registrar_compra(self, MockCompra, mock_rollback, mock_commit, mock_add):
        # Configurar el mock
        mock_compra = MockCompra.return_value
        mock_compra.to_dict.return_value = {'id': 1, 'producto_id': 1, 'usuario_id': 1, 'cantidad': 1}
        
        # Datos de prueba
        datos_compra = {'producto_id': 1, 'usuario_id': 1}
        
        # Llamar a la función
        resultado = registrar_compra(datos_compra)
        
        # Verificar el resultado
        mock_add.assert_called_once_with(mock_compra)
        mock_commit.assert_called_once()
        self.assertEqual(resultado['status'], 'success')
        self.assertEqual(resultado['compra'], {'id': 1, 'producto_id': 1, 'usuario_id': 1, 'cantidad': 1})

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.db.session.rollback')
    @patch('app.services.Compra')
    def test_registrar_compra_faltan_datos(self, MockCompra, mock_rollback, mock_commit, mock_add):
        # Datos de prueba incompletos
        datos_compra = {'producto_id': 1}
        
        # Llamar a la función
        resultado = registrar_compra(datos_compra)
        
        # Verificar el resultado
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('Falta el campo requerido', resultado['message'])

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.db.session.rollback')
    @patch('app.services.Compra')
    @patch('app.services.Producto.query.get')
    def test_registrar_compra_integracion(self, mock_query_get, MockCompra, mock_rollback, mock_commit, mock_add):
        # Configurar el mock para Producto
        mock_producto = MagicMock()
        mock_producto.stock = 10
        mock_query_get.return_value = mock_producto
        
        # Configurar el mock para Compra
        mock_compra = MockCompra.return_value
        mock_compra.to_dict.return_value = {'id': 1, 'producto_id': 1, 'usuario_id': 1, 'cantidad': 1}
        
        # Datos de prueba
        datos_compra = {'producto_id': 1, 'usuario_id': 1, 'cantidad': 1}
        
        # Llamar a la función
        resultado = registrar_compra(datos_compra)
        
        # Verificar el resultado
        mock_add.assert_called_once_with(mock_compra)
        mock_commit.assert_called_once()
        self.assertEqual(resultado['status'], 'success')
        self.assertEqual(resultado['compra'], {'id': 1, 'producto_id': 1, 'usuario_id': 1, 'cantidad': 1})

if __name__ == '__main__':
    unittest.main()
