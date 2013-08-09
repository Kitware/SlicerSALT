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

macro(check_external_project_dependency proj)
  # Set indent variable if needed
  if(NOT DEFINED __indent)
    set(__indent "")
  else()
    set(__indent "${__indent}  ")
  endif()

  # Sanity checks
  if(NOT DEFINED ${proj}_DEPENDENCIES)
    message(FATAL_ERROR "${__indent}${proj}_DEPENDENCIES variable is NOT defined !")
  endif()

  # Display dependency of project being processed
  if("${${proj}_DEPENDENCIES}" STREQUAL "")
    message(STATUS "SuperBuild - ${__indent}${proj}[OK]")
  else()
    set(dependency_str " ")
    foreach(dep ${${proj}_DEPENDENCIES})
      if(External_${dep}_FILE_INCLUDED)
        set(dependency_str "${dependency_str}${dep}[INCLUDED], ")
      else()
        set(dependency_str "${dependency_str}${dep}, ")
      endif()
    endforeach()
    message(STATUS "SuperBuild - ${__indent}${proj} => Requires${dependency_str}")
  endif()

  # Include dependencies
  foreach(dep ${${proj}_DEPENDENCIES})
    if(NOT External_${dep}_FILE_INCLUDED)
      if (EXISTS "${${APPLICATION_NAME}_SUPERBUILD_DIR}/External_${dep}.cmake")
        include(${${APPLICATION_NAME}_SUPERBUILD_DIR}/External_${dep}.cmake)
      else()
        message(FATAL_ERROR "Could not find ${${APPLICATION_NAME}_SUPERBUILD_DIR}/External_${dep}.cmake")
      endif()
    endif()
  endforeach()

  # If project being process has dependencies, indicates it has also been added.
  if(NOT "${${proj}_DEPENDENCIES}" STREQUAL "")
    message(STATUS "SuperBuild - ${__indent}${proj}[OK]")
  endif()

  # Update indent variable
  string(LENGTH "${__indent}" __indent_length)
  math(EXPR __indent_length "${__indent_length}-2")
  if(NOT ${__indent_length} LESS 0)
    string(SUBSTRING "${__indent}" 0 ${__indent_length} __indent)
  endif()
endmacro()
