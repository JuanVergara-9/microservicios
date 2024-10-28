import unittest
from unittest.mock import patch, MagicMock
from app.services import obtener_todos_los_productos, obtener_producto_por_id, agregar_producto, registrar_compra

class TestServices(unittest.TestCase):

    @patch('services.Producto.query.all')
    def test_obtener_todos_los_productos(self, mock_query_all):
        # Configurar el mock
        mock_query_all.return_value = ['producto1', 'producto2']
        
        # Llamar a la función
        productos = obtener_todos_los_productos()
        
        # Verificar el resultado
        self.assertEqual(productos, ['producto1', 'producto2'])

    @patch('services.Producto.query.get')
    def test_obtener_producto_por_id(self, mock_query_get):
        # Configurar el mock
        mock_query_get.return_value = 'producto1'
        
        # Llamar a la función
        producto = obtener_producto_por_id(1)
        
        # Verificar el resultado
        self.assertEqual(producto, 'producto1')

    @patch('services.db.session.add')
    @patch('services.db.session.commit')
    @patch('services.Producto')
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

    @patch('services.db.session.add')
    @patch('services.db.session.commit')
    @patch('services.db.session.rollback')
    @patch('services.Compra')
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

    @patch('services.db.session.add')
    @patch('services.db.session.commit')
    @patch('services.db.session.rollback')
    @patch('services.Compra')
    def test_registrar_compra_faltan_datos(self, MockCompra, mock_rollback, mock_commit, mock_add):
        # Datos de prueba incompletos
        datos_compra = {'producto_id': 1}
        
        # Llamar a la función
        resultado = registrar_compra(datos_compra)
        
        # Verificar el resultado
        self.assertEqual(resultado['status'], 'error')
        self.assertIn('Falta el campo requerido', resultado['message'])

if __name__ == '__main__':
    unittest.main()