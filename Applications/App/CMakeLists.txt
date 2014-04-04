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

set (APPLICATION_NAME ${Slicer_MAIN_PROJECT_APPLICATION_NAME})
project(${APPLICATION_NAME}App)

# --------------------------------------------------------------------------
# Slicer supports more than one application (i.e. an application
# "OtherApp" in addition to "APPLICATION_NAMEApp").
#
# In that specific case, it is required to differentiate the two applications
# and specify which one should be considered as the *Main* one.
#
# This is usually done within the top level CMakeLists.txt file by setting the variable
# Slicer_MAIN_PROJECT.
#
# Within the Applications/OtherApp/CMakeLists.txt of the secondary application,
# the project name should be updated, the variable 'SlicerApp_APPLICATION_NAME'
# could also be optionnally set to a custom value.
#

if(${PROJECT_NAME} STREQUAL ${Slicer_MAIN_PROJECT})
  set(SlicerApp_APPLICATION_NAME ${APPLICATION_NAME})
endif()

# --------------------------------------------------------------------------
# Project dependencies
# --------------------------------------------------------------------------
find_package(${APPLICATION_NAME} REQUIRED)
include(${${APPLICATION_NAME}_USE_FILE})

set(${PROJECT_NAME}_VERSION_MAJOR ${${APPLICATION_NAME}_VERSION_MAJOR})
set(${PROJECT_NAME}_VERSION_MINOR ${${APPLICATION_NAME}_VERSION_MINOR})
set(${PROJECT_NAME}_VERSION_PATCH ${${APPLICATION_NAME}_VERSION_PATCH})
if(DEFINED ${APPLICATION_NAME}_VERSION_TWEAK)
  set(${PROJECT_NAME}_VERSION_TWEAK ${${APPLICATION_NAME}_VERSION_TWEAK})
endif()
if(DEFINED ${APPLICATION_NAME}_VERSION_RC)
  set(${PROJECT_NAME}_VERSION_RC ${${APPLICATION_NAME}_VERSION_RC})
endif()
set(${PROJECT_NAME}_VERSION_FULL ${${APPLICATION_NAME}_VERSION})

#  --------------------------------------------------------------------------
# Build option(s)
# --------------------------------------------------------------------------
set(Slicer_HAS_CONSOLE_IO_SUPPORT TRUE)
if(WIN32)
  option(Slicer_BUILD_WIN32_CONSOLE "Build ${PROJECT_NAME} executable as a console app on windows (allows debug output)" ON)
  set(Slicer_HAS_CONSOLE_IO_SUPPORT ${Slicer_BUILD_WIN32_CONSOLE})
endif()

# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------
set(SlicerApp_SRCS
  qAppAboutDialog.cxx
  qAppAboutDialog.h
  qAppMainWindow.cxx
  qAppMainWindow.h
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppAboutDialog.cxx
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppAboutDialog.h
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppMainWindow.cxx
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppMainWindow.h
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppMainWindow_p.h
  )

set(SlicerApp_MOC_SRCS
  qAppAboutDialog.h
  qAppMainWindow.h
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppAboutDialog.h
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/qSlicerAppMainWindow.h
  )

set(SlicerApp_UI_SRCS
  Resources/UI/qAppAboutDialog.ui
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/Resources/UI/qSlicerAppAboutDialog.ui
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/Resources/UI/qSlicerAppMainWindow.ui
  )

set(SlicerApp_RESOURCES
  Resources/App.qrc
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp/Resources/SlicerApp.qrc
  ${qSlicerBaseQTGUI_SOURCE_DIR}/Resources/qSlicerBaseQTGUI.qrc
  ${qSlicerModulesCore_SOURCE_DIR}/Resources/qSlicerModulesCore.qrc
  ${${APPLICATION_NAME}_SOURCE_DIR}/Utilities/Qt/Resources.qrc
  )

QT4_WRAP_CPP(SlicerApp_SRCS ${SlicerApp_MOC_SRCS})
QT4_WRAP_UI(SlicerApp_UI_CXX ${SlicerApp_UI_SRCS})
QT4_ADD_RESOURCES(SlicerApp_QRC_SRCS ${SlicerApp_RESOURCES})

