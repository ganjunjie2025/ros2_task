import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    
     #获取默认的urdf路径
    urdf_packages_path=get_package_share_directory('robot_description')
    default_xacro_path=os.path.join(urdf_packages_path,'urdf','easy_robot','easy_robot.xacro')
    default_gazebo_world_path=os.path.join(urdf_packages_path,'world','world.world')
    #获取一个urdf的参数方便修改
    action_declare_arg_model_path=launch.actions.DeclareLaunchArgument(
        name='model',default_value=str(default_xacro_path),description="加载的模型路径"
    )
     #获取文件路径获取内容转换为参数值
    substitutions_command_result=launch.substitutions.Command(['xacro ',
          launch.substitutions.LaunchConfiguration('model')]
     )
    
    robot_description_value=launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result,
        value_type=str
    )
    
    action_robot_state_publisher=launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description_value}]
    )

    action_launch_gazebo=launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']
        ),
        launch_arguments=[('world',default_gazebo_world_path),('verbose','true')]
    )

    action_spawn_entity=launch_ros.actions.Node(
       package='gazebo_ros',
       executable='spawn_entity.py',
       arguments=['-topic','/robot_description',
                  '-entity','easy_robot'
       ]
    )

    return launch.LaunchDescription([
           action_declare_arg_model_path,
           action_robot_state_publisher,
           action_launch_gazebo,
           action_spawn_entity
    ])