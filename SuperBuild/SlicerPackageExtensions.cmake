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

set(proj SlicerPackageExtensions)

#-----------------------------------------------------------------------------
# List here all the extensions that should be built and packaged in Slicer.
# 
# Each extension name listed here corresponds to a file named 
# "External_<extensionName>.cmake" found in "<root>/Superbuild"
# directory.
#
set(${proj}_EXTENSIONS
  SPHARM-PDM
  shape4D
  ShapeRegressionExtension
  )

set(APPLICATION_NAME "SlicerSALT")

#-----------------------------------------------------------------------------
# This variable is updated at *CONFIGURE* time in each extension external projects
# and is expected to contain list of paths of this form:
#
#   /path/to/<extensionName>-build/[inner-build/]_CPack_Packages
#
set(${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS)

#-----------------------------------------------------------------------------
# This block will be executed when the project SlicerPackageExtensions defined below
# is configured.
#
# It allows to gather the list of extension "packaged" directories at *BUILD* time after
# the extensions have effectively been built and packaged.
#
# This is required because path are of the form
# 
#   /path/to/<extensionName>-build/_CPack_Packages/<platform>/<archiveType>/<packageName>
#
# and it is not practical to "guess" the exact <platform>, <archiveType> and <packageName> when configuring
# the top-level project.
#

if(DEFINED ${proj}_CONFIGURE)

  set(extension_install_dirs)

  foreach(cpack_package_dir IN LISTS EXTENSION_CPACK_PACKAGE_DIRS)

    set(extension_install_dir ${cpack_package_dir})

    # Lookup platform
    set(platform "unknown")
    foreach(_platform IN ITEMS "Darwin" "Linux" "win64")
      if(IS_DIRECTORY ${cpack_package_dir}/${_platform})
        set(platform ${_platform})
        break()
      endif()
    endforeach()
    set(extension_install_dir "${extension_install_dir}/${platform}")

    # Lookup archive_type
    set(archive_type "unknown")
    foreach(_archive_type IN ITEMS "TGZ" "ZIP")
      if(IS_DIRECTORY ${cpack_package_dir}/${platform}/${_archive_type})
        set(archive_type ${_archive_type})
        break()
      endif()
    endforeach()
    set(extension_install_dir "${extension_install_dir}/${archive_type}")

    # Lookup package name
    file(
      GLOB files
      RELATIVE ${extension_install_dir}/
      ${extension_install_dir}/*
      )
    set(package_name "unknown")
    foreach(file IN LISTS files)
      if(IS_DIRECTORY ${extension_install_dir}/${file})
        set(package_name ${file})
      endif()
    endforeach()
    set(extension_install_dir "${extension_install_dir}/${package_name}")

    # Sanity check
    if(NOT EXISTS ${extension_install_dir})
      message(WARNING "Skipping extension packaged directory: [${extension_install_dir}] does not exist.")
      continue()
    endif()

    #------------------------------------------------------------------------------
    # The SPT application has generally extension manager switched off.
    # To get to the generated extension libraries on Mac you need to go down 3 levels
    # of directories of the package dir - package_dir/Application_name.app/Contents/Extensions-<Rev#>.
    # Hence the following special case for the Apple.

    if(APPLE)
      set(extension_install_dir "${extension_install_dir}/${APPLICATION_NAME}.app/Contents")
      file(
        GLOB files
        RELATIVE ${extension_install_dir}/
        ${extension_install_dir}/*
        )
      set(extensions_dir "unknown")
      foreach(file IN LISTS files)
        if(IS_DIRECTORY ${extension_install_dir}/${file})
          set(extensions_dir ${file})
        endif()
      endforeach()
      set(extension_install_dir "${extension_install_dir}/${extensions_dir}")

      # get to the extension name directory (this is where lib and share directories live)
      file(
        GLOB files
        RELATIVE ${extension_install_dir}/
        ${extension_install_dir}/*
        )
      set(extension_name_dir "unknown")
      foreach(file IN LISTS files)
        if(IS_DIRECTORY ${extension_install_dir}/${file})
          set(extension_name_dir ${file})
        endif()
      endforeach()
      set(extension_install_dir "${extension_install_dir}/${extension_name_dir}")

    endif()

    list(APPEND extension_install_dirs
      ${extension_install_dir}
      )
  endforeach()

  string (REPLACE ";" "^^" extension_install_dirs "${extension_install_dirs}")
  message(STATUS "Slicer_EXTENSION_INSTALL_DIRS in slicer package extensions: ${extension_install_dirs}")

  # Re-configure Slicer
  execute_process(
    COMMAND ${CMAKE_COMMAND} -DSlicer_EXTENSION_INSTALL_DIRS:STRING=${extension_install_dirs} .
    WORKING_DIRECTORY ${Slicer_INNER_BUILD_DIR}
    )
  return()
endif()

#-----------------------------------------------------------------------------
include(ExternalProject)

#-----------------------------------------------------------------------------
# Set dependency list
set(${proj}_DEPENDENCIES ${${proj}_EXTENSIONS})

# Variable used in dependent External_* files
set(Slicer_INNER_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/Slicer-build)

# Include dependent projects if any
ExternalProject_Include_Dependencies(SlicerPackageExtensions
  DEPENDS_VAR SlicerPackageExtensions_DEPENDENCIES
  SUPERBUILD_VAR Slicer_SUPERBUILD
  )

set(config ${CMAKE_BUILD_TYPE})
if(DEFINED CMAKE_CONFIGURATION_TYPES)
  set(config ${CMAKE_CFG_INTDIR})
endif()

_sb_list_to_string("^^" "${${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS}" ${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS)
message(STATUS "${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS: ${${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS}")

ExternalProject_Add(${proj}
  ${${proj}_EP_ARGS}
  DOWNLOAD_COMMAND ""
  SOURCE_DIR ${proj}
  BUILD_IN_SOURCE 1
  CONFIGURE_COMMAND ${CMAKE_COMMAND}
    -DSlicer_INNER_BUILD_DIR:PATH=${Slicer_INNER_BUILD_DIR}
    -DEXTENSION_CPACK_PACKAGE_DIRS:STRING=${${APPLICATION_NAME}_EXTENSION_CPACK_PACKAGE_DIRS}
    -D${proj}_CONFIGURE=1
    -DAPPLICATION_NAME:STRING=${APPLICATION_NAME}
    -P ${CMAKE_CURRENT_LIST_FILE}
  BUILD_COMMAND ${CMAKE_COMMAND} --build ${Slicer_INNER_BUILD_DIR} --config ${config} --target package
  INSTALL_COMMAND ""
  DEPENDS
    ${${proj}_DEPENDENCIES} Slicer
  )

