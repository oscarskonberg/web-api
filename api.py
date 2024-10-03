from flask import Flask, request, jsonify, render_template

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

@app.route("/customer")
def customer_page():
    return render_template("customer.html")

@app.route("/employee")
def employee_page():
    return render_template("employee.html")

@app.route("/cars", methods=["POST"])
def create_car():
    data = request.json
    new_car = Car(data['make'], data['model'], data['year'], data['location'], data['status'])
    cars.append(new_car.__dict__)
    return jsonify({"message": "Car created successfully", "car": new_car.__dict__}), 201

@app.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(cars), 200

@app.route("/order-car", methods=["POST"])
def order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    
    customer = next((customer for customer in customers if customer['id'] == customer_id), None)
    car = next((car for car in cars if car['id'] == car_id), None)
    
    print(f"Customer: {customer}")
    print(f"Car: {car}")
    
    if customer and car and car['status'] == 'available' and customer['booked_car_id'] is None:
        car['status'] = 'booked'
        customer['booked_car_id'] = car_id
        return jsonify({"message": "Car booked successfully", "car": car, "customer": customer}), 200
    
    print(f"Booking failed: customer={customer}, car={car}, car_status={car['status'] if car else 'N/A'}, customer_booked_car_id={customer['booked_car_id'] if customer else 'N/A'}")
    return jsonify({"error": "Booking failed"}), 400

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = [
        {"customer_id": customer['id'], "car_id": customer['booked_car_id']}
        for customer in customers if customer['booked_car_id'] is not None
    ]
    return jsonify(orders), 200


if __name__ == "__main__":
    app.run(debug=True)