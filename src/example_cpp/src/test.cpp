#include"rclcpp/rclcpp.hpp"
//导入接口类型
#include"std_msgs/msg/string.hpp"
#include"std_msgs/msg/u_int32.hpp"
#include<iostream>

using std::placeholders::_1;
using namespace std;

class test_node:public rclcpp::Node{
//声明发布者
      rclcpp::Publisher<std_msgs::msg::UInt32>::SharedPtr pub_money;
//声明订阅者
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_novel;
//创建回调函数
     void callback(const std_msgs::msg::String::SharedPtr  novel){
            std_msgs::msg::UInt32 money;
            money.data=10;
            //std_msgs::msg::UInt32 result=num_1+num_2;
            pub_money->publish(money);
              RCLCPP_INFO(this->get_logger(),"读者已观看完小说,支付稿费%d",money.data);
          }

public:
      test_node(string name):rclcpp::Node(name){
      RCLCPP_INFO(this->get_logger(),"hello world");
      //创建订阅者
      sub_novel=this->create_subscription<std_msgs::msg::String>("novel",10,std::bind(&test_node::callback,this,_1));
      //创建发布者
      pub_money=this->create_publisher<std_msgs::msg::UInt32>("sub_money",10);
  }

};



int main(int argc,char ** argv){
      rclcpp::init(argc,argv);
      auto node=make_shared<test_node>("test_cpp");
      rclcpp::spin(node);
      rclcpp::shutdown();
}