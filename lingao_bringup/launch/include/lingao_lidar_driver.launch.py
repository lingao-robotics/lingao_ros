from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

ARGUMENTS = [
    DeclareLaunchArgument('chassis_model', default_value='MiniUGV-20A',
                          description='Lidar topic name'),
    DeclareLaunchArgument('lidar_type', default_value='nvilidar',
                          description='Lidar Model'),
    DeclareLaunchArgument('lidar_topic_name', default_value='scan',
                          description='Lidar topic name'),
    DeclareLaunchArgument('lidar_frame_id', default_value='laser_link',
                          description='Lidar frame id'),
]

def generate_launch_description():

    pkg_lingao_bringup = get_package_share_directory('lingao_bringup')

    # Launch files
    lidar_launch_dir = PathJoinSubstitution(
        [pkg_lingao_bringup, 'launch/include/lidar/'])
    
    imu_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([lidar_launch_dir, 'lidar_driver_' ,LaunchConfiguration('lidar_type'),'.launch.py']),
        launch_arguments={
            'chassis_model': LaunchConfiguration('chassis_model'),
            'topic_name': LaunchConfiguration('lidar_topic_name'),
            'frame_id': LaunchConfiguration('lidar_frame_id'),
        }.items())

    return LaunchDescription([
        LaunchDescription(ARGUMENTS),
        imu_launch
    ])