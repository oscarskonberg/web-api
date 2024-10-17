from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/add_car', methods=['POST'])
def add_car():
    data = request.get_json()
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    location = data.get('location')
    status = data.get('status')

    # Her skal lagring i database implementeres senere
    return jsonify({'message': 'Car added', 'car': data}), 201

@app.route('/cars', methods=['GET'])
def get_cars():
    # Her skal henting fra database implementeres senere
    return jsonify({'message': 'Retrieve all cars'}), 200

@app.route('/car/<model>', methods=['GET'])
def get_car(model):
    # Her skal henting av spesifikk bil implementeres senere
    return jsonify({'message': f'Retrieve car with model {model}'}), 200

@app.route('/update_car/<model>', methods=['PUT'])
def update_car(model):
    data = request.get_json()
    # Her skal oppdatering i database implementeres senere
    return jsonify({'message': f'Car with model {model} updated', 'updated_data': data}), 200

@app.route('/delete_car/<model>', methods=['DELETE'])
def delete_car(model):
    # Her skal sletting fra database implementeres senere
    return jsonify({'message': f'Car with model {model} deleted'}), 200

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)

