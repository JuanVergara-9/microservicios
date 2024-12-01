from flask import Flask, request, jsonify
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from app.saga_orquestador import SagaOrchestrator
from app.tasks import task1, task2, compensate_task1, compensate_task2

app = Flask(__name__)

MICROSERVICES = {
    'catalogo': 'http://ms-catalogo:5001',
    'compras': 'http://ms-compras:5002',
    'inventario': 'http://ms-inventario:5003',
    'pagos': 'http://ms-pagos:5004'
}

class MicroserviceProxy:
    def __init__(self, service_name):
        self.service_name = service_name
        self.base_url = MICROSERVICES.get(service_name)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def forward_request(self, path, method, headers, data, cookies):
        if not self.base_url:
            return jsonify({'error': 'Servicio no encontrado'}), 404

        url = f"{self.base_url}/{path}"
        response = requests.request(
            method=method,
            url=url,
            headers={key: value for key, value in headers if key != 'Host'},
            data=data,
            cookies=cookies,
            allow_redirects=False
        )

        return response.content, response.status_code, response.headers.items()

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, path):
    proxy = MicroserviceProxy(service)
    response_content, status_code, headers = proxy.forward_request(
        path, request.method, request.headers, request.get_data(), request.cookies
    )
    return response_content, status_code, headers

@app.route('/saga_example', methods=['POST'])
def saga_example():
    saga = SagaOrchestrator()
    saga.add_step(task1, compensate_task1)
    saga.add_step(task2, compensate_task2)
    result = saga.execute()
    if result['success']:
        return jsonify({"message": "Saga completed successfully"}), 200
    else:
        return jsonify({"error": "Saga failed and compensated"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)