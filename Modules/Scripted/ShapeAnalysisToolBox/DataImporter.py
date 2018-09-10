import vtk, ctk, qt, slicer
from slicer.ScriptedLoadableModule import (ScriptedLoadableModule,
                                           ScriptedLoadableModuleLogic,
                                           ScriptedLoadableModuleWidget,
                                           ScriptedLoadableModuleTest)
import csv
import logging
import os

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
    self.parent.contributors = ["Hina Shah (Kitware Inc.), Pablo Hernandez (Kitware Inc,)"]
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
    self.modelDict = {}
    self.segmentationDict = {}
    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.polyDataDict = {}
    self.TOPOLOGY_TYPES = {
        0: 'Circle/Torus/Mobius Strip',
        1: 'Disk',
        2: 'Sphere',
        -2: 'Double Torus',
        -4: 'Triple Torus',
    }
    # help variable to map continious indices to TOPOLOGY_TYPES. Used in comboBoxes
    self.topologyTypeToIndex = {
        0: 0,
        1: 1,
        2: 2,
        -2: 3,
        -4: 4,
    }
    self.indexToTopologyType = {
        0: 0,
        1: 1,
        2: 2,
        3: -2,
        4: -4,
    }
    self.expectedTopologiesBySegment = {}
    self.inconsistentTopologyDict = {}

    self.numberOfDifferentSegments = 0
    self.dictSegmentNamesWithIntegers = dict()
    self.singleDisplayedSegmentation = None
    self.createSingleDisplaySegmentModelNode()

  def setSaveCleanData(self, save):
    self.saveCleanData = save

  def createSingleDisplaySegmentModelNode(self):
    if self.singleDisplayedSegmentation is None:
      self.singleDisplayedSegmentation = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())
      self.singleDisplayedSegmentation.CreateDefaultDisplayNodes()
      self.singleDisplayedSegmentation.SetName('CurrentSegmentation')

  #
  # Reset all the data for data import
  #
  def cleanup(self):
    logging.debug('Deleting nodes')
    if self.labelMapDict is not None:
      for nodeName in self.labelMapDict.keys():
        logging.debug('Deleting label map node: ' + nodeName)
        slicer.mrmlScene.RemoveNode(self.labelMapDict[nodeName])
        slicer.mrmlScene.RemoveNode(self.segmentationDict[nodeName])

    if self.modelDict is not None:
      for nodeName in self.modelDict.keys():
        logging.debug('Deleting model node: ' + nodeName)
        slicer.mrmlScene.RemoveNode(self.modelDict[nodeName])
        slicer.mrmlScene.RemoveNode(self.segmentationDict[nodeName])

    if self.singleDisplayedSegmentation is not None:
      slicer.mrmlScene.RemoveNode(self.singleDisplayedSegmentation)
      self.singleDisplayedSegmentation = None

    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.inconsistentTopologyDict = {}
    self.polyDataDict = {} # Dictionary that has all the segmentations.
    self.numberOfDifferentSegments = 0

  def checkLabelRangeConsistency(self, inputNumberOfSegments):
    """
    Check that the input number of segments is the same than the current number of segments in the cohort.
    Return tuple [boolean, labelRange].
    boolean is false if not consistent with current self.labelRangeInCohort. True otherwise.
    labelRange is (0, inputNumberOfSegments)
    """
    labelRange = (0, inputNumberOfSegments)
    if self.labelRangeInCohort != (-1, -1) and labelRange != self.labelRangeInCohort:
      logging.error('Label range {} does not match with the existing label range in cohort {}.'.format(labelRange, self.labelRangeInCohort))
      return False, labelRange

    return True, labelRange

  def importLabelMap(self, path):
    """
    Populate labelMapDict, segmentationDict, labelRangeInCohort
    Fails if number of labels is different than pre-existing value for labelRangeInCohort
    Returns false if errors, and no class variable is modified.
    """
    directory, fileName = os.path.split(path)

    labelMapNode = slicer.util.loadLabelVolume(path, returnNode=True)[1]
    if labelMapNode is None:
      logging.error('Failed to load ' + fileName + 'as a labelmap')
      # make sure each one is a labelmap
      return False

    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", labelMapNode.GetName() + '_allSegments')
    segmentationNode.SetDisplayVisibility(False)
    segmentationLogic = slicer.modules.segmentations.logic()
    segmentationLogic.ImportLabelmapToSegmentationNode(labelMapNode,
                                                       segmentationNode)
    closedSurface = segmentationNode.CreateClosedSurfaceRepresentation()
    if closedSurface is False:
      logging.error('Failed to create closed surface representation for filename: {}.'.format(path))
      return False

    labelRangeConsistent, labelRange = self.checkLabelRangeConsistency(segmentationNode.GetSegmentation().GetNumberOfSegments())
    if not labelRangeConsistent:
      logging.warning('LabelMap in path: {} has not been loaded into segmentationDict.'.format(path))
      return False

    # Add to the dicts only if succesful
    self.labelMapDict[fileName] = labelMapNode
    self.segmentationDict[fileName] = segmentationNode
    self.labelRangeInCohort = labelRange
    return True

  def importModel(self, path):
    """
    Create segmentation from a model (with only one shape). The labelRangeInCohort would be (0,1), just one segment.
    If your model is a model hierarchy (containing different shapes in the same file), use
    importModelHierarchy (not implemented).
    Populate segmentationDict and set labelRangeInCohort to (0,1)
    """
    directory, fileName = os.path.split(path)

    modelNode = slicer.util.loadModel(path, returnNode=True)[1]
    if modelNode is None:
      logging.error('Failed to load ' + fileName + 'as a model')
      return False

    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", modelNode.GetName() + '_allSegments')
    segmentationNode.SetDisplayVisibility(False)
    segmentationLogic = slicer.modules.segmentations.logic()
    segmentationLogic.ImportModelToSegmentationNode(modelNode,
                                                    segmentationNode)
    # To allow better mixing with label maps.
    # We change the name of the model (originally set to the filename in vtkSlicerSegmentationModuleLogic)
    # XXX Better option would be to use terminologies, see: https://discourse.slicer.org/t/finding-corresponding-segments-in-segmentations/4055/4
    segmentationNode.GetSegmentation().GetSegment(modelNode.GetName()).SetName('1')
    closedSurface = segmentationNode.CreateClosedSurfaceRepresentation()
    if closedSurface is False:
      logging.error('Failed to create closed surface representation for filename: {}.'.format(path))
      return False

    labelRangeConsistent, labelRange = self.checkLabelRangeConsistency(segmentationNode.GetSegmentation().GetNumberOfSegments())
    if not labelRangeConsistent:
      logging.warning('Model in path: {} has not been loaded into segmentationDict.'.format(path))
      return False

    # Add to the dicts only if succesful
    self.modelDict[fileName] = modelNode
    self.segmentationDict[fileName] = segmentationNode
    self.labelRangeInCohort = labelRange
    return True

  def importSegmentation(self, path):
    """
    Populate segmentationDict, labelRangeInCohort
    Fails if number of labels is different than pre-existing value for labelRangeInCohort
    Returns false if errors, and no class variable is modified.
    """
    directory, fileName = os.path.split(path)

    segmentationNode = slicer.util.loadSegmentation(path, returnNode=True)[1]
    if segmentationNode is None:
      logging.error('Failed to load ' + fileName + 'as a segmentation')
      return False
    segmentationNode.SetDisplayVisibility(False)

    labelRangeConsistent, labelRange = self.checkLabelRangeConsistency(segmentationNode.GetSegmentation().GetNumberOfSegments())
    if not labelRangeConsistent:
      logging.warning('Segmentation in path: {} has not been loaded into segmentationDict.'.format(path))
      return False

    # Add to the dicts only if succesful
    self.segmentationDict[fileName] = segmentationNode
    self.labelRangeInCohort = labelRange
    return True

  def filePathsFromCSVFile(self, csvFileName):
    """
    Return filePaths from CSV.
    It assumes that csvFileName contains one filepath per row.
    """
    filePaths = []
    with open(csvFileName, 'r') as csvfile:
      has_header = csv.Sniffer().has_header(csvfile.read(1024))
      csvfile.seek(0) # Rewind
      reader = csv.reader(csvfile)
      # ignore the header
      if has_header:
        next(reader, None)
      # assuming that each row is just a file path.
      for row in reader:
        if len(row) > 0:
          filePaths.append(row[0])

    return filePaths


        # Depending on the mode fill the structures table.
        # TODO: add directory parsing based on mode
    # else:
    #   logging.error("Importing from directory is not yet supported")
  def importFiles(self, filePaths):
    """
    Call the appropiate import function from a heteregeneous list of file paths.
    Raises TypeError if not existent file or unhandled filetype by this module.
    Files with a different number of labels/segments than the first one loaded are ignored with a warning.
    Return true if success, raise error otherwise.
    """
    for path in filePaths:
      fileType = slicer.app.ioManager().fileType(path)
      logging.debug("Path [{}] has file type [{}]".format(path, fileType))
      if fileType == 'VolumeFile':
        self.importLabelMap(path)
      elif fileType == 'SegmentationFile':
        self.importSegmentation(path)
      elif fileType == 'ModelFile':
        self.importModel(path)
      elif fileType == 'NoFile':
        raise TypeError("Path [{}] is not existent or has an unknown file type for Slicer [{}]".format(path, fileType))
      else:
        raise TypeError("Path [{}] has file type [{}], but this module does not handle it".format(path, fileType))

    return True

  def _computeModeOfSegment(self, inputTopologyDict, inputSegmentName):
    """
    Compute the mode of the segmentName among the population
    Raise error if input dict is empty or not nested.
    Returns the mode value, or
    None if inputSegmentName is not found in the dictionary.

    Example:
    {
    name0:
      {'segmentName0': '0', 'segmentName1': '1'},
    name1:
      {'segmentName0': '1', 'segmentName1': '0'}
    name2:
      {'segmentName0': '1', 'segmentName1': '0'}
    }
    It would return '1' if inputSegmentName == 'segmentName0'
                    '0' if inputSegmentName == 'segmentName1'
    """
    from collections import Counter
    # Check is a nested dictionary
    if not isinstance(inputTopologyDict[next(iter(inputTopologyDict))], dict):
      raise ValueError('Input is not a nested dictionary', inputTopologyDict)
    # Use the first key...
    segmentTopologies = list()
    for name in inputTopologyDict:
      if inputSegmentName in inputTopologyDict[name]:
        segmentTopologies.append(inputTopologyDict[name][inputSegmentName])

    if not segmentTopologies:
      logging.warning('There is no segments with segmentName {} in input dict {}.'.format(inputSegmentName, inputTopologyDict))
      return None

    # dev: in most_common elements with equal counts are ordered arbitrarily
    return Counter(segmentTopologies).most_common(1)[0][0]

  def initExpectedTopologyBySegmentWithModes(self, inputTopologyDictionary):
    """
    Compute the mode of each segment, populating the dict:
    Example:
    {'segmentName0' : 2, 'segmentName1': 0'}
    Where the integers correspond to the enum TOPOLOGY_TYPES
    """
    self.expectedTopologiesBySegment = {}
    segmentNames = set()
    for name in inputTopologyDictionary:
      for segmentName in inputTopologyDictionary[name]:
        segmentNames.add(segmentName)

    for segmentName in segmentNames:
      topologyType = self._computeModeOfSegment(inputTopologyDictionary, segmentName)
      validTopologyType = (topologyType in self.TOPOLOGY_TYPES)
      if not validTopologyType:
        logging.error("Topology type: {} for segmentName {}, is invalid, use a key from {}".format(topologyType, segmentName, self.TOPOLOGY_TYPES))
        return
      self.expectedTopologiesBySegment[segmentName] = long(topologyType)

  #
  # Function to estimate topology of segmentations, and check for consistencies.
  #
  def populateTopologyDictionary(self):
    """
    PRE: Requires segmentationDict populated from files with importXXX
    POST: populate topologyDict, polyDataDict
    return void
    Note that this is independent of labelRangeInCohort, the keys of the two level dictionary would be:
    [nodeName][SegmentName]
    SegmentName might not be alphanumerical, create a map self.dictSegmentNamesWithIntegers
    between strings and ints.
    """

    # Create vtk objects that will be used to clean the geometries
    for nodeName in self.segmentationDict.keys():
      # Topology table is a dictionary of dictionaries.
      self.topologyDict[nodeName] = {}
      self.polyDataDict[nodeName] = {}
      segmentationNode = self.segmentationDict[nodeName]
      for segmentIndex in range(segmentationNode.GetSegmentation().GetNumberOfSegments()):
        segmentName = segmentationNode.GetSegmentation().GetNthSegmentID(segmentIndex)
        # 0 label is assumed to be the background. XXX Pablo: assumed where?
        if segmentName == "0":
          continue
        polydata = segmentationNode.GetClosedSurfaceRepresentation(segmentName)
        if polydata is None:
          logging.warning('Ignoring segment id ' + segmentName + ' for case: ' + nodeName)
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
        self.topologyDict[nodeName][segmentName] = topologyNumber

        if self.saveCleanData:
          self.polyDataDict[nodeName][segmentName] = cleanData
        else:
          self.polyDataDict[nodeName][segmentName] = polydata

        del edges
        del largestComponent
        del cleanData

  def populateInconsistentTopologyDict(self):
    """
    PRE: Requires topologyDict to be populated
    Uses checkTopologyConsistency to populate self.inconsistentTopologyDict
    """
    if not self.topologyDict:
      logging.error('Topology Dict is not populated')
      return

    consistent, self.inconsistentTopologyDict = self.checkTopologyConsistency(self.topologyDict)

  def populateDictSegmentNamesWithIntegers(self):
    """
    Populate numberOfDifferentSegments and dictSegmentNamesWithIntegers from existing topologyDict.
    """
    if self.topologyDict is None:
      logging.warning("Cannot populate dictSegmentNamesWithIntegers without topologyDict")
      return
    self.numberOfDifferentSegments = 0
    for nodeName in self.topologyDict:
      for segmentName in self.topologyDict[nodeName]:
        if not segmentName in self.dictSegmentNamesWithIntegers:
          self.numberOfDifferentSegments+=1
          self.dictSegmentNamesWithIntegers[segmentName] = self.numberOfDifferentSegments


  def checkTopologyConsistency(self, inputTopologyDictionary):
    """
    Return list with (boolean, dict of dicts of inconsistent entries: { nodeName: {segmentName, inconsistentTopology} } )
    the boolean reflects existence of inconsistencies
    It uses the dictionary expectedTopologiesBySegment. If empty, it automatically init it computing the mode by segment.
    """
    if not self.expectedTopologiesBySegment:
      self.initExpectedTopologyBySegmentWithModes(inputTopologyDictionary)

    inconsistenciesExist = False
    inconsistentSegments = {}

    for nameNode, segmentsDict in inputTopologyDictionary.iteritems():
      for segmentName, topologyType in segmentsDict.iteritems():
        if topologyType != self.expectedTopologiesBySegment[segmentName]:
          inconsistentSegments[nameNode] = {}
          inconsistentSegments[nameNode][segmentName] = topologyType

    if inconsistentSegments:
      inconsistenciesExist = True

    return (inconsistenciesExist, inconsistentSegments)

  def reset3dView(self):
    layoutManager = slicer.app.layoutManager()
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()

  def displaySegment(self, nodeName, segmentName):
    # if segmentName == '0':
    #   self.segmentationDict[nodeName].SetDisplayVisibility(True)
    #   self.reset3dView()
    #   return
    if self.segmentationDict[nodeName].GetDisplayVisibility():
      self.segmentationDict[nodeName].SetDisplayVisibility(False)

    polydata = None

    if nodeName in self.polyDataDict and segmentName in self.polyDataDict[nodeName]:
      polydata = self.polyDataDict[nodeName][segmentName] #elf.segmentationDict[nodeName].GetClosedSurfaceRepresentation(segmentName)
    if polydata is None:
      logging.error('Polydata for ' + nodeName + ' and ' + segmentName + ' does not exist!!')
      return

    self.createSingleDisplaySegmentModelNode()

    self.singleDisplayedSegmentation.SetAndObservePolyData(polydata)
    self.singleDisplayedSegmentation.SetDisplayVisibility(1)
    color = [0, 0, 0, 0]

    segmentNameNum = int(segmentName)
    slicer.util.getNode('GenericAnatomyColors').GetColor(segmentNameNum, color)
    self.singleDisplayedSegmentation.GetDisplayNode().SetColor(color[0:3])
    self.reset3dView()


  def getLabelRangeInCohort(self):
    return self.labelRangeInCohort

  def getTopologyString(self, nodeName, inputSegmentName):
    segmentName = str(inputSegmentName)
    topologyString = 'n/a'
    if nodeName in self.topologyDict and segmentName in self.topologyDict[nodeName]:
      topologyNum = self.topologyDict[nodeName][segmentName]
      topologyString = self.TOPOLOGY_TYPES.get(topologyNum, 'n/a')
    return topologyString

  def getConsistencyString(self, nodeName, inputSegmentName):
    """
    Return 'Consistent' or 'Inconsistent' depending if the nodeName and segmentName are in
    the inconsistentTopologyDict.
    """
    segmentName = str(inputSegmentName)
    consistentTopologyString = 'Consistent'

    if nodeName in self.inconsistentTopologyDict:
      if segmentName in self.inconsistentTopologyDict[nodeName]:
        consistentTopologyString = 'Inconsistent'

    return consistentTopologyString

  def getTopologyAndConsistencyString(self, nodeName, inputSegmentName):
    """
    Return strings with topology type and consistency of a segment.
    """
    return self.getTopologyString(nodeName, inputSegmentName), self.getConsistencyString(nodeName, inputSegmentName)

