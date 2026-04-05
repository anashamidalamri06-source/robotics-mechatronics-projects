# Create ROS2 package
ros2 pkg create --build-type ament_python robot_controller

# Install dependencies
sudo apt install python3-pynput  # For keyboard controller

# Build package
colcon build

# Source setup
source install/setup.bash
