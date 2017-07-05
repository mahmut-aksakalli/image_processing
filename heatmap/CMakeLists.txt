cmake_minimum_required(VERSION 2.8.12)
project(colormap)

add_executable(colormap colormap.cpp)

find_package( OpenCV REQUIRED )
target_link_libraries( colormap ${OpenCV_LIBS} )
