# curve fitting algorithm from http://www2.mpia-hd.mpg.de/~robitaille/PY4SCI_SS_2014/_static/15.%20Fitting%20models%20to%20data.html
# frequency estimation algorithm from https://gist.github.com/endolith/255291
# parabolic function algorithm from https://github.com/endolith/waveform-analyzer/blob/master/common.py

import csv 
import sys
import math as m
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.mlab import find 
from scipy.optimize import curve_fit
from scipy.signal import fftconvolve

your_csv_file = input('Enter a csv filename: ')
delta_t = int(input('Enter time delay (in milliseconds): '))/1000

def read_csv_to_table_without_header (csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        readings = []
        for row in reader:
            readings.append(row)
    return readings

table = read_csv_to_table_without_header(your_csv_file)
n = len(table)

# assume 30 ms increments between data points
# for a 4s time window, there will be a maximum of 133 data points
acceleration_time_values = np.arange(0, n*delta_t, delta_t)

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
print("Mean X (not normalised): " + str(m.floor(np.mean(acceleration_x_values))))

acceleration_x_values -= np.mean(acceleration_x_values)
acceleration_y_values -= np.mean(acceleration_y_values)
acceleration_z_values -= np.mean(acceleration_z_values)

# estimate the frequency for curve fitting

def parabolic(f, x):
    """
    Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
    f is a vector and x is an index for that vector.
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = np.diff(corr)
    start = find(d > 0)[0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = np.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px

f = freq_from_autocorr(acceleration_x_values, 1/delta_t)
angular_f = f * 2*np.pi
print('Frequency of this wave: ' + str(round(f,2)))

def func(acceleration_time_values, a, b, c): 
    return a*np.sin(angular_f*acceleration_time_values + b) + c

popt, pcov = curve_fit(func, acceleration_time_values, acceleration_x_values)
print('Curve fitting formula: Acceleration(t) (m/s^2) = ' + str(m.floor(popt[0])) + 'sin(' + str(m.floor(angular_f)) + 't + ' + str(m.floor(popt[1])) + ')' + ' + ' + str(m.floor(popt[2])))
# print(pcov)

std_dev_x_values = m.floor(np.std(acceleration_x_values))
print('Standard Deviation of x-axis Acceleration is: ' + str(std_dev_x_values))

plt.plot(acceleration_time_values, acceleration_time_values * 0, 'g-')
plt.plot(acceleration_time_values, acceleration_x_values, 'r.')
plt.plot(acceleration_time_values, func(acceleration_time_values, popt[0], popt[1], popt[2]))
plt.show()