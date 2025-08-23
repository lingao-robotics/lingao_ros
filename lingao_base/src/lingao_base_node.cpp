/*
 * Copyright (C) 2022, LingAo Robotics, INC.
 * @Version V1.0
 * @Author owen (keaa@keaa.net)
 * @Date 2022-11-09 20:27:15
 * @LastEditTime 2022-11-09 20:37:57
 * @LastEditors owen (keaa@keaa.net)
 * @Description 
 * @FilePath /lingao_ros2/lingao_base/src/lingao_base_node.cpp
 */

#include "rclcpp/rclcpp.hpp"
#include "lingao_base_driver.h"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<LingaoRos::LingAoBaseDriver>());
  rclcpp::shutdown();
  return 0;
}
