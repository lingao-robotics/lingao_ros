#!/usr/bin/python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import LaunchConfigurationEquals


ARGUMENTS = [
    DeclareLaunchArgument('chassis_model', default_value='MiniUGV-20A',
                          description='Lidar topic name'),
    DeclareLaunchArgument('lidar_topic_name', default_value='scan',
                          description='Lidar topic name'),
    DeclareLaunchArgument('lidar_frame_id', default_value='laser_link',
                          description='Lidar frame id'),
]


def generate_launch_description():

    rplidar_s2_node = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        output='screen',
        parameters=[{
            'channel_type': 'serial',
            'serial_port': '/dev/rplidar',
            'serial_baudrate': 1000000,
            'frame_id': LaunchConfiguration('lidar_frame_id'),
            'inverted': False,
            'angle_compensate': True,
            'scan_mode': 'DenseBoost',
        }],
        remappings=[('scan', LaunchConfiguration('lidar_topic_name'))],
    )

    tf2_miniugv_20a_node = Node(
        condition=LaunchConfigurationEquals('chassis_model', 'MiniUGV-20A'),
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_pub_laser',
        arguments=["0.04", "0", "0.138", "3.14159", "0", "0", "base_link", LaunchConfiguration('lidar_frame_id')],
    )

    return LaunchDescription(ARGUMENTS + [
        rplidar_s2_node,
        tf2_miniugv_20a_node,
    ])
