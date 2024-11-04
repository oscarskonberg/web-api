from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# -------------------------Neo4j--------------------------------
# Fjernet uri, username og password for sikkerhetsgrunner
uri = ""
username = ""
password = ""

driver = GraphDatabase.driver(uri, auth=(username, password))

# -----------------------CUSTOMER-------------------------------
def create_customer_in_db(first_name, last_name, age, address):
    with driver.session() as session:
        session.run(
            "CREATE (c:Customer {firstName: $firstName, lastName: $lastName, age: $age, address: $address})",
            firstName=first_name, lastName=last_name, age=age, address=address
        )

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    create_customer_in_db(data['firstName'], data['lastName'], data['age'], data['address'])
    return jsonify({'message': 'Customer created successfully'}), 201

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

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = get_customers_from_db()
    return jsonify(customers)

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

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = update_customer_in_db(customer_id, data.get('FirstName'), data.get('LastName'), data.get('age'), data.get('address'))
    if customer:
        return jsonify(customer)
    return jsonify({'message': 'Customer not found'}), 404

def delete_customer_from_db(customer_id):
    with driver.session() as session:
        session.run("MATCH (c:Customer) WHERE ID(c) = $customer_id DELETE c", customer_id=customer_id)

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    delete_customer_from_db(customer_id)
    return jsonify({'message': 'Customer deleted'}), 200


# -----------------------CAR-------------------------------
def create_car_in_db(make, model, year, location, status):
    with driver.session() as session:
        session.run(
            "CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})",
            make=make, model=model, year=year, location=location, status=status
        )

@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    create_car_in_db(data['make'], data['model'], data['year'], data['location'], data['status'])
    return jsonify({'message': 'Car added successfully', 'car': data}), 201

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

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = get_cars_from_db()
    return jsonify(cars)

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

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    car = update_car_in_db(car_id, data.get('make'), data.get('model'), data.get('year'), data.get('location'), data.get('status'))
    if car:
        return jsonify(car)
    return jsonify({'message': 'Car not found'}), 404

def delete_car_from_db(car_id):
    with driver.session() as session:
        session.run("MATCH (c:Car) WHERE ID(c) = $car_id DELETE c", car_id=car_id)

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    delete_car_from_db(car_id)
    return jsonify({'message': 'Car deleted'}), 204

def has_customer_booked_car(customer_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id RETURN car",
            customer_id=customer_id
        )
        return result.single() is not None

def book_car(customer_id, car_id):
    with driver.session() as session:
        if has_customer_booked_car(customer_id):
            return False, "Customer has already booked a car"

        result = session.run(
            "MATCH (car:Car) WHERE ID(car) = $car_id AND car.status = 'available' "
            "WITH car MATCH (c:Customer) WHERE ID(c) = $customer_id "
            "CREATE (c)-[:BOOKED]->(car) SET car.status = 'booked' RETURN car",
            customer_id=customer_id, car_id=car_id
        ).single()

        return (True, "Car booked successfully") if result else (False, "Car is not available")

@app.route('/cars/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    success, message = book_car(customer_id, car_id)
    status_code = 200 if success else 400
    if not all([customer_id, car_id]):
        return jsonify({'message': 'customer_id and car_id are required'}), 400
    return jsonify({'message': message}), status_code

def check_booking(customer_id, car_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id RETURN car",
            customer_id=customer_id, car_id=car_id
        )
        return result.single() is not None

def cancel_order_in_db(customer_id, car_id):
    with driver.session() as session:
        # Se om kunden har booket en car
        if not check_booking(customer_id, car_id):
            return False, "Customer has not booked this car"

        # Kanseller ordren i db
        session.run(
            "MATCH (c:Customer)-[r:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id "
            "DELETE r SET car.status = 'available'",
            customer_id=customer_id, car_id=car_id
        )
        return True, "Car booking cancelled successfully"

@app.route('/cars/cancel-order', methods=['POST'])
def cancel_order():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = cancel_order_in_db(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

def rent_car_in_db(customer_id, car_id):
    with driver.session() as session:
        # Se om customer har booket en spesifikk car
        if not check_booking(customer_id, car_id):
            return False, "Customer has not booked this car"
        
        # Endre status til 'rented'
        session.run(
            "MATCH (c:Customer)-[:BOOKED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id "
            "SET car.status = 'rented'",
            customer_id=customer_id, car_id=car_id
        )
        return True, "Car rented successfully"

@app.route('/cars/rent-car', methods=['POST'])
def rent_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    success, message = rent_car_in_db(customer_id, car_id)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

def return_car_in_db(customer_id, car_id, car_status):
    with driver.session() as session:
        # Se om customer har leid en car
        result = session.run(
            "MATCH (c:Customer)-[:RENTED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id RETURN car",
            customer_id=customer_id, car_id=car_id
        )
        car = result.single()
        if not car:
            return False, "Customer has not rented this car"

        # Oppdater status på bilen
        session.run(
            "MATCH (c:Customer)-[r:RENTED]->(car:Car) WHERE ID(c) = $customer_id AND ID(car) = $car_id "
            "SET car.status = $car_status "
            "DELETE r",
            customer_id=customer_id, car_id=car_id, car_status=car_status
        )
        return True, "Car returned successfully"

@app.route('/cars/return-car', methods=['POST'])
def return_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    car_status = data['car_status']
    success, message = return_car_in_db(customer_id, car_id, car_status)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400

# -----------------------EMPLOYEE-------------------------------
def create_employee_in_db(name, address, branch):
    with driver.session() as session:
        session.run(
            "CREATE (e:Employee {name: $name, address: $address, branch: $branch})",
            name=name, address=address, branch=branch
        )
        
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    create_employee_in_db(data['name'], data['address'], data['branch'])
    return jsonify({'message': 'Employee created successfully'}), 201

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

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = get_employees_from_db()
    return jsonify(employees)

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

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = get_employee_by_id_from_db(employee_id)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

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

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = update_employee_in_db(employee_id, data.get('name'), data.get('address'), data.get('branch'))
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

def delete_employee_from_db(employee_id):
    with driver.session() as session:
        session.run("MATCH (e:Employee) WHERE ID(e) = $employee_id DELETE e", employee_id=employee_id)

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    delete_employee_from_db(employee_id)
    return jsonify({'message': 'Employee deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)

