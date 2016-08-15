# STAGE 2: Graphing
# DATE 15 August 2016

import serial, re, time
import numpy as np 
import matplotlib.pyplot as plt
import csv
import sys

csv_file = open(sys.argv[1], 'w')
iterations_to_record = int(sys.argv[2])

acceleration_writer = csv.writer(csv_file, delimiter=',')
acceleration_writer.writerow(["Time", "X", "Y", "Z"])

# connect to Arduino port with 9600 baud
arduino = serial.Serial('/dev/cu.usbmodem1411', 9600) # connection via USB
# arduino = serial.Serial('/dev/cu.HC-06-DevB', 9600) # connection via Bluetooth

hz = 5
interval = 1/hz

def sampling_round(value, hz):
    return round(value*hz)/hz

no_of_coordinates = 200
now = int(time.time())
past = now - (no_of_coordinates/hz) # hz is the number of samples per second, gives the right number of x-coordinates to match y-coordinates
future = now
#print('past', past)
#print('future', future)

lowest_y_coordinate = 0
highest_y_coordinate = 1000

plt.ion()
accel_xdata = [0.0] * no_of_coordinates
accel_ydata = [0.0] * no_of_coordinates
accel_zdata = [0.0] * no_of_coordinates
x_axis = np.arange(past, future, interval).tolist()
line_accel_x, = plt.plot(x_axis, accel_xdata)
line_accel_y, = plt.plot(x_axis, accel_ydata)
line_accel_z, = plt.plot(x_axis, accel_zdata)
plt.ylim([lowest_y_coordinate, highest_y_coordinate])
plt.xlim([past, future])

iterations_done = 1

while (iterations_done < iterations_to_record):
    data = arduino.readline()[:-2]
    data = data.decode("utf-8")

    if data and data[0] == 'X': # start from x-coordinate values
        # ignore values appearing at the same time
        now = sampling_round(time.time(), hz)
        
        if x_axis[-1] != now:
            x_axis.append(now)
        else: 
            continue

        iterations_done += 1

        coordinates = re.match(r'X.(\d+).Y.(\d+).Z.(\d+)', data, re.I) # parse only values

        x_accel = int(coordinates.group(1)) 
        y_accel = int(coordinates.group(2))
        z_accel = int(coordinates.group(3))

        acceleration_writer.writerow([now, x_accel, y_accel, z_accel]) 

        accel_xdata.append(x_accel)
        accel_ydata.append(y_accel)
        accel_zdata.append(z_accel)
        del x_axis[0]
        del accel_xdata[0]
        del accel_ydata[0]
        del accel_zdata[0]
        line_accel_x.set_xdata(x_axis)
        line_accel_y.set_xdata(x_axis)
        line_accel_z.set_xdata(x_axis)
        line_accel_x.set_ydata(accel_xdata)
        line_accel_y.set_ydata(accel_ydata)
        line_accel_z.set_ydata(accel_zdata)
        plt.xlim([x_axis[0],x_axis[-1]])
        plt.draw()
        print(x_axis[0],x_axis[-1])
    else:
        continue

csv_file.close()