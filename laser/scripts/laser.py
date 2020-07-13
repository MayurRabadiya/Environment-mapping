#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist




x = 0
th = 0
status = 0
count = 0
speed = 0.5
turn = 1

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)


def callback(msg):
    fl = msg.ranges[360]
    ll = msg.ranges[150]
    rl = msg.ranges[550]
    global x
    global th
    global count
    while(1):
        if fl <= 1 and rl <= 1  and ll >= 1:
            x = 0
            th = 1
            count = 0
        elif fl <= 1 and rl >= 1  and ll <= 1:
            x = 1
            th = -1
            count = 0
        elif fl <= 1 and rl <= 1  and ll <= 1:
            x = 1
            th = 0
            count = 0
        else:
            x= 0
            th = 0
            count = 0

       


if __name__ == '__main__':
    try:
        
        acc = 0.1
        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0
        #fl = 0.5
        #rl = 0.1
        #ll = 1.1
        rospy.init_node('robot_cleaner')
        pub = rospy.Publisher('~cmd_vel', Twist, queue_size=5)
        

    
        sub = rospy.Subscriber('/mybot/laser/scan', LaserScan, callback)
        rate = rospy.Rate(10)

    #Receiveing the user's input
    
        print vels(speed,turn)
        while not rospy.is_shutdown():
            print x
            print th
            target_speed = speed * x
            target_turn = turn * th
            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            twist = Twist()
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
            pub.publish(twist)
            rate.sleep()

    except rospy.ROSInterruptException:
        x= 1
        th=0
        count=0