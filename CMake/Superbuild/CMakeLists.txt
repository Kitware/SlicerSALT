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

set(${APPLICATION_NAME}_DEPENDENCIES Slicer)

#-----------------------------------------------------------------------------
# WARNING - No change should be required after this comment
#           when you are adding a new external project dependency.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Declare ${APPLICATION_NAME}_EXTERNAL_LIBRARY_DIRS variable - This variable stores
# the library output directory associated with the different external project
# It's then used in Utilities/LastConfigureStep/${APPLICATION_NAME}Generate${APPLICATION_NAME}Config.cmake to
# configure ${APPLICATION_NAME}Config.cmake.in
# This variable would then be exposed to project building against ${APPLICATION_NAME}
#SET(${APPLICATION_NAME}_EXTERNAL_LIBRARY_DIRS)

#-----------------------------------------------------------------------------
# Git protocole option
#
option(${APPLICATION_NAME}_USE_GIT_PROTOCOL "If behind a firewall turn this OFF to use http instead." ON)

set(git_protocol "git")
if(NOT ${APPLICATION_NAME}_USE_GIT_PROTOCOL)
  set(git_protocol "http")
endif()

#-----------------------------------------------------------------------------
# Enable and setup External project global properties
#
include(ExternalProject)
include(EmptyExternalProject)
include(CheckExternalProjectDependency)

#SET(ep_base "${CMAKE_BINARY_DIR}/SuperBuild")
#SET_PROPERTY(DIRECTORY PROPERTY EP_BASE ${ep_base})

set(ep_install_dir ${CMAKE_BINARY_DIR}/SuperBuild/Install)
set(ep_suffix      "-cmake")

set(ep_common_c_flags "${CMAKE_C_FLAGS_INIT} ${ADDITIONAL_C_FLAGS}")
set(ep_common_cxx_flags "${CMAKE_CXX_FLAGS_INIT} ${ADDITIONAL_CXX_FLAGS}")

# Compute -G arg for configuring external projects with the same CMake generator:
if(CMAKE_EXTRA_GENERATOR)
  set(gen "${CMAKE_EXTRA_GENERATOR} - ${CMAKE_GENERATOR}")
else()
  set(gen "${CMAKE_GENERATOR}")
endif()

# Use this value where semi-colons are needed in ep_add args:
set(sep "^^")

# With CMake 2.8.9 or later, the UPDATE_COMMAND is required for updates to occur.
# For earlier versions, we nullify the update state to prevent updates and
# undesirable rebuild.
if(CMAKE_VERSION VERSION_LESS 2.8.9)
  set(${APPLICATION_NAME}_external_update UPDATE_COMMAND "")
else()
  set(${APPLICATION_NAME}_external_update LOG_UPDATE 1)
endif()

#-----------------------------------------------------------------------------
# Include external projects
#

# This variable will contain the list of CMake variable specific to each external project
# that should passed to ${APPLICATION_NAME}.
# The item of this list should have the following form: -D<EP>_DIR:PATH=${<EP>_DIR}
# where '<EP>' is an external project name.
set(${APPLICATION_NAME}_SUPERBUILD_EP_ARGS)

#-----------------------------------------------------------------------------
# Makes sure ${${APPLICATION_NAME}_BINARY_DIR}/${APPLICATION_NAME}-build/bin exists
#IF(NOT EXISTS ${${APPLICATION_NAME}_BINARY_DIR}/${APPLICATION_NAME}-build/bin)
#  FILE(MAKE_DIRECTORY ${${APPLICATION_NAME}_BINARY_DIR}/${APPLICATION_NAME}-build/bin)
#ENDIF()

#-----------------------------------------------------------------------------
# Set superbuild boolean args
#

set(${APPLICATION_NAME}_cmake_boolean_args
  BUILD_TESTING
  ${APPLICATION_NAME}_USE_KWSTYLE
  )

set(${APPLICATION_NAME}_superbuild_boolean_args)
foreach(${APPLICATION_NAME}_cmake_arg ${${APPLICATION_NAME}_cmake_boolean_args})
  list(APPEND ${APPLICATION_NAME}_superbuild_boolean_args -D${${APPLICATION_NAME}_cmake_arg}:BOOL=${${${APPLICATION_NAME}_cmake_arg}})
endforeach()

#-----------------------------------------------------------------------------
# Set CMake OSX variable to pass down the external project
set(CMAKE_OSX_EXTERNAL_PROJECT_ARGS)
if(APPLE)
  list(APPEND CMAKE_OSX_EXTERNAL_PROJECT_ARGS
    -DCMAKE_OSX_ARCHITECTURES=${CMAKE_OSX_ARCHITECTURES}
    -DCMAKE_OSX_SYSROOT=${CMAKE_OSX_SYSROOT}
    -DCMAKE_OSX_DEPLOYMENT_TARGET=${CMAKE_OSX_DEPLOYMENT_TARGET})
endif()

check_external_project_dependency(${APPLICATION_NAME})

#-----------------------------------------------------------------------------
# ${APPLICATION_NAME} Configure
#
set(proj Slicer)

if(CMAKE_GENERATOR MATCHES ".*Makefiles.*")
  set(${APPLICATION_NAME}_build_cmd "$(MAKE)")
else()
  set(${APPLICATION_NAME}_build_cmd ${CMAKE_COMMAND} --build ${${APPLICATION_NAME}_BINARY_DIR}/${proj}-build --config ${CMAKE_CFG_INTDIR})
endif()

#-----------------------------------------------------------------------------
# ${APPLICATION_NAME}
#
#MESSAGE(STATUS SUPERBUILD_EXCLUDE_${APPLICATION_NAME}BUILD_TARGET:${SUPERBUILD_EXCLUDE_B${APPLICATION_NAME}BUILD_TARGET})
if(NOT DEFINED SUPERBUILD_EXCLUDE_${APPLICATION_NAME}_BUILD_TARGET
    OR NOT SUPERBUILD_EXCLUDE_${APPLICATION_NAME}_BUILD_TARGET)
  set(${APPLICATION_NAME}_BUILD_TARGET_ALL_OPTION "ALL")
else()
  set(${APPLICATION_NAME}_BUILD_TARGET_ALL_OPTION "")
endif()

add_custom_target(${APPLICATION_NAME}-build ${${APPLICATION_NAME}_BUILD_TARGET_ALL_OPTION}
  COMMAND ${${APPLICATION_NAME}_build_cmd}
  WORKING_DIRECTORY ${${APPLICATION_NAME}_BINARY_DIR}/${proj}-build
  )
add_dependencies(${APPLICATION_NAME}-build ${proj})

#-----------------------------------------------------------------------------
# Custom target allowing to drive the build of ${APPLICATION_NAME} project itself
#
#add_custom_target(${APPLICATION_NAME}
#  COMMAND ${${APPLICATION_NAME}_build_cmd}
#  WORKING_DIRECTORY ${${APPLICATION_NAME}_BINARY_DIR}/${proj}-build
#  )
