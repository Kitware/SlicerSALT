#-----------------------------------------------------------------------------
set(MODULE_NAME Home)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_RESOURCES
  "Resources/SampleDataDescription/DataImporterInputData.json"
  "Resources/SampleDataDescription/MFSDAInputData.json"
  "Resources/SampleDataDescription/SPHARM-PDMTestData.json"
  "Resources/SampleDataDescription/ShapeRegressionInputData.json"
  "Resources/SampleDataDescription/SRepInitializerData.json"
  "Resources/SampleDataDescription/SVAInputData.json"
  )

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
