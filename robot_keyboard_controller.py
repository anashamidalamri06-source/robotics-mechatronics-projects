#!/usr/bin/env python3
"""
Interactive keyboard-based robot controller
Press keys to control the robot movement
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import threading
from pynput import keyboard


class KeyboardRobotController(Node):
    """ROS2 node for keyboard-controlled robot."""
    
    def __init__(self):
        super().__init__('keyboard_robot_controller')
        
        # Parameters
        self.declare_parameter('linear_vel', 0.5)
        self.declare_parameter('angular_vel', 0.5)
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        
        self.linear_vel = self.get_parameter('linear_vel').value
        self.angular_vel = self.get_parameter('angular_vel').value
        
        # Publisher
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            self.get_parameter('cmd_vel_topic').value,
            10
        )
        
        # Velocity storage
        self.twist = Twist()
        
        # Listener thread
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
        # Publish timer
        self.timer = self.create_timer(0.1, self.publish_velocity)
        
        self.print_controls()
    
    def on_key_press(self, key):
        """Handle keyboard input."""
        try:
            # Arrow keys or WASD
            if key == keyboard.Key.up or (hasattr(key, 'char') and key.char == 'w'):
                self.twist.linear.x = self.linear_vel
                self.twist.angular.z = 0.0
            elif key == keyboard.Key.down or (hasattr(key, 'char') and key.char == 's'):
                self.twist.linear.x = -self.linear_vel
                self.twist.angular.z = 0.0
            elif key == keyboard.Key.left or (hasattr(key, 'char') and key.char == 'a'):
                self.twist.linear.x = 0.0
                self.twist.angular.z = self.angular_vel
            elif key == keyboard.Key.right or (hasattr(key, 'char') and key.char == 'd'):
                self.twist.linear.x = 0.0
                self.twist.angular.z = -self.angular_vel
            elif hasattr(key, 'char') and key.char == ' ':
                # Space to stop
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.get_logger().info('Stopped')
            elif key == keyboard.Key.esc:
                # ESC to exit
                self.get_logger().info('Exiting...')
                return False
        except AttributeError:
            pass
    
    def publish_velocity(self):
        """Publish velocity commands."""
        self.cmd_vel_pub.publish(self.twist)
    
    def print_controls(self):
        """Print control instructions."""
        self.get_logger().info('=' * 50)
        self.get_logger().info('Keyboard Robot Controller')
        self.get_logger().info('=' * 50)
        self.get_logger().info('Controls:')
        self.get_logger().info('  W / Up Arrow    - Move Forward')
        self.get_logger().info('  S / Down Arrow  - Move Backward')
        self.get_logger().info('  A / Left Arrow  - Turn Left')
        self.get_logger().info('  D / Right Arrow - Turn Right')
        self.get_logger().info('  Space          - Stop')
        self.get_logger().info('  ESC            - Exit')
        self.get_logger().info('=' * 50)


def main(args=None):
    rclpy.init(args=args)
    controller = KeyboardRobotController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.listener.stop()
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
