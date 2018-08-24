import vtk, ctk, qt, slicer
from slicer.ScriptedLoadableModule import (ScriptedLoadableModule,
                                           ScriptedLoadableModuleLogic,
                                           ScriptedLoadableModuleWidget,
                                           ScriptedLoadableModuleTest)
from CommonUtilities import MRMLUtility
import os
import logging

#
# DataImporter
#

class DataImporter(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Data Importer"
    self.parent.categories = ["Shape Analysis Toolbox"]
    self.parent.dependencies = []
    self.parent.contributors = ["Hina Shah (Kitware Inc.)", "Pablo Hernandez (Kitware Inc,)"]
    self.parent.helpText = """
    This module import label images and segmentations from files and folders and compute the topology number of each segment.
    topologyNumber = cleanData.GetNumberOfPoints() - edges.GetNumberOfLines() + cleanData.GetNumberOfPolys()
    """
    self.parent.acknowledgementText = """
    This project is funded by NIBIB R01EB021391
    """ # replace with organization, grant and thanks.

#
# DataImporterLogic
#

class DataImporterLogic(ScriptedLoadableModuleLogic):

  def __init__(self):
    ScriptedLoadableModuleLogic.__init__(self)

    self.saveCleanData = False
    self.labelMapDict = {}
    self.segmentationDict = {}
    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.inconsistentTopologyDict = {}
    self.polyDataDict = {}
    self.TOPOLOGY_TYPES = {
        0: 'Circle/Torus/Mobius Strip',
        1: 'Disk',
        2: 'Sphere',
        -2: 'Double Torus',
        -4: 'Triple Torus',
    }

    self.singleDisplayedSegmentation = None
    # self.createSingleDisplaySegmentModelNode()

  def setSaveCleanData(self, save):
    self.saveCleanData = save

  def createSingleDisplaySegmentModelNode(self):
    if MRMLUtility.isMRMLNodeEmpty(self.singleDisplayedSegmentation, 'vtkMRMLModelNode'):
      self.singleDisplayedSegmentation = MRMLUtility.createNewMRMLNode('CurrentSegmentation', slicer.vtkMRMLModelNode())

  #
  # Reset all the data for data import
  #
  def cleanup(self):
    logging.info('Deleting nodes')
    if self.labelMapDict is not None:
      for node_name in self.labelMapDict.keys():
        logging.info('Deleting node: ' + node_name)
        MRMLUtility.removeMRMLNode(self.labelMapDict[node_name])
        MRMLUtility.removeMRMLNode(self.segmentationDict[node_name])

    if self.singleDisplayedSegmentation is not None:
      MRMLUtility.removeMRMLNode(self.singleDisplayedSegmentation)
      self.singleDisplayedSegmentation = None

    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.inconsistentTopologyDict = {}
    self.polyDataDict = {} # Dictionary that has all the segmentations.

  def importLabelMap(self, path):
    """
    Populate labelMapDict, segmentationDict, labelRangeInCohort
    Fails if number of labels is different than pre-existing value for labelRangeInCohort
    Returns false if errors, and no class variable is modified.
    """
    # load each file
    directory, fileName = os.path.split(path)

    labelMapVolume = slicer.util.loadLabelVolume(path, returnNode=True)[1]
    if labelMapVolume is None:
      logging.error('Failed to load ' + fileName + 'as a labelmap')
      # make sure each one is a labelmap
      return False

    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", labelMapVolume.GetName() + '_allSegments' )
    segmentationNode.SetDisplayVisibility(False)
    segmentationLogic = slicer.modules.segmentations.logic()
    segmentationLogic.ImportLabelmapToSegmentationNode(labelMapVolume,
                                                       segmentationNode)
    closedSurface = segmentationNode.CreateClosedSurfaceRepresentation()
    if closedSurface is False:
      logging.error('Failed to create closed surface representation')
      return False

    # find how many labels each file has
    # XXX: What happen if different number of labels? just fail is ok?
    labelRange = labelMapVolume.GetImageData().GetScalarRange()
    labelRange = (int(labelRange[0]), int(labelRange[1]))
    logging.debug('Cohort label range for ' + str(fileName) + ': ' + str(labelRange))
    if self.labelRangeInCohort != (-1, -1) and labelRange != self.labelRangeInCohort:
      logging.error('Number of labels do not match in the cohort')
      return False

    # Add to the dicts only if succesful
    self.labelMapDict[fileName] = labelMapVolume
    self.segmentationDict[fileName] = segmentationNode
    self.labelRangeInCohort = labelRange
    return True

  def importSegmentation(self, path):
    """
    Populate segmentationDict, labelRangeInCohort
    Fails if number of labels is different than pre-existing value for labelRangeInCohort
    Returns false if errors, and no class variable is modified.
    """
    # load each file
    directory, fileName = os.path.split(path)

    segmentationNode = slicer.util.loadSegmentation(path, returnNode=True)[1]
    if segmentationNode is None:
      logging.error('Failed to load ' + fileName + 'as a segmentation')
      # make sure each one is a labelmap
      return False
    segmentationNode.SetDisplayVisibility(False)

    # find how many labels each file has
    # XXX: What happen if different number of labels? just fail is ok?
    labelRange = (0, segmentationNode.GetSegmentation().GetNumberOfSegments())
    logging.debug('Cohort label range for ' + str(fileName) + ': ' + str(labelRange))
    if self.labelRangeInCohort != (-1, -1) and labelRange != self.labelRangeInCohort:
      logging.error('Label range {} do not match with the existing cohort {}.'.format(labelRange, self.labelRangeInCohort))
      return False

    # Add to the dicts only if succesful
    self.segmentationDict[fileName] = segmentationNode
    self.labelRangeInCohort = labelRange
    return True

  def importFiles(self, filePaths):
    """
    Call the appropiate import function from a heteregeneous list of file paths.
    Raises TypeError if not existent file or unhandled filetype by this module.
    """
    for path in filePaths:
      fileType = slicer.app.ioManager().fileType(path)
      logging.debug("Path [{}] has file type [{}]".format(path, fileType))
      if fileType == 'VolumeFile':
        self.importLabelMap(path)
      elif fileType == 'SegmentationFile':
        self.importSegmentation(path)
      elif fileType == 'NoFile':
        raise TypeError("Path [{}] is not existent or has an unknown file type for Slicer [{}]".format(path, fileType))
      else:
        raise TypeError("Path [{}] has file type [{}], but this module does not handle it".format(path, fileType))

  def getLabelRangeInCohort(self):
    return self.labelRangeInCohort

  def _computeModeOfNestedDict(self, dictOfDicts):
    """
    Compute the mode of the ultimate leaf from a dict of dict
    Returns the mode, or none if dict is empty.
    { firstKey: {nestKey0: '0', nestKey1: '0', nestKey2: '1'} }
    It would return '0' in the example.
    """
    from collections import Counter
    # Check is a nested dictionary
    if not isinstance(dictOfDicts[next(iter(dictOfDicts))], dict):
      raise ValueError('Input is not a nested dictionary', dictOfDicts)
    # Use the first key...
    firstKey = next(iter(dictOfDicts))
    return Counter(list(dictOfDicts[firstKey].values())).most_common(1)[0][0]

  #
  # Function to estimate topology of segmentations, and check for consistencies.
  #
  def populateTopologyDictionary(self):
    """
    PRE: Requires segmentationDict, labelRangeInCohort populated from files with importXXX
    POST: populate topologyDict, polyDataDict
    return void
    """

    # Create vtk objects that will be used to clean the geometries
    for nodeName in self.segmentationDict.keys():
      # Topology table is a dictionary of dictionaries.
      self.topologyDict[nodeName] = {}
      self.polyDataDict[nodeName] = {}
      for segmentNum in range(self.labelRangeInCohort[0], self.labelRangeInCohort[1] + 1):
        # 0 label is assumed to be the background.
        if segmentNum == 0:
          continue
        segmentId = str(segmentNum)
        polydata = self.segmentationDict[nodeName].GetClosedSurfaceRepresentation(segmentId)
        if polydata is None:
          logging.info('Ignoring segment id ' + segmentId + ' for case: ' + nodeName)
          continue

        polydataCleaner = vtk.vtkCleanPolyData()
        connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
        extractEdgeFilter = vtk.vtkExtractEdges()

        # clean up polydata
        polydataCleaner.SetInputData(polydata)
        polydataCleaner.Update()
        cleanData = polydataCleaner.GetOutput()

        # Get the largest connected component
        connectivityFilter.SetInputData(cleanData)
        connectivityFilter.SetExtractionModeToLargestRegion()
        connectivityFilter.SetScalarConnectivity(0)
        connectivityFilter.Update()
        largestComponent = connectivityFilter.GetOutput()

        # Clean the largest component to get rid of spurious points
        polydataCleaner.SetInputData(largestComponent)
        polydataCleaner.Update()
        cleanData = polydataCleaner.GetOutput()

        # run extract edge filter
        extractEdgeFilter.SetInputData(cleanData)
        extractEdgeFilter.Update()
        edges = extractEdgeFilter.GetOutput()

        # calculate the numbers
        topologyNumber = cleanData.GetNumberOfPoints() - edges.GetNumberOfLines() + cleanData.GetNumberOfPolys()
        self.topologyDict[nodeName][segmentNum] = topologyNumber

        if self.saveCleanData:
          self.polyDataDict[nodeName][segmentNum] = cleanData
        else:
          self.polyDataDict[nodeName][segmentNum] = polydata

        del edges
        del largestComponent
        del cleanData

    consistent, self.inconsistentTopologyDict = self.checkTopologyConsistency(self.topologyDict,
                                                                              expectedTopologyType = self._computeModeOfNestedDict(self.topologyDict))

  def checkTopologyConsistency(self, inputTopologyDictionary, expectedTopologyType = None):
    """
    return list with (boolean, dict of dicts of inconsistent entries: { nodeName: {segmentNumber, inconsistentTopology} } )
    the boolean says if there are or not inconsistencies
    if expectedTopologyType is "", the expectedTopologyType is set to the mode of the values in input dictionary.
    """
    inconsistenciesExist = False
    inconsistentSegments = {}

    # Check input expectedTopologyType is valid, if default, provide one.
    # Convert to long if not None
    expectedTopologyType = long(expectedTopologyType) if expectedTopologyType else expectedTopologyType
    if expectedTopologyType is not None:
      validExpectedTopology = (expectedTopologyType in self.TOPOLOGY_TYPES)
      if not validExpectedTopology:
        logging.error("Provided expected topology key: {}, is invalid, use a key from {}".format(expectedTopologyType, self.TOPOLOGY_TYPES))
        return
      else:
        logging.debug("Provided expected topology key: {}, is valid ({})".format(expectedTopologyType, self.TOPOLOGY_TYPES[expectedTopologyType]))

    else: #  Compute the expectedTopologyType to be the mode of the topologies
      expectedTopologyType = long(self._computeModeOfNestedDict(inputTopologyDictionary))

    for nameNode, segmentsDict in inputTopologyDictionary.iteritems():
      for segmentNum, topologyType in segmentsDict.iteritems():
        if topologyType != expectedTopologyType:
          inconsistentSegments[nameNode] = {}
          inconsistentSegments[nameNode][segmentNum] = topologyType

    if inconsistentSegments:
      inconsistenciesExist = True

    return (inconsistenciesExist, inconsistentSegments)

  def reset3dView(self):
    layoutManager = slicer.app.layoutManager()
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()

  def displaySegment(self, nodeName, segmentId):
    if segmentId == '0':
      self.segmentationDict[nodeName].SetDisplayVisibility(True)
      self.reset3dView()
      return

    if self.segmentationDict[nodeName].GetDisplayVisibility() is 1:
      self.segmentationDict[nodeName].SetDisplayVisibility(False)

    segmentIdNum = int(segmentId)
    polydata = None

    if nodeName in self.polyDataDict.keys() and segmentIdNum in self.polyDataDict[nodeName].keys():
      polydata = self.polyDataDict[nodeName][segmentIdNum] #elf.segmentationDict[nodeName].GetClosedSurfaceRepresentation(segmentId)
    if polydata is None:
      logging.error('Polydata for ' + nodeName + ' and ' + segmentId + ' does not exist!!')
      return

    self.createSingleDisplaySegmentModelNode()

    self.singleDisplayedSegmentation.SetAndObservePolyData(polydata)
    self.singleDisplayedSegmentation.SetDisplayVisibility(1)
    color = [0, 0, 0, 0]

    slicer.util.getNode('GenericAnatomyColors').GetColor(segmentIdNum, color)
    self.singleDisplayedSegmentation.GetDisplayNode().SetColor(color[0:3])
    self.reset3dView()

  def getTopologyAndConsistencyString(self, nodeName, segmentId):
    """
    Rturn strings with topology type and consistency of a segment.
    """
    segmentNum = int(segmentId)
    topologyString = 'n/a'
    consistentTopologyString = 'Consistent'

    if nodeName in self.topologyDict and segmentNum in self.topologyDict[nodeName]:
      topologyNum = self.topologyDict[nodeName][segmentNum]
      topologyString = self.TOPOLOGY_TYPES.get(topologyNum, 'n/a')

    if nodeName in self.inconsistentTopologyDict:
      if segmentNum in self.inconsistentTopologyDict[nodeName]:
        consistentTopologyString = 'Inconsistent'

    return topologyString, consistentTopologyString

#
# DataImporterWidget
#

class DataImporterWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    #
    #   Global variables
    #
    self.logic = DataImporterLogic()

    #
    #  Interface
    #
    loader = qt.QUiLoader()
    self.moduleName = 'DataImporter'
    scriptedModulesPath = eval('slicer.modules.%s.path' % self.moduleName.lower())
    scriptedModulesPath = os.path.dirname(scriptedModulesPath)
    path = os.path.join(scriptedModulesPath, 'Resources', '%s.ui' % self.moduleName)
    qfile = qt.QFile(path)
    qfile.open(qt.QFile.ReadOnly)
    widget = loader.load(qfile, self.parent)
    self.layout = self.parent.layout()
    self.widget = widget
    self.layout.addWidget(widget)

    self.FolderNameLineEdit = self.getWidget('InputFolderNameLineEdit')
    self.DirectoryButton = self.getWidget('DirectoryButton')
    self.DirectoryButton.connect('clicked(bool)', self.onClickDirectoryButton)
    #### TODO: support displaying the files, but only be able to choose a folder:
    #https://forum.qt.io/topic/62138/qfiledialog-choose-directories-only-but-show-files-as-well/13
    # self.DirectoryButton.setFileMode(qt.QFileDialog.DirectoryOnly)
    # self.DirectoryButton.setOption(qt.QFileDialog.DontUseNativeDialog, True)
    # self.DirectoryButton.setOption(qt.QFileDialog.ShowDirsOnly, False)

    self.ImportButton = self.getWidget('ImportButton')
    self.ImportButton.connect('clicked(bool)', self.onClickImportButton)
    self.DataInputTypeGroupBox = self.getWidget('DataInputTypeGroupBox')
    self.SubjectsTableWidget = self.getWidget('SubjectsTableWidget')
    self.StructuresSliderWidget = self.getWidget('StructuresSliderWidget')
    self.CurrentStructureTopologyLineEdit = self.getWidget('CurrentStructureTopologyLineEdit')
    self.CohortTopologyLineEdit = self.getWidget('CohortTopologyLineEdit')
    self.SaveCleanDataCheckBox = self.getWidget('checkBoxSaveCleanData')
    self.SaveCleanDataCheckBox.setChecked(True)
    self.SaveCleanDataCheckBox.connect('toggled(bool)', self.onSaveCleanDataCheckBoxToggled)

    self.SubjectsTableWidget.connect('cellClicked(int, int)', self.onSubjectTableWidgetClicked)
    self.StructuresSliderWidget.connect('valueChanged(double)', self.onStructuresSliderWidgetChanged)
    self.StructuresSliderWidget.minimum = 0
    self.StructuresSliderWidget.maximum = 0

    # Initialize the beginning input type.
    self.onSaveCleanDataCheckBoxToggled()

  #
  # Reset all the data for data import
  #
  # def cleanup(self):
  #   logging.debug('Deleting nodes')
  #   if self.SubjectsTableWidget is not None:
  #     self.SubjectsTableWidget.setRowCount(0)
  #   self.logic.cleanup()

  #
  # Functions to recover the widget in the .ui file
  #
  def getWidget(self, objectName):
    return self.findWidget(self.widget, objectName)

  def findWidget(self, widget, objectName):
    if widget.objectName == objectName:
      return widget
    else:
      for w in widget.children():
        resulting_widget = self.findWidget(w, objectName)
        if resulting_widget:
          return resulting_widget
    return None

  #
  # Routine to import the segmentation files given file names
  # This right now only handles the csv mode.
  # TODO: should also handle cases when surface files are given
  #
  def importFiles(self, filePaths):

    numCases = 0
    self.SubjectsTableWidget.setColumnCount(1)
    self.SubjectsTableWidget.setHorizontalHeaderLabels(['Subject name'])
    self.SubjectsTableWidget.verticalHeader().setVisible(False)
    self.SubjectsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
    self.SubjectsTableWidget.setSelectionMode(qt.QAbstractItemView.SingleSelection)

    if self.logic.importFiles(filePaths):

      for path in filePaths:
        # load each file
        pathPair = os.path.split(path)
        fileName = pathPair[1]

        # extract just the filename, and populate the tablewidget
        rowPosition = self.SubjectsTableWidget.rowCount
        self.SubjectsTableWidget.insertRow(rowPosition)
        self.SubjectsTableWidget.setItem(rowPosition, 0, qt.QTableWidgetItem(fileName))
        numCases = numCases + 1
      self.SubjectsTableWidget.setCurrentCell(0, 0)
    else:
      return

    labelRangeInCohort = self.logic.getLabelRangeInCohort()
    self.StructuresSliderWidget.minimum = int(labelRangeInCohort[0])
    self.StructuresSliderWidget.maximum = int(labelRangeInCohort[1])
    self.StructuresSliderWidget.setValue(0)

    # Populate the topology table
    self.logic.populateTopologyDictionary()

    self.onSubjectTableWidgetClicked(0, 0)

  '''
  GUI Callback functions
  '''
  #
  #  Handle request to import data
  #

  def onClickImportButton(self):
    pass
    # filenames = []
    # self.cleanup()
    # if self.importFromCSV:
    #   with open(self.csvFileName, 'r') as csvfile:
    #     reader = csv.reader(csvfile)
    #     # ignore the header
    #     next(reader, None)
    #     # assuming that each row is just a file path.
    #     for row in reader:
    #       if len(row) > 0:
    #         filenames.append(row[0])
    #     # Import all files
    #     self.importFiles(filenames)

        # Depending on the mode fill the structures table.
        # TODO: add directory parsing based on mode
    # else:
    #   logging.error("Importing from directory is not yet supported")

  def onClickDirectoryButton(self):
    hola = self.DirectoryButton.getOpenFileName(self.widget)
    print hola
    self.FolderNameLineEdit.text  = hola
    # self.CSVFileNameLineEdit.text = self.csvFileName
    # self.csvFileName = qt.QFileDialog.getOpenFileName(self.widget, "Open CSV File", ".", "CSV Files (*.csv)")
    # self.CSVFileNameLineEdit.text = self.csvFileName
    # self.importFromCSV = True

  def onInputType_chosen(self, b):
    inputTypeText = b.text
    if b.isChecked():
      self.inputType = inputTypeText

  def onSubjectTableWidgetClicked(self, row, column):
    nodeName = self.SubjectsTableWidget.item(row, column).text()
    segmentId = str(int(self.StructuresSliderWidget.value))
    self.logic.displaySegment(nodeName, segmentId)
    self.updateTopologyDisplay(nodeName, segmentId)

  def onStructuresSliderWidgetChanged(self, value):
    nodeName = self.SubjectsTableWidget.currentItem().text()
    segmentId = str(int(value))
    self.logic.displaySegment(nodeName, segmentId)
    self.updateTopologyDisplay(nodeName, segmentId)

  def onSaveCleanDataCheckBoxToggled(self):
    self.logic.setSaveCleanData(self.SaveCleanDataCheckBox.isChecked())

  '''
  Supplemental functions to update the visualizations
  '''

  def updateTopologyDisplay(self, nodeName, segmentId):
    topologyString, consistentTopologyString = self.logic.getTopologyAndConsistencyString(nodeName, segmentId)
    self.CurrentStructureTopologyLineEdit.setText(topologyString)
    self.CohortTopologyLineEdit.setText(consistentTopologyString)

  def __del__(self):
    self.cleanup()

# DataImporterLogic
#

class DataImporterTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

    self.testDir = os.path.join(slicer.app.temporaryPath, 'DataImporterTest')
    self.downloads = ()
    self.casesLabelMap = (
      'case01.nrrd',
      'case02.nrrd'
    )
    self.casesSegmentation = (
      'case01_allSegments.seg.nrrd',
      'case02_allSegments.seg.vtm',
    )

    # create dir if non-existant
    if not os.path.isdir(self.testDir):
      os.mkdir(self.testDir)

    # populate self.download()
    self.downloadData()

  def downloadData(self):
    """
    Download data, unzip and populate self.downloads
    """
    logging.info("-- Start download")
    import urllib
    self.downloads = (
        ('https://data.kitware.com/api/v1/item/5b7c5b758d777f06857c890d/download', 'case01.nrrd', slicer.util.loadLabelVolume),
        ('https://data.kitware.com/api/v1/item/5b7c5b798d777f06857c8910/download', 'case02.nrrd', slicer.util.loadLabelVolume),
        ('https://data.kitware.com/api/v1/item/5b7f43eb8d777f06857cb204/download', 'case01_allSegments.seg.nrrd', slicer.util.loadSegmentation),
        ('https://data.kitware.com/api/v1/item/5b802f178d777f06857cb665/download', 'case02_allSegments.seg.vtm.zip', 'Unzip'),
    )

    for url, name, loader in self.downloads:
      filePath = os.path.join(self.testDir, name)
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader == 'Unzip' and not os.path.exists(filePath[:-4]) :
        slicer.app.applicationLogic().Unzip(filePath, self.testDir)
        logging.info("Unzipping done")

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.delayDisplay('Starting...')
    self.setUp()

    ##### importLabelMap #####
    for fileName in self.casesLabelMap:
      self.test_importLabelMapFromFile(fileName)

    ##### importSegmentation #####
    for fileName in self.casesSegmentation:
      self.test_importSegmentationFromFile(fileName)

    ##### importFromDirectory #####
    self.test_importFiles()

    self.delayDisplay('All tests passed!')

  def printMembers(self, logic):
    print 'labelMapDict', logic.labelMapDict
    print 'segmentationDict', logic.segmentationDict
    print 'cohort label range', logic.labelRangeInCohort

    print 'topologyDict', logic.topologyDict
    print 'inconsistentTopologyDict', logic.inconsistentTopologyDict
    print 'polyDataDict', logic.polyDataDict


  def test_importLabelMapFromFile(self, fileName):
    """
    Exercises correctness of importLabelMap (single file), plus test methods on LabelMap data:
    - populateTopologyDictionary
    - checkTopologyConsistency
    """
    logging.info('-- Starting test for %s --' % (fileName))
    filePath = os.path.join(self.testDir, fileName)
    logic = DataImporterLogic()
    self.assertTrue(logic.importLabelMap(filePath))

    logic.populateTopologyDictionary()

    self.printMembers(logic)

    if fileName == 'case01.nrrd':
      self.assertNotEqual(logic.labelMapDict, dict())
      self.check_case01(logic, fileName)
    elif fileName == 'case02.nrrd':
      self.assertNotEqual(logic.labelMapDict, dict())
      self.check_case02(logic, fileName)

    logging.info('-- Test for %s passed! --' % (fileName))

  def check_case01(self, logic, fileName):
    logging.info('-- Checking case01 --')
    self.assertTrue('case01' in fileName)

    self.assertNotEqual(logic.segmentationDict, dict())
    self.assertEqual(logic.labelRangeInCohort, (0, 5))
    self.assertNotEqual(logic.topologyDict, dict())
    self.assertNotEqual(logic.polyDataDict, dict())
    self.assertNotEqual(logic.inconsistentTopologyDict, dict())

    segmentId = 1 # Disk
    topologyString, consistentTopologyString = logic.getTopologyAndConsistencyString(fileName, segmentId)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[0])
    self.assertEqual(consistentTopologyString, 'Inconsistent')

    segmentId = 2 # Sphere
    topologyString, consistentTopologyString = logic.getTopologyAndConsistencyString(fileName, segmentId)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[2])
    self.assertEqual(consistentTopologyString, 'Consistent')

    logging.info('-- case01 passed! --')

  def check_case02(self, logic, fileName):
    logging.info('-- Checking case02 --')
    self.assertTrue('case02' in fileName)

    self.assertNotEqual(logic.segmentationDict, dict())
    self.assertEqual(logic.labelRangeInCohort, (0, 5))
    self.assertNotEqual(logic.topologyDict, dict())
    self.assertNotEqual(logic.polyDataDict, dict())
    # All consistent
    self.assertEqual(logic.inconsistentTopologyDict, dict())

    segmentId = 2 # Sphere
    topologyString, consistentTopologyString = logic.getTopologyAndConsistencyString(fileName, segmentId)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[2])
    self.assertEqual(consistentTopologyString, 'Consistent')

    logging.info('-- case02 passed! --')

  def test_importSegmentationFromFile(self, fileName):
    """
    Exercises correctness of importSegmentation (single file), plus test methods on LabelMap data:
    - populateTopologyDictionary
    - checkTopologyConsistency
    """
    logging.info('-- Starting segmentation test for %s --' % (fileName))
    filePath = os.path.join(self.testDir, fileName)
    logic = DataImporterLogic()
    self.assertTrue(logic.importSegmentation(filePath))

    logic.populateTopologyDictionary()

    self.printMembers(logic)

    if fileName == 'case01_allSegments.seg.nrrd' :
      self.check_case01(logic, fileName)
    elif fileName == 'case02_allSegments.seg.vtm' :
      self.check_case02(logic, fileName)

    logging.info('-- Test for %s passed! --' % (fileName))

  def test_importFiles(self):
    """
    Test importing more images from a folder
    """
    logging.info('-- Starting test_importFiles --')
    self.assertTrue(os.path.isdir(self.testDir))
    logic = DataImporterLogic()

    # Load one label map and one segmentation
    preNumberOfNodesLabelMapVolume = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLLabelMapVolumeNode")
    preNumberOfNodesSegmentation = slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLSegmentationNode")
    filePaths = [os.path.join(self.testDir, self.casesLabelMap[0]),
                 os.path.join(self.testDir, self.casesSegmentation[1])
                 ]
    logic.importFiles(filePaths)
    self.assertEqual(slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLLabelMapVolumeNode"), preNumberOfNodesLabelMapVolume + 1)
    self.assertEqual(slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLSegmentationNode"), preNumberOfNodesSegmentation + 2)

    # Try to load not existing file
    filePaths = [os.path.join(self.testDir, 'not_existing_for_sure.nrrd'),]
    self.assertRaises(TypeError, logic.importFiles, filePaths)

    logging.info('-- test_importFiles passed! --')

