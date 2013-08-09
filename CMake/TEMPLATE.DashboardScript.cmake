#============================================================================
#
# Copyright (c) Kitware Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#============================================================================

#
# OS: Windows 7 Professional x64
# Hardware: Intel Core2 Duo P8600 2.4GHz
# GPU: GeForce GTX 280M
#

# Note: The specific version and processor type of this machine should be reported in the
# header above. Indeed, this file will be send to the dashboard as a NOTE file.

cmake_minimum_required(VERSION 2.8.10)

#
# Dashboard properties
#
set(MY_OPERATING_SYSTEM "Windows7") # Windows, Linux, Darwin...
set(MY_COMPILER "VS2008express")

if (NOT MY_QT_VERSION)
  set(MY_QT_VERSION "4.7.4")
endif()

set(QT_QMAKE_EXECUTABLE "C:/work/Qt/qt-${MY_QT_VERSION}-debug-32bit-vs2008/bin/qmake.exe")
set(CTEST_SITE "Alienware.kitware") # for example: mymachine.kitware, mymachine.dkfz, ...
set(CTEST_DASHBOARD_ROOT "")

if (NOT MY_CMAKE_VERSION)
   set(MY_CMAKE_VERSION "CMake 2.8.10")
endif()

set(CTEST_CMAKE_COMMAND   "C:/Program Files (x86)/${MY_CMAKE_VERSION}/bin/cmake.exe")
if (NOT CTEST_CMAKE_GENERATOR)
  set(CTEST_CMAKE_GENERATOR "Visual Studio 9 Win32")
endif()
if (NOT MY_BITNESS)
  set(MY_BITNESS "32")
endif()
#
# Dashboard options
#
set(WITH_KWSTYLE FALSE)
set(WITH_MEMCHECK FALSE)
set(WITH_COVERAGE FALSE)
set(WITH_DOCUMENTATION FALSE)

if (NOT CTEST_BUILD_CONFIGURATION)
  set(CTEST_BUILD_CONFIGURATION "Debug")
endif()

set(CTEST_TEST_TIMEOUT 500)
set(CTEST_BUILD_FLAGS "") # Use multiple CPU cores to build
set(CTEST_LOG_FILE "${CTEST_DASHBOARD_ROOT}/Logs/Nightly-${CTEST_BUILD_CONFIGURATION}}-${MY_BITNESS}bits.log")

# experimental:
#     - run_ctest() macro will be called *ONE* time
#     - binary directory will *NOT* be cleaned
# continuous:
#     - run_ctest() macro will be called EVERY 5 minutes ...
#     - binary directory will *NOT* be cleaned
#     - configure/build will be executed *ONLY* if the repository has been updated
# nightly:
#     - run_ctest() macro will be called *ONE* time
#     - binary directory *WILL BE* cleaned
if (NOT SCRIPT_MODE)
  set(SCRIPT_MODE "experimental") # "experimental", "continuous", "nightly"
endif()

#
# Project specific properties
#
set(CTEST_SOURCE_DIRECTORY "${CTEST_DASHBOARD_ROOT}/...-${CTEST_BUILD_CONFIGURATION}-${GIT_BRANCH_NAME}")
if (NOT CTEST_BINARY_DIRECTORY)
  set(CTEST_BINARY_DIRECTORY "${CTEST_DASHBOARD_ROOT}/...-Superbuild-${CTEST_BUILD_CONFIGURATION}-${MY_BITNESS}bits-${SCRIPT_MODE}-${MY_QT_VERSION}-${MY_CMAKE_VERSION}")
endif()

# Additionnal CMakeCache options - For example:
set(ADDITIONNAL_CMAKECACHE_OPTION "")

# set any extra environment variables here
set(ENV{DISPLAY} ":0")

find_program(CTEST_COVERAGE_COMMAND NAMES gcov)
find_program(CTEST_MEMORYCHECK_COMMAND NAMES valgrind)
find_program(CTEST_GIT_COMMAND NAMES git)
message ("********************************************************COMMAND : ${CTEST_GIT_COMMAND}")

#
# Git repository - Overwrite the default value provided by the driver script
#
# set(GIT_REPOSITORY http://github.com/YOURUSERNAME/....git)
# set(GIT_BRANCH_NAME master)

##########################################
# WARNING: DO NOT EDIT BEYOND THIS POINT #
##########################################

set(CTEST_NOTES_FILES "${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}")

#
# Project specific properties
#
set(CTEST_PROJECT_NAME "...")
set(CTEST_BUILD_NAME "${MY_OPERATING_SYSTEM}-${MY_COMPILER}-${MY_BITNESS}-QT${MY_QT_VERSION}-${MY_CMAKE_VERSION}-${CTEST_BUILD_CONFIGURATION}-${GIT_BRANCH_NAME}")

#
# Display build info
#
message("site name: ${CTEST_SITE}")
message("build name: ${CTEST_BUILD_NAME}")
message("script mode: ${SCRIPT_MODE}")
message("coverage: ${WITH_COVERAGE}, memcheck: ${WITH_MEMCHECK}")

#
# Convenient macro allowing to download a file
#
macro(downloadFile url dest)
  file(DOWNLOAD ${url} ${dest} STATUS status)
  list(GET status 0 error_code)
  list(GET status 1 error_msg)
  if(error_code)
    message(FATAL_ERROR "error: Failed to download ${url} - ${error_msg}")
  endif()
endmacro()

#
# Download and include dashboard driver script
#

set(url http://midas3.kitware.com/midas/download?items=28862)
set(dest ${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}.driver)
downloadFile(${url} ${dest})
include(${dest})
