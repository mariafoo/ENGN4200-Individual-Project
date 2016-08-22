# STAGE 2: Writing Data
# DATE 15 August 2016

import serial, re, time
import csv
import sys

csv_file = open(sys.argv[1], 'w')
iterations_to_record = int(sys.argv[2])

acceleration_writer = csv.writer(csv_file, delimiter=',')
acceleration_writer.writerow(["Time", "Delta Time", "X", "Y", "Z"])

matching_regex = re.compile('Time.(\d+).X.(\d+).Y.(\d+).Z.(\d+)', re.I)

iterations_done = 0
prev_ms = 0

# connect to Arduino port with 9600 baud
arduino = serial.Serial('/dev/cu.usbmodem1411', baudrate=9600) # connection via USB
# arduino.open('/dev/cu.HC-06-DevB') # connection via Bluetooth

# arduino.flushInput()

skipped = False

while (iterations_done < iterations_to_record):

    data = arduino.readline()[:-2]
    data = data.decode("utf-8")

    if data and data[0] == 'T': # start from Time

        coordinates = re.match(matching_regex, data) # parse only values

        if not bool(coordinates):
            continue

        time_ms = int(coordinates.group(1))

        if not skipped and time_ms != 0:
            continue
        elif not skipped and time_ms == 0:
            skipped = True
        else:
            pass

        x_accel = int(coordinates.group(2)) 
        y_accel = int(coordinates.group(3))
        z_accel = int(coordinates.group(4))

        delta_ms = time_ms - prev_ms
        
        prev_ms = time_ms

        acceleration_writer.writerow([time_ms, delta_ms, x_accel, y_accel, z_accel])

        iterations_done += 1

    else:
        continue

arduino.close()
csv_file.close()