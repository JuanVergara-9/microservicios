import unittest
from unittest.mock import patch, MagicMock
from app.services import obtener_todos_los_items, obtener_item_por_id, agregar_item, actualizar_stock

class TestServices(unittest.TestCase):

    @patch('app.services.Item.query.all')
    def test_obtener_todos_los_items(self, mock_query_all):
        mock_query_all.return_value = ['item1', 'item2']
        items = obtener_todos_los_items()
        self.assertEqual(items, ['item1', 'item2'])

    @patch('app.services.Item.query.get')
    def test_obtener_item_por_id(self, mock_query_get):
        mock_query_get.return_value = 'item1'
        item = obtener_item_por_id(1)
        self.assertEqual(item, 'item1')

    @patch('app.services.db.session.add')
    @patch('app.services.db.session.commit')
    @patch('app.services.Item')
    def test_agregar_item(self, MockItem, mock_commit, mock_add):
        mock_item = MockItem.return_value
        mock_item.nombre = 'Item Test'
        nuevo_item = agregar_item('Item Test', 'Descripción Test', 100.0, 10)
        mock_add.assert_called_once_with(mock_item)
        mock_commit.assert_called_once()
        self.assertEqual(nuevo_item.nombre, 'Item Test')

    @patch('app.services.db.session.commit')
    @patch('app.services.Item.query.get')
    def test_actualizar_stock(self, mock_query_get, mock_commit):
        mock_item = mock_query_get.return_value
        mock_item.stock = 10
        actualizar_stock(1, 5)
        self.assertEqual(mock_item.stock, 15)
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()