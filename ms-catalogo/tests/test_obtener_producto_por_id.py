import unittest
from unittest.mock import patch
from app.services import obtener_producto_por_id

class TestObtenerProductoPorId(unittest.TestCase):

    @patch('app.services.Producto.query.get')
    def test_obtener_producto_por_id(self, mock_query_get):
        # Configurar el mock
        mock_query_get.return_value = 'producto1'
        
        # Llamar a la función
        producto = obtener_producto_por_id(1)
        
        # Verificar el resultado
        self.assertEqual(producto, 'producto1')

    @patch('app.services.Producto.query.get')
    def test_obtener_producto_por_id_no_existe(self, mock_query_get):
        # Configurar el mock para devolver None
        mock_query_get.return_value = None
        
        # Llamar a la función
        producto = obtener_producto_por_id(999)
        
        # Verificar el resultado
        self.assertIsNone(producto)

if __name__ == '__main__':
    unittest.main()