from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection details 
uri = "neo4j+s://c1a528e1.databases4j.io"
username = "neo4j"
password = "S6TD4YbelBzmDilMjShCUveiQihCHR_84YgrY4v7NVE"

# Driver for connecting to the database
driver = GraphDatabase.driver(uri, auth=(username, password))

# --------------------------CAR--------------------------
# CREATE a car
def create_car(make, model, year, location, status):
    with driver.session() as session:
        session.run(
            "CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})",
            make=make, model=model, year=year, location=location, status=status
        )

# Flask route - CREATE a car
@app.route('/add_car', methods=['POST'])
def add_car_route():
    data = request.get_json()
    create_car(data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car added successfully', 'car': data}), 201


# Function to get all cars
def get_cars():
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

# Flask route - get all cars
@app.route('/cars', methods=['GET'])
def get_cars_route():
    cars = get_cars()
    return jsonify(cars)


#tror vi mangler en UPDATE og DELETE for car

# --------------------------CUSTOMER--------------------------
# CREATE a customer
def create_customer(first_name, last_name, age, address):
    with driver.session() as session:
        session.run(
            "CREATE (c:Customer {firstName: $firstName, lastName: $lastName, age: $age, address: $address})",
            firstName=first_name, lastName=last_name, age=age, address=address
        )

# Flask route - CREATE a customer
@app.route('/customers', methods=['POST'])
def create_customer_route():
    data = request.get_json()
    create_customer(data['FirstName'], data['LastName'], data['age'], data['address'])
    return jsonify({'message': 'Customer created successfully'}), 201

# Function to GET all customers
def get_customers():
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

# Flask route - GET all customers
@app.route('/customers', methods=['GET'])
def get_customers_route():
    customers = get_customers()
    return jsonify(customers)

# GET a customer by last name
def get_customer_by_last_name(last_name):
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

# Flask route - GET a customer by last name
@app.route('/customers/lastname/<string:last_name>', methods=['GET'])
def get_customer_by_last_name_route(last_name):
    customer = get_customer_by_last_name(last_name)
    if customer:
        return jsonify(customer)
    return jsonify({'message': 'Customer not found'}), 404


#tror vi mangler en UPDATE og DELETE for customer


# --------------------------EMPLOYEE--------------------------
# CREATE an employee
def create_employee(name, address, branch):
    with driver.session() as session:
        session.run(
            "CREATE (e:Employee {name: $name, address: $address, branch: $branch})",
            name=name, address=address, branch=branch
        )
# Flask route - CREATE an employee
@app.route('/employees', methods=['POST'])
def create_employee_route():
    data = request.get_json()
    create_employee(data['name'], data['address'], data['branch'])
    return jsonify({'message': 'Employee created successfully'}), 201



# GET all employees
def get_employees():
    with driver.session() as session:
        result = session.run("MATCH (e:Employee) RETURN e.name AS name, e.address AS address, e.branch AS branch")
        employees = []
        for record in result:
            employees.append({
                "name": record["name"],
                "address": record["address"],
                "branch": record["branch"]
            })
        return employees

# Flask route - GET all employees
@app.route('/employees', methods=['GET'])
def get_employees_route():
    employees = get_employees()
    return jsonify(employees)


# GET an employee by ID
def get_employee_by_id(employee_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (e:Employee) WHERE ID(e) = $employee_id RETURN e.name AS name, e.address AS address, e.branch AS branch",
            employee_id=employee_id
        )
        record = result.single()
        if record:
            return {
                "name": record["name"],
                "address": record["address"],
                "branch": record["branch"]
            }
        return None


# Flask route - GET an employee by ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee_route(employee_id):
    employee = get_employee_by_id(employee_id)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

# UPDATE an employee
def update_employee(employee_id, name, address, branch):
    with driver.session() as session:
        result = session.run(
            "MATCH (e:Employee) WHERE ID(e) = $employee_id "
            "SET e.name = $name, e.address = $address, e.branch = $branch "
            "RETURN e.name AS name, e.address AS address, e.branch AS branch",
            employee_id=employee_id, name=name, address=address, branch=branch
        )
        record = result.single()
        if record:
            return {
                "name": record["name"],
                "address": record["address"],
                "branch": record["branch"]
            }
        return None

# Flask route - UPDATE an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee_route(employee_id):
    data = request.get_json()
    employee = update_employee(employee_id, data.get('name'), data.get('address'), data.get('branch'))
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

# DELETE an employee
def delete_employee(employee_id):
    with driver.session() as session:
        session.run("MATCH (e:Employee) WHERE ID(e) = $employee_id DELETE e", employee_id=employee_id)

 
# Flask route - DELETE an employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    delete_employee(employee_id)
    return jsonify({'message': 'Employee deleted'}), 204



    # --------------------------Implement en endpoint-...--------------------------
# 

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

# Flask route to rent a car
@app.route('/rent_car', methods=['POST'])
def rent_car_route():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = rent_car(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

# Function to check if a customer has booked a car
def has_customer_booked_car(customer_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id RETURN car",
            customer_id=customer_id
        )
        return result.single() is not None

# Function to check if a customer has booked a specific car
def check_booking(customer_id, car_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id RETURN car",
            customer_id=customer_id, car_id=car_id
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

# Function to rent a car
def rent_car(customer_id, car_id):
    with driver.session() as session:
        # Check if the customer has booked the specific car
        if not check_booking(customer_id, car_id):
            return False, "Customer has not booked this car"
        
        # Change the car status to 'rented'
        session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id "
            "SET car.status = 'rented'",
            customer_id=customer_id, car_id=car_id
        )
        return True, "Car rented successfully"

# (local test)
if __name__ == '__main__':
    app.run(debug=True)