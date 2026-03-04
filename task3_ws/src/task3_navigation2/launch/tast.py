from launch import LaunchDescription
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
import launch

def generate_launch_description():
    
     #获取默认的nav路径
    task3_nav2_packages_path=get_package_share_directory('task3_navigation2')
    nav2_bringup_dir=get_package_share_directory("nav2_bringup")
    rviz_config_dir=os.path.join(nav2_bringup_dir,'rviz2','nav2_default_view.rviz')
    #配置launch参数：
    use_sim_time=launch.substitutions.LaunchConfiguration(
        'use_sim_time',default='true'
    )
    map_yaml_path=launch.substitutions.LaunchConfiguration(
        'map',default=os.path.join(task3_nav2_packages_path,'maps','map.yaml')
    )
    nav2_param_path=launch.substitutions.LaunchConfiguration(
        'param_file',default=os.path.join(task3_nav2_packages_path,'config','nav2_params.yaml')
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time',default_value=use_sim_time,description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('map',default_value=map_yaml_path,description='Full path to map file to load'),
        DeclareLaunchArgument('params_file',default_value=nav2_param_path,description='Full path to param file to load'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_bringup_dir,'/launch','/bringup_launch.py']),
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path}.items(),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
    ])