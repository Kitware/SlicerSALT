import os, sys
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
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
    #
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
    self.StructuresTableWidget = self.getWidget('StructuresTableWidget')

    # Initialize the beginning input type.
    self.onInputType_chosen(self.AutoSegInputType)
    self.onInputType_chosen(self.FSLInputType)
    self.onInputType_chosen(self.FreeSurferInputType)
    self.onInputType_chosen(self.GeneralInputType)

  def cleanup(self):
    pass

  # Functions to recovery the widget in the .ui file
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

  def importFiles(self, filePaths):

    numCases = 0
    self.SubjectsTableWidget.setColumnCount(1)
    self.SubjectsTableWidget.setHorizontalHeaderLabels(['Subject name'])
    self.SubjectsTableWidget.verticalHeader().setVisible(False)

    for path in filePaths:
      # load each file
      pathPair = os.path.split(path)
      directory = pathPair[0]
      fileName = pathPair[1]
      print 'processing case: ' + path
      self.testCaseDict[fileName] = MRMLUtility.loadMRMLNode(fileName, directory, fileName, 'LabelMap')
      if self.testCaseDict[fileName] is None:
        print 'Failed to load ' + fileName + 'as a labelmap'
        # make sure each one is a labelmap
        continue

      # find how many labels each file has..

      # extract just the filename, and populate the tablewidget
      rowPosition = self.SubjectsTableWidget.rowCount
      self.SubjectsTableWidget.insertRow(rowPosition)
      self.SubjectsTableWidget.setItem(rowPosition, 0, qt.QTableWidgetItem(fileName))
      numCases = numCases + 1
      print 'Columnt count is: ' + str(self.SubjectsTableWidget.columnCount)
      print 'Row size is: ' + str(self.SubjectsTableWidget.rowCount)
      # given labels, and current mode fill the structure table

  #
  #  Handle request to import data
  #
  def onImportButton(self):
    filenames = []
    if self.importFromCSV:
      with open(self.csvFileName, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # ignore the header
        next(reader, None)
        # assuming that each row is just a file path.
        for row in reader:
          filenames.append(row[0])
        print filenames
        print 'input type is: ' + self.inputType
        self.importFiles(filenames)
        # Import all files
        # Depending on the mode fill the structures table.
    else:
      print "Importing from directory is not yet supported"

  def onCSVFileBrowsePushButton(self):
    self.csvFileName = qt.QFileDialog.getOpenFileName(self.widget, "Open CSV File", ".", "CSV Files (*.csv)")
    self.CSVFileNameLineEdit.text = self.csvFileName
    self.importFromCSV = True
    print self.csvFileName

  def onInputType_chosen(self, b):
    inputTypeText = b.text
    if b.isChecked():
      self.inputType = inputTypeText
#
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