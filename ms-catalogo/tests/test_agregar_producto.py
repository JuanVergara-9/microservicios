import unittest
from unittest.mock import patch, MagicMock
from app.services import agregar_producto

class TestAgregarProducto(unittest.TestCase):

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.Producto')
    def test_agregar_producto(self, MockProducto, mock_commit, mock_add):
        # Configurar el mock
        mock_producto = MockProducto.return_value
        mock_producto.nombre = 'Producto Test'
        
        # Llamar a la función
        nuevo_producto = agregar_producto('Producto Test', 'Descripción Test', 100.0, 10)
        
        # Verificar el resultado
        mock_add.assert_called_once_with(mock_producto)
        mock_commit.assert_called_once()
        self.assertEqual(nuevo_producto.nombre, 'Producto Test')

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.Producto')
    def test_agregar_producto_excepcion(self, MockProducto, mock_commit, mock_add):
        # Configurar el mock para lanzar una excepción
        mock_commit.side_effect = Exception('Error al agregar producto')
        
        # Llamar a la función y verificar que lanza una excepción
        with self.assertRaises(Exception):
            agregar_producto('Producto Test', 'Descripción Test', 100.0, 10)

if __name__ == '__main__':
    unittest.main()


