from geometry_msgs.msg import PoseStamped,Pose
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
import rclpy
from rclpy.node import Node
import rclpy.time
from tf2_ros import TransformListener,Buffer
import math
from tf_transformations import euler_from_quaternion,quaternion_from_euler
import time
import yaml
from rclpy.duration import Duration
from geometry_msgs import Twist
 
class auto_patrol_node(BasicNavigator):
    def __init__ (self,node_name='patrol_node'):
        super().__init__(node_name)
        self.sub_cmd=self.create_subscription(Twist,'nav_cmd_vel',speed_callback,10)
        self.pub_cmd=self.create_publisher(Twist,'cmd_vel',10)
        self.scal=1.0
        #声明相关参数：
        #初始化坐标点：
        self.declare_parameter('initial_point',[0.0, 0.0, 0.0]) 
         
        default_action_list=[{
          'goal_points':[-2.0,1.0],
          'yaw':3.14,
          'stop_time':5.0
           },
           {'acc_speed':1.5},
           {'goal_points':[0.0,0.0]}
           ]

        default_task=yaml.dump(default_action_list)
        self.declare_parameter('nav2_action',default_task)
        
        self.initial_point_=self.get_parameter('initial_point').value
        nav2_action_str=self.get_parameter('nav2_action').value   #获取参数的值（在这里实际上是字典）

        self.nav2_action_=yaml.safe_load(nav2_action_str)       #我们遍历的实际上是列表，所以这里将字典转换成列表
    
        self.buffer_=Buffer()
        self.listener_=TransformListener(self.buffer_,self)


    def get_pose(self,x,y,yaw):  #返回PoseStamped
        pose=PoseStamped()
        pose.header.frame_id='map'
        #pose.header.stamp=self.get_clock().now().to_msg()
        pose.pose.position.x=x
        pose.pose.position.y=y
        quat=quaternion_from_euler(0.0,0.0,yaw)
        pose.pose.orientation.x=quat[0]
        pose.pose.orientation.y=quat[1]
        pose.pose.orientation.z=quat[2]
        pose.pose.orientation.w=quat[3]
        return pose

    def set_initial_pose(self):    #初始化机器人的位姿
         
        self.initial_point_=self.get_parameter('initial_point').value
        
        init_pose=self.get_pose(self.initial_point_[0],self.initial_point_[1],self.initial_point_[2])
         #等待导航可用
        self.setInitialPose(init_pose)
        self.waitUntilNav2Active()
            
    def nav_to_goal(self,goal_point): 
        self.goToPose(goal_point)

        while not self.isTaskComplete():
           feedback=self.getFeedback()
           self.get_logger().info(f'剩余距离：{feedback.distance_remaining:.2f}m')
         
        result=self.getResult()
        self.get_logger().info(f'导航结果是：{result}')

    def stop_for_duration(self, duration_sec):
        self.get_logger().info(f"开始停留 {duration_sec} 秒")
        start_time = self.get_clock().now()
        target_time = start_time + Duration(seconds=duration_sec)
        while self.get_clock().now() < target_time:
            rclpy.spin_once(self, timeout_sec=0.1)
        self.get_logger().info(f"当前停留完成！")
    
    def acc_speed(self,scal_):
        self.scal=scal_
        self.get_logger().info(f"当前速度已经变为原来的{scal_}倍")

    def speed_callback(self,msg):
        self.current_speed_linear=msg.twist.linear.x
        self.current_speed_angular=msg.twist.angular.z
        twist=Twist()
        twist.twist.linear.x=self.current_speed_linear*self.scal
        twist.twist.linear.y=self.current_speed_angular*self.scal
        self.pub_cmd.publish(twist)

def main():
    rclpy.init()
    patrol_node=auto_patrol_node()
    patrol_node.set_initial_pose()
    x_past=patrol_node.initial_point_[0]
    y_past=patrol_node.initial_point_[1]

    for idx,action_dict in enumerate(patrol_node.nav2_action_):
      for action_key,action_value in action_dict.items():
        if action_key=="goal_points":
            x=action_value[0]
            y=action_value[1]
            patrol_node.get_logger().info(f"当前行为：导航到({x},{y})")
            goal_pose = patrol_node.get_pose(x,y,0.0)
            patrol_node.nav_to_goal(goal_pose)
            patrol_node.get_logger().info(f"此次导航过程:({x_past},{y_past})->({x},{y})完成")
            x_past=x
            y_past=y
        elif action_key =="yaw":
            yaw=action_value
            patrol_node.get_logger().info(f"当前行为：旋转弧度{yaw}")
            goal_pose=patrol_node.get_pose(x_past,y_past,yaw)
            patrol_node.nav_to_goal(goal_pose)
            patrol_node.get_logger().info(f"旋转弧度：{yaw}完成")
        elif action_key =="stop_time":
            stop_time=action_value
            patrol_node.get_logger().info(f"当前行为：停留{stop_time}s")
            patrol_node.get_logger().info(f"当前停止行动{stop_time}s")
            patrol_node.stop_for_duration(stop_time)
        elif action_key=="acc_speed":
            sacl_=action_value
            patrol_node.acc_speed(sacl_)

    patrol_node.get_logger().info("任务成功完成！")

    rclpy.shutdown()
        