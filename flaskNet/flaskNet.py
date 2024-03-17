from flask import Flask,render_template,redirect,request,url_for,jsonify
# from forms import 
from itertools import zip_longest
import json
import csv
import gpios

app = Flask(__name__,template_folder='temp')

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        # Read all rows into a list
        rows = list(csv_reader)
        # Extract the last 100 rows if there are more than 100 rows, otherwise all rows
        last_100_rows = rows[-100:] if len(rows) > 100 else rows
        transposed = zip_longest(*last_100_rows, fillvalue='')
        for row in transposed:
            data.append(row)
    return data


@app.route('/', methods = ['GET','POST'] )
def home():
    return render_template('home.html') 

@app.route('/dashboard')
def dashboard():
    # Read data from CSV and transpose it
    sensor_data = read_csv('sensor_data.csv')
    # Sensor names list
    sensor_names = ['solar', 'temp', 'humidity', 'soil moisture']
    # Pass data and sensor names to the template
    return render_template('dashboard.html', sensor_data=sensor_data, sensor_names=sensor_names)
    


# Route to serve the controls page with toggle switches
@app.route('/controls')
def controls():
    gpio_state = gpios.get_data()
    return render_template('controls.html', gpio_state=gpio_state)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    
    # Extract sensor data from the received JSON
    sensor_data = [
        data.get("solar"),
        data.get("temperature"),
        data.get("humidity"),
        data.get("moisture")
    ]
    print(sensor_data)
    # Append sensor data to the CSV file
    with open('sensor_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(sensor_data)
    
    return gpios.get_data()
    

@app.route('/gpio_data', methods=['POST'])
def receive_gpio_data():
    data = request.json
    print("Received GPIO data:", data)
    # Here you can handle the received GPIO data as needed
    gpios.update_gpio_state(data)
    return jsonify(success=True)

@app.route('/get_gpio_state', methods=['GET'])
def get_gpio_state():
    data = gpios.get_data()
    print(type(data),"\n",data)
    return data

# Route to handle AJAX requests for toggling GPIO values
@app.route('/toggle_gpio', methods=['POST'])
def toggle_gpio():
    gpio_id = request.json['id']
    gpio_state = gpios.get_data()
    gpio_state[gpio_id] = 1 - gpio_state.get(gpio_id, 0)  # Toggle GPIO value (0 to 1 or 1 to 0)
    gpios.update_gpio_state(gpio_state)
    return jsonify({'success': True})


def start():
    app.run(debug=True,port=80,host='0.0.0.0')


