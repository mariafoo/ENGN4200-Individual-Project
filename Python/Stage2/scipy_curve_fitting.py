# following instructions from http://www2.mpia-hd.mpg.de/~robitaille/PY4SCI_SS_2014/_static/15.%20Fitting%20models%20to%20data.html

import csv 
import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt 

def read_csv_to_table_without_header (csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        readings = []
        for row in reader:
            readings.append(row)
    return readings

table = read_csv_to_table_without_header(sys.argv[1])

# table data is in this format:
# [ 
#   [T, X, Y, Z], 
#   [T, X, Y, Z],
#   ... 
# ]
acceleration_x_values = np.array([int(row[1]) for row in table])
acceleration_y_values = np.array([int(row[2]) for row in table])
acceleration_z_values = np.array([int(row[3]) for row in table])

# normalise it to 0 mean
acceleration_x_values -= np.mean(acceleration_x_values)
acceleration_y_values -= np.mean(acceleration_y_values)
acceleration_z_values -= np.mean(acceleration_z_values)

# assume 30 ms increments between data points
# for a 4s time window, there will be a maximum of 133 data points
acceleration_time_values = np.arange(0, 3.99, 0.03)

    # def freq_from_ZCR(sig, fs):
    # Find all indices right before a rising-edge zero crossing
    # indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

    # crossings = interpolate(indices, sig)

        # return fs / np.mean(np.diff(crossings))

    def func(acceleration_time_values, a, b, c): 
        return a*np.sin(2*np.pi*(1/1.5)*acceleration_time_values + b) + c

    popt, pcov = curve_fit(func, acceleration_time_values, acceleration_x_values)
    print(popt)
    print(pcov)
    plt.plot(acceleration_time_values, acceleration_x_values, 'r.')
    plt.plot(acceleration_time_values, func(acceleration_time_values, popt[0], popt[1], popt[2]))
    plt.show()