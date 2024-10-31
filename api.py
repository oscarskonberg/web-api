from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection details
uri = "neo4j+s://9568fa27.databases.neo4j.io"
username = "neo4j"
password = "kLStTek7OYFEyJfSL61y7y4vNAMHQoW6iLmBGeBEVdU"

# Driver for connecting to the database
driver = GraphDatabase.driver(uri, auth=(username, password))

# -----------------------CUSTOMER-------------------------------
# Function to create a customer in the database
def create_customer_in_db(first_name, last_name, age, address):
    with driver.session() as session:
        session.run(
            "CREATE (c:Customer {firstName: $firstName, lastName: $lastName, age: $age, address: $address})",
            firstName=first_name, lastName=last_name, age=age, address=address
        )

# Flask route to create a customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    create_customer_in_db(data['FirstName'], data['LastName'], data['age'], data['address'])
    return jsonify({'message': 'Customer created successfully'}), 201

# Function to get all customers from the database
def get_customers_from_db():
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

# Flask route to get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = get_customers_from_db()
    return jsonify(customers)
    
#----------------------OBS
# Function to get a customer by last name from the database
def get_customer_by_last_name_from_db(last_name):
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
#----------------------OBS
# Flask route to get a customer by last name
@app.route('/customers/lastname/<string:last_name>', methods=['GET'])
def get_customer_by_last_name(last_name):
    customer = get_customer_by_last_name_from_db(last_name)
    if customer:
        return jsonify(customer)
    return jsonify({'message': 'Customer not found'}), 404

# Function to update a customer in the database
def update_customer_in_db(customer_id, first_name, last_name, age, address):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer) WHERE ID(c) = $customer_id "
            "SET c.firstName = $firstName, c.lastName = $lastName, c.age = $age, c.address = $address "
            "RETURN c.firstName AS firstName, c.lastName AS lastName, c.age AS age, c.address AS address",
            customer_id=customer_id, firstName=first_name, lastName=last_name, age=age, address=address
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

# Flask route to update a customer
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = update_customer_in_db(customer_id, data.get('FirstName'), data.get('LastName'), data.get('age'), data.get('address'))
    if customer:
        return jsonify(customer)
    return jsonify({'message': 'Customer not found'}), 404

# Function to delete a customer from the database
def delete_customer_from_db(customer_id):
    with driver.session() as session:
        session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id DELETE c", customer_id=customer_id)

# Flask route to delete a customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    delete_customer_from_db(customer_id)
    return jsonify({'message': 'Customer deleted'}), 204


# -----------------------CAR-------------------------------
# Function to create a car in the database
def create_car_in_db(make, model, year, location, status):
    with driver.session() as session:
        session.run(
            "CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})",
            make=make, model=model, year=year, location=location, status=status
        )

# Flask route to create a car
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    create_car_in_db(data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car added successfully', 'car': data}), 201

# Function to get all cars from the database
def get_cars_from_db():
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

# Flask route to get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = get_cars_from_db()
    return jsonify(cars)

# Function to update a car in the database
def update_car_in_db(car_id, make, model, year, location, status):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Car) WHERE ID(c) = $car_id "
            "SET c.make = $make, c.model = $model, c.year = $year, c.location = $location, c.status = $status "
            "RETURN c.make AS make, c.model AS model, c.year AS year, c.location AS location, c.status AS status",
            car_id=car_id, make=make, model=model, year=year, location=location, status=status
        )
        record = result.single()
        if record:
            return {
                "make": record["make"],
                "model": record["model"],
                "year": record["year"],
                "location": record["location"],
                "status": record["status"]
            }
        return None

# Flask route to update a car
@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    car = update_car_in_db(car_id, data.get('make'), data.get('model'), data.get('year'), data.get('location'), data.get('status'))
    if car:
        return jsonify(car)
    return jsonify({'message': 'Car not found'}), 404

# Function to delete a car from the database
def delete_car_from_db(car_id):
    with driver.session() as session:
        session.run("MATCH (c:Car) WHERE ID(c) = $car_id DELETE c", car_id=car_id)

# Flask route to delete a car
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    delete_car_from_db(car_id)
    return jsonify({'message': 'Car deleted'}), 204


# -----------------------EMPLOYEE-------------------------------
# Function to create an employee in the database
def create_employee_in_db(name, address, branch):
    with driver.session() as session:
        session.run(
            "CREATE (e:Employee {name: $name, address: $address, branch: $branch})",
            name=name, address=address, branch=branch
        )

# Flask route to create an employee
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    create_employee_in_db(data['name'], data['address'], data['branch'])
    return jsonify({'message': 'Employee created successfully'}), 201

# Function to get all employees from the database
def get_employees_from_db():
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

# Flask route to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = get_employees_from_db()
    return jsonify(employees)

# Function to get an employee by ID from the database
def get_employee_by_id_from_db(employee_id):
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

# Flask route to get an employee by ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = get_employee_by_id_from_db(employee_id)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

# Function to update an employee in the database
def update_employee_in_db(employee_id, name, address, branch):
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

# Flask route to update an employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = update_employee_in_db(employee_id, data.get('name'), data.get('address'), data.get('branch'))
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

# Function to delete an employee from the database
def delete_employee_from_db(employee_id):
    with driver.session() as session:
        session.run("MATCH (e:Employee) WHERE ID(e) = $employee_id DELETE e", employee_id=employee_id)

# Flask route to delete an employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    delete_employee_from_db(employee_id)
    return jsonify({'message': 'Employee deleted'}), 204

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

# Flask route to book a car
@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = book_car(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

# Function to cancel a car booking
def cancel_order_car(customer_id, car_id):
    with driver.session() as session:
        # Check if the customer has booked the car
        if not check_booking(customer_id, car_id):
            return False, "Customer has not booked this car"

        # Cancel the booking
        session.run(
            "MATCH (c:Customer)-[r:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id "
            "DELETE r SET car.status = 'available'",
            customer_id=customer_id, car_id=car_id
        )
        return True, "Car booking cancelled successfully"

# Flask route to cancel a car booking
@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car_route():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = cancel_order_car(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

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

# Flask route to rent a car
@app.route('/rent-car', methods=['POST'])
def rent_car_route():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = rent_car(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

# Function to return a car
def return_car(customer_id, car_id, car_status):
    with driver.session() as session:
        # Check if the customer has rented the car
        result = session.run(
            "MATCH (c:Customer)-[:RENTED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id RETURN car",
            customer_id=customer_id, car_id=car_id
        )
        car = result.single()
        if not car:
            return False, "Customer has not rented this car"

        # Update the car status
        session.run(
            "MATCH (car:Car) WHERE ID(car) = $car_id "
            "SET car.status = $car_status "
            "WITH car "
            "MATCH (c:Customer)-[r:RENTED]->(car) WHERE ID(c) = $customer_id "
            "DELETE r",
            car_id=car_id, car_status=car_status, customer_id=customer_id
        )
        return True, "Car returned successfully"

# Flask route to return a car
@app.route('/return-car', methods=['POST'])
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

# (local test)
if __name__ == '__main__':
    app.run(debug=True)
