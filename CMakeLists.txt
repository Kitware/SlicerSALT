cmake_minimum_required(VERSION 3.13.4)

# Enable C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Slicer sources
include(FetchContent)
if(NOT DEFINED slicersources_SOURCE_DIR)
  # Download Slicer sources and set variables slicersources_SOURCE_DIR and slicersources_BINARY_DIR
  FetchContent_Populate(slicersources
    GIT_REPOSITORY https://github.com/Slicer/Slicer
    GIT_TAG        1efef1b35da0f95835c4f56def90629782cd492e
    GIT_PROGRESS   1
    )
else()
  set(slicersources_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/slicersources-subbuild)
endif()

# macOS initialization
set(CMAKE_MODULE_PATH ${slicersources_SOURCE_DIR}/CMake ${CMAKE_MODULE_PATH})
include(SlicerInitializeOSXVariables)

# Update CMake module path
set(SlicerSALT_CMAKE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/CMake")
list(INSERT CMAKE_MODULE_PATH 0 ${SlicerSALT_CMAKE_DIR})
add_subdirectory(${SlicerSALT_CMAKE_DIR})
list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_CURRENT_BINARY_DIR}/CMake")

project(SlicerSALT)

# Configure Application
set(Slicer_APPLICATIONS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/Applications)
set(Slicer_MAIN_PROJECT "SlicerSALTApp")

# Set organization
set(Slicer_ORGANIZATION_DOMAIN "kitware.com")
set(Slicer_ORGANIZATION_NAME   "Kitware, Inc.")

# Default home and favorite modules
set(Slicer_DEFAULT_HOME_MODULE "Home")
set(Slicer_DEFAULT_FAVORITE_MODULES "Data, Volumes, Models, Transforms, Markups, SegmentEditor")

