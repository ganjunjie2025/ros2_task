from geometry_msgs.msg import PoseStamped,Pose
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
import rclpy
from rclpy.node import Node
import rclpy.time
from tf2_ros import TransformListener,Buffer
import math
from tf_transformations import euler_from_quaternion,quaternion_from_euler
 
class auto_partol_node(BasicNavigator):
    def __init__ (self,node_name='patrol_node'):
        super().__init__(node_name)
        #声明相关参数：
        self.declare_parameter('initial_point',[0.0, 0.0, 0.0]) #初始化坐标点
        self.declare_parameter('goal_points',[0.0, 0.0, 0.0, 1.0, 1.0, 1.57])

        self.inital_point_=self.get_parameter('initial_point').value
        self.goal_points_=self.get_parameter('goal_points').value
        self.buffer_=Buffer()
        self.listener_=TransformListener(self.buffer_,self)


    def get_pose(self,x,y,yaw):  #返回PoseStamped
        pose=PoseStamped()
        pose.header.frame_id='map'
        pose.pose.position.x=x
        pose.pose.position.y=y
        quat=quaternion_from_euler(0.0,0.0,yaw)
        pose.pose.orientation.x=quat[0]
        pose.pose.orientation.y=quat[1]
        pose.pose.orientation.z=quat[2]
        pose.pose.orientation.w=quat[3]
        return pose

    def inital_pose(self):    #初始化机器人的位姿
         
        self.inital_point_=self.get_parameter('initial_point').value
        
        init_pose=self.get_pose(self.inital_point_[0],self.inital_point_[1],self.inital_point_[2])
         #等待导航可用
        self.setInitialPose(init_pose)
        self.waitUntilNav2Active()

    def get_goal_points(self):   #得到目标点的集合
        
        points=[]
        self.goal_points_=self.get_parameter('goal_points').value
        for index in range(int(len(self.goal_points_)/3)):
            x=self.goal_points_[index*3]
            y=self.goal_points_[index*3+1]
            yaw=self.goal_points_[index*3+2]
            points.append([x,y,yaw])
            self.get_logger().info(f"获取目标点：{index}->{x},{y},{yaw}")
        return points
            
    def nav_to_goal(self,goal_point): 
        self.goToPose(goal_point)

        while not self.isTaskComplete():
           feedback=self.getFeedback()
           self.get_logger().info(f'剩余距离：{feedback.distance_remaining}')
         
        result=self.getResult()
        self.get_logger().info(f'导航结果是：{result}')

    def get_current_pose(self):
        while rclpy.ok():
            try:
                result=self.buffer_.lookup_transform('map','base_footprint',
                       rclpy.time.Time(seconds=0.0),rclpy.time.Duration(seconds=1.0)
                )
                transform = result.transform
                self.get_logger().info(f"平移:{transform.translation}")
                return transform
            except Exception as e:
                self.get_logger().warn(f"获取坐标变换失败：原因{str(e)}")

def main():
    rclpy.init()
    partol_node=auto_partol_node()
    
    partol_node.inital_pose()

    while rclpy.ok():
        points=partol_node.get_goal_points()
        for point in points:
            x,y,yaw=point[0],point[1],point[2]
            goal_pose=partol_node.get_pose(x,y,yaw)
            partol_node.nav_to_goal(goal_pose)

    rclpy.shutdown()
        