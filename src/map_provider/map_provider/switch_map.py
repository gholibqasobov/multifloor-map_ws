#!/usr/bin/env python3

import sys
import time
import subprocess
import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty

class MapSwitcher(Node):
    def __init__(self):
        super().__init__('map_switcher')
        self.declare_parameter('map_dir', 'src/map_provider/maps')  # Set path to maps folder

    def switch_map(self, floor_number):
        map_dir = self.get_parameter('map_dir').get_parameter_value().string_value
        map_file = f"{map_dir}/floor_{floor_number}.yaml"

        # Kill existing map_server
        subprocess.run(["pkill", "-f", "nav2_map_server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)  # Wait for proper shutdown

        # Launch new map_server
        subprocess.Popen([
            "ros2", "run", "nav2_map_server", "map_server",
            "--ros-args", "-r", "__node:=map_server",
            "-p", f"yaml_filename:={map_file}"
        ])
        time.sleep(2)  # Allow time for map_server to launch
        
        # Configure map_server lifecycle node
        subprocess.run(["ros2", "lifecycle", "set", "/map_server", "configure"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
	
        # Activate map_server lifecycle node
        subprocess.run(["ros2", "lifecycle", "set", "/map_server", "activate"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.get_logger().info(f"Switched to map: {map_file}")

        

def main(args=None):
    rclpy.init(args=args)
    node = MapSwitcher()
    
    if len(sys.argv) < 2:
        print("Usage: ros2 run <your_package> switch_map.py <floor_number>")
        sys.exit(1)
    
    floor_number = sys.argv[1]
    success = node.switch_map(floor_number)

    if success:
        node.destroy_node()
    else:
        rclpy.shutdown()

if __name__ == "__main__":
    main()

