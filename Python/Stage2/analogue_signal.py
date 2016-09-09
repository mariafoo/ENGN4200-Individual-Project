import csv
import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import leastsq

def read_csv_to_objects (csv_file_path):

    # skip = 10

    with open(csv_file_path, 'r') as csv_file:

        # if (not skip == 0):
        #     skip = skip - 1
        #     continue

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

# acceleration_time_values = np.array([int(row['Time']) for row in acceleration_readings])
acceleration_time_values = np.arange(0, 360000, 30)

acceleration_x_values = np.array([int(row['X']) for row in acceleration_readings])
acceleration_y_values = np.array([int(row['Y']) for row in acceleration_readings])
acceleration_z_values = np.array([int(row['Z']) for row in acceleration_readings])

# construct an arbitrary sine wave to converge to the data
# we have to guess the parameters in this case

# guess the wave vertical offset
guess_mean_x = np.mean(acceleration_x_values)
# guess the wave amplitude (this is derived from root mean square amplitude of a sine wave)
guess_std_x = 3 * np.std(acceleration_x_values) / (2**0.5)
# guess the phase 
guess_phase_x = 0
# construct the guessed wave
guess_wave_x = guess_std_x * np.sin(acceleration_time_values + guess_phase_x) + guess_mean_x

# define the function to optimize, in this case, we want to minimize the difference
# between the actual data and our "guessed" parameters
optimize_func = lambda x: x[0] * np.sin(acceleration_time_values + x[1]) + x[2] - acceleration_x_values
est_std_x, est_phase_x, est_mean_x = leastsq(optimize_func, [guess_std_x, guess_phase_x, guess_mean_x])[0]

# recreate the fitted curve using the optimized parameters
fitted_wave_x = est_std_x * np.sin(acceleration_time_values + est_phase_x) + est_mean_x

plt.plot(acceleration_x_values, '.')
#plt.plot(guess_wave_x, label='guess wave x')
#plt.plot(fitted_wave_x, label='fitted wave x')
plt.legend()
plt.show()