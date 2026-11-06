cmake_minimum_required(VERSION 3.20)
project(RLTetris CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# The engine: compile its four files directly deliberately do not
# add_subdirectory(extern/Tetris) because its CMakeLists.txt hard-requires
# GLFW, Vulkan, vk-bootstrap and glslc, none of which a headless build needs
set(TETRIS_DIR ${CMAKE_SOURCE_DIR}/extern/Tetris)
add_library(tetris_engine STATIC
    ${TETRIS_DIR}/src/Grid.cpp
    ${TETRIS_DIR}/src/Block.cpp
    ${TETRIS_DIR}/src/Blocks.cpp
    ${TETRIS_DIR}/src/Engine.cpp
)
target_include_directories(tetris_engine PUBLIC ${TETRIS_DIR}/src/include)
set_target_properties(tetris_engine PROPERTIES POSITION_INDEPENDENT_CODE ON)

# pybind11 finds Python through CMake's FindPython (uses Python_EXECUTABLE).
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core cpp/bindings.cpp)
target_link_libraries(_core PRIVATE tetris_engine)

# Write the built module next to the Python package so `import rltetris._core` works.
set_target_properties(_core PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python/rltetris)
