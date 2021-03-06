import eventlet
eventlet.monkey_patch()

from flask import Flask, make_response, jsonify
from fractal_landscape import build_landscape

import eventlet.wsgi
import numpy as np
import requests
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


microservices_urls = {
    'terrain': 'http://localhost:7000',
    'field_objects': 'http://localhost:7001',
    'socket': 'http://localhost:9000'
}

@app.route('/')
def test_connect():
    return 'Docker hosting image on port 7000'


@app.route('/get_landscape')
def get_landscape():
    seed = datetime.datetime.now()
    seed = seed.hour + 24 * (seed.day + 31 * seed.month) * 4352 + 32454354
    # terrain = build_landscape(250, 250, seed=seed, octaves=1).tolist()
    terrain = np.zeros((250, 250)).tolist()
    requests.post(microservices_urls['field_objects']+'/store_terrain', json = {'terrain':terrain})
    requests.post(microservices_urls['socket']+'/send_terrain', json = {'terrain':terrain})
    # Delete once stored in Redis
    print('in get landscape')
    # return jsonify({'terrain': terrain}, 201)
    # return jsonify('ok')
    return 'ok'


if __name__ == '__main__':
    print('running')
    # app.run(host='0.0.0.0', port=7000, debug=True)
    eventlet.wsgi.server(eventlet.listen(('', 7000)), app, debug=True)

