import unittest
import time
from app import create_app

class TestPerformance(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_response_time(self):
        start_time = time.time()
        response = self.client.get('/pagos')
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.5)  # Verificar que la respuesta sea menor a 0.5 segundos

if __name__ == '__main__':
    unittest.main()