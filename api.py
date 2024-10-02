from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for cars
cars = []
car_id_counter = 1

class Car:
    def __init__(self, make, model, year, location, status):
        global car_id_counter
        self.id = car_id_counter
        car_id_counter += 1
        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status

@app.route("/cars", methods=["POST"])
def create_car():
    data = request.json
    new_car = Car(data['make'], data['model'], data['year'], data['location'], data['status'])
    cars.append(new_car.__dict__)
    return jsonify(new_car.__dict__), 201

@app.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(cars), 200

@app.route("/cars/<int:id>", methods=["GET"])
def get_car(id):
    car = next((car for car in cars if car['id'] == id), None)
    if car:
        return jsonify(car), 200
    return jsonify({"error": "Car not found"}), 404

@app.route("/cars/<int:id>", methods=["PUT"])
def update_car(id):
    data = request.json
    car = next((car for car in cars if car['id'] == id), None)
    if car:
        car.update(data)
        return jsonify(car), 200
    return jsonify({"error": "Car not found"}), 404

@app.route("/cars/<int:id>", methods=["DELETE"])
def delete_car(id):
    global cars
    cars = [car for car in cars if car['id'] != id]
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)