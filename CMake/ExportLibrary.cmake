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

macro(export_library)
  set(target ${PROJECT_NAME})
  set_property(GLOBAL APPEND PROPERTY ${APPLICATION_NAME}_INCLUDE_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
    )
  if (TARGET ${target})
    set_property(GLOBAL APPEND PROPERTY ${APPLICATION_NAME}_LIBRARIES
      ${target}
      )
    if(WIN32)
      get_target_property(output_directory ${target} RUNTIME_OUTPUT_DIRECTORY)
    else()
      get_target_property(output_directory ${target} LIBRARY_OUTPUT_DIRECTORY)
    endif()
    set_property(GLOBAL APPEND PROPERTY ${APPLICATION_NAME}_LIBRARY_DIRS
      ${output_directory}
      )
  endif()
endmacro()
