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

set(${APPLICATION_NAME}_DEPENDENCIES Slicer SlicerPackageExtensions)

#-----------------------------------------------------------------------------
# WARNING - No change should be required after this comment
#           when you are adding a new external project dependency.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Git protocol option
#
option(${APPLICATION_NAME}_USE_GIT_PROTOCOL "If behind a firewall turn this OFF to use http instead." ON)

set(git_protocol "git")
if(NOT ${APPLICATION_NAME}_USE_GIT_PROTOCOL)
  set(git_protocol "http")
endif()

#-----------------------------------------------------------------------------
# Enable and setup External project global properties
#

set(ep_suffix "-cmake")
set(ep_common_c_flags "${CMAKE_C_FLAGS_INIT} ${ADDITIONAL_C_FLAGS}")
set(ep_common_cxx_flags "${CMAKE_CXX_FLAGS_INIT} ${ADDITIONAL_CXX_FLAGS}")

#-----------------------------------------------------------------------------
# Include remote modules
#

include(ExternalProjectAddSource)

#ExternalProject_Add_Source(MyRemoteModule
#  GIT_REPOSITORY ${git_protocol}://github.com/MyUser/MyRemoteModule.git
#  GIT_TAG "123456790"
#  SOURCE_DIR_VAR MyRemoteModule_SOURCE_DIR
#  )
#list(APPEND Slicer_REMOTE_DEPENDENCIES MyRemoteModule)

set(Slicer_REMOTE_SOURCE_DIRS
#  ${MyRemoteModule_SOURCE_DIR}
  )
set_property(GLOBAL APPEND PROPERTY ${APPLICATION_NAME}_MODULES ${Slicer_REMOTE_SOURCE_DIRS})

#-----------------------------------------------------------------------------
# Include external projects
#

ExternalProject_Include_Dependencies(${APPLICATION_NAME}
  PROJECT_VAR APPLICATION_NAME
  DEPENDS_VAR ${APPLICATION_NAME}_DEPENDENCIES)
