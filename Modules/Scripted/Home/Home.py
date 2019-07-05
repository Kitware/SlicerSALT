import os
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import (ScriptedLoadableModule,
                                           ScriptedLoadableModuleWidget)
import SampleData
import logging
import json
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

        # Instantiate and connect widgets ...
        # TEXT
        text = """
<br>
<u>Workflow quick-reference:</u><br>
<br>
The drop-down Modules are ordered to follow the basic workflow for choosing and using data.  As a quick reference, the basic steps involve:<br>
<br>
&nbsp; 1. Use the <a href="#DataImporter"><b>Data importer</b></a> module to load your segmentations from FreeSurf, FSL, Autoseg, or a bunch of vtp's<br><br>
&nbsp; 2. Use <a href="#ShapePopulationViewer"><b>Shape Population Viewer</b></a> to do a quality check on the imported data<br><br>
&nbsp; 3. Use <a href="#ShapeAnalysisModule"><b>SPHARM Shape Analysis Module</b></a> to do spherical harmonics based analysis<br><br>
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

                SampleData.SampleDataLogic.registerCustomSampleDataSource(
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

    def onAnchorClicked(self, url):
        moduleName = url.fragment()
        slicer.util.selectModule(moduleName)

    @staticmethod
    def downloadSampleDataInFolder(source):
        widget = slicer.modules.sampledata.widgetRepresentation().self()
        sampleDataLogic = widget.logic

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
