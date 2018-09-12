set(proj python-scipy)

# Set dependency list
set(${proj}_DEPENDENCIES NUMPY LAPACK)

# Include dependent projects if any
ExternalProject_Include_Dependencies(${proj} 
  PROJECT_VAR proj 
  DEPENDS_VAR ${proj}_DEPENDENCIES
  #SUPERBUILD_VAR Slicer_SUPERBUILD
  )

if(Slicer_USE_SYSTEM_${proj})
  ExternalProject_FindPythonPackage(
    MODULE_NAME "scipy"
    REQUIRED
    )
endif()

if(NOT Slicer_USE_SYSTEM_SciPy)

  set(EP_SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj})

  include(ExternalProjectForNonCMakeProject)

  # environment
  set(_env_script ${CMAKE_BINARY_DIR}/${proj}_Env.cmake)
  ExternalProject_Write_SetBuildEnv_Commands(${_env_script})
  ExternalProject_Write_SetPythonSetupEnv_Commands(${_env_script} APPEND)
  if(WIN32)
  file(APPEND ${_env_script}
"#------------------------------------------------------------------------------
# Added by '${CMAKE_CURRENT_LIST_FILE}'

set(ENV{CONDA_INSTALL_LOCN} \"C:/Miniconda3/envs/flang-env\")
set(ENV{FLANG_BIN_PATH} \"C:/Miniconda3/envs/flang-env/Library/bin\")
set(ENV{FLANG_LIB_PATH} \"C:/Miniconda3/envs/flang-env/Library/lib\")
set(ENV{LIB} \"\$ENV{LIB};\$ENV{FLANG_LIB_PATH}\")
set(ENV{PATH} \"\$ENV{PATH};\$ENV{FLANG_BIN_PATH}\")
set(ENV{CC} \"C:/Miniconda3/envs/flang-env/Library/bin/clang-cl.exe\")
set(ENV{CXX} \"C:/Miniconda3/envs/flang-env/Library/bin/clang-cl.exe\")
set(ENV{FC} \"C:/Miniconda3/envs/flang-env/Library/bin/flang.exe\")
")
  endif()

  # configure step
  set(_configure_script ${CMAKE_BINARY_DIR}/${proj}_configure_step.cmake)
  file(WRITE ${_configure_script}
"include(\"${_env_script}\")
set(${proj}_WORKING_DIR \"${EP_SOURCE_DIR}\")
file(WRITE \"${EP_SOURCE_DIR}/site.cfg\" \"\")
ExternalProject_Execute(${proj} \"configure\" \"${PYTHON_EXECUTABLE}\" setup.py config)
")

if(WIN32)
  set(_fortran_compiler "flang")
else()
  set(_fortran_compiler "gfortran")
endif()

  # build step
  set(_build_script ${CMAKE_BINARY_DIR}/${proj}_build_step.cmake)
  file(WRITE ${_build_script}
"include(\"${_env_script}\")
set(${proj}_WORKING_DIR \"${EP_SOURCE_DIR}\")
ExternalProject_Execute(${proj} \"build\" \"${PYTHON_EXECUTABLE}\" setup.py build --fcompiler=${_fortran_compiler})
")

  # install step
  set(_install_script ${CMAKE_BINARY_DIR}/${proj}_install_step.cmake)
  file(WRITE ${_install_script}
"include(\"${_env_script}\")
set(${proj}_WORKING_DIR \"${EP_SOURCE_DIR}\")
ExternalProject_Execute(${proj} \"install\" \"${PYTHON_EXECUTABLE}\" setup.py install)
")

  set(_version "1.1.0")

  #------------------------------------------------------------------------------
  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    URL "https://files.pythonhosted.org/packages/07/76/7e844757b9f3bf5ab9f951ccd3e4a8eed91ab8720b0aac8c2adcc2fdae9f/scipy-${_version}.tar.gz"
    URL_HASH SHA256=878352408424dffaa695ffedf2f9f92844e116686923ed9aa8626fc30d32cfd1
    DOWNLOAD_DIR ${CMAKE_BINARY_DIR}
    SOURCE_DIR ${EP_SOURCE_DIR}
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ${CMAKE_COMMAND} -P ${_configure_script}
    BUILD_COMMAND ${CMAKE_COMMAND} -P ${_build_script}
    INSTALL_COMMAND ${CMAKE_COMMAND} -P ${_install_script}
    DEPENDS
      ${${proj}_DEPENDENCIES}
    )

  ExternalProject_GenerateProjectDescription_Step(${proj}
    VERSION ${_version}
    )

  #-----------------------------------------------------------------------------
  # Sanity checks

  foreach(varname IN ITEMS
      python_DIR
      PYTHON_SITE_PACKAGES_SUBDIR
      )
    if("${${varname}}" STREQUAL "")
      message(FATAL_ERROR "${varname} CMake variable is expected to be set")
    endif()
  endforeach()

else()
  ExternalProject_Add_Empty(${proj} DEPENDS ${${proj}_DEPENDENCIES})
endif()
