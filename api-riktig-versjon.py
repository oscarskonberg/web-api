from flask import Flask, jsonify, request

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


#Customers
#Oppretter en ny kunde ved hjelp av POST
@app.route('/customers', methods=['POST'])
#Funksjonen som oppretter en kunde
def create_customer():
    data = request.get_json()
    customer = {
        'personalId': len(customers) + 1,  # Genererer en enkel ID
        'firstName': data['FirstName'],
        'lastName': data['LastName'],
        'age': data['age'],
        'address': data['address']
    }
    customers.append(customer)
    return jsonify(customer), 201


#Henter alle kunder ved hjelp av GET 
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

# Hent en kunde basert på ID
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = find_customer(customer_id)
    if customer:
        return jsonify(customer)
    return jsonify({'message': 'Customer not found'}), 404


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

