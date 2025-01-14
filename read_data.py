import serial #the serial communication with the Arduino 
import time #to handle delys and tie - related functions 
import sqlite3 # interacting with SQLite database 
               # is a self-contained, high reliabiliy, full feature SQL databas engine 
import pytz
from datetime import datetime



#define the I2C bus and sensor I2C address
I2C_BUS = 1 #typically 1 on rapberry pi 
SENSOR_ADDR = 0x59 #I2C address for the SEN5x sensor 

#this is where the buses come into play I think 


serial_port = '/dev/ttyUSB0' #this is the serial port for the arduino 
baud_rate = 115200 #baud rate is how often a signal changes its state per second in a communication channel , must match arduino 
ser = serial.Serial(serial_port, baud_rate) #init the serial connection 

#init the SQLite database
def init_db():

    conn = sqlite3.connect('sensor_data.db') #connection is opened, database will be made if it doesnt exist

    c = conn.cursor() # makes cursor object : : Interface used to interact with the database, executing commands and returing results 

    c.execute(''' CREATE TABLE IF NOT EXISTS air_quality (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              pm1_0 REAL, 
              pm2_5 REAL, 
              pm4_0 REAL, 
              pm10_0 REAL, 
              humidity REAL, 
              temperature REAL, 
              voc_index REAL, 
              nox_index REAL, 
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)'''  )

    #REAL holds a value 4 bytes in size 
    #autoincrement 

    #commit transactions (save changed) and close the connection 
    conn.commit()
    conn.close()




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


def read_data():
    while True:
        #read a line of data from the serial port 
        if ser.in_waiting > 0:  #checks if theres data waiting in the serial buffer 
            data = ser.readline().decode('utf-8', errors='ignore').strip() #reads data from Arduino and decodes it from bytes to string 
            print(f" Received data: {data}")
           
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
            except Exception as e:
                print(f"Error parsing data: {e}")

        time.sleep(1)

        #to see the data in the data base run this

        # sqlite3 sensor_data.db

        #SELECT * FROM air_quality ORDER BY timestamp DESC LIMIT 10; 
        #SELECT * FROM air_quality;
        # .tables to see your tables 
        # table name: air_quality
        # too see setup : .schema air_quality

if __name__ == '__main__':
    init_db()
    read_data()
