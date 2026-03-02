#include<iostream>
#include"rclcpp/rclcpp.hpp"
//#include"std_msgs/msg/u_int32.hpp"
#include"calculate_num_interfaces/msg/calculate.hpp"
#include<cstdlib>
#include<ctime>
#include<chrono>

using namespace std;
//using std::placeholders::_1;

//创建发布类：
class pub_num:public rclcpp::Node{
//声明发布者：
      rclcpp::Publisher<calculate_num_interfaces::msg::Calculate>::SharedPtr input_num;
//声明定时器成员变量：
      rclcpp::TimerBase::SharedPtr timer_;
//创建回调函数：
      void callback(){
            //cout<<"callback被调用了"<<endl;
         calculate_num_interfaces::msg::Calculate input;
         input.num1=rand()%100;
         input.num2=rand()%100;
         input_num->publish(input);
         RCLCPP_INFO(this->get_logger(),"num1=%d,num2=%d",input.num1,input.num2);
      } 
public: 
       pub_num(string name):Node(name){
         srand((unsigned)time(NULL));
          //创建发布者：
          input_num=this->create_publisher<calculate_num_interfaces::msg::Calculate>("calculate_cpp",10);
          //规定每2秒发布一次消息：
          int period=2;
          timer_=this->create_wall_timer(std::chrono::seconds(period),std::bind(&pub_num::callback,this));
       }

};


int main(int argc,char **argv){

      rclcpp::init(argc,argv);
      auto pub_node=make_shared<pub_num>("pub_node");
      rclcpp::spin(pub_node);
      rclcpp::shutdown();
}

