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
# Usage:
# \code
# configure_file_multiple_times INPUT_FILE OUTPUT_FILE NUMBER_OF_CONFIGURE)
# \endcode
#
# INPUT_FILE and OUTPUT_FILE are used to configure file using the configure_file.
# NUMBER_OF_CONFIGURE is the number of times the file is configured.
#

macro(configure_file_multiple_times)
  include(CMakeParseArguments)
  set(oneValueArgs INPUT_FILE OUTPUT_FILE NUMBER_OF_CONFIGURE)
  cmake_parse_arguments(MY "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  if("${MY_INPUT_FILE}" STREQUAL "" OR "${MY_OUTPUT_FILE}" STREQUAL "")
    message(FATAL_ERROR "error: INPUT_FILE and OUTPUT_FILE should be specified !")
  endif()

  if(NOT EXISTS "${MY_SOURCE_DIR}")
    set(MY_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
  endif()

  configure_file(${MY_INPUT_FILE} ${MY_OUTPUT_FILE})

  set(number 1)
  while (${MY_NUMBER_OF_CONFIGURE} GREATER number)
    configure_file(${MY_OUTPUT_FILE} ${MY_OUTPUT_FILE})
    math(EXPR number "${number} + 1" ) # decrement number
  endwhile()

endmacro()

