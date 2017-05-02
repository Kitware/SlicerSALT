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

set(proj Slicer)

set(${proj}_DEPENDENCIES "")
ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR ${proj}_DEPENDENCIES)

if(${CMAKE_PROJECT_NAME}_USE_SYSTEM_${proj})
  message(FATAL_ERROR "Enabling ${CMAKE_PROJECT_NAME}_USE_SYSTEM_${proj} is not supported")
endif()

if(DEFINED ${proj}_DIR AND NOT EXISTS ${${proj}_DIR})
  message(FATAL_ERROR "${proj}_DIR variable is defined but corresponds to nonexistent directory")
endif()

if(NOT DEFINED ${proj}_DIR)

  if(NOT DEFINED git_protocol)
      set(git_protocol "git")
  endif()

  set(${proj}_DIR ${CMAKE_BINARY_DIR}/S-bld)
  set(${proj}_PREFIX ${CMAKE_BINARY_DIR}/${proj}-prefix)
  set(${proj}_INTERNAL_DEPENDENCIES_LIST ${APPLICATION_NAME}
    # List here additional external projects
    )

  find_package(Qt4 REQUIRED)

  get_property(${APPLICATION_NAME}_MODULES GLOBAL PROPERTY ${APPLICATION_NAME}_MODULES)
  set(${proj}_QTLOADABLEMODULES_DISABLED
    SceneViews
    SlicerWelcome
    ViewControllers
    )
  set(${proj}_QTSCRIPTEDMODULES_DISABLED
    DataProbe
    Endoscopy
    LabelStatistics
    PerformanceTests
    SampleData
    SurfaceToolbox
    VectorToScalarVolume
    )
  set(Slicer_CLIMODULES_DISABLED
    ACPCTransform
    AddScalarVolumes
    CastScalarVolume
    CheckerBoardFilter
    CreateDICOMSeries
    CurvatureAnisotropicDiffusion
    ExecutionModelTour
    ExpertAutomatedRegistration
    ExtractSkeleton
    FreesurferSurfaceSectionExtraction
    GaussianBlurImageFilter
    GradientAnisotropicDiffusion
    GrayscaleFillHoleImageFilter
    GrayscaleGrindPeakImageFilter
    GrayscaleModelMaker
    HistogramMatching
    ImageLabelCombine
    LabelMapSmoothing
    MaskScalarVolume
    MedianImageFilter
    ModelToLabelMap
    MultiplyScalarVolumes
    N4ITKBiasFieldCorrection
    OrientScalarVolume
    PETStandardUptakeValueComputation
    ProbeVolumeWithModel
    RobustStatisticsSegmenter
    SimpleRegionGrowingSegmentation
    SubtractScalarVolumes
    ThresholdScalarVolume
    VotingBinaryHoleFillingImageFilter
    MergeModels
    ModelMaker
    ResampleDTIVolume
    # ResampleScalarVectorDWIVolume # Needed by 'CropVolume' module
    )
  # Legacy
  list(APPEND Slicer_CLIMODULES_DISABLED
    BSplineToDeformationField
    FiducialRegistration
    ResampleScalarVolume
    )

  if(DEFINED ${proj}_SOURCE_DIR)
    list(APPEND ${proj}_EP_ARGS DOWNLOAD_COMMAND "")
  else()
    set(${proj}_SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj})
    list(APPEND ${proj}_EP_ARGS
      GIT_REPOSITORY ${git_protocol}://github.com/hina-shah/Slicer.git
      GIT_TAG e3d63a2f257578448191bd4009b77ed09599eb55
      )
  endif()

  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    SOURCE_DIR ${${proj}_SOURCE_DIR}
    BINARY_DIR ${${proj}_DIR}
    PREFIX ${${proj}_PREFIX}
    INSTALL_COMMAND ""
    CMAKE_CACHE_ARGS
      -DSlicer_ORGANIZATION_DOMAIN:STRING=${APPLICATION_DOMAIN}
      -DSlicer_ORGANIZATION_NAME:STRING=${APPLICATION_VENDOR}
      -DSlicer_DEFAULT_HOME_MODULE:STRING=Home
      -DBUILD_TESTING:BOOL=OFF
      # Compile options
      -DADDITIONAL_C_FLAGS:STRING=${ADDITIONAL_C_FLAGS}
      -DADDITIONAL_CXX_FLAGS:STRING=${ADDITIONAL_CXX_FLAGS}
      -DCMAKE_C_COMPILER:FILEPATH=${CMAKE_C_COMPILER}
      -DCMAKE_C_FLAGS:STRING=${ep_common_c_flags}
      -DCMAKE_CXX_COMPILER:FILEPATH=${CMAKE_CXX_COMPILER}
      -DCMAKE_CXX_FLAGS:STRING=${ep_common_cxx_flags}
      -DCMAKE_EXE_LINKER_FLAGS:STRING=${CMAKE_EXE_LINKER_FLAGS}
      -DCMAKE_SHARED_LINKER_FLAGS:STRING=${CMAKE_SHARED_LINKER_FLAGS}
      # Install paths
      -D${proj}_INSTALL_BIN_DIR:STRING=${${APPLICATION_NAME}_INSTALL_BIN_DIR}
      -D${proj}_INSTALL_LIB_DIR:STRING=${${APPLICATION_NAME}_INSTALL_BIN_DIR}
      # Qt
      -DQT_QMAKE_EXECUTABLE:FILEPATH=${QT_QMAKE_EXECUTABLE}
      -D${proj}_REQUIRED_QT_VERSION:STRING=${QT_VERSION_MAJOR}.${QT_VERSION_MINOR}.${QT_VERSION_PATCH}
      #-D${proj}_ADDITIONAL_REQUIRED_QT_MODULES:STRING=PHONON
      # External projects
      -DEXTERNAL_PROJECT_ADDITIONAL_DIR:PATH=${${APPLICATION_NAME}_SUPERBUILD_DIR}
      -D${proj}_ADDITIONAL_DEPENDENCIES:STRING=${${proj}_INTERNAL_DEPENDENCIES_LIST}
      -D${proj}_USE_GIT_PROTOCOL:BOOL=${${APPLICATION_NAME}_USE_GIT_PROTOCOL}
      -D${proj}_DIR:PATH=${${proj}_DIR} # Required by External_<APPLICATION_NAME>.cmake
      # Application
      -D${APPLICATION_NAME}_SOURCE_DIR:PATH=${${APPLICATION_NAME}_SOURCE_DIR} # needed by External_${APPLICATION_NAME}.cmake
      -D${APPLICATION_NAME}App_APPLICATION_NAME:STRING=${APPLICATION_NAME}
      -D${proj}_APPLICATIONS_DIR:PATH=${${APPLICATION_NAME}_SOURCE_DIR}/Applications
      -D${proj}_MAIN_PROJECT:STRING=${APPLICATION_NAME}App
      # Slicer features
      -D${proj}_BUILD_DICOM_SUPPORT:BOOL=ON
      -D${proj}_BUILD_DIFFUSION_SUPPORT:BOOL=OFF
      -D${proj}_BUILD_EXTENSIONMANAGER_SUPPORT:BOOL=OFF
      -D${proj}_BUILD_MULTIVOLUME_SUPPORT:BOOL=OFF
      -D${proj}_USE_NUMPY:BOOL=ON
      -D${proj}_USE_OpenIGTLink:BOOL=OFF
      -D${proj}_USE_PYTHONQT_WITH_TCL:BOOL=OFF
      -D${proj}_USE_PYTHONQT:BOOL=ON
      -D${proj}_USE_QtTesting:BOOL=OFF
      -D${proj}_USE_SimpleITK:BOOL=OFF
      # Slicer built-in modules
      -D${proj}_CLIMODULES_DISABLED:STRING=${${proj}_CLIMODULES_DISABLED}
      -D${proj}_QTLOADABLEMODULES_DISABLED:STRING=${${proj}_QTLOADABLEMODULES_DISABLED}
      -D${proj}_QTSCRIPTEDMODULES_DISABLED:STRING=${${proj}_QTSCRIPTEDMODULES_DISABLED}
      -D${proj}_BUILD_EMSegment:BOOL=OFF
      # Slicer remote modules
      -D${proj}_BUILD_BRAINSTOOLS:BOOL=OFF
      -D${proj}_BUILD_ChangeTrackerPy:BOOL=OFF
      -D${proj}_BUILD_CompareVolumes:BOOL=OFF
      -D${proj}_BUILD_DataStore:BOOL=OFF
      -D${proj}_BUILD_LandmarkRegistration:BOOL=OFF
      -D${proj}_EXTENSION_SOURCE_DIRS:STRING=${${APPLICATION_NAME}_MODULES}
      # Slicer favorite modules
      -DSlicer_DEFAULT_FAVORITE_MODULES:STRING=SubjectHierarchy,Volumes,Models,Transforms,Editor
    DEPENDS
      ${${proj}_DEPENDENCIES}
    )

  # This custom external project step forces the build and later
  # steps to run whenever a top level build is done...
  #
  # BUILD_ALWAYS flag is available in CMake 3.1 that allows force build
  # of external projects without this workaround. Remove this workaround
  # and use the CMake flag instead, when Slicer's required minimum CMake
  # version will be at least 3.1.
  #
  if(CMAKE_CONFIGURATION_TYPES)
    set(BUILD_STAMP_FILE "${CMAKE_CURRENT_BINARY_DIR}/${proj}-prefix/src/${proj}-stamp/${CMAKE_CFG_INTDIR}/${proj}-build")
  else()
    set(BUILD_STAMP_FILE "${CMAKE_CURRENT_BINARY_DIR}/${proj}-prefix/src/${proj}-stamp/${proj}-build")
  endif()
  ExternalProject_Add_Step(${proj} forcebuild
    COMMAND ${CMAKE_COMMAND} -E remove ${BUILD_STAMP_FILE}
    COMMENT "Forcing build step for '${proj}'"
    DEPENDEES build
    ALWAYS 1
    )

else()
  ExternalProject_Add_Empty(${proj} DEPENDS ${${proj}_DEPENDENCIES})
endif()
