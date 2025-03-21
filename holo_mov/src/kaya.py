#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class KayaControlNode:
    def __init__(self):
        rospy.init_node('kaya_control_node', anonymous=True)

        # Publisher to send velocity commands to the Kaya robot
        self.cmd_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Define movement sequence
        self.movement_sequence = [
            'move_left',
            'stop',
        ]

        '''
        'move_left',
            'move_right',
            'rotate_left',
            'backward',
            'rotate_right'
        '''

        self.current_index = 0
        self.sequence_duration = 40.0  # Duration for each movement in seconds
        self.start_time = rospy.Time.now()

        # Define velocities for different movements
        self.velocity = Twist()

        # Set loop rate
        self.rate = rospy.Rate(1)  # 1 Hz (1 second per iteration)

    def move_kaya(self):
        while not rospy.is_shutdown():
            # Determine the elapsed time for current movement
            elapsed_time = (rospy.Time.now() - self.start_time).to_sec()

            # Check if it's time to switch to the next movement in the sequence
            if elapsed_time > self.sequence_duration:
                self.current_index = (self.current_index + 1) % len(self.movement_sequence)
                self.start_time = rospy.Time.now()

            # Set velocity based on the current movement in the sequence
            self.set_movement(self.movement_sequence[self.current_index])

            # Publish the velocity command
            self.cmd_vel_publisher.publish(self.velocity)
            rospy.loginfo(f'Movement State: {self.movement_sequence[self.current_index]} | '
                          f'Publishing: x={self.velocity.linear.x}, y={self.velocity.linear.y}, z={self.velocity.angular.z}')
            
            self.rate.sleep()

    def set_movement(self, state):
        # Set the velocity based on the movement state
        if state == 'forward':
            self.velocity.linear.x = 0.2
            self.velocity.linear.y = 0.0
            self.velocity.angular.z = 0.0
        elif state == 'backward':
            self.velocity.linear.x = -0.2
            self.velocity.linear.y = 0.0
            self.velocity.angular.z = 0.0
        elif state == 'move_left':
            self.velocity.linear.x = 0.0
            self.velocity.linear.y = 0.3
            self.velocity.angular.z = 0.0
        elif state == 'move_right':
            self.velocity.linear.x = 0.0
            self.velocity.linear.y = -0.3
            self.velocity.angular.z = 0.0
        elif state == 'rotate_left':
            self.velocity.linear.x = 0.0
            self.velocity.linear.y = 0.0
            self.velocity.angular.z = 0.2
        elif state == 'rotate_right':
            self.velocity.linear.x = 0.0
            self.velocity.linear.y = 0.0
            self.velocity.angular.z = -0.2
        elif state == 'stop':
            self.velocity.linear.x = 0.0
            self.velocity.linear.y = 0.0
            self.velocity.angular.z = 0.0
        else:
            # Default to no movement if state is unknown
            self.velocity.linear.x = 0.0
            self.velocity.angular.z = 0.0

def main():
    node = KayaControlNode()
    try:
        node.move_kaya()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
