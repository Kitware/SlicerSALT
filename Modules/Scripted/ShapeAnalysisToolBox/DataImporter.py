import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from CommonUtilities import *
import csv

#
# ShapeAnalysisModule
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
    self.parent.contributors = ["Hina Shah (Kitware Inc.)"]
    self.parent.helpText = """
    """
    self.parent.acknowledgementText = """
    This project is funded by NIBIB
    """ # replace with organization, grant and thanks.

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
    # TODO: add the logic
    #self.logic = DataImporterLogic(self)

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

    self.CSVFileBrowsePushButton = self.getWidget('CSVFileBrowsePushButton')
    self.CSVFileBrowsePushButton.connect('clicked(bool)', self.onCSVFileBrowsePushButton)
    self.ImportButton = self.getWidget('ImportButton')
    self.ImportButton.connect('clicked(bool)', self.onImportButton)
    self.CSVFileNameLineEdit = self.getWidget('CSVFileNameLineEdit')
    self.DataInputTypeGroupBox = self.getWidget('DataInputTypeGroupBox')
    self.AutoSegInputType = self.getWidget('AutoSegInputType')
    self.AutoSegInputType.toggled.connect(lambda: self.onInputType_chosen(self.AutoSegInputType))
    self.FSLInputType = self.getWidget('FSLInputType')
    self.FSLInputType.toggled.connect(lambda: self.onInputType_chosen(self.FSLInputType))
    self.FreeSurferInputType = self.getWidget('FreeSurferInputType')
    self.FreeSurferInputType.toggled.connect(lambda: self.onInputType_chosen(self.FreeSurferInputType))
    self.GeneralInputType = self.getWidget('GeneralInputType')
    self.GeneralInputType.toggled.connect(lambda: self.onInputType_chosen(self.GeneralInputType))
    self.SubjectsTableWidget = self.getWidget('SubjectsTableWidget')
    self.StructuresSliderWidget = self.getWidget('StructuresSliderWidget')
    self.CurrentStructureTopologyLineEdit = self.getWidget('CurrentStructureTopologyLineEdit')
    self.CohortTopologyLineEdit = self.getWidget('CohortTopologyLineEdit')

    self.SubjectsTableWidget.connect('cellClicked(int, int)', self.onSubjectTableWidgetClicked)
    self.StructuresSliderWidget.connect('valueChanged(double)', self.onStructuresSliderWidgetChanged)
    self.StructuresSliderWidget.minimum = 0
    self.StructuresSliderWidget.maximum = 0

    # Initialize the beginning input type.
    self.onInputType_chosen(self.AutoSegInputType)
    self.onInputType_chosen(self.FSLInputType)
    self.onInputType_chosen(self.FreeSurferInputType)
    self.onInputType_chosen(self.GeneralInputType)

    self.testCaseDict = {}
    self.segmentationDict = {}
    self.topologyDict = {}
    self.consistentTopologyDict = {}

    self.singleDisplayedSegmentation = None
    self.createSingDisplaySegmentModelNode()
    self.labelRangeInCohort = (-1, -1)

  def createSingDisplaySegmentModelNode(self):
    if MRMLUtility.isMRMLNodeEmpty(self.singleDisplayedSegmentation, 'vtkMRMLModelNode'):
      self.singleDisplayedSegmentation = MRMLUtility.createNewMRMLNode('CurrentSegmentation', 'vtkMRMLModelNode')

  #
  # Reset all the data for data import
  # TODO: content should move to logic
  #
  def cleanup(self):
    print 'Deleting nodes'
    if self.SubjectsTableWidget is not None:
      self.SubjectsTableWidget.setRowCount(0)
    if self.testCaseDict is not None:
      for node_name in self.testCaseDict.keys():
        print 'Deleting node: ' + node_name
        MRMLUtility.removeMRMLNode(self.testCaseDict[node_name])
        MRMLUtility.removeMRMLNode(self.segmentationDict[node_name])

    if self.singleDisplayedSegmentation is not None:
      MRMLUtility.removeMRMLNode(self.singleDisplayedSegmentation)
      self.singleDisplayedSegmentation = None

    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.consistentTopologyDict = {}

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
  # TODO: part of this should move to logic
  # TODO: should also handle cases when surface files are given
  #
  def importFiles(self, filePaths):

    numCases = 0
    self.SubjectsTableWidget.setColumnCount(1)
    self.SubjectsTableWidget.setHorizontalHeaderLabels(['Subject name'])
    self.SubjectsTableWidget.verticalHeader().setVisible(False)
    self.SubjectsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
    self.SubjectsTableWidget.setSelectionMode(qt.QAbstractItemView.SingleSelection)
    for path in filePaths:
      # load each file
      pathPair = os.path.split(path)
      directory = pathPair[0]
      fileName = pathPair[1]
      self.testCaseDict[fileName] = MRMLUtility.loadMRMLNode(fileName, directory, fileName, 'LabelMap')
      if self.testCaseDict[fileName] is None:
        print 'ERROR: Failed to load ' + fileName + 'as a labelmap'
        # make sure each one is a labelmap
        continue

      # Create segmentation representations.
      self.segmentationDict[fileName] = MRMLUtility.createNewMRMLNode(fileName + '_allSegments', 'vtkMRMLSegmentationNode')
      slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(self.testCaseDict[fileName],
                                                                            self.segmentationDict[fileName])
      t = self.segmentationDict[fileName].CreateClosedSurfaceRepresentation()
      if t == False:
        print 'ERROR: Failed to create closed surface representation'
        continue

      self.segmentationDict[fileName].SetDisplayVisibility(False)

      # find how many labels each file has..
      labelRange = self.testCaseDict[fileName].GetImageData().GetScalarRange()
      if self.labelRangeInCohort != (-1, -1) and labelRange != self.labelRangeInCohort:
        print 'ERROR: Number of labels do not match in the cohort'
        return

      self.labelRangeInCohort = labelRange

      # extract just the filename, and populate the tablewidget
      rowPosition = self.SubjectsTableWidget.rowCount
      self.SubjectsTableWidget.insertRow(rowPosition)
      self.SubjectsTableWidget.setItem(rowPosition, 0, qt.QTableWidgetItem(fileName))
      numCases = numCases + 1
    self.SubjectsTableWidget.setCurrentCell(0, 0)

    print 'Cohort label range is: ' + str(self.labelRangeInCohort)
    # given labels, and current mode populate the structures slider
    self.labelRangeInCohort = (int(self.labelRangeInCohort[0]), int(self.labelRangeInCohort[1]))
    self.StructuresSliderWidget.minimum = int(self.labelRangeInCohort[0])
    self.StructuresSliderWidget.maximum = int(self.labelRangeInCohort[1])
    self.StructuresSliderWidget.setValue(0)

    # Populate the topology table
    self.populateTopologyDictionary()

    self.onSubjectTableWidgetClicked(0,0)

  #
  # Function to estimate topology of segmentations, and check for consistencies.
  # TODO: Should move to logic
  #
  def populateTopologyDictionary(self):

    # Create vtk objects that will be used to clean the geometries
    polydataCleaner = vtk.vtkCleanPolyData()
    connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
    extractEdgeFilter = vtk.vtkExtractEdges()

    firstValue = {} # This will be used for checking consistent, inconsistent topologies

    for nodeName in self.testCaseDict.keys():
      # Topology table is a dictionary of dictionaries.
      self.topologyDict[nodeName] = {}
      for segmentNum in range(self.labelRangeInCohort[0], self.labelRangeInCohort[1]+1):
        # 0 label is assumed to be the background.
        if segmentNum == 0:
          continue
        segmentId = str(segmentNum)
        polydata = self.segmentationDict[nodeName].GetClosedSurfaceRepresentation(segmentId)
        if polydata == None:
          print 'Ignoring segment id ' + segmentId + ' for case: ' + nodeName
          continue
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
        #print 'Topology number of ' + nodeName + ' segment: ' + segmentId + ' is: ' + str(topologyNumber)
        #print 'Number of edges: ' + str(edges.GetNumberOfLines()) + ' Number of points: ' + \
        #  str(cleanData.GetNumberOfPoints() ) + ' Number of polys: ' + str(cleanData.GetNumberOfPolys())

        self.topologyDict[nodeName][segmentNum] = topologyNumber
        del cleanData
        del edges
        del largestComponent

        # Check for consistency in the cohort for this segment label
        if segmentNum not in self.consistentTopologyDict.keys():
          self.consistentTopologyDict[segmentNum] = 'Consistent'
          firstValue[segmentNum] = self.topologyDict[nodeName][segmentNum]
          #print 'Adding segment num ' + segmentId + ' with top number: ' + str(topologyNumber) + ' For consistencies'
        elif firstValue[segmentNum] != self.topologyDict[nodeName][segmentNum] \
              and self.consistentTopologyDict[segmentNum] is 'Consistent':
          self.consistentTopologyDict[segmentNum] = 'InConsistent'
          #print 'Setting to inconsistent for segment num: ' + segmentId + ' and current number: ' + str(topologyNumber)

  '''
  GUI Callback functions
  '''
  #
  #  Handle request to import data
  #
  def onImportButton(self):
    filenames = []
    self.cleanup()
    if self.importFromCSV:
      with open(self.csvFileName, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # ignore the header
        next(reader, None)
        # assuming that each row is just a file path.
        for row in reader:
          filenames.append(row[0])
        # Import all files
        self.importFiles(filenames)
        # Depending on the mode fill the structures table.
        # TODO: add directory parsing based on mode
    else:
      print "Importing from directory is not yet supported"

  def onCSVFileBrowsePushButton(self):
    self.csvFileName = qt.QFileDialog.getOpenFileName(self.widget, "Open CSV File", ".", "CSV Files (*.csv)")
    self.CSVFileNameLineEdit.text = self.csvFileName
    self.importFromCSV = True

  def onInputType_chosen(self, b):
    inputTypeText = b.text
    if b.isChecked():
      self.inputType = inputTypeText

  def onSubjectTableWidgetClicked(self, row, column):
    nodeName = self.SubjectsTableWidget.item(row, column).text()
    segmentId = str(int(self.StructuresSliderWidget.value))
    self.displaySegment(nodeName, segmentId)
    self.updateTopologyDisplay(nodeName, segmentId)

  def onStructuresSliderWidgetChanged(self, value):
    nodeName = self.SubjectsTableWidget.currentItem().text()
    segmentId = str(int(value))
    self.displaySegment(nodeName, segmentId)
    self.updateTopologyDisplay(nodeName, segmentId)

  '''
  Supplemental functions to update the visualizations
  '''
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

    polydata = self.segmentationDict[nodeName].GetClosedSurfaceRepresentation(segmentId)
    if polydata == None:
      print 'ERROR: polydata for ' + nodeName + ' and ' + segmentId + ' does not exist!!'
      return

    self.createSingDisplaySegmentModelNode()

    self.singleDisplayedSegmentation.SetAndObservePolyData(polydata)
    self.singleDisplayedSegmentation.SetDisplayVisibility(1)
    color = [0,0,0,0]
    segmentIdNum = int(self.StructuresSliderWidget.value)
    slicer.util.getNode('GenericAnatomyColors').GetColor(segmentIdNum, color)
    self.singleDisplayedSegmentation.GetDisplayNode().SetColor(color[0:3])
    self.reset3dView()

  def updateTopologyDisplay(self, nodeName, segmentId):
    segmentNum = int(segmentId)
    topologyString = 'n/a'

    # TODO: topology and consistency string should come from logic
    if nodeName in self.topologyDict and segmentNum in self.topologyDict[nodeName]:
      topologyNum = self.topologyDict[nodeName][segmentNum]
      topologyString = {
        1: 'Disk',
        0: 'Circle/Torus/Mobius Strip',
        2: 'Sphere',
        -2: 'Double Torus',
        -4: 'Triple Torus',
      }.get(topologyNum, 'n/a')
    self.CurrentStructureTopologyLineEdit.setText(topologyString)
    consistentTopologyString = self.consistentTopologyDict[segmentNum] \
                                if segmentNum in self.consistentTopologyDict.keys() else 'n/a'
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

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.delayDisplay(' Tests Passed! ')