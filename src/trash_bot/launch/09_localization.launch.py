import os
import random
import math
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory



def launch_setup(context, *args, **kwargs):
    trash_share   = get_package_share_directory('trash_bot')

    world_path   = os.path.join(trash_share, 'worlds', 'trash_world.sdf')
    amcl_params  = os.path.join(trash_share, 'config', '09_amcl_params.yaml')
    rviz_config  = os.path.join(trash_share, 'config', '09_localization.rviz')

    map_yaml = LaunchConfiguration('map').perform(context)

    # Random spawn pose inside the closed room
    x   = -4.7
    y   = 2.5
    yaw = 0
    print(f'[localization.launch] Random spawn: x={x}, y={y}, yaw={yaw:.3f} rad')

    return [
        # ── 1. Simulation stack (Gazebo + bridge + RSP + spawn at random pose)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(trash_share, 'launch', '09_trash_robot.launch.py')
            ),
            launch_arguments={
                'world':       world_path,
                'launch_rviz': 'false',
                'spawn_x':     str(x),
                'spawn_y':     str(y),
                'spawn_yaw':   str(yaw),
            }.items(),
        ),

        # ── 2. Map server — serves the saved .pgm map on /map ───────────────
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[{'yaml_filename': map_yaml, 'use_sim_time': True}],
            output='screen',
        ),

        # ── 3. AMCL — particle filter localisation ──────────────────────────
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            parameters=[
                amcl_params,
                {'use_sim_time': True,
                 'initial_pose.x':   0.0,
                 'initial_pose.y':   0.0,
                 'initial_pose.yaw': 0.0},
            ],
            output='screen',
        ),

        # ── 4. Lifecycle manager — activates map_server and amcl ────────────
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            parameters=[{
                'use_sim_time': True,
                'autostart':    True,
                'node_names':   ['map_server', 'amcl'],
            }],
            output='screen',
        ),

        # ── 5. RViz2 ────────────────────────────────────────────────────────
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=os.path.expanduser('/home/minj/ros2_ws/map/ewha_office_map.yaml'),
            description='Absolute path to a nav2 map YAML file',
        ),
        OpaqueFunction(function=launch_setup),
    ])
