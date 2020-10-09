#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

def clbk_laser(msg):
    # 720/5 = 144
    regions = [ 
      min(min(msg.ranges[0:143]),15),
      min(min(msg.ranges[144:287]),15),
      min(min(msg.ranges[288:431]),15),
      min(min(msg.ranges[432:575]),15),
      min(min(msg.ranges[576:713]),15),
     ]
    rospy.loginfo(regions)

def main():
    rospy.init_node('readinglaser')
    sub= rospy.Subscriber("/m2wr/laser/scan", LaserScan, clbk_laser)

    rospy.spin()

if __name__ == '__main__':
    main()