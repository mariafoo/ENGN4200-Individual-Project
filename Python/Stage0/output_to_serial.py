# STAGE 0: Accelerometer output to serial
# DATE 28 September 2015

import serial, re 

# connect to Arduino port with 38400 baud
arduino = serial.Serial('/dev/cu.usbmodem1411',38400)

while True: 
    data = arduino.readline()[:-2]
    data = data.decode("utf-8")
    if data and data[0] == 'X': # start from x-coordinate values
        coordinates = re.match(r'X.(\d{3}).Y.(\d{3}).Z.(\d{3})',data, re.I) # parse only values
        print(coordinates.group(1))
        print(coordinates.group(2))
        print(coordinates.group(3))
    else:
        continue