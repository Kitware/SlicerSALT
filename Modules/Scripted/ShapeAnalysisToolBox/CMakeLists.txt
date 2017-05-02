#-----------------------------------------------------------------------------
set(modules
  DataImporter
  )
  
set(MODULE_PYTHON_RESOURCES
  Resources/DataImporter.ui
  CommonUtilities/__init__.py
  CommonUtilities/utility.py
  )

foreach(module ${modules})
  #-----------------------------------------------------------------------------
  set(MODULE_NAME ${module})

  #-----------------------------------------------------------------------------
  set(MODULE_PYTHON_SCRIPTS
    ${MODULE_NAME}.py
    )
  #-----------------------------------------------------------------------------
  slicerMacroBuildScriptedModule(
    NAME ${MODULE_NAME}
    SCRIPTS ${MODULE_PYTHON_SCRIPTS}
    RESOURCES ${MODULE_PYTHON_RESOURCES}
    WITH_GENERIC_TESTS
    )
endforeach()
