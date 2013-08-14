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
# Slicer
#
set(proj Slicer)

# Make sure this file is included only once
get_filename_component(proj_filename ${CMAKE_CURRENT_LIST_FILE} NAME_WE)
if(${proj_filename}_proj)
  return()
endif()
set(${proj_filename}_proj ${proj})

# Sanity checks
if(DEFINED ${proj}_DIR AND NOT EXISTS ${${proj}_DIR})
  message(FATAL_ERROR "${proj}_DIR variable is defined but corresponds to non-existing directory")
endif()

# Set dependency list
set(${proj}_DEPENDENCIES "")

# Include dependent projects if any
check_external_project_dependency(${proj})

set(${proj}_INTERNAL_DEPENDENCIES_LIST "${APPLICATION_NAME}")

# Restore the proj variable
get_filename_component(proj_filename ${CMAKE_CURRENT_LIST_FILE} NAME_WE)
set(proj ${${proj_filename}_proj})

if(NOT DEFINED ${proj}_DIR)
  message(STATUS "${__indent}Adding project ${proj}")
  find_package(Qt4 REQUIRED)

  # Set CMake OSX variable to pass down the external project
  set(CMAKE_OSX_EXTERNAL_PROJECT_ARGS)
  if(APPLE)
    list(APPEND CMAKE_OSX_EXTERNAL_PROJECT_ARGS
      -DCMAKE_OSX_ARCHITECTURES=${CMAKE_OSX_ARCHITECTURES}
      -DCMAKE_OSX_SYSROOT=${CMAKE_OSX_SYSROOT}
      -DCMAKE_OSX_DEPLOYMENT_TARGET=${CMAKE_OSX_DEPLOYMENT_TARGET})
  endif()
  set(${proj}_DIR ${CMAKE_BINARY_DIR}/${proj}-build)

  # Retrieve modules
  get_property(${APPLICATION_NAME}_MODULES GLOBAL PROPERTY ${APPLICATION_NAME}_MODULES)

  # Set slicer build directory
  set(${proj}_DIR ${CMAKE_BINARY_DIR}/${proj}-build)

  # Order the list of modules to build properly
  set(${APPLICATION_NAME}_MODULES_LIST)
  foreach(module ${${APPLICATION_NAME}_MODULES})
    if(${APPLICATION_NAME}_MODULES_LIST)
      set(${APPLICATION_NAME}_MODULES_LIST "${${APPLICATION_NAME}_MODULES_LIST}^^${module}")
    else()
      set(${APPLICATION_NAME}_MODULES_LIST ${module})
    endif()
  endforeach()

  # \todo
  #string(REPLACE ";" "\\^\\^" ${APPLICATION_NAME}_MODULES_LIST ${${APPLICATION_NAME}_MODULES})
  #string(REPLACE ";" "^^" ${proj}_INTERNAL_DEPENDENCIES_LIST ${${proj}_INTERNAL_DEPENDENCIES})

  ExternalProject_Add(${proj}
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
    BINARY_DIR ${${proj}_DIR}
    PREFIX ${proj}${ep_suffix}
    GIT_REPOSITORY "git://kwsource.kitwarein.com/slicer/slicer.git"
    GIT_TAG "741055078503a05d0a2c42706e08e22aa05853c7"
    ${${APPLICATION_NAME}_external_update}
    INSTALL_COMMAND ""
    CMAKE_GENERATOR ${gen}
    LIST_SEPARATOR &&
    CMAKE_ARGS
      -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
      -DCMAKE_CXX_FLAGS:STRING=${ep_common_cxx_flags}
      -DCMAKE_C_FLAGS:STRING=${ep_common_c_flags}
      -DCMAKE_INSTALL_PREFIX:PATH=${ep_install_dir}
      ${CMAKE_OSX_EXTERNAL_PROJECT_ARGS}
      -DADDITIONAL_C_FLAGS:STRING=${ADDITIONAL_C_FLAGS}
      -DADDITIONAL_CXX_FLAGS:STRING=${ADDITIONAL_CXX_FLAGS}
      -DBUILD_TESTING:BOOL=OFF
      -DCTEST_USE_LAUNCHERS:BOOL=${CTEST_USE_LAUNCHERS}
      -D${proj}_INSTALL_BIN_DIR:STRING=${${APPLICATION_NAME}_INSTALL_BIN_DIR}
      -D${proj}_INSTALL_LIB_DIR:STRING=${${APPLICATION_NAME}_INSTALL_BIN_DIR}
      -DGIT_EXECUTABLE:FILEPATH=${GIT_EXECUTABLE}
      -D${proj}_USE_GIT_PROTOCOL:BOOL=${${APPLICATION_NAME}_USE_GIT_PROTOCOL}
      -DQT_QMAKE_EXECUTABLE:FILEPATH=${QT_QMAKE_EXECUTABLE}
      -DSlicer_REQUIRED_QT_VERSION:STRING=${QT_VERSION_MAJOR}.${QT_VERSION_MINOR}.${QT_VERSION_PATCH}
      -DSlicer_ADDITIONAL_DEPENDENCIES:STRING=${${proj}_INTERNAL_DEPENDENCIES_LIST}
      -DSlicer_ADDITIONAL_EXTERNAL_PROJECT_DIR:PATH=${${APPLICATION_NAME}_SUPERBUILD_DIR}
      -D${APPLICATION_NAME}_SOURCE_DIR:PATH=${${APPLICATION_NAME}_SOURCE_DIR} # needed by External_${APPLICATION_NAME}.cmake
      -DSlicer_MAIN_PROJECT:STRING=${APPLICATION_NAME}App
      -D${APPLICATION_NAME}App_APPLICATION_NAME:STRING=${APPLICATION_NAME}
      -DSlicer_APPLICATIONS_DIR:PATH=${${APPLICATION_NAME}_SOURCE_DIR}/Applications
      -DSlicer_BUILD_DICOM_SUPPORT:BOOL=ON
      -DSlicer_BUILD_DIFFUSION_SUPPORT:BOOL=OFF
      -DSlicer_BUILD_EXTENSIONMANAGER_SUPPORT:BOOL=OFF
      -DSlicer_USE_QtTesting:BOOL=OFF
      -DSlicer_USE_PYTHONQT:BOOL=ON
      -DSlicer_QTLOADABLEMODULES_DISABLED:STRING=SlicerWelcome
      -DSlicer_BUILD_ChangeTrackerPy:BOOL=OFF
      -DSlicer_BUILD_MultiVolumeExplorer:BOOL=OFF
      -DSlicer_BUILD_MultiVolumeImporter:BOOL=OFF
      -DSlicer_BUILD_EMSegment:BOOL=OFF
      -DSlicer_BUILD_SkullStripper:BOOL=OFF
      -DSlicer_BUILD_SlicerWebGLExport:BOOL=OFF
      -DSlicer_USE_OpenIGTLink:BOOL=OFF
      -DSlicer_BUILD_OpenIGTLinkIF:BOOL=OFF
      -DSlicer_BUILD_BRAINSTOOLS:BOOL=OFF
      -DSlicer_BUILD_EXTENSIONS:BOOL=OFF
      -DSlicer_EXTENSION_SOURCE_DIRS:STRING=${${APPLICATION_NAME}_MODULES_LIST}
      -DSlicer_DIR:PATH=${${proj}_DIR}
      -DSlicer_PLATFORM_CHECK:BOOL=OFF
    DEPENDS
      ${${proj}_DEPENDENCIES}
    )

else()
  # The project is provided using ${proj}_DIR, nevertheless since other project may depend on ${proj},
  # let's add an 'empty' one
  #empty_external_project(${proj} "${${proj}_DEPENDENCIES}")
endif()

#list(APPEND ${APPLICATION_NAME}_SUPERBUILD_EP_ARGS -${proj}_DIR:PATH=${${proj}_DIR})

