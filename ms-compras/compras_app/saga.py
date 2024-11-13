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