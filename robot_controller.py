#!/usr/bin/env python3
"""
ROS2 Mobile Robot Velocity Controller Node
Controls a mobile robot by publishing velocity commands to cmd_vel topic
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys


class RobotControllerNode(Node):
    """
    A ROS2 node that controls a mobile robot's velocity.
    
    Publishers:
        - /cmd_vel: geometry_msgs/Twist messages for robot velocity control
    
    Parameters:
        - linear_vel: Linear velocity (m/s) - default: 0.5
        - angular_vel: Angular velocity (rad/s) - default: 0.5
        - max_linear_vel: Maximum linear velocity - default: 1.0
        - max_angular_vel: Maximum angular velocity - default: 1.0
    """
    
    def __init__(self):
        super().__init__('robot_controller')
        
        # Declare and get parameters
        self.declare_parameter('linear_vel', 0.5)
        self.declare_parameter('angular_vel', 0.5)
        self.declare_parameter('max_linear_vel', 1.0)
        self.declare_parameter('max_angular_vel', 1.0)
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        
        self.linear_vel = self.get_parameter('linear_vel').value
        self.angular_vel = self.get_parameter('angular_vel').value
        self.max_linear_vel = self.get_parameter('max_linear_vel').value
        self.max_angular_vel = self.get_parameter('max_angular_vel').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        
        # Create publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            cmd_vel_topic,
            10
        )
        
        # Create a timer to publish velocity commands periodically
        self.timer = self.create_timer(0.1, self.velocity_callback)
        
        self.get_logger().info(f'Robot Controller initialized')
        self.get_logger().info(f'Publishing to topic: {cmd_vel_topic}')
        self.get_logger().info(f'Linear velocity: {self.linear_vel} m/s')
        self.get_logger().info(f'Angular velocity: {self.angular_vel} rad/s')
    
    def velocity_callback(self):
        """Publish velocity commands to the robot."""
        twist = Twist()
        twist.linear.x = self.linear_vel
        twist.angular.z = self.angular_vel
        
        self.cmd_vel_pub.publish(twist)
        self.get_logger().debug(
            f'Published velocity - Linear: {twist.linear.x}, Angular: {twist.angular.z}'
        )
    
    def move_forward(self, speed=None):
        """
        Move the robot forward.
        
        Args:
            speed: Linear velocity (m/s). If None, uses default.
        """
        if speed is None:
            speed = self.linear_vel
        
        speed = self.clamp_velocity(speed, self.max_linear_vel)
        self.linear_vel = speed
        self.angular_vel = 0.0
        self.get_logger().info(f'Moving forward at {speed} m/s')
    
    def move_backward(self, speed=None):
        """
        Move the robot backward.
        
        Args:
            speed: Linear velocity magnitude (m/s). If None, uses default.
        """
        if speed is None:
            speed = self.linear_vel
        
        speed = self.clamp_velocity(speed, self.max_linear_vel)
        self.linear_vel = -speed
        self.angular_vel = 0.0
        self.get_logger().info(f'Moving backward at {speed} m/s')
    
    def turn_left(self, angular_speed=None):
        """
        Rotate the robot left (counter-clockwise).
        
        Args:
            angular_speed: Angular velocity (rad/s). If None, uses default.
        """
        if angular_speed is None:
            angular_speed = self.angular_vel
        
        angular_speed = self.clamp_velocity(angular_speed, self.max_angular_vel)
        self.linear_vel = 0.0
        self.angular_vel = angular_speed
        self.get_logger().info(f'Turning left at {angular_speed} rad/s')
    
    def turn_right(self, angular_speed=None):
        """
        Rotate the robot right (clockwise).
        
        Args:
            angular_speed: Angular velocity (rad/s). If None, uses default.
        """
        if angular_speed is None:
            angular_speed = self.angular_vel
        
        angular_speed = self.clamp_velocity(angular_speed, self.max_angular_vel)
        self.linear_vel = 0.0
        self.angular_vel = -angular_speed
        self.get_logger().info(f'Turning right at {angular_speed} rad/s')
    
    def stop(self):
        """Stop the robot."""
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        self.get_logger().info('Robot stopped')
    
    def set_velocity(self, linear_x, angular_z):
        """
        Set custom velocity values.
        
        Args:
            linear_x: Linear velocity (m/s)
            angular_z: Angular velocity (rad/s)
        """
        self.linear_vel = self.clamp_velocity(linear_x, self.max_linear_vel)
        self.angular_vel = self.clamp_velocity(angular_z, self.max_angular_vel)
        self.get_logger().info(
            f'Velocity set - Linear: {self.linear_vel}, Angular: {self.angular_vel}'
        )
    
    @staticmethod
    def clamp_velocity(value, max_value):
        """
        Clamp velocity to maximum value.
        
        Args:
            value: Velocity value
            max_value: Maximum absolute velocity
            
        Returns:
            Clamped velocity
        """
        if value > max_value:
            return max_value
        elif value < -max_value:
            return -max_value
        return value


def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
        node.stop()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
