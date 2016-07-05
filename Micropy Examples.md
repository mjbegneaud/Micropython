#Micropython Examples
***
***

##Counters, etc.

Example of modifier used with counter for While loop.
The % keeps the value of intensity between 0 and 255, so when it reaches 256, it becomes 0 again and repeats.

	import pyb
	
	led = pyb.LED(4)
	intensity = 0
	while True:
		intensity = (intensity +1) % 255
		led.intensity(intensity)
		pyb.delay(20)
	
		
***
##Timing
Example of restricting a loop to a certain rate (in the case where a loop might be quicker than the desired time)
	
	while True:
	  start = pyb.millis()
	  ...do stuff...
	  elapsed = pyb.elapsed_millis(start)
	  if elapsed < 50: pyb.delay(50 - elapsed)
	  
	  
***
##Switch Use

Example of using switch to initiate an activity which will stop once the switch is pressed again

	import pyb

	# creating objects
	accel = pyb.Accel()
	blue = pyb.LED(4)
	switch = pyb.Switch()

	# loop
	while True:

	    # wait for interrupt
	    # this reduces power consumption while waiting for switch press
	    pyb.wfi()
	
	    # start if switch is pressed
	    if switch():
	        pyb.delay(200)                      # delay avoids detection of multiple presses
	        blue.on()                           # blue LED indicates file open
	        log = open('1:/log.csv', 'w')       # open file on SD (SD: '1:/', flash: '0/)
	
	        # until switch is pressed again
	        while not switch():
	            t = pyb.millis()                            # get time
	            x, y, z = accel.filtered_xyz()              # get acceleration data
	            log.write('{},{},{},{}\n'.format(t,x,y,z))  # write data to file
	
	        # end after switch is pressed again
	        log.close()                         # close file
	        blue.off()                          # blue LED indicates file closed
	        pyb.delay(200)                      # delay avoids detection of multiple presses



***
##Accelerometer Use

Example to print accelerometer values to REPL prompt.

	import pyb
	
	switch = pyb.Switch()
	accel = pyb.Accel()
	
	while True:
		if switch():
			x, y, z, tilt = accel.x(), accel.y(), accel.z(), accel.tilt()
			accel_filtered = accel.filtered_xyz()
			print('\nfiltered = ',accel_filtered,'\nx = ',x,'\ny = ',y,'\nz = ',z,'\ntilt = ',tilt)
		pyb.delay(200)
- Note that filtered accelerometer values are the sum values of the previous three function calls of accel.<axes> plus the current values. To get the normal values, divide the filtered values by 4.q


