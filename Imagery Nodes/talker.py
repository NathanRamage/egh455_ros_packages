#!/usr/bin/env python
import rospy
from picamera import PiCamera
from picamera.array import PiRGBArray
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String
import time
import cv2
import numpy as np
import ros_numpy

sw=480
sh=368
camera=PiCamera()
camera.resolution=(sw, sh)
camera.framerate=1

rawCapture=PiRGBArray(camera, size=(sw,sh))
time.sleep(0.1)

count=0

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

def detect(img):
    global previous

    cascade = cv2.CascadeClassifier("/home/pi/catkin_ws/src/image_node/src/cascade.xml")
    rects = cascade.detectMultiScale(img, 1.012,1, cv2.CASCADE_SCALE_IMAGE,(20,20),maxSize=(50,50))
    detected = ""
    global count;
    count += 1;
    if len(rects) == 0:
        return [], img, detected
    rects[:, 2:] += rects[:, :2]
    if len(rects > 0):
        if (count < 10):
            detected = "Sign Detected000" + str(count)
        elif count >= 10 and  count< 100:
            detected = "Sign Detected00" + str(count)
        elif count >= 100 and count < 1000:
            detected = "Sign Detected0" + str(count)
        else:
            detected = "Sign Detected" + str(count)
    else:
        if (count < 10):
            detected = "No Sign Detected000" + str(count)
        elif count >= 10 and count < 100:
            detected = "No Sign Detected00" + str(count)
        elif count >= 100 and count < 1000:
            detected = "No Sign Detected0" + str(count)
        else:
            detected = "No Sign Detected" + str(count)
    return rects, img, detected


pubtext = rospy.Publisher('imgtext', String, queue_size=10)
pubimage = rospy.Publisher('imagechatter', Image, queue_size=10)
rospy.init_node('image_node', anonymous=True)
rate = rospy.Rate(1)
br = CvBridge()
for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    try:
        image=frame.array

        img = image
        rects,img, detected= detect(img)
        box(rects, img)
        #cv2.imshow("frame", img)
        rospy.loginfo('publishing text')
        pubtext.publish(detected)
        rospy.loginfo('publishing image')
        pubimage.publish(br.cv2_to_imgmsg(img, "bgr8"))
        rate.sleep();
        key=cv2.waitKey(1) &0xFF
        rawCapture.truncate(0)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    except KeyboardInterrupt:
        print("shutting down image node node")
        rospy.signal_shutdown("Ctrl+C pressed")
        sys.exit();

'''def talker():
    pubtext = rospy.Publisher('imgtext', String, queue_size=10)
    pubimage = rospy.Publisher('imagechatter', Image, queue_size=10)
    rospy.init_node('image_node', anonymous=True)
    br = CvBridge()
    capture = cv2.VideoCapture(0)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        try:
            [status,img] = capture.read()
            #img = image
            rects,img, detected= detect(img)
            box(rects, img)

            rospy.loginfo('publishing text')
            pubtext.publish(detected)
            rospy.loginfo('publishing image')
            print(img)
            arr = ros_numpy.numpify(img)
            print("imshow(img)")
            cv2.imshow("frame", img)
            print(arr)
            #pubimage.publish(br.cv2_to_imgmsg(arr, "bgr8"))
            rate.sleep();
        except KeyboardInterrupt:
            print("shutting down image node node")
            rospy.signal_shutdown("Ctrl+C pressed")
            sys.exit();

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass'''
