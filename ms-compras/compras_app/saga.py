class SagaState:
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class SagaEvent:
    CREATE_ORDER = 'create_order'
    RESERVE_INVENTORY = 'reserve_inventory'
    PROCESS_PAYMENT = 'process_payment'
    COMPLETE_ORDER = 'complete_order'
    CANCEL_ORDER = 'cancel_order'

class SagaStep:
    def __init__(self, action, compensation):
        self.action = action
        self.compensation = compensation

class Saga:
    def __init__(self):
        self.steps = []
        self.state = SagaState.PENDING

    def add_step(self, action, compensation):
        self.steps.append(SagaStep(action, compensation))

    def execute(self):
        completed_steps = []
        try:
            for step in self.steps:
                step.action()
                completed_steps.append(step)
            self.state = SagaState.COMPLETED
        except Exception as e:
            self.state = SagaState.FAILED
            for step in reversed(completed_steps):
                step.compensation()
            raise e
