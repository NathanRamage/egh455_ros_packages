#!/usr/bin/env python
import sys
import pigpio
import rospy
import time
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('tempchatter', String, queue_size=10)
	rospy.init_node('tempTalker', anonymous=True)
	rate = rospy.Rate(1) # 10hz

    	TEMP_HUMD_ADDRESS = 0x40
   	TEMP_MEASURE_NOHOLD = 0xF3
   	HUMD_MEASURE_NOHOLD = 0xF5

    	gpio = pigpio.pi()
    	handle = gpio.i2c_open(1, TEMP_HUMD_ADDRESS)



	while not rospy.is_shutdown():
		try:
			# Request a humidity reading
            		gpio.i2c_write_device(handle, [HUMD_MEASURE_NOHOLD])
            		# Give the sensor time to calculate
            		time.sleep(0.1);
            		# Attempt to read 2 bytes of data (specified in datasheet)
            		(count, data) = gpio.i2c_read_device(handle, 2)
            		# Clear the last to bits of LSB to 00.
            		# According to datasheet LSB of RH is always xxxxxx10
            		h_lsb = data[1] & 0xFC
            		h_msb = data[0]
            		# Convert the raw data to a measurement
            		h_mesurment = int(h_msb << 8 | h_lsb)
            		# Convert the measurement into the right units
            		h_result = (125.0 * h_mesurment / 65536) - 6
            		print("Humid: %d" % h_result) # Humidity as a percentage

            		msg = str(int(h_result)) + " "

            		gpio.i2c_write_device(handle, [TEMP_MEASURE_NOHOLD])
            		time.sleep(0.1);
		        (count, data) = gpio.i2c_read_device(handle, 2)
            		t_lsb = data[1] & 0xFC
            		t_msb = data[0]
            		t_mesurment = int(t_msb << 8 | t_lsb)
            		t_result = (175.72 * t_mesurment / 65536) - 46.85;
            		print("Temp: %d" % t_result) # Temperature in Celsius

            		msg += str(int(t_result))

            		pub.publish(msg)

            		rate.sleep()
		except KeyboardInterrupt:
			print("shutting donw program")
            		gpio.i2c_close(handle)
			sys.exit()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptExcepyion:
		pass
