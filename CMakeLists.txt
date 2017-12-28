cmake_minimum_required(VERSION 3.9)

# ---------------------------------------------------------------------- #
# - Common Settings                                                    - #
# ---------------------------------------------------------------------- #

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(PARAM_COMPILER "" CACHE STRING "Compiler identifier added to library output name (FOO_PARAM_COMPILER => FOO_msvc140.dll)")
set(PARAM_ARCH "x86" CACHE STRING "Target output architecture (x86 or x64)")
set(PROJECT_API "BuildAPI_${PARAM_COMPILER}")
set(PROJECT_TEST "TestAPI_${PARAM_COMPILER}")
set(OUTPUT_DIR "${CMAKE_SOURCE_DIR}/bin/${PARAM_ARCH}")
set(COMPILE_LINK_FLAG "-m32")
set(PROJECT_SUFFIX "")

if(WIN32 OR WIN64)
    set(PROJECT_SUFFIX "_${PARAM_COMPILER}")                                                            # For Windows (msvc) we want to specify the compiler 
endif()

if(PARAM_ARCH STREQUAL "x86")
    set(COMPILE_LINK_FLAG "-m32")
else()
    set(COMPILE_LINK_FLAG "-m64")
endif()

set(VENDOR_PATH_GTEST "${CMAKE_SOURCE_DIR}/vendors/googletest")

project("EnvSetupTest${PROJECT_SUFFIX}")                                                                # Name of the parent project/solution

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${OUTPUT_DIR})                                                       # Set output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})

# ---------------------------------------------------------------------- #
# - API Library                                                        - #
# ---------------------------------------------------------------------- #

set(API_PROJECT "API${PROJECT_SUFFIX}")                                                            # Project specific variables
set(API_ROOT_PATH "${CMAKE_SOURCE_DIR}/API")
set(API_SRC_ROOT_PATH "${API_ROOT_PATH}/src")

file(
    GLOB_RECURSE API_SRC_LIST                                                                           # List of sources
    LIST_DIRECTORIES false
    "${API_SRC_ROOT_PATH}/*.c*"
    "${API_SRC_ROOT_PATH}/*.h*"
    "${API_SRC_ROOT_PATH}/*.inl"
)

add_library(${API_PROJECT} ${API_SRC_LIST})                                                        # Add the library
set_target_properties(${API_PROJECT} PROPERTIES DEBUG_POSTFIX "d")                                 # Add a 'd' to debug builds
set_target_properties(${API_PROJECT} PROPERTIES COMPILE_FLAGS ${COMPILE_LINK_FLAG} LINK_FLAGS ${COMPILE_LINK_FLAG})        # Specify x86 or x64 build

foreach(_source IN ITEMS ${API_SRC_LIST})                                                               # Add the source files to the project 
    get_filename_component(_source_path "${_source}" PATH)                                              # https://stackoverflow.com/a/33813154/735425
    file(RELATIVE_PATH _source_path_rel "${API_SRC_ROOT_PATH}" "${_source_path}")
    string(REPLACE "/" "\\" _group_path "${_source_path_rel}")
    source_group("${_group_path}" FILES "${_source}")
endforeach()

# ---------------------------------------------------------------------- #
# - TestAPI Executable                                                 - #
# ---------------------------------------------------------------------- #

set(TESTAPI_PROJECT "TestAPI${PROJECT_SUFFIX}")
set(TESTAPI_ROOT_PATH "${CMAKE_SOURCE_DIR}/Test")
set(TESTAPI_SRC_ROOT_PATH "${TESTAPI_ROOT_PATH}/src")

file(
    GLOB_RECURSE TESTAPI_SRC_LIST
    LIST_DIRECTORIES false
    "${TESTAPI_SRC_ROOT_PATH}/*.c*"
    "${TESTAPI_SRC_ROOT_PATH}/*.h*"
    "${TESTAPI_SRC_ROOT_PATH}/*.inl"
)

add_executable(${TESTAPI_PROJECT} ${TESTAPI_SRC_LIST})
set_target_properties(${APITESTAPI_PROJECT_PROJECT_NAME} PROPERTIES COMPILE_FLAGS ${COMPILE_LINK_FLAG} LINK_FLAGS ${COMPILE_LINK_FLAG})

target_include_directories(${TESTAPI_PROJECT} PUBLIC ${API_SRC_ROOT_PATH})
target_include_directories(${TESTAPI_PROJECT} PUBLIC "${VENDOR_PATH_GTEST}/include")

target_link_libraries(${TESTAPI_PROJECT} debug "${OUTPUT_DIR}/Debug/${CMAKE_FIND_LIBRARY_PREFIXES}${API_PROJECT}d${CMAKE_STATIC_LIBRARY_SUFFIX}")
target_link_libraries(${TESTAPI_PROJECT} debug "${VENDOR_PATH_GTEST}/${PARAM_COMPILER}/${PARAM_ARCH}/${CMAKE_FIND_LIBRARY_PREFIXES}gtestd${CMAKE_STATIC_LIBRARY_SUFFIX}")
target_link_libraries(${TESTAPI_PROJECT} debug "${VENDOR_PATH_GTEST}/${PARAM_COMPILER}/${PARAM_ARCH}/${CMAKE_FIND_LIBRARY_PREFIXES}gtest_maind${CMAKE_STATIC_LIBRARY_SUFFIX}")
target_link_libraries(${TESTAPI_PROJECT} optimized "${OUTPUT_DIR}/Release/${CMAKE_FIND_LIBRARY_PREFIXES}${API_PROJECT}${CMAKE_STATIC_LIBRARY_SUFFIX}")
target_link_libraries(${TESTAPI_PROJECT} optimized "${VENDOR_PATH_GTEST}/${PARAM_COMPILER}/${PARAM_ARCH}/${CMAKE_FIND_LIBRARY_PREFIXES}gtest${CMAKE_STATIC_LIBRARY_SUFFIX}")
target_link_libraries(${TESTAPI_PROJECT} optimized "${VENDOR_PATH_GTEST}/${PARAM_COMPILER}/${PARAM_ARCH}/${CMAKE_FIND_LIBRARY_PREFIXES}gtest_main${CMAKE_STATIC_LIBRARY_SUFFIX}")

add_dependencies(${TESTAPI_PROJECT} ${API_PROJECT})

foreach(_source IN ITEMS ${TESTAPI_SRC_LIST})
    get_filename_component(_source_path "${_source}" PATH)
    file(RELATIVE_PATH _source_path_rel "${TESTAPI_SRC_ROOT_PATH}" "${_source_path}")
    string(REPLACE "/" "\\" _group_path "${_source_path_rel}")
    source_group("${_group_path}" FILES "${_source}")
endforeach()