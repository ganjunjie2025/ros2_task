cmake_minimum_required(VERSION 3.8)
project(example_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(calculate_num_interfaces REQUIRED)
  
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

add_executable(test_cpp src/test.cpp)
add_executable(pub_num_node src/pub_num.cpp)
add_executable(sub_num_node src/sub_num.cpp)

ament_target_dependencies(test_cpp rclcpp)
ament_target_dependencies(test_cpp calculate_num_interfaces)
ament_target_dependencies(test_cpp std_msgs)

ament_target_dependencies(pub_num_node rclcpp)
ament_target_dependencies(pub_num_node calculate_num_interfaces)
ament_target_dependencies(pub_num_node std_msgs)

ament_target_dependencies(sub_num_node rclcpp)
ament_target_dependencies(sub_num_node calculate_num_interfaces)
ament_target_dependencies(sub_num_node std_msgs)


install(TARGETS
test_cpp
pub_num_node
sub_num_node
DESTINATION lib/${PROJECT_NAME}
)

