#!/usr/bin/env python
import rospy
import sys
import time
import serial
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('co2chatter', String, queue_size=10)
	rospy.init_node('co2talker', anonymous=True)
	rate = rospy.Rate(1) # 1hz

	ser = serial.Serial('/dev/ttyACM0', 96000, timeout=0)

	while not rospy.is_shutdown():
		try:
			msg = ser.readline()
			msg_str = msg.decode("utf-8")
			print("trying...")
			if "Z" in msg_str and "z" in msg_str:
				print("stripping output")
				msg_str.strip('\r')
				msg_str.strip('\n')
				rospy.loginfo(msg_str)
				pub.publish(msg_str)
				print("published")
				rate.sleep()
		except KeyboardInterrupt:
			print("shutting donw program")
			rospy.signal_shutdown("Ctrl+C pressed")
			ser.close()
			sys.exit()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
