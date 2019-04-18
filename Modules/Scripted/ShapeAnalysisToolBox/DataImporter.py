import vtk, ctk, qt, slicer
from slicer.ScriptedLoadableModule import (ScriptedLoadableModule,
                                           ScriptedLoadableModuleLogic,
                                           ScriptedLoadableModuleWidget,
                                           ScriptedLoadableModuleTest)
from collections import Counter
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
    self.parent.contributors = ["Pablo Hernandez (Kitware Inc,), Hina Shah (Kitware Inc.)"]
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
  TOPOLOGY_STRIP_TYPE = 0
  TOPOLOGY_DISK_TYPE = 1
  TOPOLOGY_SPHERE_TYPE = 2
  TOPOLOGY_DOUBLE_TORUS_TYPE = -2
  TOPOLOGY_TRIPLE_TORUS_TYPE = -4
  TOPOLOGY_MULTIPLE_HOLES_TYPE = -9999
  TOPOLOGY_TYPES = {
    TOPOLOGY_STRIP_TYPE : 'Circle/Torus/Mobius Strip',
    TOPOLOGY_DISK_TYPE : 'Disk',
    TOPOLOGY_SPHERE_TYPE : 'Sphere',
    TOPOLOGY_DOUBLE_TORUS_TYPE : 'Double Torus',
    TOPOLOGY_TRIPLE_TORUS_TYPE : 'Triple Torus',
    TOPOLOGY_MULTIPLE_HOLES_TYPE : 'Multiple Holes',
  }

  def __init__(self):
    ScriptedLoadableModuleLogic.__init__(self)

    self.saveCleanData = False
    self.labelMapDict = {}
    self.modelDict = {}
    self.segmentationDict = {}
    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.polyDataDict = {}
    # help variable to map continuous indices to TOPOLOGY_TYPES. Used in comboBoxes
    self.topologyTypeToIndex = {
      self.TOPOLOGY_STRIP_TYPE : 0,
      self.TOPOLOGY_DISK_TYPE : 1,
      self.TOPOLOGY_SPHERE_TYPE : 2,
      self.TOPOLOGY_DOUBLE_TORUS_TYPE : 3,
      self.TOPOLOGY_TRIPLE_TORUS_TYPE : 4,
      self.TOPOLOGY_MULTIPLE_HOLES_TYPE : 5,
    }
    self.indexToTopologyType = {index: topologyType for topologyType, index in self.topologyTypeToIndex.items()}
    self.expectedTopologiesBySegment = {}
    self.inconsistentTopologyDict = {}

    self.numberOfDifferentSegments = 0
    self.dictSegmentNamesWithIntegers = dict()

    self.freesurfer_import=False
    self.freesurfer_wanted_segments=[]


    scene = slicer.mrmlScene
    count = scene.GetNumberOfNodes()
    for idx in range(count):
      node = scene.GetNthNode(idx)
      node_type = node.GetClassName()
      name = node.GetName()
      id = node.GetID()
      if node_type == 'vtkMRMLColorTableNode':
        print(name)

  def setSaveCleanData(self, save):

    self.saveCleanData = save

  #
  # Reset all the data for data import
  #
  def cleanup(self):
    logging.debug('Deleting nodes')
    if self.labelMapDict is not None:
      for nodeName in self.labelMapDict:
        logging.debug('Deleting label map node: ' + nodeName)
        slicer.mrmlScene.RemoveNode(self.labelMapDict[nodeName])

    if self.modelDict is not None:
      for nodeName in self.modelDict:
        logging.debug('Deleting model node: ' + nodeName)
        slicer.mrmlScene.RemoveNode(self.modelDict[nodeName])

    if self.segmentationDict is not None:
      for nodeName in self.segmentationDict:
        logging.debug('Deleting segmentation node: ' + nodeName)
        slicer.mrmlScene.RemoveNode(self.segmentationDict[nodeName])

    self.labelMapDict = {}
    self.modelDict = {}
    self.segmentationDict = {}
    self.labelRangeInCohort = (-1, -1)
    self.topologyDict = {}
    self.polyDataDict = {}
    self.expectedTopologiesBySegment = {}
    self.inconsistentTopologyDict = {}

    self.numberOfDifferentSegments = 0
    self.dictSegmentNamesWithIntegers = dict()

  def __del__(self):

    self.cleanup()

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

    labelMapNode.SetDisplayVisibility(False)
    file_name = os.path.splitext(fileName)[0]
    if self.freesurfer_import == True:
      subject_name = os.path.split(os.path.split(directory)[0])[1]
      segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", subject_name+' '+file_name+'_SelectedSegments')
    else:
      segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", labelMapNode.GetName() + '_allSegments')
    segmentationLogic = slicer.modules.segmentations.logic()
    segmentationLogic.ImportLabelmapToSegmentationNode(labelMapNode,
                                                       segmentationNode)

    #if importing from freesurfer
    if self.freesurfer_import == True:
      to_remove_ids=[]
      freesurfer_found_segments=[]
      

      for segmentIndex in range(segmentationNode.GetSegmentation().GetNumberOfSegments()):
        segmentId = segmentationNode.GetSegmentation().GetNthSegmentID(segmentIndex)
        segmentName = segmentationNode.GetSegmentation().GetSegment(segmentId).GetName()
        if segmentName not in self.freesurfer_wanted_segments:
          to_remove_ids.append(segmentId)
        else:
          freesurfer_found_segments.append(segmentName)
          label_id=segmentName.split('_')[1]
          seg_name=self.freesurfer_lut_dict[label_id]['name']
          color=self.freesurfer_lut_dict[label_id]['color']
          segment = segmentationNode.GetSegmentation().GetSegment(segmentId)

          
          segment_name=subject_name+' '+file_name+' '+seg_name
          segment.SetName(segment_name)
          # segment.SetName(seg_name)
          segment.SetColor(color)

      if len(freesurfer_found_segments)!=len(self.freesurfer_wanted_segments):
        unpresent_segments=self.freesurfer_wanted_segments[:]
        for seg in freesurfer_found_segments:
          del unpresent_segments[unpresent_segments.index(seg)]
        unpresent_segments = map(lambda x: self.freesurfer_lut_dict[x.split('_')[1]]['name'], unpresent_segments) 
        logging.warning('Unable to find all segments, {} have not been found.'.format(unpresent_segments))
        logging.warning('LabelMap in path: {} has not been loaded into segmentationDict.'.format(path))
        return False

      for segmentId in to_remove_ids:
        segmentationNode.GetSegmentation().RemoveSegment(segmentId)

    else:
      for segmentIndex in range(segmentationNode.GetSegmentation().GetNumberOfSegments()):
        segmentId = segmentationNode.GetSegmentation().GetNthSegmentID(segmentIndex)
        segment = segmentationNode.GetSegmentation().GetSegment(segmentId)
        segmentName = segment.GetName()

          
        segment_name=file_name+' '+seg_name
        segment.SetName(segment_name)
      


    closedSurface = segmentationNode.CreateClosedSurfaceRepresentation()

    # m_h = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelHierarchyNode", subject_name+' '+file_name+' Segments')
    # segmentationLogic.ExportAllSegmentsToModelHierarchy(segmentationNode,m_h)

    # collec=vtk.vtkCollection()
    # m_h.GetChildrenModelNodes(collec)

    # for i in range(collec.GetNumberOfItems()):
    #   m_n = collec.GetItemAsObject(i)
    #   displaynode=m_n.GetDisplayNode()
    #   displaynode.BackfaceCullingOff()
    #   displaynode.SetVisibility(False)

    segmentationNode.SetDisplayVisibility(False)
    segmentationNode.GetDisplayNode().SetAllSegmentsVisibility(False)

    if closedSurface is False:
      logging.error('Failed to create closed surface representation for filename: {}.'.format(path))
      return False

    labelRangeConsistent, labelRange = self.checkLabelRangeConsistency(segmentationNode.GetSegmentation().GetNumberOfSegments())
    if not labelRangeConsistent:
      logging.warning('LabelMap in path: {} has not been loaded into segmentationDict.'.format(path))
      return False

    # Add to the dicts only if succesful
    if self.freesurfer_import == True:
      subject_name = os.path.split(os.path.split(directory)[0])[1]
      file_name = os.path.splitext(fileName)[0]
      name = subject_name+' '+file_name

      self.labelMapDict[name] = labelMapNode
      self.segmentationDict[name] = segmentationNode
      self.labelRangeInCohort = labelRange
    else:
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
    modelNode.SetDisplayVisibility(False)

    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", modelNode.GetName() + '_allSegments')
    segmentationLogic = slicer.modules.segmentations.logic()
    segmentationLogic.ImportModelToSegmentationNode(modelNode,
                                                    segmentationNode)
    # To allow better mixing with label maps.
    # We change the name of the model (originally set to the filename in vtkSlicerSegmentationModuleLogic)
    # XXX Better option would be to use terminologies, see: https://discourse.slicer.org/t/finding-corresponding-segments-in-segmentations/4055/4
    file_name = os.path.splitext(fileName)[0]
    segmentationNode.GetSegmentation().GetSegment(modelNode.GetName()).SetName(file_name+' 1')
    closedSurface = segmentationNode.CreateClosedSurfaceRepresentation()
    segmentationNode.SetDisplayVisibility(False)
    # segmentationNode.GetDisplayNode().SetAllSegmentsVisibility(False)
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
    # segmentationNode.GetDisplayNode().SetAllSegmentsVisibility(False)

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
    self.found_segments =[]
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

    Example::
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
    Example::
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
        logging.warning("Topology: [{}] for segmentName: '{}', shows multiple holes. Use a key from {}".format(topologyType, segmentName, self.TOPOLOGY_TYPES))
        topologyType = self.TOPOLOGY_MULTIPLE_HOLES_TYPE

      self.expectedTopologiesBySegment[segmentName] = long(topologyType)

  def setFreeSurferimport(self,bool):

    self.freesurfer_import=bool

  
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
    for nodeName in self.segmentationDict:
      # Topology table is a dictionary of dictionaries.
      self.topologyDict[nodeName] = {}
      self.polyDataDict[nodeName] = {}
      segmentationNode = self.segmentationDict[nodeName]
      for segmentIndex in range(segmentationNode.GetSegmentation().GetNumberOfSegments()):
        segmentId = segmentationNode.GetSegmentation().GetNthSegmentID(segmentIndex)
        segmentName = segmentationNode.GetSegmentation().GetSegment(segmentId).GetName()

        # 0 label is assumed to be the background. XXX Pablo: assumed where?
        if segmentName == "0":
          continue
        polydata = segmentationNode.GetClosedSurfaceRepresentation(segmentId)
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
    return consistent, self.inconsistentTopologyDict

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
    if not self.expectedTopologiesBySegment:# or self.expectedTopologiesBySegment.keys() != inputTopologyDictionary.keys():
      self.initExpectedTopologyBySegmentWithModes(inputTopologyDictionary)

    inconsistenciesExist = False
    inconsistentSegments = {}

    for nameNode, segmentsDict in inputTopologyDictionary.iteritems():
      for segmentName, topologyType in segmentsDict.iteritems():
        if topologyType != self.expectedTopologiesBySegment[segmentName]:
          if not nameNode in inconsistentSegments:
            inconsistentSegments[nameNode] = {}
          inconsistentSegments[nameNode][segmentName] = topologyType

    if inconsistentSegments:
      inconsistenciesExist = True

    return (inconsistenciesExist, inconsistentSegments)

  def getLabelRangeInCohort(self):

    return self.labelRangeInCohort

  def getTopologyString(self, nodeName, inputSegmentName):
    segmentName = str(inputSegmentName)
    topologyString = 'n/a'
    if nodeName in self.topologyDict and segmentName in self.topologyDict[nodeName]:
      topologyNum = self.topologyDict[nodeName][segmentName]
      if not topologyNum in self.TOPOLOGY_TYPES:
        topologyString = str(topologyNum) + ': '
        topologyString += self.TOPOLOGY_TYPES[self.TOPOLOGY_MULTIPLE_HOLES_TYPE]
      else:
        topologyString = self.TOPOLOGY_TYPES[topologyNum]
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
  #FreeSurfer tab functions
  #
  def initFreeSurferLUT(self,LUT_path):
    #import labels LUT
    numbers=['0','1','2','3','4','5','6','7','8','9']
    self.freesurfer_lut_dict=dict()
    with open(LUT_path,'r') as LUT:
      line = LUT.readline()
      while line:
        filtered_line=list(filter(None, line.split(' ')))
        if len(filtered_line)>0 and filtered_line[0][0] in numbers:
          color = [int(filtered_line[2])/255.0,int(filtered_line[3])/255.0,int(filtered_line[4])/255.0]
          self.freesurfer_lut_dict[filtered_line[0]]={'name':filtered_line[1],'color':color}
        line = LUT.readline()

  def getFreeSurferAvailableSegmentIds(self,template_path):
    #check available labels for ONE subject, 
    #we assume that there is a consistency across the analysable labels in the freesurfer pipeline
    #additional labels correspond to anomalies

    label_ids = [] 

    directory, fileName = os.path.split(template_path)
    labelMapNode = slicer.util.loadLabelVolume(template_path, returnNode=True)[1]

    if labelMapNode is None:
      logging.error('Failed to load ' + fileName + 'as a labelmap')
      # make sure each one is a labelmap
      return False

    labelMapNode.SetDisplayVisibility(False)
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", labelMapNode.GetName() + '_allSegments')
    segmentationLogic = slicer.modules.segmentations.logic()
    segmentationLogic.ImportLabelmapToSegmentationNode(labelMapNode,
                                                       segmentationNode)

    for segmentIndex in range(segmentationNode.GetSegmentation().GetNumberOfSegments()):
      segmentId = segmentationNode.GetSegmentation().GetNthSegmentID(segmentIndex)
      segmentName = segmentationNode.GetSegmentation().GetSegment(segmentId).GetName()

      label_id = segmentName.split('_')[1]

      label_ids.append(label_id)

    slicer.mrmlScene.RemoveNode(segmentationNode)
    slicer.mrmlScene.RemoveNode(labelMapNode)

    return label_ids

  #
  #Shape analysis structure
  #
  def generateShapeAnlaysisStructure(self,save_path):
    segmentationLogic = slicer.modules.segmentations.logic()

    for name,segmentation_node in self.segmentationDict.items():
      for segmentIndex in range(segmentation_node.GetSegmentation().GetNumberOfSegments()):
        segmentId = segmentation_node.GetSegmentation().GetNthSegmentID(segmentIndex)
        full_segmentName = segmentation_node.GetSegmentation().GetSegment(segmentId).GetName()
        segmentName = full_segmentName.split(' ')[-1]
        directory_path = os.path.join(save_path,segmentName)
        input_directory_path = os.path.join(directory_path,'input')
        output_directory_path = os.path.join(directory_path,'output')

        labelMap_filename = full_segmentName.replace(" ", "_")+'.nrrd'
        labelMap_filepath = os.path.join(input_directory_path,labelMap_filename)

        polydata_filename = full_segmentName.replace(" ", "_")+'.vtk'
        polydata_filepath = os.path.join(input_directory_path,polydata_filename)

        segmentIdList = vtk.vtkStringArray()
        segmentIdList.InsertNextValue(segmentId)

        #save label map
        exported_labelmap = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode", full_segmentName+' LabelMap')
        segmentationLogic.ExportSegmentsToLabelmapNode(segmentation_node,segmentIdList,exported_labelmap)
        slicer.util.saveNode(exported_labelmap, labelMap_filepath)
        slicer.mrmlScene.RemoveNode(exported_labelmap)

        #save Polydata
        exported_hierarchy = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelHierarchyNode", full_segmentName+' Model')
        segmentationLogic.ExportSegmentsToModelHierarchy(segmentation_node,segmentIdList,exported_hierarchy)
        collec = vtk.vtkCollection()
        exported_hierarchy.GetChildrenModelNodes(collec)
        exported_model = collec.GetItemAsObject(0)
        slicer.util.saveNode(exported_model, polydata_filepath)
        slicer.mrmlScene.RemoveNode(exported_hierarchy)
        slicer.mrmlScene.RemoveNode(exported_model)

        #create output directory
        if not os.path.isdir(output_directory_path):
          os.mkdir(output_directory_path)

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
    self.shape_analysis_folder=''
    self.filteredFilePathsList = list()

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    #
    #   Global variables
    #
    self.logic = DataImporterLogic()
    self.directoryPath = ''
    self.filteredFilePathsList = list()
    self.tableWidgetItemDefaultFlags = qt.Qt.NoItemFlags | qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled
    self.displayOnClick = True
    self.shape_analysis_folder=''

    # Table columns
    self.subjectsColumnName = 0
    self.subjectsColumnConsistency = 1
    # Note that these values change on initSegmentsTable/initSegmentsMultiTable
    self.segmentsColumnSubjectName = -1
    self.segmentsColumnSegmentName = 0
    self.segmentsColumnTopologyCurrent = 1
    self.segmentsColumnTopologyExpected = 2

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

    #Qtabwidget
    self.ImporterTypeTabWidget = self.getWidget('ImporterTypeTabWidget')
    self.ImporterTypeTabWidget.setCurrentIndex(1)
    self.ImporterTypeTabWidget.connect('currentChanged(int)',self.onCurrentTabChanged)
    self.ImporterTypeTabWidget.setCurrentIndex(0)

    #Browse Directory Button
    self.InputFolderNameLineEdit = self.getWidget('InputFolderNameLineEdit')
    self.FolderDirectoryButton = self.getWidget('FolderDirectoryButton')
    self.FolderDirectoryButton.connect('directoryChanged(QString)', self.onDirectoryChanged)

    #Browse CSV Button
    self.InputCSVFileNameLineEdit = self.getWidget('InputCSVFileNameLineEdit')
    self.CSVBrowseFilePushButton = self.getWidget('CSVBrowseFilePushButton')
    self.CSVBrowseFilePushButton.setIcon(qt.QApplication.style().standardIcon(qt.QStyle.SP_DirIcon))
    self.CSVBrowseFilePushButton.connect('clicked(bool)', self.onClickCSVBrowseFilePushButton)

    #FreeSurfer Tab
    self.freesurferFilesOfInterest=dict()
    self.freesurferFilesOfInterest['aseg']=os.path.normpath("mri/aseg.mgz")
    self.freesurferFilesOfInterest['aparc+aseg']=os.path.normpath("mri/aparc+aseg.mgz")
    self.freesurferFilesOfInterest['aparc.a2009s+aseg']=os.path.normpath("mri/aparc.a2009s+aseg.mgz")
    #home directory
    self.InputFreeSurferHomeFolderNameLineEdit = self.getWidget('InputFreeSurferHomeFolderNameLineEdit')
    self.FreeSurferBrowseHomeFolderPushButton = self.getWidget('FreeSurferBrowseHomeFolderPushButton')
    self.FreeSurferBrowseHomeFolderPushButton.connect('directoryChanged(QString)', self.onFreeSurferHomeDirectoryChanged)
    #subjects directory
    self.InputFreeSurferSubjectsFolderNameLineEdit = self.getWidget('InputFreeSurferSubjectsFolderNameLineEdit')
    self.FreeSurferBrowseSubjectsFolderPushButton = self.getWidget('FreeSurferBrowseSubjectsFolderPushButton')
    self.FreeSurferBrowseSubjectsFolderPushButton.connect('directoryChanged(QString)', self.onFreeSurferSubjectsDirectoryChanged)
    #File Select
    self.InputFreeSurferFileSelection = self.getWidget('InputFreeSurferFileSelection')
    self.InputFreeSurferFileSelection.connect('currentIndexChanged(QString)',self.onFreeSurferFileSelectionChanged)
    #FreeSurfer Subjects table
    self.InputFreeSurferSubjectsTable = self.getWidget('InputFreeSurferSubjectsTable')
    self.FreeSurferImportAllSubjectsOption = self.getWidget('FreeSurferImportAllSubjectsOption')
    self.FreeSurferImportAllSubjectsOption.stateChanged.connect(self.onStateChangedFreeSurferImportAllSubjectsOption)
    self.onStateChangedFreeSurferImportAllSubjectsOption_is_running=False
    #FreeSurfer Segments table
    self.InputFreeSurferSegmentsTable = self.getWidget('InputFreeSurferSegmentsTable')
    self.FreeSurferImportAllSegmentsOption = self.getWidget('FreeSurferImportAllSegmentsOption')
    self.FreeSurferImportAllSegmentsOption.stateChanged.connect(self.onStateChangedFreeSurferImportAllSegmentsOption)
    self.onStateChangedFreeSurferImportAllSegmentsOption_is_running=False
    #look for freesurfer default hme path and subjects path
    if ('FREESURFER_HOME' in os.environ.keys()):
      self.FreeSurfer_home_path = os.environ['FREESURFER_HOME']
      self.FreeSurferBrowseHomeFolderPushButton.directory=self.FreeSurfer_home_path
    if ('SUBJECTS_DIR' in os.environ.keys()):
      self.FreeSurfer_subjects_path = os.environ['SUBJECTS_DIR']
      self.FreeSurferBrowseSubjectsFolderPushButton.directory=self.FreeSurfer_subjects_path
    #populate the file combobox
    for file_name in self.freesurferFilesOfInterest.keys():
      self.InputFreeSurferFileSelection.addItem(file_name)


    self.ImportButton = self.getWidget('ImportButton')
    self.ImportButton.connect('clicked(bool)', self.onClickImportButton)
    self.DataInputTypeGroupBox = self.getWidget('DataInputTypeGroupBox')
    self.SubjectsTableWidget = self.getWidget('SubjectsTableWidget')
    self.SegmentsTableWidget = self.getWidget('SegmentsTableWidget')
    self.SaveCleanDataCheckBox = self.getWidget('checkBoxSaveCleanData')
    self.SaveCleanDataCheckBox.setChecked(True)
    self.SaveCleanDataCheckBox.connect('toggled(bool)', self.onSaveCleanDataCheckBoxToggled)

    self.SubjectsTableWidget.connect('cellClicked(int, int)', self.onSubjectsTableWidgetCellClicked)
    self.SegmentsTableWidget.connect('cellClicked(int, int)', self.onSegmentsTableWidgetCellClicked)

    self.DisplaySelectedPushButton = self.getWidget('DisplaySelectedPushButton')
    self.DisplaySelectedPushButton.connect('clicked(bool)', self.onClickDisplaySelectedPushButton)
    self.DisplayOnClickCheckBox = self.getWidget('DisplayOnClickCheckBox')
    self.DisplayOnClickCheckBox.connect('toggled(bool)', self.onDisplayOnClickCheckBoxToggled)
    # Set self.displayOnClick according to ui file
    self.onDisplayOnClickCheckBoxToggled()

    # Initialize the beginning input type.
    self.onSaveCleanDataCheckBoxToggled()


    #Shape Analysis Structure Generation
    self.InputShapeAnalysisFolderNameLineEdit = self.getWidget('InputShapeAnalysisFolderNameLineEdit')
    self.ShapeAnalysisFolderPushButton = self.getWidget('ShapeAnalysisFolderPushButton')
    self.ShapeAnalysisFolderPushButton.connect('directoryChanged(QString)', self.onShapeAnalysisFolderChanged)
    self.CreateShapeAnalysisStructurePushButton = self.getWidget('CreateShapeAnalysisStructurePushButton')
    self.CreateShapeAnalysisStructurePushButton.connect('clicked(bool)', self.onGenerateShapeAnalysisStructure)

  #
  # Reset all the data for data import
  #
  def cleanup(self):
    logging.debug('Cleaning up widget')
    self.resetFreeSurferSubjectsTable()
    self.resetFreeSurferSegmentsTable()
    self.resetSubjectsTable()
    self.resetSegmentsTable()
    self.resetGlobalVariables()

  def __del__(self):

    self.cleanup()

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
    self.resetSubjectsTable()
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
    self.SubjectsTableWidget.verticalHeader().setVisible(False)
    self.SubjectsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)

  def initSegmentsTable(self):
    """
    Set options and headers of SegmentsTable for the case of a single subject displayed.
    Does not require any other data structure populated.
    """
    self.resetSegmentsTable()
    self.segmentsColumnSubjectName = -1
    self.segmentsColumnSegmentName = 0
    self.segmentsColumnTopologyCurrent = 1
    self.segmentsColumnTopologyExpected = 2
    segmentNameColumnLabel = 'Segment Name'
    topologyCurrentColumnLabel = 'Current Segment Topology'
    topologyExpectedColumnLabel = 'Expected Cohort Topology'
    self.SegmentsTableWidget.setColumnCount(3)
    self.SegmentsTableWidget.setHorizontalHeaderLabels([
      segmentNameColumnLabel,
      topologyCurrentColumnLabel,
      topologyExpectedColumnLabel
    ])
    self.SegmentsTableWidget.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
    self.SegmentsTableWidget.verticalHeader().setVisible(False)
    self.SegmentsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)

  def initSegmentsMultiTable(self):
    """
    Set options and headers of SegmentsTable for the case of multiple subjects displayed.
    Does not require any other data structure populated.
    """
    self.resetSegmentsTable()
    self.segmentsColumnSubjectName = 0
    self.segmentsColumnSegmentName = 1
    self.segmentsColumnTopologyCurrent = 2
    self.segmentsColumnTopologyExpected = 3
    subjectNameColumnLabel = 'Subject'
    segmentNameColumnLabel = 'Segment'
    topologyCurrentColumnLabel = 'Current Segment Topology'
    topologyExpectedColumnLabel = 'Expected Cohort Topology'
    self.SegmentsTableWidget.setColumnCount(4)
    self.SegmentsTableWidget.setHorizontalHeaderLabels([
      subjectNameColumnLabel,
      segmentNameColumnLabel,
      topologyCurrentColumnLabel,
      topologyExpectedColumnLabel
    ])
    self.SegmentsTableWidget.horizontalHeader().setSectionResizeMode(qt.QHeaderView.Stretch)
    self.SegmentsTableWidget.verticalHeader().setVisible(False)
    self.SegmentsTableWidget.setSelectionBehavior(qt.QAbstractItemView.SelectRows)

  def resetSubjectsTable(self):
    if self.SubjectsTableWidget is not None:
      self.SubjectsTableWidget.setRowCount(0)

  def resetSegmentsTable(self):
    if self.SegmentsTableWidget is not None:
      self.SegmentsTableWidget.setRowCount(0)

  def getRowsFromSelectedIndexes(self, tableWidget):
    """ Return set with unique rows from selectedIndexes of input table. """
    currentSelectedIndexes = tableWidget.selectedIndexes()
    uniqueRowIndexes = set()
    for qModelIndex in currentSelectedIndexes:
      uniqueRowIndexes.add(qModelIndex.row())
    return list(uniqueRowIndexes)

  def populateSegmentsTableWithCurrentSubjectsSelection(self):
    uniqueRowIndexes = self.getRowsFromSelectedIndexes(self.SubjectsTableWidget)
    # Get Names from rows
    if len(uniqueRowIndexes) == 1:
      self.initSegmentsTable()
      name = self.SubjectsTableWidget.item(uniqueRowIndexes[0], self.subjectsColumnName).text()
      self.populateSegmentsTable(name)
      return 

    self.initSegmentsMultiTable()
    for row in uniqueRowIndexes:
      name = self.SubjectsTableWidget.item(row, self.subjectsColumnName).text()
      self.populateSegmentsMultiTable(name)

  def updateSubjectsTableConsistencyColumn(self):
    self.SubjectsTableWidget.setSortingEnabled(False)
    consistencyColumn = 1 
    rowCount = self.SubjectsTableWidget.rowCount
    if not rowCount:
      return
    inconsistenciesExist, inconsistentDict = self.logic.populateInconsistentTopologyDict()
    for row in range(0, rowCount):
      name = self.SubjectsTableWidget.item(row, 0).text()
      consistency = 'Consistent'
      countInconsistencies = 0
      if name in inconsistentDict:
        countInconsistencies = len(inconsistentDict[name])
      if countInconsistencies > 0:
        consistency = '# Inconsistencies: ' + str(countInconsistencies)
      self.SubjectsTableWidget.item(row, consistencyColumn).setText(consistency)


    #XXX is this the best place to trigger re-populate?
    self.resetSegmentsTable()
    self.populateSegmentsTableWithCurrentSubjectsSelection()
    self.SubjectsTableWidget.setSortingEnabled(True)

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
    # User can change self.logic.expectedTopologiesBySegment prior to call this function
    inconsistenciesExist, inconsistentDict = self.logic.populateInconsistentTopologyDict()
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
    POST: Populates SegmentsTable (appending) for given name.
    """
    if not self.logic.topologyDict:
      logging.error("Trying to populateSegmentsTable with non existant topologyDict.")
      return
    if not nameKey in self.logic.topologyDict:
      logging.error("Input nameKey: {} does not exist in topologyDict.".format(nameKey))
      return
    # Required to safely populate table when sorting is enabled, restored later.
    self.SegmentsTableWidget.setSortingEnabled(False)
    # Block signals while populating programatically
    self.SegmentsTableWidget.blockSignals(True)
    self.SegmentsTableWidget.hide()

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
      comboBox.connect('currentIndexChanged(int)', lambda index, name=segmentName: self.onSegmentTableWidgetComboBoxCurrentIndexChanged(index, name))
      self.SegmentsTableWidget.setCellWidget(rowPosition, topologyExpectedColumn, comboBox)


    # Restore sorting
    self.SegmentsTableWidget.setSortingEnabled(True)
    # Restore signals
    self.SegmentsTableWidget.blockSignals(False)
    self.SegmentsTableWidget.show()

  def populateSegmentsMultiTable(self, nameKey):
    """
    Given the name acting as first key for self.logic.topologyDict,
    populates the segment table for the subject with such a name.
    PRE: topologyDict has to have a key equal to input nameKey
    POST: Populates SegmentsTable (appending) for given name.
    The difference between this and populateSegmentsTable is that
    the table is populated differentely.
    """
    ### TODO: Merge both populateSegmentsXTable to avoid repetition.
    if not self.logic.topologyDict:
      logging.error("Trying to populateSegmentsMultiTable with non existant topologyDict.")
      return
    if not nameKey in self.logic.topologyDict:
      logging.error("Input nameKey: {} does not exist in topologyDict.".format(nameKey))
      return
    # Required to safely populate table when sorting is enabled, restored later.
    self.SegmentsTableWidget.setSortingEnabled(False)
    # Block signals while populating programatically
    self.SegmentsTableWidget.blockSignals(True)
    self.SegmentsTableWidget.hide()

    subjectNameColumn = 0
    segmentNameColumn = 1
    topologyCurrentColumn = 2
    topologyExpectedColumn = 3
    # cohortConsistencyColumn = 2
    for segmentName in self.logic.topologyDict[nameKey]:
      # Populate segmentName row
      rowPosition = self.SegmentsTableWidget.rowCount
      self.SegmentsTableWidget.insertRow(rowPosition)

      # subjectName
      subjectNameItem = qt.QTableWidgetItem(nameKey)
      subjectNameItem.setFlags(self.tableWidgetItemDefaultFlags)
      self.SegmentsTableWidget.setItem(rowPosition, subjectNameColumn, subjectNameItem )
      # segmentName
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
      comboBox.connect('currentIndexChanged(int)', lambda index, name=segmentName: self.onSegmentTableWidgetComboBoxCurrentIndexChanged(index, name))
      self.SegmentsTableWidget.setCellWidget(rowPosition, topologyExpectedColumn, comboBox)


    # Restore sorting
    self.SegmentsTableWidget.setSortingEnabled(True)
    # Restore signals
    self.SegmentsTableWidget.blockSignals(False)
    self.SegmentsTableWidget.show()

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
    self.onSubjectsTableWidgetCellClicked(0, 0)

  #freesurfer tab functions
  def resetFreeSurferSubjectsTable(self):
    if self.InputFreeSurferSubjectsTable is not None:
      self.InputFreeSurferSubjectsTable.setRowCount(0)

  def initFreeSurferSubjectsTable(self):
    self.resetFreeSurferSubjectsTable()
    self.freesurferSubjectImport = 0
    self.freesurferSubjectName = 1
    freesurferSubjectImportLabel = 'Import'
    freesurferSubjectLabel = 'Subject'
    self.InputFreeSurferSubjectsTable.setColumnCount(2)
    self.InputFreeSurferSubjectsTable.setHorizontalHeaderLabels([
      freesurferSubjectImportLabel,
      freesurferSubjectLabel
    ])
    self.InputFreeSurferSubjectsTable.verticalHeader().setVisible(False)
    self.InputFreeSurferSubjectsTable.setSortingEnabled(True)
    self.InputFreeSurferSubjectsTable.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
    #resize the columns nicely
    #pyQt5
    try:
      header = self.InputFreeSurferSubjectsTable.horizontalHeader()
      header.setSectionResizeMode(self.freesurferSubjectImport, qt.QHeaderView.ResizeToContents)   
      header.setSectionResizeMode(self.freesurferSubjectName, qt.QHeaderView.Stretch) 
    #pyQt4
    except:
      header = self.InputFreeSurferSubjectsTable.horizontalHeader()
      header.setResizeMode(self.freesurferSubjectImport, qt.QHeaderView.ResizeToContents)  
      header.setResizeMode(self.freesurferSubjectName, qt.QHeaderView.Stretch) 

  def addRowToFreeSurferSubjectsTable(self,subject_name,path):
    #create checkbox with a centered layout
    check_box = qt.QCheckBox()
    check_box.setChecked(False)
    check_box.stateChanged.connect(lambda state, x=path: self.onToggleFreeSurferSubjectSelection(x))

    container = qt.QWidget();
    layout = qt.QHBoxLayout(container);
    layout.addWidget(check_box);
    layout.setAlignment(qt.Qt.AlignCenter);
    layout.setContentsMargins(0,0,0,0);
    container.setLayout(layout);
    

    rowPosition = self.InputFreeSurferSubjectsTable.rowCount
    self.InputFreeSurferSubjectsTable.insertRow(rowPosition)
    self.InputFreeSurferSubjectsTable.setCellWidget(rowPosition , self.freesurferSubjectImport,container)
    self.InputFreeSurferSubjectsTable.setItem(rowPosition , self.freesurferSubjectName, qt.QTableWidgetItem(subject_name))

  def resetFreeSurferSegmentsTable(self):
    if self.InputFreeSurferSegmentsTable is not None:
      self.InputFreeSurferSegmentsTable.setRowCount(0)

  def initFreeSurferSegmentsTable(self):
    self.resetFreeSurferSegmentsTable()
    self.freesurferSegmentsImport = 0
    self.freesurferSegmentsName = 1
    freesurferSegmentsImportLabel = 'Import'
    freesurferSegmentsLabel = 'Segment'
    self.InputFreeSurferSegmentsTable.setColumnCount(2)
    self.InputFreeSurferSegmentsTable.setHorizontalHeaderLabels([
      freesurferSegmentsImportLabel,
      freesurferSegmentsLabel
    ])
    self.InputFreeSurferSegmentsTable.verticalHeader().setVisible(False)
    self.InputFreeSurferSegmentsTable.setSortingEnabled(True)
    self.InputFreeSurferSegmentsTable.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
    #resize the columns nicely
    #pyQt5
    try:
      header = self.InputFreeSurferSegmentsTable.horizontalHeader()
      header.setSectionResizeMode(self.freesurferSubjectImport, qt.QHeaderView.ResizeToContents)   
      header.setSectionResizeMode(self.freesurferSubjectName, qt.QHeaderView.Stretch) 
    #pyQt4
    except:
      header = self.InputFreeSurferSegmentsTable.horizontalHeader()
      header.setResizeMode(self.freesurferSubjectImport, qt.QHeaderView.ResizeToContents)  
      header.setResizeMode(self.freesurferSubjectName, qt.QHeaderView.Stretch) 

  def addRowToFreeSurferSegmentsTable(self,segment_name,label_id):
    #create checkbox with a centered layout
    check_box = qt.QCheckBox()
    check_box.setChecked(False)
    check_box.stateChanged.connect(lambda state, x=label_id: self.onToggleFreeSurferSegmentSelection(x))

    container = qt.QWidget();
    layout = qt.QHBoxLayout(container);
    layout.addWidget(check_box);
    layout.setAlignment(qt.Qt.AlignCenter);
    layout.setContentsMargins(0,0,0,0);
    container.setLayout(layout);
    

    rowPosition = self.InputFreeSurferSegmentsTable.rowCount
    self.InputFreeSurferSegmentsTable.insertRow(rowPosition)
    self.InputFreeSurferSegmentsTable.setCellWidget(rowPosition , self.freesurferSegmentsImport,container)
    self.InputFreeSurferSegmentsTable.setItem(rowPosition , self.freesurferSegmentsName, qt.QTableWidgetItem(segment_name))

  def uncheckFreeSurferTables(self):
    #uncheck subjects
    subject_number = self.InputFreeSurferSubjectsTable.rowCount
    for i_row in range(subject_number):
      self.InputFreeSurferSubjectsTable.cellWidget(i_row,0).children()[1].blockSignals(True)
      self.InputFreeSurferSubjectsTable.cellWidget(i_row,0).children()[1].setChecked(False)
      self.InputFreeSurferSubjectsTable.cellWidget(i_row,0).children()[1].blockSignals(False)

    #uncheck segments
    segment_number = self.InputFreeSurferSegmentsTable.rowCount
    for i_row in range(segment_number):
      self.InputFreeSurferSegmentsTable.cellWidget(i_row,0).children()[1].blockSignals(True)
      self.InputFreeSurferSegmentsTable.cellWidget(i_row,0).children()[1].setChecked(False)
      self.InputFreeSurferSegmentsTable.cellWidget(i_row,0).children()[1].blockSignals(False)
  
  def resetFreeSurferTab(self):
    self.logic.freesurfer_wanted_segments=[]
    self.uncheckFreeSurferTables()
  
  def resetCSVTab(self):
    #reset CSV tab
    self.InputCSVFileNameLineEdit.text=''

  def resetDirectoryTab(self):
    #reset directroy tab
    self.InputFolderNameLineEdit.text=''
    self.FolderDirectoryButton.blockSignals(True)
    self.FolderDirectoryButton.directory = '/'
    self.FolderDirectoryButton.blockSignals(False)
  '''
  GUI Callback functions
  '''
  #Shape Analysis Structure Generation
  def onShapeAnalysisFolderChanged(self,directoryPath):
    logging.debug("onShapeAnalysisFolderChanged: {}".format(directoryPath))
    # Create a list of files from the directory
    directory = qt.QDir(directoryPath)
    if not directory.exists():
      logging.error("Directory {} does not exist.".format(directory))
      return

    self.shape_analysis_folder = directoryPath
    self.InputShapeAnalysisFolderNameLineEdit.text = directoryPath

  def onGenerateShapeAnalysisStructure(self):
    logging.debug("onGenerateShapeAnalysisStructure")

    #check for imported data
    if len(self.logic.segmentationDict)==0:
      logging.error("Empty segmentation dictionary, import data before generating the Shape Analysis Structure.")
      return

    if self.shape_analysis_folder == '':
      logging.error("No Shape Analysis folder specified")
      return

    self.logic.generateShapeAnlaysisStructure(self.shape_analysis_folder)

    print('the shape analysis folder located at %s is ready' %(self.shape_analysis_folder))

  #resize tabs
  def onCurrentTabChanged(self,index):
    #resize tabs to fit minimal space
    for i in range(self.ImporterTypeTabWidget.count):
      if(i!=index):
        self.ImporterTypeTabWidget.widget(i).setSizePolicy(qt.QSizePolicy.Ignored, qt.QSizePolicy.Ignored);
    self.ImporterTypeTabWidget.widget(index).setSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Preferred);
    self.ImporterTypeTabWidget.widget(index).resize(self.ImporterTypeTabWidget.widget(index).minimumSizeHint);
    self.ImporterTypeTabWidget.widget(index).adjustSize();

    #empty import list
    self.filteredFilePathsList=[]
    #reset import option of other tabs
    tab_text=self.ImporterTypeTabWidget.tabText(index)
    if tab_text=='Import from FreeSurfer':
      self.logic.setFreeSurferimport(True)
      try:
        self.resetDirectoryTab()
        self.resetCSVTab()
      except:
        pass

    elif tab_text=='Import from CSV':
      self.logic.setFreeSurferimport(False)
      try:
        self.resetFreeSurferTab()
        self.resetDirectoryTab()
      except:
        pass

    elif tab_text=='Import from directory':
      self.logic.setFreeSurferimport(False)
      try:
        self.resetFreeSurferTab()
        self.resetCSVTab()
      except:
        pass

    else:
      try:
        self.logic.setFreeSurferimport(False)
        self.resetFreeSurferTab()
        self.resetDirectoryTab()
        self.resetCSVTab()
      except:
        pass

  #FreeSurfer UI Callbacks
  def onFreeSurferHomeDirectoryChanged(self, freesurfer_home_path):
    logging.debug("onFreeSurferHomeDirectoryChanged: {}".format(freesurfer_home_path))

    LUT_path = os.path.join(freesurfer_home_path,'FreeSurferColorLUT.txt')
    if not os.path.isfile(LUT_path):
      logging.error("Directory {} is not a valid FreeSurfer directory, impossible to find FreeSurferColorLUT.txt.".format(directory))
      return

    #Set directory variable and lineEdit
    self.freesurfer_home_path = freesurfer_home_path
    self.InputFreeSurferHomeFolderNameLineEdit.text = freesurfer_home_path

    #init the correspondance labels->segment names dict
    self.logic.initFreeSurferLUT(LUT_path)

  def onFreeSurferSubjectsDirectoryChanged(self, freesurfer_subjects_path):
    """
    Populates self.directoryPath and self.filteredFilePathsList
    containing a list of files contained in the directoryPath
    that can be used in this module.
    """
    logging.debug("onFreeSurferSubjectsDirectoryChanged: {}".format(freesurfer_subjects_path))
    #Check directory existance
    directory = qt.QDir(freesurfer_subjects_path)
    if not directory.exists():
      logging.error("Directory {} does not exist.".format(directory))
      return
    #Set directory variable and lineEdit
    self.freesurfer_subjects_path = freesurfer_subjects_path
    self.InputFreeSurferSubjectsFolderNameLineEdit.text = freesurfer_subjects_path



    #init subject list and segments list
    current_file=self.InputFreeSurferFileSelection.currentText
    if current_file != '':
      self.onFreeSurferFileSelectionChanged(current_file)

  def onFreeSurferFileSelectionChanged(self, file_name):
    self.filteredFilePathsList=[]

    self.initFreeSurferSubjectsTable()
    self.initFreeSurferSegmentsTable()
    if file_name == "":
      return

    subjects_path = self.freesurfer_subjects_path
    file_path = self.freesurferFilesOfInterest[file_name]

    for subject_name in os.listdir(subjects_path):
      subject_path=os.path.join(subjects_path,subject_name)

      if os.path.isdir(subject_path):
        abs_path=os.path.join(subject_path,file_path)
        if os.path.isfile(abs_path):
          template_path=abs_path
          self.addRowToFreeSurferSubjectsTable(subject_name,abs_path)

    label_ids = self.logic.getFreeSurferAvailableSegmentIds(template_path)
    self.logic.freesurfer_wanted_segments=[]

    #populate segments selection table
    for label_id in label_ids:
      segment_name=self.logic.freesurfer_lut_dict[label_id]['name']
      #segment_name=label_id
      self.addRowToFreeSurferSegmentsTable(segment_name,label_id)

  def onToggleFreeSurferSubjectSelection(self,path):
    if not self.onStateChangedFreeSurferImportAllSubjectsOption_is_running:
      self.FreeSurferImportAllSubjectsOption.blockSignals(True)
      self.FreeSurferImportAllSubjectsOption.setChecked(False)
      self.FreeSurferImportAllSubjectsOption.blockSignals(False)


    if path in self.filteredFilePathsList:
      index=self.filteredFilePathsList.index(path)
      self.filteredFilePathsList.pop(index)
    else:
      self.filteredFilePathsList.append(path)

    # for select_path in self.filteredFilePathsList:
    #   print(select_path)

  def onStateChangedFreeSurferImportAllSubjectsOption(self):
    self.onStateChangedFreeSurferImportAllSubjectsOption_is_running=True
    subject_number = self.InputFreeSurferSubjectsTable.rowCount

    for i_row in range(subject_number):
      if self.FreeSurferImportAllSubjectsOption.isChecked():
        self.InputFreeSurferSubjectsTable.cellWidget(i_row,0).children()[1].setChecked(True)
      else:
        self.InputFreeSurferSubjectsTable.cellWidget(i_row,0).children()[1].setChecked(False)
    self.onStateChangedFreeSurferImportAllSubjectsOption_is_running=False

  def onToggleFreeSurferSegmentSelection(self,label_id):
    if not self.onStateChangedFreeSurferImportAllSegmentsOption_is_running:
      self.FreeSurferImportAllSegmentsOption.blockSignals(True)
      self.FreeSurferImportAllSegmentsOption.setChecked(False)
      self.FreeSurferImportAllSegmentsOption.blockSignals(False)

    label_id='Label_'+label_id
    if label_id in self.logic.freesurfer_wanted_segments:
      index=self.logic.freesurfer_wanted_segments.index(label_id)
      self.logic.freesurfer_wanted_segments.pop(index)
    else:
      self.logic.freesurfer_wanted_segments.append(label_id)

  def onStateChangedFreeSurferImportAllSegmentsOption(self):
    self.onStateChangedFreeSurferImportAllSegmentsOption_is_running=True
    segment_number = self.InputFreeSurferSegmentsTable.rowCount

    for i_row in range(segment_number):
      if self.FreeSurferImportAllSegmentsOption.isChecked():
        self.InputFreeSurferSegmentsTable.cellWidget(i_row,0).children()[1].setChecked(True)
      else:
        self.InputFreeSurferSegmentsTable.cellWidget(i_row,0).children()[1].setChecked(False)
    self.onStateChangedFreeSurferImportAllSegmentsOption_is_running=False

 

  #
  #  Handle request to import data
  #
  def onClickImportButton(self):
    if not self.filteredFilePathsList:
      logging.warning('List of files is empty, choose a folder or a csv file to import first.')
      return

    if len(self.logic.segmentationDict) != 0:
      logging.warning('Importing new data will delete the previous import')

      if  slicer.util.confirmYesNoDisplay('Importing new data will delete the previous import,\ndo you want to import anyway?', windowTitle=None):
        self.logic.cleanup()
        self.resetSubjectsTable()
        self.resetSegmentsTable()

        
      else:
        logging.info("import aborted")
        return


    self.importFiles(self.filteredFilePathsList)

    #print(self.logic.polyDataDict)

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

  def onSubjectsTableWidgetCellClicked(self, row, column):
    """
    On click in Subjects table populates segment table, and optionally display indexes.
    """
    if self.SubjectsTableWidget.rowCount == 0:
      return

    self.populateSegmentsTableWithCurrentSubjectsSelection()

    if self.displayOnClick:
      self.displaySelectedIndexes()

  def onSegmentsTableWidgetCellClicked(self, row, column):
    """
    On click in Subjects, optionally display indexes.
    """
    if self.SegmentsTableWidget.rowCount == 0:
      return

    if self.displayOnClick:
      self.displaySelectedIndexes()

  def onSegmentTableWidgetComboBoxCurrentIndexChanged(self, index, name):
    # Change self.logic.expectTopologiesBySegment
    newTopology = self.logic.indexToTopologyType[index]
    logging.debug("SegmentTableWidgetComboBox changed. index: {}, name: {}, newTopology: {}.".format(index, name, newTopology))
    self.logic.expectedTopologiesBySegment[name] = newTopology
    # Update Consistency column in SubjectsTable
    self.updateSubjectsTableConsistencyColumn()
    
  def onSaveCleanDataCheckBoxToggled(self):

    self.logic.setSaveCleanData(self.SaveCleanDataCheckBox.isChecked())

  def onDisplayOnClickCheckBoxToggled(self):

    self.displayOnClick = self.DisplayOnClickCheckBox.isChecked()

  def onClickDisplaySelectedPushButton(self):

    self.displaySelectedIndexes()

  '''
  Supplemental functions to update the visualizations
  '''
  def center3dView(self):
    layoutManager = slicer.app.layoutManager()
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()

  def setVisibilitySegmentations(self, visibility):
    """ visiblity boolean """
    nodes = [node for node in self.logic.segmentationDict.values()]
    for node in nodes:
      displayNode = node.GetDisplayNode()
      displayNode.SetVisibility(visibility)
      displayNode.SetAllSegmentsVisibility(visibility)

  def hideAllSegmentations(self):

    self.setVisibilitySegmentations(False)

  def displaySelectedIndexes(self):
    self.SubjectsTableWidget.setSortingEnabled(False)
    self.SegmentsTableWidget.setSortingEnabled(False)
    self.hideAllSegmentations()
    # Get selection of both tables
    rowsSubjects = self.getRowsFromSelectedIndexes(self.SubjectsTableWidget)
    rowsSegments = self.getRowsFromSelectedIndexes(self.SegmentsTableWidget)
    countSubjects = len(rowsSubjects)
    countSegments = len(rowsSegments)
    if not countSubjects and not countSegments:
      pass

    # Update column indexes (sanity)
    segmentsColumnCount = self.SegmentsTableWidget.columnCount
    hasSegmentsColumnSubjectName = True if segmentsColumnCount == 4 else False
    if hasSegmentsColumnSubjectName:
      self.segmentsColumnSubjectName = 0
      self.segmentsColumnSegmentName = 1
      self.segmentsColumnTopologyCurrent = 2
      self.segmentsColumnTopologyExpected = 3
    else:
      self.segmentsColumnSubjectName = -1
      self.segmentsColumnSegmentName = 0
      self.segmentsColumnTopologyCurrent = 1
      self.segmentsColumnTopologyExpected = 2

    # segmentationNodes = list() 
    # segmentationNodes.append(node)
    for row in rowsSubjects: 
      subjectName = self.SubjectsTableWidget.item(row, self.subjectsColumnName).text()
      node = self.logic.segmentationDict[subjectName]
      segmentationDisplayNode = node.GetDisplayNode()
      segmentationDisplayNode.SetVisibility(True)
      if countSegments == 0:
        segmentationDisplayNode.SetAllSegmentsVisibility(True)
        self.center3dView()

    subjectName = None
    for row in rowsSegments: 
      if hasSegmentsColumnSubjectName:
        subjectName = self.SegmentsTableWidget.item(row, self.segmentsColumnSubjectName).text()
      else:
        if countSubjects: 
          subjectName = self.SubjectsTableWidget.item(rowsSubjects[0], self.subjectsColumnName).text()
        else:
          continue

      node = self.logic.segmentationDict[subjectName]
      segmentName = self.SegmentsTableWidget.item(row, self.segmentsColumnSegmentName).text()
      segmentId = node.GetSegmentation().GetSegmentIdBySegmentName(segmentName)
      segmentationDisplayNode = node.GetDisplayNode()
      segmentationDisplayNode.SetVisibility(True)
      segmentationDisplayNode.SetSegmentVisibility(segmentId, True)

    self.SubjectsTableWidget.setSortingEnabled(True)
    self.SegmentsTableWidget.setSortingEnabled(True)

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
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[logic.TOPOLOGY_STRIP_TYPE])

    segmentName = "2" # Sphere
    topologyString = logic.getTopologyString(fileName, segmentName)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[logic.TOPOLOGY_SPHERE_TYPE])

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
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[logic.TOPOLOGY_SPHERE_TYPE])

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
    segmentName = "1" # Sphere
    topologyString, consistentTopologyString = logic.getTopologyAndConsistencyString(fileName, segmentName)
    self.assertEqual(topologyString, logic.TOPOLOGY_TYPES[logic.TOPOLOGY_SPHERE_TYPE])
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

