from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def task1():
    return {'success': True}

def compensate_task1():
    pass

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def task2():
    return {'success': True}

def compensate_task2():
    pass