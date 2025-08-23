from launch import LaunchDescription
from launch_ros.actions import Node
from launch.conditions import LaunchConfigurationEquals, LaunchConfigurationNotEquals
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

ARGUMENTS = [
    DeclareLaunchArgument('chassis_model', default_value='MiniUGV-20A',
                          description='set lingao mobile robot model'),
    DeclareLaunchArgument('imu_type', default_value='onboard_imu',
                          description='IMU Model'),
]

def generate_launch_description():
    pkg_lingao_bringup = get_package_share_directory('lingao_bringup')
    pkg_lingao_description = get_package_share_directory('lingao_description')

    # Launch files
    lingao_base_driver_launch_file = PathJoinSubstitution(
        [pkg_lingao_bringup, 'launch/include', 'lingao_base_driver.launch.py'])

    lingao_imu_launch_file = PathJoinSubstitution(
        [pkg_lingao_bringup, 'launch/include', 'lingao_imu_driver.launch.py'])

    ekf_localization_yaml = PathJoinSubstitution(
        [pkg_lingao_bringup, 'params/ekf_localization.yaml'])

    lingao_base_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(lingao_base_driver_launch_file),
        condition= LaunchConfigurationNotEquals('imu_type', 'onboard_imu'),
        launch_arguments={
            'publish_imu': 'false'
        }.items())

    lingao_base_driver_imu_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(lingao_base_driver_launch_file),
        condition= LaunchConfigurationEquals('imu_type', 'onboard_imu'),
        launch_arguments={
            'publish_imu': 'true'
        }.items())

    lingao_imu_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(lingao_imu_launch_file),
        launch_arguments={
            'chassis_model': LaunchConfiguration('chassis_model'),
            'imu_type': LaunchConfiguration('imu_type'),
            'imu_topic_name': '/imu/data',
            'imu_frame_id': 'imu_frame_id'
        }.items())

    ekf_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[PathJoinSubstitution(ekf_localization_yaml)],
        remappings=[
            ("/odometry/filtered", "/odom"),
        ],)

    lingao_description_launch = IncludeLaunchDescription(
        PathJoinSubstitution([pkg_lingao_description, 'launch', 'description.launch.py']),
        launch_arguments={
            # 'chassis_model': 'MiniUGV-10A'
        }.items())

    return LaunchDescription([
        LaunchDescription(ARGUMENTS),
        lingao_description_launch,
        lingao_base_driver_launch,
        lingao_base_driver_imu_launch,
        lingao_imu_launch,
        ekf_localization_node,
    ])
    