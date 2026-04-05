from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_controller',
            executable='robot_controller',
            name='robot_controller',
            output='screen',
            parameters=[
                {'linear_vel': 0.5},
                {'angular_vel': 0.5},
                {'max_linear_vel': 1.0},
                {'max_angular_vel': 1.0},
                {'cmd_vel_topic': '/cmd_vel'},
            ],
        ),
    ])
