import vtk, qt, ctk, slicer, PythonQt


# ICON_DIR = os.path.dirname(os.path.realpath(__file__)) + '/Resources/Icons/'

#
# Home
#

class Home:
    def __init__(self, parent):
        parent.title = "Home"
        parent.categories = ["Shape Analysis Toolbox"]
        parent.dependencies = []
        parent.contributors = ["Hina Shah (Kitware Inc), Laura Pascal (Kitware Inc), Beatriz Paniagua (Kitware Inc), ."]
        parent.helpText = """<center>
        <br>
        <b>Welcome to SlicerSALT!</b><br>
        <br>
        Visit <a href="https://bpaniagua.github.io/slicersalt.github.io/">slicersalt.github.io</a> for more information about SlicerSALT.<br>
        <br>
        Documentation and tutorials can be found at: <a href="https://bpaniagua.github.io/slicersalt.github.io/docs/">slicersalt.github.io/docs</a><br>
        </center>
        """
        parent.acknowledgementText = """
        <center> <br>SlicerSALT is an open source software package for doing shape analysis of image segmentations using different methods. <br>
        <br> Ongoing development, maintenance, distribution, and training is managed by UNC Chapel Hill, M.D. Cancer Center at The University of Texas, NYU Tandon School of Engineering and Kitware Inc.<br>
        <br> The project is funded by NIH grant: NIBIB R01EB021391 (Paniagua B). <br>
        <br> SlicerSALT is supported by NIH and the Slicer Community. <br>
        </center>
        """

        # parent.icon = qt.QIcon("%s/cranioIcon.png" % ICON_DIR)

        self.parent = parent


#
# qHomeWidget
#

class HomeWidget:
    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
        self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()

    def setup(self):

        # TEXT
        text = """
<br>
<u>Workflow quick-reference:</u><br>
<br>
The drop-down Modules are ordered to follow the basic workflow for choosing and using data.  As a quick reference, the basic steps involve:<br>
<br>
&nbsp; 1. Use the <a href="#"><b>Data importer</b></a> module to load your segmentations from FreeSurf, FSL, Autoseg, or a bunch of vtp's<br><br>
&nbsp; 2. Use <a href="#"><b>Shape Population Viewer</b></a> to do a quality check on the imported data<br><br>
&nbsp; 3. Use <a href="#"><b>SPHARM Shape Analysis Module</b></a> to do spherical harmonics based analysis<br><br>
&nbsp; 4. Use the <a href="#"><b>Study-specific Shape Analysis</b></a> module.<br><br>
&nbsp; 5. Use the <a href="#"><b>S-Rep Shape Analysis</b></a> module to do shape analysis via skeletal representations.<br><br>
&nbsp; 6. Use the <a href="#"><b>Shape Evaluator</b></a> module to compute a mean shape and see how the population varies.<br><br>
&nbsp; 7. Use <a href="#"><b>Shape Regressions</b></a> module to do regression based analysis.<br><br>
&nbsp; 8. Use the <a href="#"><b>Shape Statistics</b></a> module.<br><br>
"""

        # TEXTEDIT
        self.HomeTextSection = qt.QTextEdit()
        self.HomeTextSection.setReadOnly(True)
        self.HomeTextSection.setText(text)
        self.HomeTextSection.setMinimumHeight(400)
        self.HomeTextSection.connect('cursorPositionChanged()', self.slot)
        self.layout.addWidget(self.HomeTextSection)

        # SPACER
        self.layout.addStretch()

    def slot(self):
        pos = self.HomeTextSection.textCursor().position()

        if pos >= 181 and pos <= 194 :
            slicer.util.selectModule(slicer.moduleNames.DataImporter)
        elif pos >= 288 and pos <= 311 :
            slicer.util.selectModule(slicer.moduleNames.ShapePopulationViewer)
        elif pos >= 365 and pos <= 393 :
            slicer.util.selectModule(slicer.moduleNames.ShapeAnalysisModule)
        elif pos >= 449 and pos <= 478 :
            slicer.util.selectModule(slicer.moduleNames.GroupWiseRegistrationModule)
        elif pos >= 501 and pos <= 522 :
            slicer.util.selectModule(slicer.moduleNames.SkeletalRepresentationVisualizer)
        elif pos >= 594 and pos <= 610 :
            slicer.util.selectModule(slicer.moduleNames.Home) #SVA
        elif pos >= 686 and pos <= 703 :
            slicer.util.selectModule(slicer.moduleNames.RegressionComputation)
        elif pos >= 758 and pos <= 774 :
             slicer.util.selectModule(slicer.moduleNames.Home) #MFSDA
