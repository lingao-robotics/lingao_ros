from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


ARGUMENTS = [
    DeclareLaunchArgument('odom_frame_id', default_value='odom',
                          description='Odometry frame id'),
    DeclareLaunchArgument('base_frame_id', default_value='base_link',
                          description='Base frame id'),
    DeclareLaunchArgument('pub_odom_tf', default_value='false',
                          description='Publish Odometry transform'),
    DeclareLaunchArgument('linear_scale', default_value='1.0',
                          description='Linear Velocity Calibration Scale'),
    DeclareLaunchArgument('angular_scale', default_value='1.0',
                          description='Angular velocity calibration scale'),
    DeclareLaunchArgument('stamped_control', default_value='false',
                          description='Subscribe cmd_vel as geometry_msgs/TwistStamped'),
    DeclareLaunchArgument("publish_imu", default_value='false',
                          description="Publish onboard imu"),
    DeclareLaunchArgument("odom_topic_remap", default_value="raw_odom",
                          description="Remap odometry topic name"),
    DeclareLaunchArgument("imu_topic_remap", default_value="imu/onboard_imu",
                          description="Remap onboard imu topic name")
]

def generate_launch_description():

    lingao_base_node = Node(
        package='lingao_base',
        name='lingao_base_driver',
        executable='lingao_base_node',
        output='screen',
        parameters=[{
            "port_name": '/dev/lingao',
            "port_baud": 230400,
            "odom_frame_id": LaunchConfiguration("odom_frame_id"),
            "base_frame_id": LaunchConfiguration("base_frame_id"),
            "pub_odom_tf": LaunchConfiguration("pub_odom_tf"),
            "linear_scale": LaunchConfiguration("linear_scale"),
            "angular_scale": LaunchConfiguration("angular_scale"),
            "stamped_control": LaunchConfiguration("stamped_control"),
            "publish_imu": LaunchConfiguration("publish_imu"),
            "imu_frame_id": "imu_link",
            "imu_calibrate_gyro": True,
            "imu_cailb_samples": 300,
            "cmd_vel_sub_timeout": 1.0,
        }],
        remappings=[
            ("~/odom", LaunchConfiguration("odom_topic_remap")),
            ("~/onboard_imu", LaunchConfiguration("imu_topic_remap")),
            ("~/cmd_vel", "cmd_vel"),
        ],
        )

    return LaunchDescription(ARGUMENTS + [
        lingao_base_node
    ])
