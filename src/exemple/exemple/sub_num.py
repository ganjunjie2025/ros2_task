import rclpy
from rclpy.node import Node
from calculate_num_interfaces.msg import Calculate

class sub_num(Node):
    def __init__ (self,name):
        super().__init__(name)
        #创建订阅者：
        self.sub_num=self.create_subscription(Calculate,"calculate_py",self.callback,10)
        #编写回调函数：
    def callback(self,input):
        self.result=input.num1+input.num2
        self.get_logger().info("num1+num2=%d"%self.result)

def main(args=None):
    rclpy.init(args=None)
    sub_sum_node=sub_num("sub_num")
    rclpy.spin(sub_sum_node)
    rclpy.shutshow