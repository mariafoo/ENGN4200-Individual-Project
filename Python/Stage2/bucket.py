# python bucket.py path-to-csv-to-read path-to-directory-to-hold-bucketed-csv-files

import csv 
import sys

def read_csv_to_objects (csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        header = next(reader)
        readings = []
        for row in reader:
            reading = {}
            for index, heading in enumerate(header):
                reading[heading] = row[index]
            readings.append(reading)
    return readings

acceleration_readings = read_csv_to_objects(sys.argv[1])
partition_directory = sys.argv[2]

# bucket the data in 4 second segments
# 4 seconds is going to be our time window
# 4 seconds is 2 * 2 seconds
# 2 seconds is the period for 30 revolutions per second

time_window_ms = 4000
time_interval_per_reading_ms = 30
data_points_per_window = time_window_ms // time_interval_per_reading_ms

# now we can bucket the data by data_points_per_window

file_index = 0
partitioned_csv = open(partition_directory + '/' + str(file_index) + '.csv', 'w')
partition_writer = csv.writer(partitioned_csv, delimiter=',')
for i, row in enumerate(acceleration_readings):
    partition_writer.writerow([row['Time'], row['X'], row['Y'], row['Z']])    
    if ((i + 1) % data_points_per_window == 0):
        file_index = file_index + 1
        partitioned_csv.close()
        partitioned_csv = open(partition_directory + '/' + str(file_index) + '.csv', 'w')
        partition_writer = csv.writer(partitioned_csv, delimiter=',')

partitioned_csv.close()