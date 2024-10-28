import unittest
from unittest.mock import patch
from app.services import obtener_todos_los_productos

class TestObtenerTodosLosProductos(unittest.TestCase):

    @patch('app.services.Producto.query.all')
    def test_obtener_todos_los_productos(self, mock_query_all):
        # Configurar el mock
        mock_query_all.return_value = ['producto1', 'producto2']
        
        # Llamar a la función
        productos = obtener_todos_los_productos()
        
        # Verificar el resultado
        self.assertEqual(productos, ['producto1', 'producto2'])

if __name__ == '__main__':
    unittest.main()
