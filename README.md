# multifloor-map_ws
1. **Clone the repository**:
   ```bash
   git clone https://github.com/gholibqasobov/multifloor-map_ws.git
   ```

2. **Build the packages**:
   ```bash
      colcon build --symlink-install
      ```

3. **In one terminal open rviz2, add map and assign topic /map. In another terminal run the following command:**:
   ```bash
        ros2 run map_provider swtich_map 1
      ```

Number 1 here means floor number 1. Save the maps in this structure:
   ```bash
   floor_{number}.pgm, floor_{number}.yaml 
   ```
