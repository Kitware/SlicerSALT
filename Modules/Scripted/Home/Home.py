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
&nbsp; 4. Use <a href="#"><b>Shape Regressions</b></a> module to do regression based analysis.<br><br>
&nbsp; 5. Use the <a href="#"><b>Study-specific Shape Analysis</b></a> module.<br><br>
&nbsp; 6. Use the <a href="#"><b>Shape Statistics</b></a> module.<br><br>
&nbsp; 7. Use the <a href="#"><b>S-Rep Shape Analysis</b></a> module to do shape analysis via skeletal representations.<br><br>
&nbsp; 8. Use the <a href="#"><b>Save Results</b></a> module to generate a NIRFAST-compatible mesh from the segmented tissue (label maps)<br><br>
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

        if pos >= 264 and pos <= 270 :
            slicer.util.selectModule(slicer.moduleNames.DataImporter)
        elif pos >= 317 and pos <= 334 :
            slicer.util.selectModule(slicer.moduleNames.VolumeRendering)
        elif pos >= 384 and pos <= 389 :
            slicer.util.selectModule(slicer.moduleNames.CropVolume)
        elif pos >= 499 and pos <= 533 :
            slicer.util.selectModule(slicer.moduleNames.SegmentEditor)
        elif pos >= 662 and pos <= 676 :
            slicer.util.selectModule(slicer.moduleNames.Segmentations)
        elif pos >= 748 and pos <= 756 :
            slicer.util.selectModule(slicer.moduleNames.Markups)
        elif pos >= 825 and pos <= 837 :
            slicer.util.selectModule(slicer.moduleNames.Image2Mesh)
	elif pos >= 1081 and pos <= 1107 :
             slicer.util.selectModule(slicer.moduleNames.Mesh2Image)
