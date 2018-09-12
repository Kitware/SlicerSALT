set(proj python-pandas)

# Set dependency list
set(${proj}_DEPENDENCIES python NUMPY python-scipy python-cython python-pip)

if(NOT DEFINED Slicer_USE_SYSTEM_${proj})
  set(Slicer_USE_SYSTEM_${proj} ${Slicer_USE_SYSTEM_python})
endif()

# Include dependent projects if any
ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR ${proj}_DEPENDENCIES)

if(Slicer_USE_SYSTEM_${proj})
  ExternalProject_FindPythonPackage(
    MODULE_NAME "pandas"
    REQUIRED
    )
endif()

if(NOT Slicer_USE_SYSTEM_${proj})

set(_version "0.23.4")

  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    URL "https://files.pythonhosted.org/packages/e9/ad/5e92ba493eff96055a23b0a1323a9a803af71ec859ae3243ced86fcbd0a4/pandas-${_version}.tar.gz"
    URL_HASH SHA256=5b24ca47acf69222e82530e89111dd9d14f9b970ab2cd3a1c2c78f0c4fbba4f4
    DOWNLOAD_DIR ${CMAKE_BINARY_DIR}
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ${PYTHON_EXECUTABLE} -m pip install pytz python-dateutil
    BUILD_COMMAND ""
    INSTALL_COMMAND ${PYTHON_EXECUTABLE} setup.py install
    LOG_INSTALL 1
    DEPENDS
      ${${proj}_DEPENDENCIES}
    )

  ExternalProject_GenerateProjectDescription_Step(${proj}
    VERSION ${_version}
    )

else()
  ExternalProject_Add_Empty(${proj} DEPENDS ${${proj}_DEPENDENCIES})
endif()