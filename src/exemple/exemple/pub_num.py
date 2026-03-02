import rclpy
from rclpy.node import Node
from calculate_num_interfaces.msg import Calculate
import random

class pub_num(Node):
    def __init__ (self,name):
        super().__init__ (name)
        #创建发布者：
        self.pub_num=self.create_publisher(Calculate,"calculate_py",10)
        #每两秒发布一次消息：
        period=2
        self.timer=self.create_timer(period,self.callback)
    
    #编写回调函数：
    def callback(self):
        input=Calculate()
        input.num1=random.randint(0,99)
        input.num2=random.randint(0,99)
        self.pub_num.publish(input)
        self.get_logger().info("num1=%d,num2=%d"%(input.num1,input.num2))

def main(args=None):
    rclpy.init(args=args)
    pub_num_node=pub_num("pub_num")
    rclpy.spin(pub_num_node)
    rclpy.shutdown




