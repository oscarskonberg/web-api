from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
cars = []
customers = []
employees = []
car_id_counter = 1
customer_id_counter = 1
employee_id_counter = 1

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

class Customer:
    def __init__(self, name, age, address):
        global customer_id_counter
        self.id = customer_id_counter
        customer_id_counter += 1
        self.name = name
        self.age = age
        self.address = address
        self.booked_car_id = None
        self.rented_car_id = None

class Employee:
    def __init__(self, name, address, branch):
        global employee_id_counter
        self.id = employee_id_counter
        employee_id_counter += 1
        self.name = name
        self.address = address
        self.branch = branch

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

@app.route("/customers", methods=["POST"])
def create_customer():
    data = request.json
    new_customer = Customer(data['name'], data['age'], data['address'])
    customers.append(new_customer.__dict__)
    return jsonify(new_customer.__dict__), 201

@app.route("/customers", methods=["GET"])
def get_customers():
    return jsonify(customers), 200

@app.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):
    customer = next((customer for customer in customers if customer['id'] == id), None)
    if customer:
        return jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 404

@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    data = request.json
    customer = next((customer for customer in customers if customer['id'] == id), None)
    if customer:
        customer.update(data)
        return jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 404

@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    global customers
    customers = [customer for customer in customers if customer['id'] != id]
    return '', 204

@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.json
    new_employee = Employee(data['name'], data['address'], data['branch'])
    employees.append(new_employee.__dict__)
    return jsonify(new_employee.__dict__), 201

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees), 200

@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    employee = next((employee for employee in employees if employee['id'] == id), None)
    if employee:
        return jsonify(employee), 200
    return jsonify({"error": "Employee not found"}), 404

@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.json
    employee = next((employee for employee in employees if employee['id'] == id), None)
    if employee:
        employee.update(data)
        return jsonify(employee), 200
    return jsonify({"error": "Employee not found"}), 404

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    global employees
    employees = [employee for employee in employees if employee['id'] != id]
    return '', 204

@app.route("/order-car", methods=["POST"])
def order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    customer = next((customer for customer in customers if customer['id'] == customer_id), None)
    car = next((car for car in cars if car['id'] == car_id), None)
    if customer and car and car['status'] == 'available' and customer['booked_car_id'] is None:
        car['status'] = 'booked'
        customer['booked_car_id'] = car_id
        return jsonify({"message": "Car booked successfully"}), 200
    return jsonify({"error": "Booking failed"}), 400

@app.route("/cancel-order-car", methods=["POST"])
def cancel_order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    customer = next((customer for customer in customers if customer['id'] == customer_id), None)
    car = next((car for car in cars if car['id'] == car_id), None)
    if customer and car and customer['booked_car_id'] == car_id:
        car['status'] = 'available'
        customer['booked_car_id'] = None
        return jsonify({"message": "Car booking cancelled successfully"}), 200
    return jsonify({"error": "Cancellation failed"}), 400

@app.route("/rent-car", methods=["POST"])
def rent_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    customer = next((customer for customer in customers if customer['id'] == customer_id), None)
    car = next((car for car in cars if car['id'] == car_id), None)
    if customer and car and customer['booked_car_id'] == car_id:
        car['status'] = 'rented'
        customer['rented_car_id'] = car_id
        customer['booked_car_id'] = None
        return jsonify({"message": "Car rented successfully"}), 200
    return jsonify({"error": "Renting failed"}), 400

@app.route("/return-car", methods=["POST"])
def return_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    status = data['status']
    customer = next((customer for customer in customers if customer['id'] == customer_id), None)
    car = next((car for car in cars if car['id'] == car_id), None)
    if customer and car and customer['rented_car_id'] == car_id:
        car['status'] = status
        customer['rented_car_id'] = None
        return jsonify({"message": "Car returned successfully"}), 200
    return jsonify({"error": "Return failed"}), 400

if __name__ == "__main__":
    app.run(debug=True)