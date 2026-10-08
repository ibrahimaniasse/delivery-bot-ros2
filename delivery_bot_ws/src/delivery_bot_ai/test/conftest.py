import sys
from unittest.mock import MagicMock

# Mock ROS 2 packages so tests can execute without a sourced ROS environment
ros_modules = [
    "rclpy",
    "rclpy.node",
    "rclpy.qos",
    "sensor_msgs",
    "sensor_msgs.msg",
    "nav_msgs",
    "nav_msgs.msg",
    "geometry_msgs",
    "geometry_msgs.msg",
    "std_msgs",
    "std_msgs.msg",
]

for mod_name in ros_modules:
    if mod_name not in sys.modules:
        mock = MagicMock()
        # Provide base Node class for inheritance
        if mod_name == "rclpy.node":
            mock.Node = object
        sys.modules[mod_name] = mock
