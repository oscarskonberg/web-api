from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection details
uri = "neo4j+s://c1a528e1.databases.neo4j.io"
username = "neo4j"
password = "S6TD4YbelBzmDilMjShCUveiQihCHR_84YgrY4v7NVE"

driver = GraphDatabase.driver(uri, auth=(username, password))

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

if __name__ == '__main__':
    app.run(debug=True)

#employee - (MARLENE)
#create (POST), read (GET), update (PUT) and delete (DELETE)

#opprett employee
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

#Henter employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

#Henter employee basert på ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((emp for emp in employee if emp['employeeId'] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404  #error beskjed dersom employee ikke finnes/er lagt til

#Oppdater employee basert på ID
@app.route('/employeea/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = next((emp for emp in employees if emp['employeeId'] == employee_id), None)
    if employee:
        employee['name'] = data.get('name', employee['name'])
        employee['address'] = data.get('address', employee['address'])
        employee['branch'] = data.get('branch', employee['branch'])
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404  #error beskjed dersom employee ikke finnes/er lagt til

#Slett employee basert på ID
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    global employees 
    employees = [emp for emp in employees if emp['employeeId'] != employee_id]
    return jsonify ({'message': 'Employee delete'}), 204

#(local test) !!!!!!!!!!
#if __name__ == '__main__':
    #app.run(debug=True)