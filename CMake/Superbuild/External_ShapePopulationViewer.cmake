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
#
# External project for the project.
#

set(proj ShapePopulationViewer)

# Set dependency list
set(${proj}_DEPENDENCIES Slicer)

# Include dependent projects if any
ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR ${proj}_DEPENDENCIES)

if(${CMAKE_PROJECT_NAME}_USE_SYSTEM_${proj})
  message(FATAL_ERROR "Enabling ${CMAKE_PROJECT_NAME}_USE_SYSTEM_${proj} is not supported !")
endif()

# Sanity checks
if(DEFINED ${proj}_DIR AND NOT EXISTS ${${proj}_DIR})
  message(FATAL_ERROR "${proj}_DIR variable is defined but corresponds to non-existing directory")
endif()

if(NOT DEFINED ${proj}_DIR AND NOT ${CMAKE_PROJECT_NAME}_USE_SYSTEM_${proj})

  if(NOT DEFINED git_protocol)
    set(git_protocol "git")
  endif()

  set(config ${CMAKE_BUILD_TYPE})
  if(DEFINED CMAKE_CONFIGURATION_TYPES)
    set(config ${CMAKE_CFG_INTDIR})
  endif()

  set(${proj}_DIR ${CMAKE_BINARY_DIR}/${proj}-build)
  set(${proj}_PACKAGE_DIR ${${proj}_DIR})
  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    GIT_REPOSITORY "${git_protocol}://github.com/NIRALUser/ShapePopulationViewer.git"
    GIT_TAG "5888b0ea7e32dbed9df90407dbbaa4605ccba0a8"
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
    BINARY_DIR ${${proj}_DIR}
    INSTALL_COMMAND ${CMAKE_COMMAND} --build ${${proj}_PACKAGE_DIR} --config ${config} --target package
    CMAKE_CACHE_ARGS
      -DCMAKE_CXX_FLAGS:STRING=${ep_common_cxx_flags}
      -DCMAKE_C_FLAGS:STRING=${ep_common_c_flags}
      -DCMAKE_BUILD_TYPE:STRING=${config}
      -DSlicer_DIR:PATH=${Slicer_DIR}/Slicer-build
      -D${proj}_BUILD_SLICER_EXTENSION:BOOL=ON
    DEPENDS
      ${${proj}_DEPENDENCIES}
    )

  list(APPEND ${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS
    ${${proj}_PACKAGE_DIR}/_CPack_Packages
    )
  MESSAGE(STATUS "~~~~~ Appended _cpack_packages for ${proj}, the variable is: ${${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS}")
else()
  ExternalProject_Add_Empty(${proj} DEPENDS ${${proj}_DEPENDENCIES})
endif()