set(SlicerApp_INCLUDE_DIRECTORIES
  ${CMAKE_CURRENT_BINARY_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${Slicer_SOURCE_DIR}/Applications/SlicerApp
  ${Slicer_BINARY_DIR}/Applications/SlicerApp
  ${Slicer_Base_INCLUDE_DIRS}
  ${MRMLCore_INCLUDE_DIRS}
  ${MRMLLogic_INCLUDE_DIRS}
  ${qMRMLWidgets_INCLUDE_DIRS}
  ${qSlicerModulesCore_SOURCE_DIR}
  ${qSlicerModulesCore_BINARY_DIR}
  ${ITKFactoryRegistration_INCLUDE_DIRS}
  )
include_directories(${SlicerApp_INCLUDE_DIRECTORIES})

# --------------------------------------------------------------------------
# Translation
# --------------------------------------------------------------------------
set(KIT_LIBRARY_NAME "q${PROJECT_NAME}")

if(Slicer_BUILD_I18N_SUPPORT)
  set(TS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/Resources/Translations/")
  get_property(Slicer_LANGUAGES GLOBAL PROPERTY Slicer_LANGUAGES)

  include(${Slicer_SOURCE_DIR}/CMake/SlicerMacroTranslation.cmake)
  SlicerMacroTranslation(
    SRCS ${SlicerApp_SRCS}
    UI_SRCS ${SlicerApp_UI_SRCS}
    TS_DIR ${TS_DIR}
    TS_BASEFILENAME ${KIT_LIBRARY_NAME}
    TS_LANGUAGES ${Slicer_LANGUAGES}
    QM_OUTPUT_DIR_VAR QM_OUTPUT_DIR
    QM_OUTPUT_FILES_VAR QM_OUTPUT_FILES
    )

  set_property(GLOBAL APPEND PROPERTY Slicer_QM_OUTPUT_DIRS ${QM_OUTPUT_DIR})
endif()

# --------------------------------------------------------------------------
# Build the library
# --------------------------------------------------------------------------

add_library(${KIT_LIBRARY_NAME}
  ${SlicerApp_SRCS}
  ${SlicerApp_UI_CXX}
  ${SlicerApp_QRC_SRCS}
  ${QM_OUTPUT_FILES}
  )
set_target_properties(${KIT_LIBRARY_NAME} PROPERTIES LABELS ${PROJECT_NAME})

set(SlicerApp_LIBRARIES
  qSlicerBaseQTApp
  )

target_link_libraries(${KIT_LIBRARY_NAME}
  ${SlicerApp_LIBRARIES}
  )

#----------------------------------------------------------------------------
# ITKv3: Ensure ITKIOReview library is packaged on MacOSX
#----------------------------------------------------------------------------
if(Slicer_BUILD_EXTENSIONMANAGER_SUPPORT)
  # Force linking against ITKIOReview library to ensure it will be packaged and
  # fixed-up on MacOSX. That way extensions depending on the associated code
  # will load properly.
  # On unix-like platform, by using gcc the dependency should NOT be
  # optimized out. Hence, it is not required to explicitly call a function.
  # See http://slicer-devel.65872.n3.nabble.com/ITK-lib-missing-from-Mac-Slicer-package-needed-for-Plastimatch-tt4027274.html
  if(APPLE AND ITK_VERSION_MAJOR EQUAL 3)
    target_link_libraries(${KIT_LIBRARY_NAME} ITKIOReview)
  endif()
endif()

# --------------------------------------------------------------------------
# Configure Application Bundle Resources (Mac Only)
# --------------------------------------------------------------------------
if(Q_WS_MAC)
  set(apple_icon_file "DesktopIcon.icns")
  set(apple_bundle_sources "${CMAKE_CURRENT_SOURCE_DIR}/Resources/Icons/XLarge/${apple_icon_file}")

  if(NOT EXISTS "${apple_bundle_sources}")
    message(FATAL_ERROR "error: ${apple_bundle_sources} corresponds to an nonexistent file. "
                        "In case the main application name as been updated, make sure the associated icns icon exists.")
  endif()

  set_source_files_properties(
    "${apple_bundle_sources}"
    PROPERTIES
    MACOSX_PACKAGE_LOCATION Resources
    )
  set(MACOSX_BUNDLE_ICON_FILE ${apple_icon_file})
endif(Q_WS_MAC)

if(QT_MAC_USE_COCOA)
  get_filename_component(qt_menu_nib
    "@QT_QTGUI_LIBRARY_RELEASE@/Resources/qt_menu.nib"
    REALPATH)

  set(qt_menu_nib_sources
    "${qt_menu_nib}/classes.nib"
    "${qt_menu_nib}/info.nib"
    "${qt_menu_nib}/keyedobjects.nib"
    )
  set_source_files_properties(
    ${qt_menu_nib_sources}
    PROPERTIES
    MACOSX_PACKAGE_LOCATION Resources/qt_menu.nib
    )
  else(QT_MAC_USE_COCOA)
    set(qt_menu_nib_sources)
endif(QT_MAC_USE_COCOA)

# --------------------------------------------------------------------------
# Apply user-defined properties to the library target.
# --------------------------------------------------------------------------
if(Slicer_LIBRARY_PROPERTIES)
  set_target_properties(${KIT_LIBRARY_NAME} PROPERTIES ${Slicer_LIBRARY_PROPERTIES})
endif(Slicer_LIBRARY_PROPERTIES)

install(TARGETS ${KIT_LIBRARY_NAME}
  RUNTIME DESTINATION ${Slicer_INSTALL_BIN_DIR} COMPONENT RuntimeLibraries
  LIBRARY DESTINATION ${Slicer_INSTALL_LIB_DIR} COMPONENT RuntimeLibraries
  ARCHIVE DESTINATION ${Slicer_INSTALL_LIB_DIR} COMPONENT Development
  )

# --------------------------------------------------------------------------
# Build the executable
# --------------------------------------------------------------------------
if(NOT APPLE)
  set(SlicerApp_EXE_SUFFIX -real)
endif()

set(SlicerApp_EXE_OPTIONS)
if(WIN32)
  if(NOT Slicer_BUILD_WIN32_CONSOLE)
    set(SlicerApp_EXE_OPTIONS WIN32)
  endif()
endif()

if(APPLE)
  set(SlicerApp_EXE_OPTIONS MACOSX_BUNDLE)
endif()

add_executable(${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}
  ${SlicerApp_EXE_OPTIONS}
  Main.cxx
  ${apple_bundle_sources}
  ${qt_menu_nib_sources}
  )
set_target_properties(${PROJECT_NAME}${SlicerApp_EXE_SUFFIX} PROPERTIES LABELS ${PROJECT_NAME})

if(APPLE)
  set(link_flags "-Wl,-rpath,@loader_path/../")
  set_target_properties(${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}
    PROPERTIES
      OUTPUT_NAME ${SlicerApp_APPLICATION_NAME}
      MACOSX_BUNDLE_BUNDLE_VERSION "${Slicer_VERSION_FULL}"
      LINK_FLAGS ${link_flags}
    )
  if(DEFINED Slicer_VERSION_TWEAK)
    set_target_properties(${PROJECT_NAME}${SlicerApp_EXE_SUFFIX} PROPERTIES
      MACOSX_BUNDLE_SHORT_VERSION_STRING "${Slicer_VERSION_MAJOR}.${Slicer_VERSION_MINOR}.${Slicer_VERSION_PATCH}"
      )
  endif()
endif()

if(WIN32)
  if(Slicer_USE_PYTHONQT)
    # HACK - See http://www.na-mic.org/Bug/view.php?id=1180
    get_filename_component(_python_library_name_we ${PYTHON_LIBRARY} NAME_WE)
    get_target_property(_slicerapp_output_dir
      ${PROJECT_NAME}${SlicerApp_EXE_SUFFIX} RUNTIME_OUTPUT_DIRECTORY)
    add_custom_command(
      TARGET ${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}
      POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy_if_different
              ${PYTHON_LIBRARY_PATH}/${_python_library_name_we}.dll
              ${_slicerapp_output_dir}/${CMAKE_CFG_INTDIR}
      COMMENT "Copy '${_python_library_name_we}.dll' along side '${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}' executable. See Slicer issue #1180"
      )
  endif()
endif()

target_link_libraries(${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}
  ${KIT_LIBRARY_NAME}
  )

#-----------------------------------------------------------------------------
# Configure
# --------------------------------------------------------------------------
set(MY_LIBRARY_EXPORT_DIRECTIVE "Q_SLICER_APP_EXPORT")
set(MY_EXPORT_HEADER_PREFIX ${KIT_LIBRARY_NAME})
set(MY_LIBNAME ${KIT_LIBRARY_NAME})

configure_file(
  ${Slicer_SOURCE_DIR}/CMake/qSlicerExport.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/qSlicerAppExport.h
  )
set(dynamicHeaders
  "${dynamicHeaders};${CMAKE_CURRENT_BINARY_DIR}/${MY_EXPORT_HEADER_PREFIX}Export.h")

# --------------------------------------------------------------------------
# Install
# --------------------------------------------------------------------------
if(NOT APPLE)
  set(SlicerApp_INSTALL_DESTINATION_ARGS RUNTIME DESTINATION ${Slicer_INSTALL_BIN_DIR})
else()
  set(SlicerApp_INSTALL_DESTINATION_ARGS BUNDLE DESTINATION ".")
endif()

install(TARGETS ${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}
  ${SlicerApp_INSTALL_DESTINATION_ARGS}
  COMPONENT Runtime)

# --------------------------------------------------------------------------
# Configure Slicer Launcher (Only for main application)
# --------------------------------------------------------------------------
if(${PROJECT_NAME} STREQUAL ${Slicer_MAIN_PROJECT})
  if(Slicer_USE_CTKAPPLAUNCHER)
    include(${CTKAPPLAUNCHER_DIR}/CMake/ctkAppLauncher.cmake)

    # Define list of extra 'application to launch' to associate with the launcher
    set(extraApplicationToLaunchListForBuildTree)
    if(EXISTS "${QT_DESIGNER_EXECUTABLE}")
      ctkAppLauncherAppendExtraAppToLaunchToList(
        LONG_ARG designer
        HELP "Start Qt designer using Slicer plugins"
        PATH ${QT_DESIGNER_EXECUTABLE}
        OUTPUTVAR extraApplicationToLaunchListForBuildTree
        )
    endif()
    set(executables)
    if(UNIX)
      list(APPEND executables gnome-terminal xterm ddd gdb)
    elseif(WIN32)
      list(APPEND executables VisualStudio cmd)
      set(VisualStudio_EXECUTABLE ${CMAKE_BUILD_TOOL})
      set(cmd_ARGUMENTS "/c start cmd")
    endif()
    foreach(executable ${executables})
      find_program(${executable}_EXECUTABLE ${executable})
      if(${executable}_EXECUTABLE)
        message(STATUS "Enabling Slicer launcher option: --${executable}")
        ctkAppLauncherAppendExtraAppToLaunchToList(
          LONG_ARG ${executable}
          HELP "Start ${executable}"
          PATH ${${executable}_EXECUTABLE}
          ARGUMENTS ${${executable}_ARGUMENTS}
          OUTPUTVAR extraApplicationToLaunchListForBuildTree
          )
      endif()
    endforeach()

    include(SlicerBlockCTKAppLauncherSettings)
    set(splash_image_path ${CMAKE_CURRENT_SOURCE_DIR}/Resources/Images/SplashScreen.png)

    set(${PROJECT_NAME}_LIBRARY_PATHS_BUILD ${SLICER_LIBRARY_PATHS_BUILD})
    foreach(${APPLICATION_NAME}_LIBRARY_DIR ${${APPLICATION_NAME}_LIBRARY_DIRS})
      list(APPEND ${PROJECT_NAME}_LIBRARY_PATHS_BUILD ${${APPLICATION_NAME}_LIBRARY_DIR}/<CMAKE_CFG_INTDIR>)
    endforeach()

    ctkAppLauncherConfigure(
      TARGET ${PROJECT_NAME}${SlicerApp_EXE_SUFFIX}
      APPLICATION_INSTALL_SUBDIR ${Slicer_INSTALL_BIN_DIR}
      APPLICATION_NAME ${SlicerApp_APPLICATION_NAME}
      APPLICATION_REVISION ${${APPLICATION_NAME}_WC_REVISION}
      ORGANIZATION_DOMAIN ${${APPLICATION_NAME}_ORGANIZATION_DOMAIN}
      ORGANIZATION_NAME ${${APPLICATION_NAME}_ORGANIZATION_NAME}
      USER_ADDITIONAL_SETTINGS_FILEBASENAME ${SLICER_REVISION_SPECIFIC_USER_SETTINGS_FILEBASENAME}
      SPLASH_IMAGE_PATH ${splash_image_path}
      SPLASH_IMAGE_INSTALL_SUBDIR ${Slicer_INSTALL_BIN_DIR}
      SPLASHSCREEN_HIDE_DELAY_MS 3000
      HELP_SHORT_ARG "-h"
      HELP_LONG_ARG "--help"
      NOSPLASH_ARGS "--no-splash,--help,--version,--home,--program-path,--no-main-window"
      EXTRA_APPLICATION_TO_LAUNCH_BUILD ${extraApplicationToLaunchListForBuildTree}
      DESTINATION_DIR ${Slicer_BINARY_DIR}
      LIBRARY_PATHS_BUILD "${${PROJECT_NAME}_LIBRARY_PATHS_BUILD}"
      PATHS_BUILD "${SLICER_PATHS_BUILD}"
      ENVVARS_BUILD "${SLICER_ENVVARS_BUILD}"
      LIBRARY_PATHS_INSTALLED "${SLICER_LIBRARY_PATHS_INSTALLED}"
      PATHS_INSTALLED "${SLICER_PATHS_INSTALLED}"
      ENVVARS_INSTALLED "${SLICER_ENVVARS_INSTALLED}"
      )
    # HACK - Waiting "ctkAppLauncherConfigure" macro is updated so that it reconfigures the settings,
    #        if possible, only if "SlicerBlockCTKAppLauncherSettings.cmake" has been modified.
    #        Let's force a systematic reconfiguration of SlicerLauncherSettings.
    add_custom_target(${SlicerApp_APPLICATION_NAME}RemoveLauncherSettings
      COMMAND ${CMAKE_COMMAND} -E remove
        ${Slicer_BINARY_DIR}/${SlicerApp_APPLICATION_NAME}LauncherSettings.ini
        ${Slicer_BINARY_DIR}/${SlicerApp_APPLICATION_NAME}LauncherSettingsToInstall.ini
      )
    add_dependencies(${SlicerApp_APPLICATION_NAME}RemoveLauncherSettings ${PROJECT_NAME}${SlicerApp_EXE_SUFFIX})
    add_dependencies(${SlicerApp_APPLICATION_NAME}ConfigureLauncher ${SlicerApp_APPLICATION_NAME}RemoveLauncherSettings)

    if(NOT APPLE)
      if(Slicer_HAS_CONSOLE_IO_SUPPORT)
        install(PROGRAMS "${Slicer_BINARY_DIR}/${SlicerApp_APPLICATION_NAME}${CMAKE_EXECUTABLE_SUFFIX}" DESTINATION ".")
      else()
        install(
          PROGRAMS "${CTKAPPLAUNCHER_DIR}/bin/CTKAppLauncherW${CMAKE_EXECUTABLE_SUFFIX}"
          DESTINATION "."
          RENAME "${SlicerApp_APPLICATION_NAME}${CMAKE_EXECUTABLE_SUFFIX}"
          )
      endif()

      install(
        FILES ${splash_image_path}
        DESTINATION ${Slicer_INSTALL_BIN_DIR}
        )
      install(
        FILES "${Slicer_BINARY_DIR}/${SlicerApp_APPLICATION_NAME}LauncherSettingsToInstall.ini"
        DESTINATION ${Slicer_INSTALL_BIN_DIR}
        RENAME ${SlicerApp_APPLICATION_NAME}LauncherSettings.ini
        )
    endif()
  endif()
endif()

# --------------------------------------------------------------------------
#if(BUILD_TESTING)
#  add_subdirectory(Testing)
#endif()
