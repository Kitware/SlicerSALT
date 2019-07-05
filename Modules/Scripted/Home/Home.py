import os
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import (ScriptedLoadableModule,
                                           ScriptedLoadableModuleWidget)
import logging
import json
from SampleData import SampleDataLogic, SampleDataWidget
from slicer.util import computeChecksum, extractAlgoAndDigest


#
# Home
#

class Home(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """
    def __init__(self, parent):
        parent.title = "Home"
        parent.categories = [""]
        parent.index = 0
        parent.dependencies = ["SampleData"]
        parent.contributors = ["Kitware, Inc., The University of North Carolina at Chapel Hill, and NYU Tandon School of Engineering"]
        parent.helpText = """<center>
        <br>
        <b>Welcome to SlicerSALT!</b><br>
        <br>
        Visit <a href="https://salt.slicer.org">salt.slicer.org</a> for more information about SlicerSALT.<br>
        <br>
        Documentation and tutorials can be found at: <a href="https://salt.slicer.org/docs/">salt.slicer.org/docs/</a><br>
        </center>
        """
        parent.acknowledgementText = """
        <center> <br>SlicerSALT is an open source software package for doing shape analysis of image segmentations using different methods. <br>
        <br> Ongoing development, maintenance, distribution, and training is managed by UNC Chapel Hill, NYU Tandon School of Engineering and Kitware Inc.<br>
        <br> The project is funded by NIH grant: NIBIB R01EB021391 (Paniagua B). <br>
        <br> SlicerSALT is supported by NIH and the Slicer Community. <br>
        </center>
        """

        slicer.app.connect("startupCompleted()", self.updateModulesMenu)

    def updateModulesMenu(self):
        moduleMenu = slicer.util.mainWindow().moduleSelector().modulesMenu()

        moduleMenu.removeCategory("Developer Tools")
        moduleMenu.removeCategory("Diffusion")
        moduleMenu.removeCategory("Converters")
        moduleMenu.removeCategory("Registration.Specialized")
        moduleMenu.removeCategory("Segmentation")

        removeFromAllModules = False
        moduleMenu.removeModule("SegmentEditor", removeFromAllModules)
        moduleMenu.removeModule("Segmentations", removeFromAllModules)
        moduleMenu.removeModule("Terminologies", removeFromAllModules)


#
# HomeWidget
#

class HomeWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # The anchor associated with each link corresponds to the name of the module to select.
        # For example, after the user click on the link associated with `href="#DataImporter"`,
        # the "DataImporter" module is selected.
        text = """
<br>
<u>Workflow quick-reference:</u><br>
<br>
The drop-down Modules are ordered to follow the basic workflow for choosing and using data.  As a quick reference, the basic steps involve:<br>
<br>
&nbsp; 1. Use the <a href="#DataImporter"><b>Data importer</b></a> module to load your segmentations from FreeSurf, FSL, Autoseg, or a bunch of vtp's<br><br>
&nbsp; 2. Use <a href="#ShapePopulationViewer"><b>Shape Population Viewer</b></a> to do a quality check on the imported data<br><br>
&nbsp; 3. Use <a href="#ShapeAnalysisModule"><b>SPHARM-PDM Generator</b></a> to do spherical harmonics based analysis<br><br>
&nbsp; 4. Use the <a href="#GroupWiseRegistrationModule"><b>Study-specific Shape Analysis</b></a> module.<br><br>
&nbsp; 5. Use the <a href="#SkeletalRepresentationVisualizer"><b>S-Rep Shape Analysis</b></a> module to do shape analysis via skeletal representations.<br><br>
&nbsp; 6. Use the <a href="#ShapeVariationAnalyzer"><b>Shape Evaluator</b></a> module to compute a mean shape and see how the population varies.<br><br>
&nbsp; 7. Use <a href="#RegressionComputation"><b>Shape Regressions</b></a> module to do regression based analysis.<br><br>
&nbsp; 8. Use the <a href="#MFSDA"><b>Shape Statistics</b></a> module.<br><br>
"""

        # TEXTEDIT
        self.HomeTextSection = qt.QTextBrowser()
        self.HomeTextSection.setHtml(text)
        self.HomeTextSection.setMinimumHeight(400)
        self.HomeTextSection.connect('anchorClicked(QUrl)', self.onAnchorClicked)
        self.layout.addWidget(self.HomeTextSection)

        # SPACER
        self.layout.addStretch()

        # SAMPLE DATA REGISTRATION
        for json_file in [
            'DataImporterInputData.json',
            'ShapeRegressionInputData.json',
            'SPHARM-PDMTestData.json',
        ]:
            with open(self.resourcePath('SampleDataDescription/%s' % json_file), 'r') as json_data:
                source_data = json.load(json_data)
                if 'iconPath' in source_data:
                  iconPath = self.resourcePath(source_data['iconPath'])
                else:
                  iconPath = None

                SampleDataLogic.registerCustomSampleDataSource(
                    category=source_data['category'],
                    sampleName=source_data['sampleName'],
                    uris=source_data['uris'],
                    checksums=source_data.get('checksums', None),
                    fileNames=source_data['fileNames'],
                    nodeNames=None,
                    thumbnailFileName=iconPath,
                    loadFileType=None,
                    customDownloader=self.downloadSampleDataInFolder,
                )

        # HIDE SAMPLE DATA 'BUILTIN' CATEGORY
        slicer.modules.sampledata.widgetRepresentation().self().setCategoryVisible('BuiltIn', False)

        self.sampleDataModuleTab = None
        self.sampleDataTabTextEdit = None

        self.moduleNameToSampleDataCategory = {
            "DataImporter": "Data Importer",
            "ShapeAnalysisModule": "SPHARM-PDM",
            "RegressionComputation": "Shape Regression",
        }

        self.sampleDataModuleTab = self.addSampleDataTab()
        self.updateSampleDataTab("Home")
        moduleMenu = slicer.util.mainWindow().moduleSelector().modulesMenu()
        moduleMenu.connect("currentModuleChanged(QString)", self.updateSampleDataTab)

    def cleanup(self):
        currentSampleDataLogic = slicer.modules.sampledata.widgetRepresentation().self().logic
        SampleDataWidget.setCategoriesFromSampleDataSources(self.sampleDataModuleTab.layout(), {}, currentSampleDataLogic)

    def onAnchorClicked(self, url):
        moduleName = url.fragment()
        slicer.util.selectModule(moduleName)

    @staticmethod
    def downloadSampleDataInFolder(source):

        if slicer.util.selectedModule() == "SampleData":
            sampleDataLogic = slicer.modules.sampledata.widgetRepresentation().self().logic
        else:
            sampleDataLogic = SampleDataLogic(logMessage=slicer.modules.HomeWidget.logSampleDataTabMessage)

        # Retrieve directory
        category = sampleDataLogic.categoryForSource(source)
        savedDirectory = slicer.app.userSettings().value(
            "SampleData/Last%sDownloadDirectory" % category,
            qt.QStandardPaths.writableLocation(qt.QStandardPaths.DocumentsLocation))

        destFolderPath = str(qt.QFileDialog.getExistingDirectory(slicer.util.mainWindow(), 'Destination Folder', savedDirectory))
        if not os.path.isdir(destFolderPath):
            return

        print('Selected data folder: %s' % destFolderPath)

        for uri, fileName, checksum  in zip(source.uris, source.fileNames, source.checksums):
            sampleDataLogic.downloadFile(uri, destFolderPath, fileName, checksum=checksum)

        # Save directory
        slicer.app.userSettings().setValue("SampleData/Last%sDownloadDirectory" % category, destFolderPath)

    @staticmethod
    def addSampleDataTab():
        tabWidget = slicer.util.findChild(slicer.util.mainWindow(), "HelpAcknowledgementTabWidget")
        sampleDataTab = qt.QWidget()
        sampleDataTab.objectName = "SampleDataTab"
        verticalLayout = qt.QVBoxLayout(sampleDataTab)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        tabWidget.addTab(sampleDataTab, "SampleData")
        return sampleDataTab

    def logSampleDataTabMessage(self, message, logLevel=logging.INFO):
        # Set text color based on log level
        if logLevel >= logging.ERROR:
          message = '<font color="red">' + message + '</font>'
        elif logLevel >= logging.WARNING:
          message = '<font color="orange">' + message + '</font>'
        # Show message in status bar
        doc = qt.QTextDocument()
        doc.setHtml(message)
        slicer.util.showStatusMessage(doc.toPlainText(),3000)
        # Show message in log window at the bottom of the module widget
        self.sampleDataTabTextEdit.insertHtml(message)
        self.sampleDataTabTextEdit.insertPlainText('\n')
        self.sampleDataTabTextEdit.ensureCursorVisible()
        self.sampleDataTabTextEdit.repaint()
        logging.log(logLevel, message)
        slicer.app.processEvents(qt.QEventLoop.ExcludeUserInputEvents)

    def updateSampleDataTab(self, moduleName):
        currentSampleDataLogic = slicer.modules.sampledata.widgetRepresentation().self().logic
        categoryLayout = self.sampleDataModuleTab.layout()
        if moduleName not in self.moduleNameToSampleDataCategory:
            SampleDataWidget.setCategoriesFromSampleDataSources(categoryLayout, {}, currentSampleDataLogic)
            label = qt.QLabel("No SampleData available for this module")
            categoryLayout.addWidget(label)
        else:
            category = self.moduleNameToSampleDataCategory[moduleName]
            sources = {category: slicer.modules.sampleDataSources[category]}
            SampleDataWidget.setCategoriesFromSampleDataSources(categoryLayout, sources, currentSampleDataLogic)
            log = qt.QTextEdit()
            log.readOnly = True
            categoryLayout.addWidget(log)
            log.insertHtml('<p>Status: <i>Idle</i></p>')
            self.sampleDataTabTextEdit = log
