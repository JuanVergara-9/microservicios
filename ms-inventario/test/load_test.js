import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 10, // Número de usuarios virtuales
    duration: '30s', // Duración de la prueba
};

export default function () {
    let producto_id = 1; // ID del producto a reservar
    let cantidad = 1; // Cantidad a reservar

    let res = http.post(`http://127.0.0.1:5000/api/v1/resrvar`, JSON.stringify({
        compra_id: Math.floor(Math.random() * 1000),
        producto_id: producto_id,
        cantidad: cantidad
    }), {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res, {
        'is status 200': (r) => r.status === 200,
        'no stock negativo': (r) => {
            if (r.json().error) {
                console.error(`Error en la respuesta: ${r.json().error}`);
                return false;
            }
            return true;
        },
    });

    sleep(1);
}

