class SagaOrchestrator:
    def __init__(self):
        self.steps = []
        self.compensation_steps = []

    def add_step(self, step, compensation_step):
        self.steps.append(step)
        self.compensation_steps.append(compensation_step)

    def execute(self):
        for step in self.steps:
            result = step()
            if not result['success']:
                self.compensate()
                return result
        return {'success': True}

    def compensate(self):
        for compensation_step in reversed(self.compensation_steps):
            compensation_step()