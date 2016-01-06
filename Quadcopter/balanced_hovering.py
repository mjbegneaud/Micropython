"""
balanced_hovering.py

This program will utilize the pyboard's onboard accelerometer to
crudely balance a quadcopter. The quadcopter must start off on a flat surface
in order to calibrate to the slightly off-set nature of the onboard accelerometer.

Created: 
	Matthew J. Begneaud
	1/5/16

Configuration:

	M1    M2		+y (front)					Micro-USB plug on front side
	 \	  /			|
	  \	 /			|
	   \/			|------> +x (right)
	   /\	
	  /	 \	
	 /    \	
	M3	  M4

* This program will eventually utilize PID control

"""


import pyb
# import PID

# Pre-determined values
HOVER_PWM_VAL = 50
X_TOL = 2
Y_TOL = 2
Z_TOL = 3
LOOP_TIME = 500

# Setup accelerometer
accel = pyb.Accel()

# Calibration on FLAT surface
pyb.delay(500)
x_zero, y_zero, z_zero = accel.x(), accel.y(), accel.z() # raw values
# zeros_filtered = accel.filtered_xyz()
# x_zero, y_zero, z_zero = zeros_filtered[0]/4, zeros_filtered[1]/4, zeros_filtered[2]/4


# Main program
while True:	
	start = pyb.millis()

	# Set PWM values to Hover; accelerometer will modify the PWM values accordingly...
	m1_PWM = HOVER_PWM_VAL
	m2_PWM = HOVER_PWM_VAL
	m3_PWM = HOVER_PWM_VAL
	m4_PWM = HOVER_PWM_VAL

	# Accelerometer data
	x_filt, y_filt, z_filt = accel.x(), accel.y(), accel.z() # raw/unfiltered values
	accel_filtered = accel.filtered_xyz()
	# x_filt, y_filt, z_filt = accel_filtered[0]/4, accel_filtered[1]/4, accel_filtered[2]/4 # filtered values
	print('\n\nzeros = ',x_zero, y_zero, z_zero,'\nfiltered = ',x_filt, y_filt, z_filt)
	
	# Error (amount of tilt occuring)
	x_error = x_filt - x_zero 
	y_error = y_filt - y_zero 
	z_error = z_filt - z_zero 
	print('\n\nerrors: ',x_error, y_error, z_error)

    # X PWM values (x tilt)
	if abs(x_error) > X_TOL:
		if x_error < 0:
			m1_PWM += 5
			m2_PWM -= 5
			m3_PWM += 5
			m4_PWM -= 5
		elif x_error > 0:
			m1_PWM -= 5
			m2_PWM += 5
			m3_PWM -= 5
			m4_PWM += 5

    # Y PWM values (y tilt)
	if abs(y_error) > Y_TOL:
		if y_error < 0:
			m1_PWM -= 5
			m2_PWM -= 5
			m3_PWM += 5
			m4_PWM += 5
		elif y_error > 0:
			m1_PWM += 5
			m2_PWM += 5
			m3_PWM -= 5
			m4_PWM -= 5
    
    # Z PWM values (counteract rise/fall)
	if abs(z_error) > Z_TOL:
		if z_error < Z_TOL: # rising
			m1_PWM -= 5
			m2_PWM -= 5
			m3_PWM -= 5
			m4_PWM -= 5
		elif z_error > Z_TOL: # falling
			m1_PWM += 5
			m2_PWM += 5
			m3_PWM += 5
			m4_PWM += 5

	# Send PWM values to motors
	# For now, lets print the values...
	print('\n\nM1 = ',m1_PWM,'\nM2 = ',m2_PWM,'\nM3 = ',m3_PWM,'\nM4 = ',m4_PWM)

	# Enforce timing of the loop
	elapsed = pyb.elapsed_millis(start)
	if elapsed < LOOP_TIME: pyb.delay(LOOP_TIME - elapsed)




# Alternate code to read accel values for debugging using the USR switch...

# import pyb

# switch = pyb.Switch()
# accel = pyb.Accel()

# while True:
#     if switch():
#         x, y, z, tilt = accel.x(), accel.y(), accel.z(), accel.tilt()
#         accel_filtered = accel.filtered_xyz()
#         print('\nfiltered = ',accel_filtered,'\nx = ',x,'\ny = ',y,'\nz = ',z,'\ntilt = ',tilt)
#     pyb.delay(200)
