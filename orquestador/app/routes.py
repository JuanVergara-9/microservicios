# orquestador/app/routes.py

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MICROSERVICES = {
    'catalogo': 'http://ms-catalogo:5001',
    'compras': 'http://ms-compras:5002',
    'inventario': 'http://ms-inventario:5003',
    'pagos': 'http://ms-pagos:5004'
}

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, path):
    if service not in MICROSERVICES:
        return jsonify({'error': 'Servicio no encontrado'}), 404

    url = f"{MICROSERVICES[service]}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)