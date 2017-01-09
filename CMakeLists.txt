#============================================================================
#
# Copyright (c) Kitware, Inc.
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

cmake_minimum_required(VERSION 3.0)

set(APPLICATION_NAME Ninja)
set(APPLICATION_DOMAIN "kitware.com")
set(APPLICATION_VENDOR "Kitware, Inc.")

#-----------------------------------------------------------------------------
set(kit ${APPLICATION_NAME})
set(${kit}_CMAKE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/CMake")
set(${kit}_CMAKE_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/CMake")
set(${kit}_SUPERBUILD_DIR ${${kit}_CMAKE_SOURCE_DIR}/Superbuild)
list(APPEND ${kit}_CMAKE_DIRS ${${kit}_CMAKE_SOURCE_DIR} ${${kit}_CMAKE_BINARY_DIR})
set(CMAKE_MODULE_PATH ${${kit}_CMAKE_DIRS} ${CMAKE_MODULE_PATH})

#-----------------------------------------------------------------------------
set(EXTERNAL_PROJECT_DIR ${${kit}_SUPERBUILD_DIR})
include(ExternalProject)
include(ExternalProjectDependency)
include(OSXVariables) # Must be called before "project"

#-----------------------------------------------------------------------------
project(${kit})

#-----------------------------------------------------------------------------
# Configure necessary cmakes
#

# Configure Use${kit}.cmake
configure_file(
  ${${kit}_CMAKE_SOURCE_DIR}/UseApplication.cmake.in
  ${${kit}_BINARY_DIR}/Use${kit}.cmake
  @ONLY
  )

# Configure External_${kit}.cmake
configure_file(
  ${${kit}_CMAKE_SOURCE_DIR}/External_Application.cmake.in
  ${${kit}_CMAKE_BINARY_DIR}/Superbuild/External_${kit}.cmake
  @ONLY
  )

#-----------------------------------------------------------------------------
include(CTest)

#-----------------------------------------------------------------------------
# Library mode: SHARED (default) or STATIC
if(NOT DEFINED BUILD_SHARED_LIBS)
  option(BUILD_SHARED_LIBS "Build ${kit} with shared libraries." ON)
  mark_as_advanced(BUILD_SHARED_LIBS)
endif()
set(${kit}_BUILD_SHARED_LIBS ${BUILD_SHARED_LIBS})

set(${kit}_INSTALL_BIN_DIR "bin")
set(${kit}_INSTALL_LIB_DIR "bin")
set(${kit}_INSTALL_INCLUDE_DIR "include")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${${kit}_BINARY_DIR}/${${kit}_INSTALL_BIN_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${${kit}_BINARY_DIR}/${${kit}_INSTALL_LIB_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${${kit}_BINARY_DIR}/${${kit}_INSTALL_LIB_DIR})

#-----------------------------------------------------------------------------
# Set a default build type if none was specified
#
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Debug' as none was specified.")
  set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the type of build." FORCE)
  mark_as_advanced(CMAKE_BUILD_TYPE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()
if(NOT CMAKE_CONFIGURATION_TYPES)
  mark_as_superbuild(VARS CMAKE_BUILD_TYPE ALL_PROJECTS)
endif()

#-----------------------------------------------------------------------------
option(${APPLICATION_NAME}_USE_VTK_DEBUG_LEAKS "Enable VTK debug leaks." ON)
set(Slicer_USE_VTK_DEBUG_LEAKS ${${APPLICATION_NAME}_USE_VTK_DEBUG_LEAKS})
mark_as_superbuild(VARS Slicer_USE_VTK_DEBUG_LEAKS:BOOL PROJECTS Slicer)

#-----------------------------------------------------------------------------
option(${APPLICATION_NAME}_USE_PYTHONQT_WITH_OPENSSL "Enable PythonQt SSL support." OFF)
set(Slicer_USE_PYTHONQT_WITH_OPENSSL ${${APPLICATION_NAME}_USE_PYTHONQT_WITH_OPENSSL})
mark_as_superbuild(VARS Slicer_USE_PYTHONQT_WITH_OPENSSL:BOOL PROJECTS Slicer)

#-----------------------------------------------------------------------------
if(WIN32)
  option(Slicer_BUILD_WIN32_CONSOLE "Build ${PROJECT_NAME} executable as a console app on windows (allows debug output)" ON)
else()
  set(Slicer_BUILD_WIN32_CONSOLE OFF)
endif()
mark_as_superbuild(VARS Slicer_BUILD_WIN32_CONSOLE:BOOL PROJECTS Slicer)

#-----------------------------------------------------------------------------
# Superbuild Option - Enabled by default
#
option(${kit}_SUPERBUILD "Build ${kit} and the projects it depends on." ON)
mark_as_advanced(${kit}_SUPERBUILD)

#-----------------------------------------------------------------------------
# Prerequisites
#-----------------------------------------------------------------------------
find_package(Subversion)
if(NOT Subversion_FOUND)
  message(FATAL_ERROR "error: Install SVN and try to re-configure")
endif()
mark_as_superbuild(VARS Subversion_SVN_EXECUTABLE PROJECTS Slicer)

find_package(Git)
if(NOT GIT_FOUND)
  message(FATAL_ERROR "error: Install Git and try to re-configure")
endif()
mark_as_superbuild(VARS GIT_EXECUTABLE PROJECTS Slicer)

#-----------------------------------------------------------------------------
# Project version number.
#
set(${kit}_VERSION_MAJOR 0)
set(${kit}_VERSION_MINOR 1)
set(${kit}_VERSION_PATCH 0)
# Releases define a tweak level
#set(${kit}_VERSION_TWEAK 0)
#set(${kit}_VERSION_RC 1)

include(ExtractRepositoryInfo)
extract_repository_info(VAR_PREFIX ${kit}) # Used to configure ${kit}VersionConfigure.h.in

if(${kit}_WC_LAST_CHANGED_DATE)
  string(REGEX REPLACE ".*([0-9][0-9][0-9][0-9]\\-[0-9][0-9]\\-[0-9][0-9]).*" "\\1"
    ${kit}_BUILDDATE "${${kit}_WC_LAST_CHANGED_DATE}")
  set(${kit}_VERSION_UID "${(${kit}_BUILDDATE}")
else()
  set(${kit}_VERSION_UID "${${kit}_WC_REVISION}")
endif()

set(${kit}_VERSION "${${kit}_VERSION_MAJOR}.${${kit}_VERSION_MINOR}")
set(${kit}_VERSION_FULL "${${kit}_VERSION}.${${kit}_VERSION_PATCH}")
if(${kit}_VERSION_RC)
  set(${kit}_VERSION_FULL "${${kit}_VERSION_FULL}-rc${${kit}_VERSION_RC}")
endif()
if(NOT DEFINED ${kit}_VERSION_TWEAK)
  set(${kit}_VERSION_FULL "${${kit}_VERSION_FULL}-${${kit}_VERSION_UID}")
endif()

#-----------------------------------------------------------------------------
# Slicer configuration
#-----------------------------------------------------------------------------
add_subdirectory(Modules)

#-----------------------------------------------------------------------------
# Superbuild script
#-----------------------------------------------------------------------------
if(${kit}_SUPERBUILD)
  add_subdirectory(${${kit}_SUPERBUILD_DIR})
  return()
endif()

# --------------------------------------------------------------------------
# Configure and install headers
# --------------------------------------------------------------------------
include(ConfigureFileMultipleTimes)
configure_file_multiple_times(
  INPUT_FILE ${${kit}_CMAKE_SOURCE_DIR}/qSlicerAppVersionConfigure.h.in
  OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/qSlicerAppVersionConfigure.h
  NUMBER_OF_CONFIGURE 2
  )
set_property(GLOBAL APPEND PROPERTY ${kit}_INCLUDE_DIRS
  ${CMAKE_CURRENT_BINARY_DIR}
  )

# --------------------------------------------------------------------------
# Sub projects
# --------------------------------------------------------------------------
include(ExportLibrary)

set(${kit}_LAUNCHER_EXECUTABLE
    ${CMAKE_CURRENT_BINARY_DIR}/../Slicer-build/${kit})
set(${kit}_LAUNCH_COMMAND
    ${${kit}_LAUNCHER_EXECUTABLE} --launcher-no-splash --launch)

add_subdirectory(Libs)

#
# The following variables have been set by each sub directory project.
# They are used to configure ${kit}Config.cmake.in.

get_property(${kit}_LIBRARIES GLOBAL PROPERTY ${kit}_LIBRARIES)
if (${kit}_LIBRARIES)
  list(REMOVE_DUPLICATES ${kit}_LIBRARIES)
endif()

get_property(${kit}_INCLUDE_DIRS GLOBAL PROPERTY ${kit}_INCLUDE_DIRS)
if (${kit}_INCLUDE_DIRS)
  list(REMOVE_DUPLICATES ${kit}_INCLUDE_DIRS)
endif()

get_property(${kit}_LIBRARY_DIRS GLOBAL PROPERTY ${kit}_LIBRARY_DIRS)
if (${kit}_LIBRARY_DIRS)
  list(REMOVE_DUPLICATES ${kit}_LIBRARY_DIRS)
endif()

# --------------------------------------------------------------------------
# Install project
# --------------------------------------------------------------------------
configure_file_multiple_times(
  INPUT_FILE ${${kit}_CMAKE_SOURCE_DIR}/ApplicationConfig.cmake.in
  OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${kit}Config.cmake
  NUMBER_OF_CONFIGURE 2
  )
