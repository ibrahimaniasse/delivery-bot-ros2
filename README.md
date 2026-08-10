# 🤖 Delivery Bot ROS2

A ROS2-based autonomous delivery robot with AI-powered navigation using Google Gemini.

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Gazebo](https://img.shields.io/badge/Gazebo-Fortress-orange)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-purple)

## 🎯 Features

- **Autonomous Navigation**: AI-powered obstacle avoidance and path planning
- **LiDAR Integration**: 360° laser scanning for environment perception
- **Gazebo Simulation**: Full simulation environment for testing
- **RViz Visualization**: Real-time robot state visualization
- **Google Gemini AI**: Intelligent decision-making for navigation

## 📁 Project Structure

```
delivery_bot_ws/
├── src/
│   ├── delivery_bot_ai/          # AI navigation package
│   │   ├── delivery_bot_ai/
│   │   │   └── obstacle_avoidance_agent.py
│   │   └── launch/
│   │       └── ai_nav.launch.py
│   ├── delivery_bot_description/  # Robot URDF/Xacro
│   │   ├── urdf/
│   │   │   └── robot.urdf.xacro
│   │   ├── config/
│   │   │   └── display.rviz
│   │   └── launch/
│   │       └── display.launch.py
│   └── delivery_bot_gazebo/       # Gazebo simulation
│       ├── worlds/
│       │   └── delivery_zone.sdf
│       └── launch/
│           └── sim.launch.py
```

## 🛠️ Prerequisites

- Ubuntu 22.04
- ROS2 Humble
- Gazebo Fortress
- Python 3.10+

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ibrahimaniasse/delivery-bot-ros2.git
cd delivery-bot-ros2
```

2. **Install dependencies**
```bash
cd delivery_bot_ws
rosdep install --from-paths src --ignore-src -r -y
```

3. **Build the workspace**
```bash
colcon build
source install/setup.bash
```

4. **Set up Google Gemini API** (for AI features)
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## 🚀 Usage

### Launch Simulation
```bash
ros2 launch delivery_bot_gazebo sim.launch.py
```

### Launch RViz Visualization
```bash
ros2 launch delivery_bot_description display.launch.py
```

### Launch AI Navigation
```bash
ros2 launch delivery_bot_ai ai_nav.launch.py
```

## 🧠 AI Navigation

The robot uses Google Gemini AI for intelligent obstacle avoidance. The AI agent:
- Analyzes LiDAR scan data
- Makes navigation decisions based on obstacle positions
- Outputs velocity commands for smooth navigation

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Ibrahima NIASSE** — [GitHub](https://github.com/ibrahimaniasse)

---

⭐ If you find this project useful, please consider giving it a star!
