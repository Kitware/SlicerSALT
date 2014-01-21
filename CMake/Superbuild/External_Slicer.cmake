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

# Set dependency list
set(${proj}_DEPENDENCIES "")

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

  set(${proj}_INTERNAL_DEPENDENCIES_LIST "${APPLICATION_NAME}")

  find_package(Qt4 REQUIRED)

  set(${proj}_DIR ${CMAKE_BINARY_DIR}/${proj}-build)

  # Retrieve modules
  get_property(${APPLICATION_NAME}_MODULES GLOBAL PROPERTY ${APPLICATION_NAME}_MODULES)

  # Set slicer build directory
  set(${proj}_DIR ${CMAKE_BINARY_DIR}/${proj}-build)

  set(Slicer_QTLOADABLEMODULES_DISABLED
    SlicerWelcome
    )
  set(Slicer_QTSCRIPTEDMODULES_DISABLED
    Endoscopy
    )
  set(Slicer_CLIMODULES_DISABLED
    ExecutionModelTour
    )

  if(DEFINED ${proj}_SOURCE_DIR)
    list(APPEND ${proj}_EP_ARGS DOWNLOAD_COMMAND "")
  else()
    set(${proj}_SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj})
    list(APPEND ${proj}_EP_ARGS
      GIT_REPOSITORY "${git_protocol}://github.com/Slicer/Slicer.git"
      GIT_TAG "62d9181e545cb05b0f1e5e55973ad6b7b49dcee8"
      )
  endif()

  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
    BINARY_DIR ${${proj}_DIR}
    PREFIX ${proj}${ep_suffix}
    INSTALL_COMMAND ""
    CMAKE_CACHE_ARGS
      -DCMAKE_CXX_FLAGS:STRING=${ep_common_cxx_flags}
      -DCMAKE_C_FLAGS:STRING=${ep_common_c_flags}
      -DADDITIONAL_C_FLAGS:STRING=${ADDITIONAL_C_FLAGS}
      -DADDITIONAL_CXX_FLAGS:STRING=${ADDITIONAL_CXX_FLAGS}
      -DBUILD_TESTING:BOOL=OFF
      -D${proj}_INSTALL_BIN_DIR:STRING=${${APPLICATION_NAME}_INSTALL_BIN_DIR}
      -D${proj}_INSTALL_LIB_DIR:STRING=${${APPLICATION_NAME}_INSTALL_BIN_DIR}
      -D${proj}_USE_GIT_PROTOCOL:BOOL=${${APPLICATION_NAME}_USE_GIT_PROTOCOL}
      # Qt
      -DQT_QMAKE_EXECUTABLE:FILEPATH=${QT_QMAKE_EXECUTABLE}
      -DSlicer_REQUIRED_QT_VERSION:STRING=${QT_VERSION_MAJOR}.${QT_VERSION_MINOR}.${QT_VERSION_PATCH}
      # External projects
      -DEXTERNAL_PROJECT_ADDITIONAL_DIR:PATH=${${APPLICATION_NAME}_SUPERBUILD_DIR}
      -DSlicer_ADDITIONAL_DEPENDENCIES:STRING=${${proj}_INTERNAL_DEPENDENCIES_LIST}
      # Application
      -D${APPLICATION_NAME}_SOURCE_DIR:PATH=${${APPLICATION_NAME}_SOURCE_DIR} # needed by External_${APPLICATION_NAME}.cmake
      -DSlicer_MAIN_PROJECT:STRING=${APPLICATION_NAME}App
      -D${APPLICATION_NAME}App_APPLICATION_NAME:STRING=${APPLICATION_NAME}
      -DSlicer_APPLICATIONS_DIR:PATH=${${APPLICATION_NAME}_SOURCE_DIR}/Applications
      # Slicer features
      -DSlicer_BUILD_DICOM_SUPPORT:BOOL=ON
      -DSlicer_BUILD_DIFFUSION_SUPPORT:BOOL=OFF
      -DSlicer_BUILD_EXTENSIONMANAGER_SUPPORT:BOOL=OFF
      -DSlicer_BUILD_MULTIVOLUME_SUPPORT:BOOL=OFF
      -DSlicer_USE_OpenIGTLink:BOOL=OFF
      -DSlicer_USE_QtTesting:BOOL=OFF
      -DSlicer_USE_PYTHONQT:BOOL=ON
      -DSlicer_USE_PYTHONQT_WITH_OPENSSL:BOOL=ON
      -DSlicer_USE_PYTHONQT_WITH_TCL:BOOL=OFF
      -DSlicer_USE_SimpleITK:BOOL=OFF
      # Slicer built-in modules
      -DSlicer_CLIMODULES_DISABLED:STRING=${Slicer_CLIMODULES_DISABLED}
      -DSlicer_QTLOADABLEMODULES_DISABLED:STRING=${Slicer_QTLOADABLEMODULES_DISABLED}
      -DSlicer_QTSCRIPTEDMODULES_DISABLED:STRING=${Slicer_QTSCRIPTEDMODULES_DISABLED}
      -DSlicer_BUILD_EMSegment:BOOL=OFF
      # Slicer remote modules
      -DSlicer_BUILD_BRAINSTOOLS:BOOL=OFF
      -DSlicer_BUILD_ChangeTrackerPy:BOOL=OFF
      -DSlicer_BUILD_CompareVolumes:BOOL=OFF
      -DSlicer_BUILD_DataStore:BOOL=OFF
      -DSlicer_BUILD_LandmarkRegistration:BOOL=OFF
      -DSlicer_EXTENSION_SOURCE_DIRS:STRING=${${APPLICATION_NAME}_MODULES}
      # Required by External_<APPLICATION_NAME>.cmake
      -DSlicer_DIR:PATH=${${proj}_DIR}
    DEPENDS
      ${${proj}_DEPENDENCIES}
    )

  # This custom external project step forces the build and later
  # steps to run whenever a top level build is done...
  ExternalProject_Add_Step(${proj} forcebuild
    COMMAND ${CMAKE_COMMAND} -E echo_append ""
    COMMENT "Forcing build step for '${proj}'"
    DEPENDEES configure
    DEPENDERS build
    ALWAYS 1
    )

else()
  ExternalProject_Add_Empty(${proj} DEPENDS ${${proj}_DEPENDENCIES})
endif()
