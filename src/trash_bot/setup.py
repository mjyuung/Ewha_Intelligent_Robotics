from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'trash_bot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
        (os.path.join('share', package_name, 'config'), glob('config/*.xml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.stl')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Minjoo Yoon',
    maintainer_email='yoonminjoo03@ewhain.net',
    description='mobile trash can robot',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'waypoint_navigator = trash_bot.09_waypoint_navigator:main',
            'trash_lidar_subscriber = trash_bot.trash_lidar_subscriber:main',
            'mission_manager = trash_bot.mission_manager:main',
            'trash_spawner = trash_bot.trash_spawner:main',
        ],
    },
)
