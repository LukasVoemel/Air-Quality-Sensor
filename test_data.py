import serial 
import time 

#set up serial communication with the arduino 
#USB0 is the serial port from the arduino 

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def read_data():
    try:
        #read a line of data from the serial port 
        if ser.in_waiting > 0:  #checks if theres data waiting in the serial buffer 
            data = ser.readline().decode('utf-8').strip() #reads data from Arduino and decodes it from bytes to string 
            print(f"{data}")
            return data
        else:
            return None
        
    except Exception as e:
        print(f"Error reading data: {e}")
        return None
   

    #try and except block: exceptions are a way to handle errors that may occur during program excecution , e variable is used to store the exception objet that is raised when the error occurs
    # The exception objcect contains good info about the error  

if __name__ == "__main__": #this checks if pyton script is being run direclty or if its being imported into another script 
    while True:
        data = read_data()
        print(data)


        time.sleep(1)

