from flask import Flask

app = Flask(__name__)







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
