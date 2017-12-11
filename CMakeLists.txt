cmake_minimum_required(VERSION 3.9)

set(PARAM_COMPILER "" CACHE STRING "Compiler identifier added to library output name (FOO_PARAM_COMPILER => FOO_msvc140.dll)")
set(PARAM_ARCH "x86" CACHE STRING "Target output architecture (x86 or x64)")
set(PROJECT_API "BuildAPI_${PARAM_COMPILER}")

if(PARAM_COMPILER STREQUAL "")
    project("EnvSetupTest")
else()
    project("EnvSetupTest_${PARAM_COMPILER}")
endif()

include_external_msproject("${PROJECT_API}" "../../API/build/VS2017_${PARAM_ARCH}/${PROJECT_API}.vcxproj")