import unittest
from unittest.mock import patch, MagicMock
from app.services import obtener_todos_los_productos, obtener_producto_por_id, agregar_producto, registrar_compra

class TestServices(unittest.TestCase):

    @patch('app.services.Producto.query.all')
    def test_obtener_todos_los_productos(self, mock_query_all):
        mock_query_all.return_value = ['producto1', 'producto2']
        productos = obtener_todos_los_productos()
        self.assertEqual(productos, ['producto1', 'producto2'])

    @patch('app.services.Producto.query.get')
    def test_obtener_producto_por_id(self, mock_query_get):
        mock_query_get.return_value = 'producto1'
        producto = obtener_producto_por_id(1)
        self.assertEqual(producto, 'producto1')

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.Producto')
    def test_agregar_producto(self, MockProducto, mock_commit, mock_add):
        mock_producto = MockProducto.return_value
        mock_producto.nombre = 'Producto Test'
        nuevo_producto = agregar_producto('Producto Test', 'Descripción Test', 100.0, 10)
        mock_add.assert_called_once_with(mock_producto)
        mock_commit.assert_called_once()
        self.assertEqual(nuevo_producto.nombre, 'Producto Test')

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.db.session.rollback')
    @patch('app.services.Compra')
    def test_registrar_compra(self, MockCompra, mock_rollback, mock_commit, mock_add):
        mock_compra = MockCompra.return_value
        mock_compra.to_dict.return_value = {'id': 1, 'producto_id': 1, 'usuario_id': 1, 'cantidad': 1}
        datos_compra = {'producto_id': 1, 'usuario_id': 1}
        resultado = registrar_compra(datos_compra)
        mock_add.assert_called_once_with(mock_compra)
        mock_commit.assert_called_once()
        self.assertEqual(resultado['status'], 'success')
        self.assertEqual(resultado['compra'], {'id': 1, 'producto_id': 1, 'usuario_id': 1, 'cantidad': 1})

if __name__ == '__main__':
    unittest.main()