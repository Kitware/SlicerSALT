cmake_minimum_required(VERSION 3.11)

# Enable C++11
if(NOT DEFINED CMAKE_CXX_STANDARD)
  if(DEFINED Qt5_DIR)
    set(CMAKE_CXX_STANDARD 11)
  else()
    set(CMAKE_CXX_STANDARD 98)
  endif()
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Slicer sources
include(FetchContent)
if(NOT DEFINED slicersources_SOURCE_DIR)
  # Download Slicer sources and set variables slicersources_SOURCE_DIR and slicersources_BINARY_DIR
  FetchContent_Populate(slicersources
    GIT_REPOSITORY https://github.com/jcfr/Slicer
    GIT_TAG        57cf303f19cce128022752c12e2af7c5af3afb92 # slicersalt-4.11-2018-11-19-559e3deb0
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
  set(CMAKE_DEFAULT_BUILD_TYPE "Release")
endif()
include(SlicerInitializeBuildType)
include(SlicerInitializeReleaseType)

# SlicerSALT options
option(SlicerSALT_BUILD_MFSDA                   "Build and bundle MFSDA extension" OFF)


# Slicer options
option(BUILD_TESTING                            "Build application test suite"                        ON)
option(Slicer_BUILD_DOCUMENTATION               "Build documentation (Doxygen, sphinx, ...)"          OFF)
if(WIN32)
  option(Slicer_BUILD_WIN32_CONSOLE             "Build application executable as a console app"       OFF)
endif()

option(Slicer_BUILD_DICOM_SUPPORT               "Build application with DICOM support"                ON)
option(Slicer_BUILD_DIFFUSION_SUPPORT           "Build application with Diffusion support"            OFF)
option(Slicer_BUILD_EXTENSIONMANAGER_SUPPORT    "Build application with ExtensionManager support"     OFF)
option(Slicer_BUILD_MULTIVOLUME_SUPPORT         "Build application with MultiVolume support"          OFF)
option(Slicer_BUILD_PARAMETERSERIALIZER_SUPPORT "Build application with parameter serializer support" OFF)
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
  DMRIInstall
  Endoscopy
  LabelStatistics
  PerformanceTests
  SampleData
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

set(extension_name "Eigen3")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/jcfr/eigen-git-mirror
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/NIRALUser/${extension_name}
  GIT_TAG        9e2e199b99396c570f5f26c0ccfd5e149f6b9d34
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Sequences

set(SEQUENCES_ENABLE_SAMPLEDATA_MODULE OFF)
mark_as_superbuild(SEQUENCES_ENABLE_SAMPLEDATA_MODULE:BOOL)

set(extension_name "Sequences")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/SlicerRt/${extension_name}
  GIT_TAG        ea6ce4b80c41160aceb1cbea52a858973a25fa9e
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Srep
set(extension_name "SlicerSkeletalRepresentation")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/SRep")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/KitwareMedical/SlicerSkeletalRepresentation
  GIT_TAG        f163fcb264b16af0b8f2a8348f9dd959b14cca23 # fix-window-build-error
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# GROUPS
set(extension_name "GROUPS")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/vicory/${extension_name}
  GIT_TAG        cba8671e95d379bc2ad2389fc1bb63e7d4cda76f # slicersalt-2018-11-16-15c897e
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})
list(APPEND EXTERNAL_PROJECT_ADDITIONAL_DIRS ${${extension_name}_SOURCE_DIR}/SuperBuild)

#-----------------------------------------------------------------------------
# MFSDA
if(SlicerSALT_BUILD_MFSDA)
  set(extension_name "MFSDA_Python")
  set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
  FetchContent_Populate(${extension_name}
    SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
    GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/vicory/${extension_name}
    GIT_TAG        a4d6b6ad94d91bfe4895f1bf8565561c38240e3b # branch: fix_extension_build
    GIT_PROGRESS   1
    QUIET
    )
  list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

  list(APPEND Slicer_ADDITIONAL_DEPENDENCIES
    python-scipy
    python-pandas
    python-statsmodels
    )
endif()

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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/jcfr/3DMetricTools
  GIT_TAG        a323e0bcfffd112e517cf28bf6a96dca10d32047 # branch: slicersalt-2017-10-06-dbd3b88a2
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/jcfr/${extension_name}
  GIT_TAG        b175600fc38671a0d139dfbaaa61165aab12bdbc # slicersalt-2018-09-27-e6c242627
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/jcfr/${extension_name}
  GIT_TAG        8112d7b1253a94426b510a53779c20118e483c1a # slicersalt-2018-11-26-92fb222
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/jcfr/${extension_name}
  GIT_TAG        c186eeb30a99a20c12cc706d2e392552992d479a # slicersalt-2018-09-17-ff44744
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/jcfr/${extension_name}
  GIT_TAG        f78ef12958847d35fb46c1eab3a2e2b59f22c437 # support-direct-integration-in-custom-slicer-app
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Add Slicer sources
add_subdirectory(${slicersources_SOURCE_DIR} ${slicersources_BINARY_DIR})
