from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

ARGUMENTS = [
    DeclareLaunchArgument('publish_imu', default_value='false', description='Publish IMU'),
    DeclareLaunchArgument(
        'stamped_control',
        default_value='false',
        description='Use TwistStamped on cmd_vel',
    ),
]

def generate_launch_description():
    pkg_lingao_base = get_package_share_directory('lingao_base')

    # Launch files
    lingao_base_driver_launch_file = PathJoinSubstitution(
        [pkg_lingao_base, 'launch', 'lingao_base_driver.launch.py'])

    lingao_base_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([lingao_base_driver_launch_file]),
        launch_arguments={
            'publish_imu': LaunchConfiguration('publish_imu'),
            'pub_odom_tf': 'false',
            'linear_scale': '1.0',
            'angular_scale': '1.0',
            'stamped_control': LaunchConfiguration('stamped_control'),
        }.items())

    return LaunchDescription(ARGUMENTS + [
        lingao_base_driver_launch
    ])
    
