import unittest
from unittest.mock import patch
from app.routes import MicroserviceProxy

class TestResiliency(unittest.TestCase):
    @patch('app.routes.requests.request')
    def test_retry_success(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.content = b'Success'
        proxy = MicroserviceProxy('catalogo')
        response_content, status_code, headers = proxy.forward_request(
            'path', 'GET', {}, b'', {}
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(response_content, b'Success')

    @patch('app.routes.requests.request')
    def test_retry_failure(self, mock_request):
        mock_request.side_effect = Exception('Temporary failure')
        proxy = MicroserviceProxy('catalogo')
        with self.assertRaises(Exception):
            proxy.forward_request('path', 'GET', {}, b'', {})

if __name__ == '__main__':
    unittest.main()