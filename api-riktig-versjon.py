from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection details
uri = "neo4j+s://c1a528e1.databases.neo4j.io"
username = "neo4j"
password = "S6TD4YbelBzmDilMjShCUveiQihCHR_84YgrY4v7NVE"

driver = GraphDatabase.driver(uri, auth=(username, password))

# In-memory storage for employees
employees = []

# Function to create a customer
def create_customer_in_neo4j(first_name, last_name, age, address):
    with driver.session() as session:
        session.run(
            "CREATE (c:Customer {firstName: $firstName, lastName: $lastName, age: $age, address: $address})",
            firstName=first_name, lastName=last_name, age=age, address=address
        )

# Function to get all customers
def get_customers_from_neo4j():
    with driver.session() as session:
        result = session.run("MATCH (c:Customer) RETURN c.firstName AS firstName, c.lastName AS lastName, c.age AS age, c.address AS address")
        customers = []
        for record in result:
            customers.append({
                "firstName": record["firstName"],
                "lastName": record["lastName"],
                "age": record["age"],
                "address": record["address"]
            })
        return customers

# Function to get a customer by last name
def get_customer_by_last_name_from_neo4j(last_name):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer {lastName: $lastName}) RETURN c.firstName AS firstName, c.lastName AS lastName, c.age AS age, c.address AS address", 
            lastName=last_name
        )
        record = result.single()
        if record:
            return {
                "firstName": record["firstName"],
                "lastName": record["lastName"],
                "age": record["age"],
                "address": record["address"]
            }
        return None

# Function to create a car
def create_car_in_neo4j(make, model, year, location, status):
    with driver.session() as session:
        session.run(
            "CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})",
            make=make, model=model, year=year, location=location, status=status
        )

# Function to get all cars
def get_cars_from_neo4j():
    with driver.session() as session:
        result = session.run("MATCH (c:Car) RETURN c.make AS make, c.model AS model, c.year AS year, c.location AS location, c.status AS status")
        cars = []
        for record in result:
            cars.append({
                "make": record["make"],
                "model": record["model"],
                "year": record["year"],
                "location": record["location"],
                "status": record["status"]
            })
        return cars

# Function to check if a customer has booked a car
def has_customer_booked_car(customer_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id RETURN car",
            customer_id=customer_id
        )
        return result.single() is not None

# Function to book a car
def book_car(customer_id, car_id):
    with driver.session() as session:
        # Check if the customer has already booked a car
        if has_customer_booked_car(customer_id):
            return False, "Customer has already booked a car"

        # Check if the car is available
        result = session.run(
            "MATCH (car:Car) WHERE ID(car) = $car_id AND car.status = 'available' RETURN car",
            car_id=car_id
        )
        car = result.single()
        if not car:
            return False, "Car is not available"

        # Book the car
        session.run(
            "MATCH (c:Customer), (car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id "
            "CREATE (c)-[:BOOKED]->(car) SET car.status = 'booked'",
            customer_id=customer_id, car_id=car_id
        )
        return True, "Car booked successfully"

# Function to return a car
def return_car(customer_id, car_id, car_status):
    with driver.session() as session:
        # Check if the customer has booked the car
        result = session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id RETURN car",
            customer_id=customer_id, car_id=car_id
        )
        car = result.single()
        if not car:
            return False, "Customer has not booked this car"

        # Update the car status
        session.run(
            "MATCH (car:Car) WHERE ID(car) = $car_id "
            "SET car.status = $car_status "
            "WITH car "
            "MATCH (c:Customer)-[r:BOOKED]->(car) WHERE ID(c) = $customer_id "
            "DELETE r",
            car_id=car_id, car_status=car_status, customer_id=customer_id
        )
        return True, "Car returned successfully"

# Flask route to book a car
@app.route('/book_car', methods=['POST'])
def book_car_route():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = book_car(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

# Flask route to return a car
@app.route('/return_car', methods=['POST'])
def return_car_route():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    car_status = data['car_status']
    success, message = return_car(customer_id, car_id, car_status)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

# Flask route to create a customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    create_customer_in_neo4j(data['FirstName'], data['LastName'], data['age'], data['address'])
    return jsonify({'message': 'Customer created successfully'}), 201

# Flask route to get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = get_customers_from_neo4j()
    return jsonify(customers)

# Flask route to get a customer by last name
@app.route('/customers/lastname/<string:last_name>', methods=['GET'])
def get_customer_by_last_name(last_name):
    customer = get_customer_by_last_name_from_neo4j(last_name)
    if customer:
        return jsonify(customer)
    return jsonify({'message': 'Customer not found'}), 404

# Flask route to create a car
@app.route('/add_car', methods=['POST'])
def add_car():
    data = request.get_json()
    create_car_in_neo4j(data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car added successfully', 'car': data}), 201

# Flask route to get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = get_cars_from_neo4j()
    return jsonify(cars)

# Flask route to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# Flask route to get an employee by ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((emp for emp in employees if emp['employeeId'] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

# Flask route to create an employee
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee = {
        'employeeId': len(employees) + 1,
        'name': data['name'],
        'address': data['address'],
        'branch': data['branch']
    }
    employees.append(employee)
    return jsonify(employee), 201

# Flask route to update an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = next((emp for emp in employees if emp['employeeId'] == employee_id), None)
    if employee:
        employee['name'] = data.get('name', employee['name'])
        employee['address'] = data.get('address', employee['address'])
        employee['branch'] = data.get('branch', employee['branch'])
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

# Flask route to delete an employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    global employees 
    employees = [emp for emp in employees if emp['employeeId'] != employee_id]
    return jsonify({'message': 'Employee deleted'}), 204

# (local test)
if __name__ == '__main__':
    app.run(debug=True)