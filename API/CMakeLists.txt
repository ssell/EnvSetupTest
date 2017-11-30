cmake_minimum_required(VERSION 3.9)

# https://www.codeproject.com/Articles/1181455/A-CMake-tutorial-for-Visual-Cplusplus-developers

# Input parameters
# https://stackoverflow.com/questions/8709877/cmake-string-options
set(PARAM_COMPILER "" CACHE STRING "Compiler identifier added to library output name (FOO_PARAM_COMPILER => FOO_msvc140.dll)")
set(PARAM_ARCH "x86" CACHE STRING "Target output architecture (x86 or x64)")

if(PARAM_COMPILER STREQUAL "")
    project("BuildAPI")
else()
    project("BuildAPI_${PARAM_COMPILER}")
endif()

# Set source directories
set(_src_root_path "${CMAKE_SOURCE_DIR}/src")

# Set output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${PARAM_ARCH}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${PARAM_ARCH}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${PARAM_ARCH}")

# Specify to use the latest C++ standard available
add_compile_options(-std=c++latest)

# Create a list of source files
file(
    GLOB_RECURSE _source_list
    LIST_DIRECTORIES false
    "${_src_root_path}/*.c*"
    "${_src_root_path}/*.h*"
    "${_src_root_path}/*.inl"
)

# Add a new library to the project using the specified source list
add_library("${PROJECT_NAME}" ${_source_list})

# Set output name (use for libraries only)
# This will change the name from API.lib to API_msvc141.lib 
# https://stackoverflow.com/a/31139717/735425
set_target_properties("${PROJECT_NAME}" PROPERTIES DEBUG_POSTFIX "d")

# Discover and add the source files. This will add subdirectories as filters.
# https://stackoverflow.com/a/33813154/735425
foreach(_source IN ITEMS ${_source_list})
    get_filename_component(_source_path "${_source}" PATH)
    file(RELATIVE_PATH _source_path_rel "${_src_root_path}" "${_source_path}")
    string(REPLACE "/" "\\" _group_path "${_source_path_rel}")
    source_group("${_group_path}" FILES "${_source}")
endforeach()
