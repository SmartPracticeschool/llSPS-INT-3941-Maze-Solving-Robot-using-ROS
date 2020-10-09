#! /usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub= None
def clbk_laser(msg):
        regions = {
            'right':  min(min(msg.ranges[0:143]), 3),
            'fright': min(min(msg.ranges[144:287]), 3),
            'front':  min(min(msg.ranges[288:431]), 3),
            'fleft':  min(min(msg.ranges[432:575]), 3),
            'left':   min(min(msg.ranges[576:713]), 3),
        }
    
        take_action(regions)
def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    if regions['front'] > 1 and regions['fleft'] > 0.5 and regions['fright'] > 0.5 and regions['left'] > 0.5 and regions['right'] > 0.5:
        state_description = 'case 1 - nothing'
        linear_x = -0.2
        angular_z = 0
    
       
    elif regions['front'] < 1 and regions['fleft'] > 0.5 and regions['fright'] < 0.5 and regions['left'] > 0.5 and regions['right'] < 0.5:
        state_description = 'case 3 - left >'
        linear_x = 0
        angular_z = 0.5
    elif regions['front'] < 1 and regions['fleft'] < 0.5 and regions['fright'] > 0.5 and regions['left'] < 0.5 and regions['right'] > 0.5:
        state_description = 'case 4 - right >'
        linear_x = 0
        angular_z =-0.5
    elif regions['front'] < 1 and regions['fleft'] < 0.5 and regions['fright'] < 0.5 and regions['left'] < 0.5 and regions['right'] < 0.5:
        state_description = 'case 5 - back'
        linear_x = 0.2
        angular_z = 0
    elif regions['front'] <1 and regions['fleft'] < 0.5 and regions['fright'] < 0.5 and regions['left'] < 0.5 and regions['right'] > 0.5:
        state_description = 'case 6 - front and fleft and fright <'
        linear_x = 0
        angular_z = - 0.5
    elif regions['front'] < 1 and regions['fleft'] < 0.5 and regions['fright'] < 0.5 and regions['left'] > 0.5 and regions['right'] < 0.5 :
        state_description = 'case 7 - front and fleft and fright <'
        linear_x = 0
        angular_z = 0.5
    elif regions['front'] > 1 and regions['fleft'] > 0.5 and regions['fright'] < 0.5 and regions['left']>0.5 and regions['right']>0.5:
        state_description = 'case 8 - fright <'
        linear_x = 0
        angular_z = 0.5
    elif regions['front'] > 1 and regions['fleft'] < 0.5 and regions['fright'] > 0.5 and regions['left']>0.5 and regions['right']>0.5:
        state_description = 'case 8 - fleft <'
        linear_x = 0
        angular_z = 0.5
    else:
        state_description = 'unknown case'
       # rospy.loginfo(regions)
        linear_x = 0.1
        angular_z = 0

    rospy.loginfo(state_description)
    msg.linear.x = -linear_x
    msg.angular.z = angular_z
    pub.publish(msg)
def main():
        global pub
    
        rospy.init_node('laser_motion')    
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)    
        sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, clbk_laser)    
        rospy.spin()
if __name__ == '__main__':
    main()