import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    trash_share   = get_package_share_directory('trash_bot')
    stb_share    = get_package_share_directory('slam_toolbox')

    world_path  = os.path.join(trash_share,   'worlds', 'trash_world.sdf')
    slam_params = os.path.join(trash_share,   'config', '09_slam_params.yaml')
    rviz_config = os.path.join(trash_share,   'config', '09_slam.rviz')

    return LaunchDescription([

        # ── 1. Simulation stack (Gazebo + bridge + RSP + spawn) ─────────────
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(trash_share, 'launch', '09_trash_robot.launch.py')
            ),
            launch_arguments={
                'world':       world_path,
                'launch_rviz': 'false',
            }.items(),
        ),

        # ── 2. slam_toolbox — online asynchronous mapping ───────────────────
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(stb_share, 'launch', 'online_async_launch.py')
            ),
            launch_arguments={
                'slam_params_file': slam_params,
                'use_sim_time':     'true',
            }.items(),
        ),

        # ── 3. RViz2 with SLAM-focused config (Map + LaserScan + TF) ───────
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
    ])
