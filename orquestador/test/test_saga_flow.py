import unittest
from app.saga_orquestador import SagaOrchestrator
from app.tasks import task1, task2, compensate_task1, compensate_task2

class TestSagaFlow(unittest.TestCase):
    def test_saga_success(self):
        saga = SagaOrchestrator()
        saga.add_step(task1, compensate_task1)
        saga.add_step(task2, compensate_task2)
        result = saga.execute()
        self.assertTrue(result['success'])

    def test_saga_failure(self):
        def failing_task():
            return {'success': False}

        saga = SagaOrchestrator()
        saga.add_step(task1, compensate_task1)
        saga.add_step(failing_task, compensate_task2)
        result = saga.execute()
        self.assertFalse(result['success'])

if __name__ == '__main__':
    unittest.main()