#
# DataImporterWidget
#

class DataImporterWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def resetGlobalVariables(self):
    self.logic.cleanup()
    self.logic = DataImporterLogic()
    self.directoryPath = ''
    self.filteredFilePathsList = list()
    self.currentSubjectNameShowingInSegmentTable = ''

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    #
    #   Global variables
    #
    self.logic = DataImporterLogic()
    self.directoryPath = ''
    self.filteredFilePathsList = list()
    # Store the name to avoid re-drawing the table
    self.currentSubjectNameShowingInSegmentTable = ''
    self.tableWidgetItemDefaultFlags = qt.Qt.NoItemFlags | qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled

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

    self.InputFolderNameLineEdit = self.getWidget('InputFolderNameLineEdit')
    self.FolderDirectoryButton = self.getWidget('FolderDirectoryButton')
    self.FolderDirectoryButton.connect('directoryChanged(QString)', self.onDirectoryChanged)

    self.InputCSVFileNameLineEdit = self.getWidget('InputCSVFileNameLineEdit')
    self.CSVBrowseFilePushButton = self.getWidget('CSVBrowseFilePushButton')
    self.CSVBrowseFilePushButton.setIcon(qt.QApplication.style().standardIcon(qt.QStyle.SP_DirIcon))
    self.CSVBrowseFilePushButton.connect('clicked(bool)', self.onClickCSVBrowseFilePushButton)

    self.ImportButton = self.getWidget('ImportButton')
    self.ImportButton.connect('clicked(bool)', self.onClickImportButton)
    self.DataInputTypeGroupBox = self.getWidget('DataInputTypeGroupBox')
    self.SubjectsTableWidget = self.getWidget('SubjectsTableWidget')
    self.SegmentsTableWidget = self.getWidget('SegmentsTableWidget')
    self.SaveCleanDataCheckBox = self.getWidget('checkBoxSaveCleanData')
    self.SaveCleanDataCheckBox.setChecked(True)
    self.SaveCleanDataCheckBox.connect('toggled(bool)', self.onSaveCleanDataCheckBoxToggled)

    self.SubjectsTableWidget.connect('cellClicked(int, int)', self.onSubjectsTableWidgetClicked)

    # Initialize the beginning input type.
    self.onSaveCleanDataCheckBoxToggled()

  #
  # Reset all the data for data import
  #
  def cleanup(self):
    logging.debug('Cleaning up widget')
    self.resetSubjectsTable()
    self.resetSegmentsTable()
    self.resetGlobalVariables()

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

  def initSubjectsTable(self):
    """
    Set options and headers of SubjectsTable.
    Does not require any other data structure populated.
    """
    ##### Subjects Table
    nameColumn = 0
    consistencyColumn = 1
    nameColumnLabel = 'Subject name'
    consistencyColumnLabel = 'Consistency'
    self.SubjectsTableWidget.setColumnCount(2)
    self.SubjectsTableWidget.setHorizontalHeaderLabels([
      nameColumnLabel,
      consistencyColumnLabel
    ])
    self.SubjectsTableWidget.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
    # Keep the column fixed
    # self.SubjectsTableWidget.horizontalHeader().setSectionResizeMode(consistencyColumn, qt.QHeaderView.Fixed)
    # self.SubjectsTableWidget.horizontalHeader().resizeSection(consistencyColumn, 50);
    self.SubjectsTableWidget.verticalHeader().setVisible(False)
    self.SubjectsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
    # self.SubjectsTableWidget.setSelectionMode(qt.QAbstractItemView.SingleSelection)

  def initSegmentsTable(self):
    """
    Set options and headers of SegmentsTable.
    Does not require any other data structure populated.
    """
    segmentNameColumn = 0
    topologyCurrentColumn = 1
    topologyExpectedColumn = 2
    segmentNameColumnLabel = 'SegmentID'
    topologyCurrentColumnLabel = 'Current Segment Topology'
    topologyExpectedColumnLabel = 'Expected Cohort Topology'
    self.SegmentsTableWidget.setColumnCount(3)
    self.SegmentsTableWidget.setHorizontalHeaderLabels([
      segmentNameColumnLabel,
      topologyCurrentColumnLabel,
      topologyExpectedColumnLabel
    ])
    self.SegmentsTableWidget.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
    # self.SegmentsTableWidget.horizontalHeader().setSectionResizeMode(viewColumn, qt.QHeaderView.Fixed)
    # self.SegmentsTableWidget.horizontalHeader().resizeSection(viewColumn, 35); # Keep the view column fixed
    self.SegmentsTableWidget.verticalHeader().setVisible(False)
    self.SegmentsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
    # self.SegmentsTableWidget.setSelectionMode(qt.QAbstractItemView.SingleSelection)

  def resetSubjectsTable(self):
    if self.SubjectsTableWidget is not None:
      self.SubjectsTableWidget.setRowCount(0)

  def resetSegmentsTable(self):
    if self.SegmentsTableWidget is not None:
      self.SegmentsTableWidget.setRowCount(0)

  def populateSubjectsTable(self):
    """
    PRE: Requires self.logic.topologyDict, and self.logic.inconsistentTopologyDict populated.
    POST: Populate SubjectTable with the names of the files
    """
    if not self.logic.topologyDict:
      logging.error("Trying to populateSubjectsTable with non existant topologyDict.")
      return

    # Required to safely populate table when sorting is enabled, restored later.
    self.SubjectsTableWidget.setSortingEnabled(False)

    nameColumn = 0
    consistencyColumn = 1
    # XXX: Let the user choose what is the expected topology?
    inconsistenciesExist, inconsistentDict = self.logic.checkTopologyConsistency(self.logic.topologyDict)
    print inconsistenciesExist, inconsistentDict
    for name in self.logic.topologyDict:
      # Populate subject names
      rowPosition = self.SubjectsTableWidget.rowCount
      self.SubjectsTableWidget.insertRow(rowPosition)
      nameItem = qt.QTableWidgetItem(name)
      nameItem.setFlags(self.tableWidgetItemDefaultFlags)
      self.SubjectsTableWidget.setItem(rowPosition, nameColumn, nameItem)

      # Populate consistency row
      consistency = 'Consistent'
      countInconsistencies = 0
      if name in inconsistentDict:
        countInconsistencies = len(inconsistentDict[name])
      if countInconsistencies > 0:
        consistency = '# Inconsistencies: ' + str(countInconsistencies)
      consistencyItem = qt.QTableWidgetItem(consistency)
      consistencyItem.setFlags(self.tableWidgetItemDefaultFlags)
      self.SubjectsTableWidget.setItem(rowPosition, consistencyColumn, consistencyItem)
      if countInconsistencies > 0:
        consistencyItem.setBackground(qt.QBrush(qt.QColor(255, 204, 203))) # light red

    # Restore sorting
    self.SubjectsTableWidget.setSortingEnabled(True)

  def populateSegmentsTable(self, nameKey):
    """
    Given the name acting as first key for self.logic.topologyDict,
    populates the segment table for the subject with such a name.
    PRE: topologyDict has to have a key equal to input nameKey
    POST: Populates SegmentsTable for given name.
    """
    if not self.logic.topologyDict:
      logging.error("Trying to populateSegmentsTable with non existant topologyDict.")
      return
    if not nameKey in self.logic.topologyDict:
      logging.error("Input nameKey: {} does not exist in topologyDict.".format(nameKey))
      return
    if nameKey == self.currentSubjectNameShowingInSegmentTable:
      return
    # Required to safely populate table when sorting is enabled, restored later.
    self.SegmentsTableWidget.setSortingEnabled(False)

    segmentNameColumn = 0
    topologyCurrentColumn = 1
    topologyExpectedColumn = 2
    # cohortConsistencyColumn = 2
    for segmentName in self.logic.topologyDict[nameKey]:
      # Populate segmentName row
      rowPosition = self.SegmentsTableWidget.rowCount
      self.SegmentsTableWidget.insertRow(rowPosition)
      segmentNameItem = qt.QTableWidgetItem(segmentName)
      segmentNameItem.setFlags(self.tableWidgetItemDefaultFlags)
      self.SegmentsTableWidget.setItem(rowPosition, segmentNameColumn, segmentNameItem )

      # Get topology and consistency of segment
      topologyCurrent, consistency = self.logic.getTopologyAndConsistencyString(nameKey, segmentName)
      # Populate topology row
      topologyCurrentItem = qt.QTableWidgetItem(topologyCurrent)
      topologyCurrentItem.setFlags(self.tableWidgetItemDefaultFlags)
      self.SegmentsTableWidget.setItem(rowPosition, topologyCurrentColumn, topologyCurrentItem)
      if consistency == 'Inconsistent':
        topologyCurrentItem.setBackground(qt.QBrush(qt.QColor(255, 204, 203))) # light red

      topologyExpected = self.logic.expectedTopologiesBySegment[segmentName]
      comboBox = self._createTopologyTypesComboBox()
      comboBox.setCurrentIndex(self.logic.topologyTypeToIndex[topologyExpected])
      # XXX
      # XXX connect currentIndexChanged combo box to modify self.logic.expectedTopologies, and then re-populateSubjectTable
      # XXX
      self.SegmentsTableWidget.setCellWidget(rowPosition, topologyExpectedColumn, comboBox)

    # Restore sorting
    self.SegmentsTableWidget.setSortingEnabled(True)
    # Order by id name
    # self.SegmentsTableWidget.sortItems(segmentNameColumn)
    # Store the name to avoid re-drawing in future calls
    self.currentSubjectNameShowingInSegmentTable = nameKey

  def _createTopologyTypesComboBox(self):
    """
    Return ComboBox with values from enum TOPOLOGY_TYPES
    """
    comboBox = qt.QComboBox()
    for string_value in self.logic.TOPOLOGY_TYPES.values():
      comboBox.addItem(string_value)

    return comboBox

  def importFiles(self, filePaths):
    """
    Use logic.importFiles, populateTopologyDict and populate tables.
    """

    if not self.logic.importFiles(filePaths):
      logging.warning("logic.importFiles issues, see raised errors.")
      return

    # Populate the topology table
    self.logic.populateTopologyDictionary()
    self.logic.populateInconsistentTopologyDict()

    ######### Init Tables ##########
    self.initSubjectsTable()
    self.initSegmentsTable()

    ######### Populate Tables ##########
    self.populateSubjectsTable()

    self.SubjectsTableWidget.setCurrentCell(0, 0)
    self.onSubjectsTableWidgetClicked(0, 0)

  '''
  GUI Callback functions
  '''
  #
  #  Handle request to import data
  #

  def onClickImportButton(self):
    if not self.filteredFilePathsList:
      logging.warning('List of files is empty, choose a folder or a csv file to import first.')
      return

    self.importFiles(self.filteredFilePathsList)

  def filterFilePaths(self, filePathsList):
    """
    Return filtered filePaths of files that are readable by this module.
    """
    filteredFilePathsList = list()
    for filePath in filePathsList:
      fileType = slicer.app.ioManager().fileType(filePath)
      if fileType == 'VolumeFile' or fileType == 'SegmentationFile' or fileType == 'ModelFile':
        filteredFilePathsList.append(filePath)
      # else:
      #   logging.debug("File: {} with fileType {} is not readable by this module.".format(filePath, fileType))

    return filteredFilePathsList

  def onClickCSVBrowseFilePushButton(self):
    csvFileName = qt.QFileDialog.getOpenFileName(self.widget, "Open CSV File", ".", "CSV Files (*.csv)")
    self.InputCSVFileNameLineEdit.text = csvFileName
    filePathsList = self.logic.filePathsFromCSVFile(csvFileName)
    self.filteredFilePathsList = self.filterFilePaths(filePathsList)

  def onDirectoryChanged(self, directoryPath):
    """
    Populates self.directoryPath and self.filteredFilePathsList
    containing a list of files contained in the directoryPath
    that can be used in this module.
    """
    logging.debug("onDirectoryChanged: {}".format(directoryPath))
    # Create a list of files from the directory
    directory = qt.QDir(directoryPath)
    if not directory.exists():
      logging.error("Directory {} does not exist.".format(directory))
      return

    self.directoryPath = directoryPath
    self.InputFolderNameLineEdit.text = directoryPath

    fileNameList = directory.entryList(qt.QDir.Files | qt.QDir.Readable)
    # Trim fileList to only accept types recognized by slicer
    filePathsList = list()
    for name in fileNameList:
      filePathsList.append(os.path.join(directoryPath, name))

    self.filteredFilePathsList = self.filterFilePaths(filePathsList)

  def onInputType_chosen(self, b):
    inputTypeText = b.text
    if b.isChecked():
      self.inputType = inputTypeText

  def onSubjectsTableWidgetClicked(self, row, column):
    """
    On click in Subject table populates segment table.
    """
    if self.SubjectsTableWidget.rowCount == 0:
      return

    nameColumn = 0
    nodeName = self.SubjectsTableWidget.item(row, nameColumn).text()
    self.resetSegmentsTable()
    self.populateSegmentsTable(nodeName)
    # segmentName = str(int(self.SegmentsSliderWidget.value))
    # self.logic.displaySegment(nodeName, segmentName)
    # self.updateTopologyDisplay(nodeName, segmentName)

  def onSegmentsTableWidgetClicked(self, row, column):
    # TODO
    pass

  # def onSegmentsSliderWidgetChanged(self, value):
  #   nodeName = self.SubjectsTableWidget.currentItem().text()
  #   segmentName = str(int(value))
  #   self.logic.displaySegment(nodeName, segmentName)
  #   self.updateTopologyDisplay(nodeName, segmentName)

  def onSaveCleanDataCheckBoxToggled(self):
    self.logic.setSaveCleanData(self.SaveCleanDataCheckBox.isChecked())

  '''
  Supplemental functions to update the visualizations
  '''

  def updateTopologyDisplay(self, nodeName, segmentName):
    topologyString, consistentTopologyString = self.logic.getTopologyAndConsistencyString(nodeName, segmentName)
    self.CurrentSegmentTopologyLineEdit.setText(topologyString)
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
    self.casesModel = (
      'sample_model.vtk',
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
        ('https://data.kitware.com/api/v1/item/5b8d65aa8d777f43cc9850f4/download', 'sample_model.vtk', slicer.util.loadModel),
    )

    for url, name, loader in self.downloads:
      filePath = os.path.join(self.testDir, name)
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader == 'Unzip' and not os.path.exists(filePath[:-4]):
        slicer.app.applicationLogic().Unzip(filePath, self.testDir)
        logging.info("Unzipping done")

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.delayDisplay('Starting...')
    self.setUp()

    ##### LabelMap #####
    for fileName in self.casesLabelMap:
      self.test_importLabelMapFromFile(fileName)

    ##### Segmentation #####
    for fileName in self.casesSegmentation:
      self.test_importSegmentationFromFile(fileName)

    ##### Model #####
    for fileName in self.casesModel:
      print "**************************"
      self.test_importModelFromFile(fileName)

    ##### CSV #####
    self.test_filenamesFromCSVFile()

    ##### All #####
    self.test_importFiles()

    ##########
    self.test_populateDictSegmentNamesWithIntegers()
    self.test_computeMode()

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
    logic.populateInconsistentTopologyDict()

    self.printMembers(logic)

    if fileName == 'case01.nrrd':
      self.assertNotEqual(logic.labelMapDict, dict())
      self.check_case01(logic, fileName)
    elif fileName == 'case02.nrrd':
      self.assertNotEqual(logic.labelMapDict, dict())
      self.check_case02(logic, fileName)

    logging.info('-- Test for %s passed (importLabelMap)! --' % (fileName))

  def check_case01(self, logic, fileName):
    logging.info('-- Checking case01 --')
    self.assertTrue('case01' in fileName)

    self.assertNotEqual(logic.segmentationDict, dict())
    self.assertEqual(logic.labelRangeInCohort, (0, 5))
    self.assertNotEqual(logic.topologyDict, dict())
    self.assertNotEqual(logic.polyDataDict, dict())

    segmentName = "1" # Disk
    topologyString = logic.getTopologyString(fileName, segmentName)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[0])

    segmentName = "2" # Sphere
    topologyString = logic.getTopologyString(fileName, segmentName)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[2])

    logging.info('-- case01 passed! --')

  def check_case02(self, logic, fileName):
    logging.info('-- Checking case02 --')
    self.assertTrue('case02' in fileName)

    self.assertNotEqual(logic.segmentationDict, dict())
    self.assertEqual(logic.labelRangeInCohort, (0, 5))
    self.assertNotEqual(logic.topologyDict, dict())
    self.assertNotEqual(logic.polyDataDict, dict())

    segmentName = "2" # Sphere
    topologyString = logic.getTopologyString(fileName, segmentName)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[2])

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
    logic.populateInconsistentTopologyDict()


    self.printMembers(logic)

    if fileName == 'case01_allSegments.seg.nrrd':
      self.check_case01(logic, fileName)
    elif fileName == 'case02_allSegments.seg.vtm':
      self.check_case02(logic, fileName)

    logging.info('-- Test for %s passed (importSegmentation)! --' % (fileName))

  def test_importModelFromFile(self, fileName):
    logging.info('-- Starting model test for %s --' % (fileName))
    filePath = os.path.join(self.testDir, fileName)
    logic = DataImporterLogic()
    self.assertTrue(logic.importModel(filePath))
    logic.populateTopologyDictionary()
    logic.populateInconsistentTopologyDict()

    self.printMembers(logic)

    self.assertNotEqual(logic.modelDict, dict())
    self.assertEqual(logic.labelRangeInCohort, (0, 1))
    self.assertNotEqual(logic.topologyDict, dict())
    self.assertNotEqual(logic.polyDataDict, dict())
    # All consistent
    self.assertEqual(logic.inconsistentTopologyDict, dict())
    segmentName = "sample_model" # Sphere
    topologyString, consistentTopologyString = logic.getTopologyAndConsistencyString(fileName, segmentName)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[2])
    self.assertEqual(consistentTopologyString, 'Consistent')

    logging.info('-- Test for %s passed (importModel) ! --' % (fileName))

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
                 os.path.join(self.testDir, self.casesSegmentation[1]),
                 ]
    logic.importFiles(filePaths)
    self.assertEqual(slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLLabelMapVolumeNode"), preNumberOfNodesLabelMapVolume + 1)
    self.assertEqual(slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLSegmentationNode"), preNumberOfNodesSegmentation + 2)

    # Try to load not existing file
    filePaths = [os.path.join(self.testDir, 'not_existing_for_sure.nrrd'), ]
    self.assertRaises(TypeError, logic.importFiles, filePaths)

    # Try file with different label cohort
    numberOfKeys = len(logic.topologyDict.keys())
    numberOfModels = len(logic.modelDict.keys())
    filePaths = [os.path.join(self.testDir, self.casesModel[0]), ]
    logic.importFiles(filePaths)
    # Warning to console, file is not loaded, and no member is modified.
    self.assertEqual(numberOfKeys, len(logic.topologyDict.keys()))
    self.assertEqual(numberOfModels, len(logic.modelDict.keys()))

    logging.info('-- test_importFiles passed! --')

  def test_populateDictSegmentNamesWithIntegers(self):
    logging.info('-- Starting test_populateDictSegmentNamesWithIntegers --')
    filePath = os.path.join(self.testDir, self.casesModel[0])
    logic = DataImporterLogic()
    logic.importFiles([filePath])
    logic.populateTopologyDictionary()
    logic.populateInconsistentTopologyDict()
    logic.populateDictSegmentNamesWithIntegers()
    self.assertEqual(len(logic.dictSegmentNamesWithIntegers.keys()), 1)
    for name in logic.topologyDict:
      for segmentName in logic.topologyDict[name]:
        self.assertTrue(segmentName in logic.dictSegmentNamesWithIntegers)
        self.assertEqual(logic.dictSegmentNamesWithIntegers[segmentName], 1)

  def test_computeMode(self):
    exampleDict = {
      'name0':
      {'segmentName0': '0', 'segmentName1': '1'},
      'name1':
      {'segmentName0': '1', 'segmentName1': '0'},
      'name2':
      {'segmentName0': '1', 'segmentName1': '0'}
    }
    logic = DataImporterLogic()
    mode0 = logic._computeModeOfSegment(exampleDict, 'segmentName0')
    mode1 = logic._computeModeOfSegment(exampleDict, 'segmentName1')
    self.assertEqual(mode0, str(1))
    self.assertEqual(mode1, str(0))
    mode_none = logic._computeModeOfSegment(exampleDict, 'non_existing')
    self.assertEqual(mode_none, None)

  def test_filenamesFromCSVFile(self):
    # Create the file:
    csvFilePath = ''
    with open(os.path.join(self.testDir, 'filePaths.csv'), 'w') as fileCsv:
      fileCsv.write(os.path.join(self.testDir, self.casesLabelMap[0]) + '\n')
      fileCsv.write(os.path.join(self.testDir, self.casesLabelMap[1]))
      csvFilePath = fileCsv.name
    logging.info("csvFilePath: {}".format(csvFilePath))
    logic = DataImporterLogic()
    filePaths = logic.filePathsFromCSVFile(csvFilePath)
    logging.info(filePaths)
    self.assertTrue(len(filePaths), 2)
    self.assertTrue(self.casesLabelMap[0] in filePaths[0])
    self.assertTrue(self.casesLabelMap[1] in filePaths[1])

