import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    lingao_chassis_model = os.getenv('LINGAO_MODEL', "MiniUGV-20A")
    lingao_imu_type = os.getenv('LINGAO_IMU', "onboard_imu")
    lingao_lidar_type = os.getenv('LINGAO_LIDAR', "nvilidar")

    # lingao_imu_type   = "onboard_imu"
    # lingao_lidar_type = "nvilidar"
    # lingao_chassis_model = "MiniUGV-20A"

    pkg_lingao_bringup = get_package_share_directory('lingao_bringup')

    # Launch files
    lingao_bringup_launch_file = PathJoinSubstitution(
        [pkg_lingao_bringup, 'launch', 'bringup.launch.py'])

    lingao_lidar_launch_file = PathJoinSubstitution(
        [pkg_lingao_bringup, 'launch/include', 'lingao_lidar_driver.launch.py'])

    lingao_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([lingao_bringup_launch_file]),
        launch_arguments={
            'chassis_model': lingao_chassis_model,
            'imu_type': lingao_imu_type,
        }.items())

    lingao_lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([lingao_lidar_launch_file]),
        launch_arguments={
            'chassis_model': lingao_chassis_model,
            'lidar_type': lingao_lidar_type,
            'lidar_topic_name': 'scan',
            'lidar_frame_id': 'laser_link',
        }.items())

    return LaunchDescription([
        lingao_bringup_launch,
        lingao_lidar_launch
    ])
