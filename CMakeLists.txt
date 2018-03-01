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
	  GIT_REPOSITORY git://github.com/Slicer/Slicer
	  GIT_TAG        e36fa70fb85aa4bea9ce7313b2ab467b4c401740 # 2018-03-01
	  GIT_PROGRESS   1
	  )
else()
  set(slicersources_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/slicersources-subbuild)
endif()

set(CMAKE_MODULE_PATH ${slicersources_SOURCE_DIR}/CMake ${CMAKE_MODULE_PATH})
include(SlicerBlockSetCMakeOSXVariables)

# Set application metadata
set(APPLICATION_NAME           "SlicerSALT")
set(Slicer_VERSION_MAJOR       "0")
set(Slicer_VERSION_MINOR       "1")
set(Slicer_VERSION_PATCH       "0")
project(${APPLICATION_NAME} VERSION "${Slicer_VERSION_MAJOR}.${Slicer_VERSION_MINOR}.${Slicer_VERSION_PATCH}")

# Set organization
set(Slicer_ORGANIZATION_DOMAIN "kitware.com")
set(Slicer_ORGANIZATION_NAME   "Kitware, Inc.")

# Configure Application
set(Slicer_APPLICATIONS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/Applications)
set(Slicer_MAIN_PROJECT ${APPLICATION_NAME}App)
set(${Slicer_MAIN_PROJECT}_APPLICATION_NAME ${APPLICATION_NAME})

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

# Slicer options
option(BUILD_TESTING                            "Build application test suite"                        ON)
option(Slicer_BUILD_DOCUMENTATION               "Build documentation (Doxygen, sphinx, ...)"          OFF)

option(Slicer_BUILD_QT_DESIGNER_PLUGINS         "Build Qt designer plugins"                           OFF)
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

# Enable Slicer built-in modules
set(Slicer_CLIMODULES_ENABLED
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
  SurfaceToolbox
  VectorToScalarVolume
  )

# Enable/Disable Slicer custom modules: To create a new module, use the SlicerExtensionWizard.
set(Slicer_EXTENSION_SOURCE_DIRS
  ${${APPLICATION_NAME}_SOURCE_DIR}/Modules/Scripted/Home
  ${${APPLICATION_NAME}_SOURCE_DIR}/Modules/Scripted/ShapeAnalysisToolBox
  )

# Add remote extension source directories
include(ExternalProjectAddSource)

Slicer_Remote_Add(MeshToLabelMap
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/NIRALUser/MeshToLabelMap.git
  GIT_TAG "9e2e199b99396c570f5f26c0ccfd5e149f6b9d34"
  LABELS REMOTE_MODULE
  )
list(APPEND Slicer_REMOTE_DEPENDENCIES MeshToLabelMap)

Slicer_Remote_Add(Sequences
  GIT_REPOSITORY ${EP_GIT_PROTOCOL}://github.com/SlicerRt/Sequences.git
  GIT_TAG "c890ed096d301ee7ea3426860a3cccfe50b377e8"
  LABELS REMOTE_MODULE
  )
list(APPEND Slicer_REMOTE_DEPENDENCIES Sequences)

# Add Slicer sources
add_subdirectory(${slicersources_SOURCE_DIR} ${slicersources_BINARY_DIR})

include(SuperBuild/SlicerPackageExtensions.cmake)