# Configure SuperBuild
set(SUPERBUILD_TOPLEVEL_PROJECT Slicer)
set(EXTERNAL_PROJECT_ADDITIONAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/SuperBuild")
include(ExternalProjectDependency)

if(NOT CMAKE_CONFIGURATION_TYPES)
  set(Slicer_DEFAULT_BUILD_TYPE "Release")
endif()
include(SlicerInitializeBuildType)
include(SlicerInitializeReleaseType)

# Installation folder and admin account requirement for Windows
if(WIN32)
  # Note: To avoid escaping issue, make sure to use forward slash when setting
  #       "Slicer_CPACK_NSIS_INSTALL_ROOT". It is replaced by "\\\\" in SlicerCPack.
  set(Slicer_CPACK_NSIS_INSTALL_REQUIRES_ADMIN_ACCOUNT ON)
  if(Slicer_CPACK_NSIS_INSTALL_REQUIRES_ADMIN_ACCOUNT)
    # User has administrative privileges, therefore we can install to shared folder
    # "C:\Program Files" or "C:\Program Files (x86)".
    if(CMAKE_CL_64)
      set(Slicer_CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES64")
    else()
      set(Slicer_CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
    endif()
  else()
    # We do not require administrative privileges, therefore we install to user folder
    # "C:\Users\<username>\AppData\Local".
    set(Slicer_CPACK_NSIS_INSTALL_ROOT "$LOCALAPPDATA/${Slicer_ORGANIZATION_NAME}")
  endif()
endif()

# SlicerSALT options
# NA


# Slicer options
option(BUILD_TESTING                            "Build application test suite"                        ON)
option(Slicer_BUILD_DOCUMENTATION               "Build documentation (Doxygen, sphinx, ...)"          OFF)
if(WIN32)
  option(Slicer_BUILD_WIN32_CONSOLE             "Build application executable as a console app"       OFF)
endif()

option(Slicer_BUILD_DICOM_SUPPORT               "Build application with DICOM support"                OFF)
option(Slicer_BUILD_DIFFUSION_SUPPORT           "Build application with Diffusion support"            OFF)
option(Slicer_BUILD_EXTENSIONMANAGER_SUPPORT    "Build application with ExtensionManager support"     OFF)
option(Slicer_BUILD_MULTIVOLUME_SUPPORT         "Build application with MultiVolume support"          OFF)
option(Slicer_BUILD_PARAMETERSERIALIZER_SUPPORT "Build application with parameter serializer support" OFF)
option(Slicer_BUILD_WEBENGINE_SUPPORT           "Build application with Qt WebEngine support"         OFF)
option(Slicer_USE_PYTHONQT                      "Build application with Python support"               ON)
option(Slicer_USE_PYTHONQT_WITH_TCL             "Build application with Python Tcl adapter layer"     OFF)
option(Slicer_USE_QtTesting                     "Build application with QtTesting support"            OFF)
option(Slicer_USE_SimpleITK                     "Build application with SimpleITK support"            OFF)

option(Slicer_BUILD_BRAINSTOOLS                 "Build application with BRAINSTools module"           OFF)
option(Slicer_BUILD_DataStore                   "Build application with DataStore module"             OFF)
option(Slicer_BUILD_CompareVolumes              "Build application with ChangeTrackerPy module"       OFF)
option(Slicer_BUILD_LandmarkRegistration        "Build application with LandmarkRegistration module"  OFF)

# Addition Slicer dependencies
set(Slicer_ADDITIONAL_DEPENDENCIES
  )

# Enable Slicer built-in modules
set(Slicer_CLIMODULES_ENABLED
  MergeModels
  ModelMaker
  ResampleDTIVolume             # Needed by ResampleScalarVectorDWIVolume
  ResampleScalarVectorDWIVolume # Depends on DiffusionApplications, needed by CropVolume
  )
set(Slicer_QTLOADABLEMODULES_ENABLED
  )
set(Slicer_QTSCRIPTEDMODULES_ENABLED
  )

# Disable Slicer built-in modules
set(Slicer_CLIMODULES_DISABLED
  )
set(Slicer_QTLOADABLEMODULES_DISABLED
  SceneViews
  SlicerWelcome
  ViewControllers
  )
set(Slicer_QTSCRIPTEDMODULES_DISABLED
  DataProbe
  Editor
  EditorLib
  Endoscopy
  LabelStatistics
  PerformanceTests
  VectorToScalarVolume
  )

# Enable/Disable Slicer custom modules: To create a new module, use the SlicerExtensionWizard.
set(Slicer_EXTENSION_SOURCE_DIRS
  ${SlicerSALT_SOURCE_DIR}/Modules/Scripted/Home
  ${SlicerSALT_SOURCE_DIR}/Modules/Scripted/ShapeAnalysisToolBox
  )

#-----------------------------------------------------------------------------
# Add Eigen3 (required by at least SlicerSkeletalRepresentation)

# Eigen3 is not a regular Slicer extension but its sources are added to
# Slicer in a similar way. This ensures that extension bundled into Slicer
# and using the target "Eigen3::Eigen" can do so after simply calling
# "find_package(Eigen3 REQUIRED)".

# we are using a branch meanwhile upstream merge proposed cmake fixes

# Disable testing of Eigen
if(NOT DEFINED EIGEN_BUILD_TESTING)
  set(EIGEN_BUILD_TESTING OFF)
endif()
mark_as_superbuild(EIGEN_BUILD_TESTING)

# Do not add convenience blas/lapack target to avoid conflict with "lapack" project
set(EIGEN_ADD_BLAS_LAPACK_TARGETS 0)
mark_as_superbuild(EIGEN_ADD_BLAS_LAPACK_TARGETS)

# Disable Qt based test to avoid finding the wrong Qt version
set(EIGEN_TEST_NOQT 1)
mark_as_superbuild(EIGEN_TEST_NOQT)

# this line affects this file where EP_GIT_PROTOCOL is used.
set(EP_GIT_PROTOCOL "https")
# this line affects the rest of the slicer superbuild
set(Slicer_USE_GIT_PROTOCOL OFF)

set(extension_name "Eigen3")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/eigen-git-mirror
  GIT_TAG        16e54382bc1938069cf9faa200f009c48964195e # slicersalt-3.3-2018-09-07-2fd9e7447
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Add remote extension source directories

#-----------------------------------------------------------------------------
# MeshToLabelMap
set(extension_name "MeshToLabelMap")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        abba97578cf86a21e89a21b81be8bcc142f0e897
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})


#-----------------------------------------------------------------------------
# Srep
set(extension_name "SlicerSkeletalRepresentation")
set(short_extension_name "SRep") # Use shorter extension name to avoid issues with too long paths on windows
set(SkeletalRepresentation_SUPERBUILD 0 CACHE INTERNAL "")
mark_as_superbuild(SkeletalRepresentation_SUPERBUILD)
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${short_extension_name}")
FetchContent_Populate(${short_extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/KitwareMedical/SlicerSkeletalRepresentation.git
  GIT_TAG        baa5290a9de6337240dab581a6d84feb0dc16efa # master
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})


#-----------------------------------------------------------------------------
# GROUPS
set(extension_name "GROUPS")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
set(RigidAlignmentModule_TITLE "SPHARM-PDM Correspondence Improvement" CACHE INTERNAL "")
mark_as_superbuild(RigidAlignmentModule_TITLE)
set(RigidAlignmentModule_CATEGORY "Shape Creation" CACHE INTERNAL "")
mark_as_superbuild(RigidAlignmentModule_CATEGORY)
set(GROUPS_BUILD_CLI_MODULE_Groups 0 CACHE INTERNAL "")
mark_as_superbuild(GROUPS_BUILD_CLI_MODULE_Groups)
set(GROUPS_BUILD_SCRIPTED_MODULE_GroupWiseRegistrationModule 0 CACHE INTERNAL "")
mark_as_superbuild(GROUPS_BUILD_SCRIPTED_MODULE_GroupWiseRegistrationModule)
set(RigidAlignment_CATEGORY "Shape Creation.Advanced" CACHE INTERNAL "")
mark_as_superbuild(VARS RigidAlignment_CATEGORY:STRING PROJECTS RigidAlignment)
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        6f372beaea16a6c8284b866f672948005d231afe # slicersalt-2022-06-27-6f372beae
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})
list(APPEND EXTERNAL_PROJECT_ADDITIONAL_DIRS ${${extension_name}_SOURCE_DIR}/SuperBuild)

