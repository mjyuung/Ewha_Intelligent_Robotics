import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    trash_share          = get_package_share_directory('trash_bot')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    world_path  = os.path.join(trash_share, 'worlds', 'trash_world.sdf')
    rviz_config = os.path.join(trash_share, 'config', 'trash_bot.rviz')
    urdf_path  = os.path.join(trash_share, 'urdf', 'moving_trashbot.urdf')
    bridge_yaml = os.path.join(trash_share, 'config', '09_bridge.yaml')

    x   = -4.7
    y   = 2.5
    yaw = 0.0

    with open(urdf_path, 'r') as f:
        robot_description = f.read()
    
    print(f'[navigation.launch] Random spawn: x={x}, y={y}, yaw={yaw:.3f} rad')

    return LaunchDescription([
        DeclareLaunchArgument('world',       default_value=world_path),
        DeclareLaunchArgument('launch_rviz', default_value='true'),
        DeclareLaunchArgument('spawn_x',     default_value='-4.7'),
        DeclareLaunchArgument('spawn_y',     default_value='2.5'),
        DeclareLaunchArgument('spawn_yaw',   default_value='0'),

        # Gazebo Fortress
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments=[('gz_args', ['-r ', LaunchConfiguration('world')])],
        ),

        # Bridge: all topics defined in config/bridge.yaml
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'config_file': bridge_yaml}],
            output='screen',
        ),

        # Publish robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
            output='screen',
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description', '-name', 'trash_bot',
                '-x', LaunchConfiguration('spawn_x'),
                '-y', LaunchConfiguration('spawn_y'),
                '-z', '0.2',
                '-Y', LaunchConfiguration('spawn_yaw'),
            ],
            output='screen',
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            condition=IfCondition(LaunchConfiguration('launch_rviz')),
            output='screen',
        ),
    ])
