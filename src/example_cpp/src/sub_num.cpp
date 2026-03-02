#include<iostream>
#include"rclcpp/rclcpp.hpp"
#include"std_msgs/msg/u_int32.hpp"
#include"calculate_num_interfaces/msg/calculate.hpp"
#include<cstdlib>
#include<ctime>
#include<chrono>

using namespace std;
using std::placeholders::_1;

//创建订阅类：
class sub_num:public rclcpp::Node{
private:
         //声明订阅者：
         rclcpp::Subscription<calculate_num_interfaces::msg::Calculate>::SharedPtr output_num;
         //创建回调函数计算结果并打印：
          void callback(const calculate_num_interfaces::msg::Calculate::SharedPtr input){
                  std_msgs::msg::UInt32 result;
                  result.data=input->num1+input->num2;
                  RCLCPP_INFO(this->get_logger(),"num1+num2=%d",result.data);
          } 
public:
         sub_num(string name):Node(name){
              //创建发布者：
              output_num=this->create_subscription<calculate_num_interfaces::msg::Calculate>("calculate_cpp",10,std::bind(&sub_num::callback,this,_1));

         }      
};

int main(int argc,char **argv){

      rclcpp::init(argc,argv);
      //auto pub_node=make_shared<pub_num>("pub_node");
      auto sub_node=make_shared<sub_num>("sub_node");
       rclcpp::spin(sub_node);
      rclcpp::shutdown();
}