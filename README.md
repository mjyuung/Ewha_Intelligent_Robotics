2026-1 이화여자대학교 지능형 로보틱스 프로젝트

# 프로젝트 설명

## 실내 쓰레기 자동 수집 시스템

본 프로젝트의 목표는 건물 내 비치된 쓰레기통이 스스로 채워진 정도를 측정해 특정 양 이상이 채워지면 배출 위치를 찾아가 내용물을 배출하고 다시 돌아오는 것이다. 이를 통해 학교나 회사 같이 유동 인구가 많고 쓰레기가 많이 발생하는 장소에서 청소 노동자의 부담을 줄이고 사용자가 쾌적한 공간을 사용할 수 있도록 한다.

# 패키지 구조

```
Ewha_Intelligent_Robotics
├── map
│   ├── ewha_office_map.pgm          # Occupancy grid map image
│   └── ewha_office_map.yaml         # Map metadata
│
├── src
│   └── trash_bot
│       ├── config/                  # Configuration files (.yaml, .rviz)
│       ├── launch/                  # ROS2 launch files
│       ├── meshes/                  # Robot mesh files (.stl)
│       ├── trash_bot/               # Python nodes and scripts
│       ├── urdf/                    # Robot URDF
│       ├── worlds/                  # Gazebo world files (.sdf)
│       │
│       ├── package.xml              # Package manifest
│       ├── setup.cfg                # Python package configuration
│       └── setup.py                 # Package installation script
│
├── .gitignore
└── README.md
```

# 실행하기

```bash
colcon build --symlink-install
source install/setup.bash
export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:{your_workspace_path}/install/trash_bot/share
ros2 launch trash_bot 09_navigation.launch.py
```

# AI 사용 내역

- Rviz TF Frame 에러 디버깅
- Gazebo Fortress 패키지 export 문제 디버깅
- Nav2 패키지 작동 에러 디버깅
- 요구사항 바탕으로 mission_manager 노드 구조 설계

# 참고한 자료

- [https://docs.nav2.org/](https://docs.nav2.org/) nav2 공식 문서
- https://github.com/SteveMacenski/slam_toolbox 깃허브 slam_toolbox 리드미 파일
- [https://gazebosim.org/docs/latest/fuel_insert/](https://gazebosim.org/docs/latest/fuel_insert/) Gazebo Fuel 모델 인서트 가이드
- [https://extensions.blender.org/add-ons/linkforge/](https://extensions.blender.org/add-ons/linkforge/) Blender Extension LinkForge 가이드
- [https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/LaserScan.html](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/LaserScan.html) ROS LaserScan 타입
- [https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/JointState.html](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/JointState.html) ROS JointState 타입
