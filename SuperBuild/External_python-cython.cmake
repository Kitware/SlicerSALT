set(proj python-cython)

# Set dependency list
set(${proj}_DEPENDENCIES python python-wheel)

if(NOT DEFINED Slicer_USE_SYSTEM_${proj})
  set(Slicer_USE_SYSTEM_${proj} ${Slicer_USE_SYSTEM_python})
endif()

# Include dependent projects if any
ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR ${proj}_DEPENDENCIES)

if(Slicer_USE_SYSTEM_${proj})
  ExternalProject_FindPythonPackage(
    MODULE_NAME "cython"
    REQUIRED
    )
endif()

if(NOT Slicer_USE_SYSTEM_${proj})

  set(_version "0.28.5")

  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    URL "https://files.pythonhosted.org/packages/21/89/ca320e5b45d381ae0df74c4b5694f1471c1b2453c5eb4bac3449f5970481/Cython-${_version}.tar.gz"
    URL_HASH "SHA256=b64575241f64f6ec005a4d4137339fb0ba5e156e826db2fdb5f458060d9979e0"
    DOWNLOAD_DIR ${CMAKE_BINARY_DIR}
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ""
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