#-----------------------------------------------------------------------------
# MFSDA

set(MFSDA_BUILD_SLICER_EXTENSION 1)
mark_as_superbuild(MFSDA_BUILD_SLICER_EXTENSION:BOOL)

set(extension_name "MFSDA_Python")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        3ee1dbbab04b4068822245e695606552a6446f3e # slicersalt-2020-01-16-0a67df1d8
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

list(APPEND Slicer_ADDITIONAL_DEPENDENCIES
  python-mfsda-requirements
  )

#-----------------------------------------------------------------------------
# ShapeVariationAnalyzer

set(ShapeVariationAnalyzer_BUILD_SLICER_EXTENSION 1)
mark_as_superbuild(ShapeVariationAnalyzer_BUILD_SLICER_EXTENSION:BOOL)

set(extension_name "ShapeVariationAnalyzer")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        9a48b6c5a51ba815e0f72baf732bd2b29ec6e96d # slicersalt-2022-04-04-102d832
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Procrustes
set(extension_name "ProcrustesRegistrationModule")
set(short_extension_name "Procrustes") # Use shorter extension name to avoid issues with too long paths on windows
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${short_extension_name}")
FetchContent_Populate(${short_extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/ProcrustesRegistrationModule.git
  GIT_TAG        52ece6b958904ff2199d1f4981e8d64c74f4c4bb # main
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})


#-----------------------------------------------------------------------------
# ModelToModelDistance

# Notes:
#
# (1) Naming is not consistent: "ModelToModelDistance" is the extension name
#     and "3DMetricTools" is both the repository and cmake project name.
#
# (2) The project provides two tools: "ModelToModelDistance" licensed under Apache 2.0
#     and "3DMeshMetric" licensed under GPLv3.
#
# (3) SlicerSALT integrates only "ModelToModelDistance" CLI
#

set(3DMetricTools_BUILD_TESTING 0)
mark_as_superbuild(3DMetricTools_BUILD_TESTING:BOOL)

set(extension_name "ModelToModelDistance")
set(${extension_name}_EXTERNAL_PROJECT_EXCLUDE_ALL TRUE)
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/3DMetricTools
  GIT_TAG        a54cb56b835b731ac3744ad6c80ece6f995f17cf # slicersalt-2021-10-29-4b4e478
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# shape4D

# Notes:
#
# shape4D executable depends on FFTW. FFTW is available under two licenses:
# (1) GPLv2 or any later version.
# (2) Commercial license removing the GPL restrictions.
# For more details, see  http://www.fftw.org/doc/License-and-Copyright.html

set(shape4D_BUILD_TESTING OFF)
mark_as_superbuild(shape4D_BUILD_TESTING:BOOL)

set(shape4D_USE_SEM ON)
mark_as_superbuild(shape4D_USE_SEM:BOOL)

set(shape4D_USE_VTK ON)
mark_as_superbuild(shape4D_USE_VTK:BOOL)

set(extension_name "shape4D")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        0c53f0a0be7144806a16ddfc13e535a145d710e8 # slicersalt-2021-10-29-215f0b6
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# ShapePopulationViewer

set(ShapePopulationViewer_BUILD_TESTING OFF)
mark_as_superbuild(ShapePopulationViewer_BUILD_TESTING:BOOL)

set(extension_name "ShapePopulationViewer")
set(${extension_name}_EXTERNAL_PROJECT_EXCLUDE_ALL TRUE)
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        529e6eb8e9df49c6ae0462d28d5ac6badae56b18 # slicersalt-2022-04-28-90fa962
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# ShapeRegressionExtension

set(ShapeRegressionExtension_BUILD_TESTING OFF)
mark_as_superbuild(ShapeRegressionExtension_BUILD_TESTING:BOOL)

set(extension_name "ShapeRegressionExtension")
set(${extension_name}_EXTERNAL_PROJECT_EXCLUDE_ALL TRUE)
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/KitwareMedical/${extension_name}
  GIT_TAG        91c3e98479ab9e25ac2ca109b92317b9e64b42f9 # slicersalt-2019-04-20-45cc2d4
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# SPHARM-PDM

set(SPHARM-PDM_BUILD_TESTING OFF)
mark_as_superbuild(SPHARM-PDM_BUILD_TESTING:BOOL)

set(extension_name "SPHARM-PDM")
set(${extension_name}_EXTERNAL_PROJECT_DEPENDENCIES LAPACK)
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        775d5c6423d991c4a324aa601d6947ff6c576384 # slicersalt-2022-04-29-1572f79
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# RegistrationBasedCorrespondence
set(RegistrationBasedCorrespondence_BUILD_TESTING OFF)
mark_as_superbuild(RegistrationBasedCorrespondence_BUILD_TESTING:BOOL)

set(extension_name "RegistrationBasedCorrespondence")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR	 ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/slicersalt/${extension_name}
  GIT_TAG        514ff33fa8ed6d679d1dc1be51e49084672a2b71 # master
  GIT_PROGRESS	 1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Add Slicer sources
add_subdirectory(${slicersources_SOURCE_DIR} ${slicersources_BINARY_DIR})
