# Set minimum supported CMake version to 3.12
cmake_minimum_required(VERSION 3.12)

set(CMAKE_CXX_STANDARD 17) # C++17 is needed for some standard library features like optional
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Define project
project(TrackingAntenna
  LANGUAGES CXX C
  VERSION 0.0.0)

## Find libraries
# Find HindsightCAN library
find_package(HindsightCAN REQUIRED)
# Find gpsd/libgps
find_package(PkgConfig REQUIRED)
pkg_check_modules(libgps REQUIRED libgps)
# Find JSON library
find_package(nlohmann_json 3.2.0 REQUIRED)
# Find Websocket++ (requires Boost System)
find_package(websocketpp REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
# Find system threading library
find_package(Threads REQUIRED)

# Add an executable for the main program.
add_executable(antenna
  # List all .cpp files here
  src/main.cpp)

# Libraries that should be linked to all executables
set(LIBS
  HindsightCAN::HindsightCAN
  ${libgps_LIBRARIES}
  websocketpp::websocketpp
  nlohmann_json::nlohmann_json
  ${Boost_LIBRARIES}
  Threads::Threads)

# Add an executable for the main program.
add_executable(antenna
  # List all .cpp files here
  src/main.cpp
  src/WebSocketServer.cpp
  src/WebSocketProtocol.cpp
  src/log.cpp)

# Link executable to libraries
target_link_libraries(antenna ${LIBS})

