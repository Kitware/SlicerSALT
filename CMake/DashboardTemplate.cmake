####################################################################################
# OS      :
# Hardware:
# GPU     :
####################################################################################
# WARNING - The specific version and processor type of this machine should be reported
# in the header above. Indeed, this file will be send to the dashboard as a NOTE file.
#
# On linux, you could run:
#     'uname -o' and 'cat /etc/*-release' to obtain the OS name.
#     'uname -mpi' to obtain hardware details.
#     'glxinfo | grep OpenGL' to obtain GPU details.
####################################################################################

cmake_minimum_required(VERSION 2.8.10)

# You could invoke the script with the following syntax:
#  ctest -S /path/to/<scriptname>.cmake -C <CTEST_BUILD_CONFIGURATION> -V
#
# Note that '-C <CTEST_BUILD_CONFIGURATION>' is mandatory on windows

#-----------------------------------------------------------------------------
# Macro allowing to set a variable to its default value only if not already defined
macro(setOnlyIfNotDefined var defaultvalue)
  if(NOT DEFINED ${var})
    set(${var} "${defaultvalue}")
  endif()
endmacro()

#-----------------------------------------------------------------------------
# Repository
#-----------------------------------------------------------------------------
setOnlyIfNotDefined(GIT_REPOSITORY git://kwsource.kitwarein.com/${CTEST_PROJECT_NAME}/${CTEST_PROJECT_NAME}.git)
setOnlyIfNotDefined(GIT_TAG master)
setOnlyIfNotDefined(DRIVER_URL http://kwsource.kitwarein.com/${CTEST_PROJECT_NAME}/${CTEST_PROJECT_NAME}/blobs/raw/${GIT_TAG}/CMake/DashboardDriver.cmake)

#-----------------------------------------------------------------------------
# Type of dashboard:
# Experimental:
#     - run_ctest() macro will be called *ONE* time
#     - binary directory will *NOT* be cleaned
# Continuous:
#     - run_ctest() macro will be called EVERY 5 minutes ...
#     - binary directory will *NOT* be cleaned
#     - configure/build will be executed *ONLY* if the repository has been updated
# Nightly:
#     - run_ctest() macro will be called *ONE* time
#     - binary directory *WILL BE* cleaned
# E.g. Experimental, Continuous, Nightly
setOnlyIfNotDefined(SCRIPT_MODE "Experimental")

#-----------------------------------------------------------------------------
# Dashboard properties
#-----------------------------------------------------------------------------
set(CTEST_PROJECT_NAME "Ninja")

# Path where to pull and build the sources.
# E.g. ${CTEST_SCRIPT_DIRECTORY}, C:/Work/Dashboards
set(CTEST_DASHBOARD_ROOT "${CTEST_SCRIPT_DIRECTORY}/${SCRIPT_MODE}")
if(NOT GIT_TAG STREQUAL "master")
  set(CTEST_DASHBOARD_ROOT "${CTEST_DASHBOARD_ROOT}/${GIT_TAG}")
endif()

# Name of the machine that will appear on CDash
# E.g. mymachine.kitware, mymachine.dkfz, ...
set(CTEST_SITE "melcor.kitware")

# Operating system of the machine
# E.g. Linux, Windows, Darwin...
set(MY_OPERATING_SYSTEM "Linux")

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

#-----------------------------------------------------------------------------
# Dashboard options
#-----------------------------------------------------------------------------
setOnlyIfNotDefined(WITH_KWSTYLE FALSE)
setOnlyIfNotDefined(WITH_MEMCHECK FALSE)
setOnlyIfNotDefined(WITH_COVERAGE FALSE)
setOnlyIfNotDefined(WITH_DOCUMENTATION FALSE)
setOnlyIfNotDefined(WITH_PACKAGES FALSE)

setOnlyIfNotDefined(CTEST_TEST_TIMEOUT 500)

# Build flags to pass to the generator.
# E.g. -j2, -j8, ""
setOnlyIfNotDefined(CTEST_BUILD_FLAGS "-j2")

# Each dashboard script should specify a unique ID per CTEST_DASHBOARD_ROOT.
# It means the following directories will be created:
#   <CTEST_DASHBOARD_ROOT>/<DIRECTORY_NAME>-<DIRECTORY_IDENTIFIER>        # Source directory
#   <CTEST_DASHBOARD_ROOT>/<DIRECTORY_NAME>-<DIRECTORY_IDENTIFIER>-build  # Build directory
set(DIRECTORY_IDENTIFIER  "0")

# Path where to save the build logs. Don't forget to create a "Logs" directory.
setOnlyIfNotDefined(CTEST_LOG_FILE "${CTEST_DASHBOARD_ROOT}/Logs/${CTEST_PROJECT_NAME}-${GIT_BRANCH_NAME}-${SCRIPT_MODE}-${CTEST_BUILD_CONFIGURATION}-${MY_BITNESS}bits.log")

#-----------------------------------------------------------------------------
# List of test that should be explicitly disabled on this machine
#-----------------------------------------------------------------------------
set(TEST_TO_EXCLUDE_REGEX "")

#-----------------------------------------------------------------------------
# Set any extra environment variables here
#-----------------------------------------------------------------------------
if(UNIX)
  set(ENV{DISPLAY} ":0")
endif()

#-----------------------------------------------------------------------------
# Required executables
#-----------------------------------------------------------------------------
find_program(CTEST_SVN_COMMAND NAMES svn)
find_program(CTEST_GIT_COMMAND NAMES git)
find_program(CTEST_COVERAGE_COMMAND NAMES gcov)
find_program(CTEST_MEMORYCHECK_COMMAND NAMES valgrind)

#-----------------------------------------------------------------------------
# Additional CMakeCache options
#-----------------------------------------------------------------------------
setOnlyIfNotDefined(ADDITIONNAL_CMAKECACHE_OPTION "")

#-----------------------------------------------------------------------------
# Build Name
#-----------------------------------------------------------------------------
# Update the following variable to match the chosen build options. This variable is used to
# generate both the build directory and the build name.
set(BUILD_OPTIONS_STRING "${MY_BITNESS}bits-QT${MY_QT_VERSION}")

#-----------------------------------------------------------------------------
# Directory name
#-----------------------------------------------------------------------------
setOnlyIfNotDefined(DIRECTORY_NAME ${CTEST_PROJECT_NAME})

#-----------------------------------------------------------------------------
# Build directory
#-----------------------------------------------------------------------------
set(CTEST_BINARY_DIRECTORY "${CTEST_DASHBOARD_ROOT}/${DIRECTORY_NAME}-${DIRECTORY_IDENTIFIER}-build")
file(WRITE "${CTEST_DASHBOARD_ROOT}/${DIRECTORY_NAME}-${DIRECTORY_IDENTIFIER}-build - ${BUILD_OPTIONS_STRING}-${CTEST_BUILD_CONFIGURATION}-${SCRIPT_MODE}.txt" "Generated by ${CTEST_SCRIPT_NAME}")

#-----------------------------------------------------------------------------
# Source directory
#-----------------------------------------------------------------------------
set(CTEST_SOURCE_DIRECTORY "${CTEST_DASHBOARD_ROOT}/${DIRECTORY_NAME}-${DIRECTORY_IDENTIFIER}")


##########################################
# WARNING: DO NOT EDIT BEYOND THIS POINT #
##########################################

set(CTEST_NOTES_FILES "${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}")

#
# Project specific properties
#
set(CTEST_BUILD_NAME "${MY_OPERATING_SYSTEM}-${MY_COMPILER}-${BUILD_OPTIONS_STRING}-${CTEST_BUILD_CONFIGURATION}-${GIT_TAG}")

#
# Display build info
#
message("CTEST_SITE ................: ${CTEST_SITE}")
message("CTEST_BUILD_NAME ..........: ${CTEST_BUILD_NAME}")
message("SCRIPT_MODE ...............: ${SCRIPT_MODE}")
message("CTEST_BUILD_CONFIGURATION .: ${CTEST_BUILD_CONFIGURATION}")
message("WITH_KWSTYLE ..............: ${WITH_KWSTYLE}")
message("WITH_COVERAGE: ............: ${WITH_COVERAGE}")
message("WITH_MEMCHECK .............: ${WITH_MEMCHECK}")
message("WITH_PACKAGES .............: ${WITH_PACKAGES}")
message("WITH_DOCUMENTATION ........: ${WITH_DOCUMENTATION}")
message("DOCUMENTATION_ARCHIVES_OUTPUT_DIRECTORY: ${DOCUMENTATION_ARCHIVES_OUTPUT_DIRECTORY}")

#
# Convenient function allowing to download a file
#
function(download_file url dest)
  file(DOWNLOAD ${url} ${dest} STATUS status)
  list(GET status 0 error_code)
  list(GET status 1 error_msg)
  if(error_code)
    message(FATAL_ERROR "error: Failed to download ${url} - ${error_msg}")
  endif()
endfunction()

#
# Download and include dashboard driver script
#
set(dest ${CTEST_SCRIPT_DIRECTORY}/${CTEST_SCRIPT_NAME}.driver)
download_file(${DRIVER_URL} ${dest})
include(${dest})
