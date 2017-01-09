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

# Usage:
# \code
# SIMPLE_TEST( <test_exec_name> <testname> [argument1 ...])
# \endcode
#
# test_exec_name variable usually matches the value of PROJECT_NAME.
#
# The macro also associates a label to the test based on the current value of test_exec_name (or CLP or EXTENSION_NAME).
#
# Optionnal test argument(s) can be passed after specifying the <testname>.

macro(SIMPLE_TEST test_exec_name testname)

  if("${test_exec_name}" STREQUAL "")
    message(FATAL_ERROR "error: test_exec_name variable is not set !")
  endif()

  if("${${APPLICATION_NAME}_LAUNCH_COMMAND}" STREQUAL "")
    message(FATAL_ERROR "error: variable is not set !")
  endif()

  if(NOT TARGET ${test_exec_name})
    message(FATAL_ERROR "error: Target '${test_exec_name}' is not defined !")
  endif()

  add_test(NAME ${testname}
           COMMAND ${${APPLICATION_NAME}_LAUNCH_COMMAND} $<TARGET_FILE:${test_exec_name}> ${testname} ${ARGN})
  set_property(TEST ${testname} PROPERTY LABELS ${test_exec_name})
endmacro()

