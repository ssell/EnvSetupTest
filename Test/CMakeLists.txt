cmake_minimum_required(VERSION 3.9)

# Force the use of C++17 (should throw a warning or error if available compiler does not support the standard)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Input parameters
# https://stackoverflow.com/questions/8709877/cmake-string-options
set(PARAM_COMPILER "" CACHE STRING "Compiler identifier added to library output name (FOO_PARAM_COMPILER => FOO_msvc140.dll)")
set(PARAM_ARCH "x86" CACHE STRING "Target output architecture (x86 or x64)")
set(COMPILER_EXTENSION "")

if(PARAM_COMPILER STREQUAL "")
    project("TestAPI")
else()
    project("TestAPI_${PARAM_COMPILER}")
    set(COMPILER_EXTENSION "_${PARAM_COMPILER}")
endif()

# Set source directories
set(_src_root_path "${CMAKE_SOURCE_DIR}/src")

# Set output directories
set(OUTPUT_DIR "${CMAKE_SOURCE_DIR}/bin/${PARAM_ARCH}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${OUTPUT_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})

# Create a list of source files
file(
    GLOB_RECURSE _source_list
    LIST_DIRECTORIES false
    "${_src_root_path}/*.c*"
    "${_src_root_path}/*.h*"
    "${_src_root_path}/*.inl"
)

# Add a new executable to the project using the specified source list
add_executable(${PROJECT_NAME} ${_source_list})

if(PARAM_ARCH STREQUAL "x86")
    set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-m32" LINK_FLAGS "-m32")
else()
    set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS "-m64" LINK_FLAGS "-m64")
endif()

# Add include directories
target_include_directories(${PROJECT_NAME} PUBLIC "../vendors/googletest-1.8.838/include/")

# Add library dependencies
target_link_libraries(${PROJECT_NAME} debug "../../../API/bin/${PARAM_ARCH}/Debug/BuildAPI${COMPILER_EXTENSION}d") 
target_link_libraries(${PROJECT_NAME} debug "../../../vendors/googletest-1.8.838/${PARAM_COMPILER}/${PARAM_ARCH}/gtestd")
target_link_libraries(${PROJECT_NAME} debug "../../../vendors/googletest-1.8.838/${PARAM_COMPILER}/${PARAM_ARCH}/gtest_maind")
target_link_libraries(${PROJECT_NAME} optimized "../../../API/bin/${PARAM_ARCH}/Release/BuildAPI${COMPILER_EXTENSION}")
target_link_libraries(${PROJECT_NAME} optimized "../../../vendors/googletest-1.8.838/${PARAM_COMPILER}/${PARAM_ARCH}/gtest")
target_link_libraries(${PROJECT_NAME} optimized "../../../vendors/googletest-1.8.838/${PARAM_COMPILER}/${PARAM_ARCH}/gtest_main")

# Discover and add the source files. This will add subdirectories as filters.
# https://stackoverflow.com/a/33813154/735425
foreach(_source IN ITEMS ${_source_list})
    get_filename_component(_source_path "${_source}" PATH)
    file(RELATIVE_PATH _source_path_rel "${_src_root_path}" "${_source_path}")
    string(REPLACE "/" "\\" _group_path "${_source_path_rel}")
    source_group("${_group_path}" FILES "${_source}")
endforeach()
