from flask import Flask, render_template, jsonify
import serial #the serial communication with the Arduino 

import time #to handle delys and tie - related functions 
import sqlite3 # interacting with SQLite database 
               # is a self-contained, high reliabiliy, full feature SQL databas engine 
import pytz
from datetime import datetime


app = Flask(__name__)

#Server setup

serial_port = '/dev/ttyUSB0' #this is the serial port for the arduino 
baud_rate = 115200 #baud rate is how often a signal changes its state per second in a communication channel , must match arduino 
ser = serial.Serial(serial_port, baud_rate) #init the serial connection 

def read_data():
    while True:
        #read a line of data from the serial port 
        if ser.in_waiting > 0:  #checks if theres data waiting in the serial buffer 
            data = ser.readline().decode('utf-8', errors='ignore').strip() #reads data from Arduino and decodes it from bytes to string 
            #print(f" Received data: {data}")
           
            try: 

                parts = data.split()
                print(parts)

                #check if there are corret number of data points 

                if len(parts) != 8:
                    print("ERROR: Expected 8 data poins but got: ", len(parts))
                    continue

                pm1_0 = float(parts[0])
                pm2_5 = float(parts[1])
                pm4_0 = float(parts[2])
                pm10_0 = float(parts[3])
                humidity = float(parts[4])
                temperature = float(parts[5])
                vocIndex = float(parts[6])
                noxIndex = float(parts[7])

                store_data(pm1_0, pm2_5, pm4_0, pm10_0, humidity, temperature, vocIndex, noxIndex)
                return [pm1_0, pm2_5, pm4_0, pm10_0, humidity, temperature, vocIndex, noxIndex ]

            except Exception as e:
                print(f"Error parsing data: {e}")

        time.sleep(1)



def store_data(pm1_0, pm2_5, pm4_0, pm10_0, humidity, temperature, voc_index, nox_index):

    #this solution will basically overrde the sql UTC timestamp with the MST timestamp so this should now insert the data as MST

    # Create the MST timezone object
    mst = pytz.timezone('America/Denver')

    # Get the current time in UTC and convert it to MST
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    mst_now = utc_now.astimezone(mst)

    # Format the MST time to a string (for example, "YYYY-MM-DD HH:MM:SS")
    mst_time = mst_now.strftime('%Y-%m-%d %H:%M:%S')

    print(mst_time)


    #open a connection to the SQLite database
    conn = sqlite3.connect('sensor_data.db')

    c = conn.cursor()

    c.execute(''' INSERT INTO air_quality (pm1_0, pm2_5, pm4_0, pm10_0, humidity, temperature, voc_index, nox_index, timestamp)
                  VALUES (?,?,?,?,?,?,?,?,?) ''',
              (pm1_0, pm2_5, pm4_0, pm10_0, humidity, temperature, voc_index, nox_index, mst_time))

    conn.commit()
    conn.close()



def get_sensor_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM air_quality ORDER BY timestamp DESC LIMIT 25")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():

    data = get_sensor_data()
    return render_template('index.html', data = data)

#this api endpoint sends the data to the frontend dynamically
@app.route('/api/data')
def api_data():
    data = get_sensor_data()
    return jsonify(data)


#this is for the real time numbers on for the dashboar
@app.route('/api/data/nondb')
def api_data_nondb():
    data = read_data()
    print(data)
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

