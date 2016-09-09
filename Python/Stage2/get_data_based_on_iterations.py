import serial, re, time
import csv
import sys

# 2 arguments, file to record into, and number of iterations to record
csv_file = open(sys.argv[1], 'w')
iterations_to_record = int(sys.argv[2])

acceleration_writer = csv.writer(csv_file, delimiter=',')
acceleration_writer.writerow(["Time", "Delta Time", "X", "Y", "Z"])

matching_regex = re.compile('Time.(\d+).X.(\d+).Y.(\d+).Z.(\d+)', re.I)

iterations_done = 0
prev_ms = 0

arduino = serial.Serial('/dev/cu.usbmodem1411', baudrate=9600, timeout=1) # connection via USB

arduino.flushInput()

first_time = True 
while (iterations_done < iterations_to_record):

    # if the starting_byte is not S, discard it until we reach an S
    starting_byte = arduino.read(1)
    if starting_byte != b"S":
        continue

    # read a byte until we reach an E
    intermediate_byte = arduino.read(1)
    message_buffer = b"" 
    while (intermediate_byte != b"E"):
        message_buffer += intermediate_byte
        intermediate_byte = arduino.read(1)

    # now we have the message buffer
    # start from Time 'T'
    message_buffer = message_buffer.decode("utf-8")
    if message_buffer and message_buffer[0] == 'T': # start from Time

        coordinates = re.match(matching_regex, message_buffer) # parse only values

        if not bool(coordinates):
            continue

        time_ms = int(coordinates.group(1))
        x_accel = int(coordinates.group(2)) 
        y_accel = int(coordinates.group(3))
        z_accel = int(coordinates.group(4))

        if first_time: 
            prev_ms = time_ms
            first_time = False

        delta_ms = time_ms - prev_ms
        
        prev_ms = time_ms

        acceleration_writer.writerow([time_ms, delta_ms, x_accel, y_accel, z_accel])
        csv_file.flush()

        iterations_done += 1

    else:
        continue

arduino.close()
csv_file.close()