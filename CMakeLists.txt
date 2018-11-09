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
    GIT_TAG        9e3e45ae9ae437f95bd4a18d1550aeeb24895b95 # slicersalt-4.11-2018-11-08-94fb4a634
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/NIRALUser/MeshToLabelMap.git
  GIT_TAG        9e2e199b99396c570f5f26c0ccfd5e149f6b9d34
  GIT_PROGRESS   1
  QUIET
  )
list(APPEND Slicer_EXTENSION_SOURCE_DIRS ${${extension_name}_SOURCE_DIR})

#-----------------------------------------------------------------------------
# Sequences
set(extension_name "Sequences")
set(${extension_name}_SOURCE_DIR "${CMAKE_BINARY_DIR}/${extension_name}")
FetchContent_Populate(${extension_name}
  SOURCE_DIR     ${${extension_name}_SOURCE_DIR}
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/phcerdan/Sequences.git
  GIT_TAG        origin/disable_sampledata # Temporary workaround, see @SlicerSALT#50
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
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/NIRALUser/GROUPS
  GIT_TAG        d33f578ec73339bf97bdac510a826d01cc7b5fb4 # 2018-09-14 (master)
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
    GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/vicory/MFSDA_Python
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
# Add Slicer sources
add_subdirectory(${slicersources_SOURCE_DIR} ${slicersources_BINARY_DIR})

#-----------------------------------------------------------------------------
# Bundle non-conventional extensions
#
# Considering that
#  (1) extensions like "SPHARM-PDM" have a SuperBuild-like structure,
#  (2) they can conditionally include external projects like VTK when build as standalone package and
#  (3) the Slicer build-system collect the list of external project only based on filenames,
# we can not simply bundle them like any other SuperBuild-like extensions (e.g SlicerOpenIGTLink).
# Trying to do so would lead to re-building unwanted projects that would conflict with Slicer own projects.
#
# For these reasons, we use "SlicerPackageExtensions" module to first package each extension
# and then re-configure Slicer to package the associated directories.
include(SuperBuild/SlicerPackageExtensions.cmake)

