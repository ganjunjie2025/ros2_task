import rclpy
from rclpy.node import Node
from std_msgs.msg import String,UInt32#导入消息类型


"""
    编写ros节点的一般步骤：
    1.导入库函数
    2.初始化客户端库
    3.新建节点对象
    4.spin循环节点
    5.关闭客户端库
"""
class test(Node):
    def __init__ (self,name):
        super().__init__(name)
        self.get_logger().info(f"hello world {name}_node" )
        #1.声明并创建发布者
        self.pur_num=self.create_publisher(String,"novel",10)
        #声明并创建订阅者
        self.sub_money=self.create_subscription(UInt32,"sub_money",self.money_callback,10)
        #编写发布逻辑并发布消息
        self.period=3
        self.count=1
        self.acount=100
        self.timer=self.create_timer(self.period,self.callback)

    def callback(self):
        msg=String()
        msg.data="李4发布第%d章节小说"%(self.count)
        self.pur_num.publish(msg)
        self.get_logger().info("%s"%msg.data)
        self.count+=1

    def money_callback(self,money):
        self.acount+=money.data
        self.get_logger().info("获得稿费%d，当前共有%d元"%(money.data,self.acount))



def main(args=None):
    rclpy.init(args=args)
    new_node=test("test_py")
    #new_node.get_logger().info("hello world test")
    rclpy.spin(new_node)
    rclpy.shoutdown
    