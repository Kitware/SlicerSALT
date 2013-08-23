# OS: Linux Ubuntu x64
# Hardware: Intel Core2 Duo P8600 2.4GHz
# GPU: GeForce GTX 280M

# Note: The specific version and processor type of this machine should be reported in the
# header above. Indeed, this file will be send to the dashboard as a NOTE file.

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

cmake_minimum_required(VERSION 2.8.10)

#-----------------------------------------------------------------------------
# Macro allowing to set a variable to its default value only if not already defined
macro(setOnlyIfNotDefined var defaultvalue)
  if(NOT DEFINED ${var})
    set(${var} "${defaultvalue}")
  endif()
endmacro()

#
# Dashboard properties
#
set(CTEST_PROJECT_NAME "Ninja")

# Path where to pull and build the sources.
# E.g. ${CTEST_SCRIPT_DIRECTORY}, C:/Work/Dashboards
set(CTEST_DASHBOARD_ROOT "${CTEST_SCRIPT_DIRECTORY}")
# Name of the machine that will appear on CDash
# E.g. mymachine.kitware, mymachine.dkfz, ...
set(CTEST_SITE "melcor.kitware")
# Operating system of the machine
# E.g. Linux, Windows, Darwin...
set(MY_OPERATING_SYSTEM "Linux")

# CMake version to use
# E.g. 2.8.10, 2.8.11.2
setOnlyIfNotDefined(MY_CMAKE_VERSION "2.8.10")
# Path of the CMake executable
# E.g. /usr/bin/cmake, C:/Program Files (x86)/CMake ${MY_CMAKE_VERSION}/bin/cmake.exe
setOnlyIfNotDefined(CTEST_CMAKE_COMMAND "/usr/bin/cmake")

# Compiler to use to compile the project.
# E.g. GCC-4.7, VS2008Express...
setOnlyIfNotDefined(MY_COMPILER "GCC-4.7")
# Bitness of the compiler to use. It can be different than the machine.
# E.g. 64, 32
setOnlyIfNotDefined(MY_BITNESS "64")
# Generator to use when configuring the CMake project.
# E.g. Unix Makefiles, Visual Studio 9 Win32
setOnlyIfNotDefined(CTEST_CMAKE_GENERATOR "Unix Makefiles")
# Build configuration
# E.g. Release, RelWithDebInfo, Debug
setOnlyIfNotDefined(CTEST_BUILD_CONFIGURATION "Release")

# Qt version to use when compiling the project.
# E.g. 4.7.4, 4.8.5
setOnlyIfNotDefined(MY_QT_VERSION "4.7.4")
# Path of the qmake executable
# E.g. /usr/bin/qmake, C:/work/Qt/qt-${MY_QT_VERSION}-debug-32bit-vs2008/bin/qmake.exe
setOnlyIfNotDefined(QT_QMAKE_EXECUTABLE "/usr/bin/qmake")

#
# Dashboard options
#
setOnlyIfNotDefined(WITH_KWSTYLE FALSE)
setOnlyIfNotDefined(WITH_MEMCHECK FALSE)
setOnlyIfNotDefined(WITH_COVERAGE FALSE)
setOnlyIfNotDefined(WITH_DOCUMENTATION FALSE)
setOnlyIfNotDefined(WITH_PACKAGES FALSE)

setOnlyIfNotDefined(CTEST_TEST_TIMEOUT 500)
# Build flags to pass to the generator.
# E.g. -j2, -j8, ""
setOnlyIfNotDefined(CTEST_BUILD_FLAGS "-j2")

# Type of dashboard:
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
# E.g. experimental, continuous, nightly
setOnlyIfNotDefined(SCRIPT_MODE "experimental")

#
# Project specific properties
#
# Path where to save the downloaded (with git) the source of the project.
setOnlyIfNotDefined(CTEST_SOURCE_DIRECTORY "${CTEST_DASHBOARD_ROOT}/${CTEST_PROJECT_NAME}-${GIT_BRANCH_NAME}-${SCRIPT_MODE}")
# Path where to build the project
# Must be short (e.g. "c:\Work\D\B-nightly") on Windows
setOnlyIfNotDefined(CTEST_BINARY_DIRECTORY "${CTEST_DASHBOARD_ROOT}/${CTEST_PROJECT_NAME}-${GIT_BRANCH_NAME}-${SCRIPT_MODE}-${CTEST_BUILD_CONFIGURATION}-${MY_BITNESS}bits-Qt${MY_QT_VERSION}-CMake${MY_CMAKE_VERSION}")
# Path where to save the build logs. Don't forget to create a "Logs" directory.
setOnlyIfNotDefined(CTEST_LOG_FILE "${CTEST_DASHBOARD_ROOT}/Logs/${CTEST_PROJECT_NAME}-${GIT_BRANCH_NAME}-${SCRIPT_MODE}-${CTEST_BUILD_CONFIGURATION}-${MY_BITNESS}bits.log")
# File to upload to CDash as notes. The first 3 lines of the script contain
# machine information that is read by CDash.
setOnlyIfNotDefined(CTEST_NOTES_FILES "${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}")

# Additionnal CMakeCache options
setOnlyIfNotDefined(ADDITIONNAL_CMAKECACHE_OPTION "")

# set any extra environment variables here
set(ENV{DISPLAY} ":0")

find_program(CTEST_COVERAGE_COMMAND NAMES gcov)
find_program(CTEST_MEMORYCHECK_COMMAND NAMES valgrind)
find_program(CTEST_GIT_COMMAND NAMES git)

#
# Git repository
#
setOnlyIfNotDefined(GIT_REPOSITORY git://kwsource.kitwarein.com/${CTEST_PROJECT_NAME}/${CTEST_PROJECT_NAME}.git)
setOnlyIfNotDefined(GIT_BRANCH_NAME master)
setOnlyIfNotDefined(DRIVER_URL http://kwsource.kitwarein.com/${CTEST_PROJECT_NAME}/${CTEST_PROJECT_NAME}/blobs/raw/${GIT_BRANCH_NAME}/CMake/DashboardDriver.cmake)


##########################################
# WARNING: DO NOT EDIT BEYOND THIS POINT #
##########################################

#
# Project specific properties
#
set(CTEST_BUILD_NAME "${MY_OPERATING_SYSTEM}-${MY_COMPILER}-${MY_BITNESS}-QT${MY_QT_VERSION}-CMake${MY_CMAKE_VERSION}-${CTEST_BUILD_CONFIGURATION}-${GIT_BRANCH_NAME}")

#
# Display build info
#
message("repo URL: ${GIT_REPOSITORY}")
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
set(dest ${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}.driver)
downloadFile(${DRIVER_URL} ${dest})
include(${dest})
