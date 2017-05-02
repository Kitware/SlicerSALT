import vtk, ctk, slicer
import logging
import os

#
# MRMLUtility
#
'''
This class harbors all the utility functions to save and remove mrml nodes
'''
class MRMLUtility(object):

    @staticmethod
    def loadMRMLNode(node_name, file_dir, file_name, file_type):
        node = slicer.util.getNode(node_name)
        if node is None:
            properties = {}
            file_path = os.path.join(file_dir, file_name)
            if file_type == 'LabelMap':
                file_type = 'VolumeFile'
                properties['labelmap'] = True
            node = slicer.util.loadNodeFromFile(file_path, file_type, properties, returnNode=True)
            node = node[1]
            if node is None:
                logging.error('!!! Failed to load: %s', file_path)
                return -1
            if file_type == 'MarkupsFiducials':
                node.SetLocked(1)
            node.SetName(node_name)
        return node

    @staticmethod
    def createNewMRMLNode(node_name, mrml_type, copy_node=None, transform=None):
        mrml_node = slicer.mrmlScene.CreateNodeByClass(mrml_type)
        if copy_node is not None:
            mrml_node.Copy(copy_node)
            if mrml_type is 'vtkMRMLModelNode':
                display_node = slicer.mrmlScene.CreateNodeByClass('vtkMRMLModelDisplayNode')
                slicer.mrmlScene.AddNode(display_node)
                display_node.UnRegister(slicer.mrmlScene)
                mrml_node.SetAndObserveDisplayNodeID(display_node.GetID())
                mrml_node.SetAndObserveStorageNodeID(None)
            elif mrml_type is 'vtkMRMLMarkupsFiducialNode':
                display_node = slicer.mrmlScene.CreateNodeByClass('vtkMRMLMarkupsDisplayNode')
                slicer.mrmlScene.AddNode(display_node)
                display_node.UnRegister(slicer.mrmlScene)
                mrml_node.SetAndObserveDisplayNodeID(display_node.GetID())
                mrml_node.SetAndObserveStorageNodeID(None)
                if transform is None:
                    print 'Transform is empty guys!'
        if transform is not None:
            mrml_node.ApplyTransform(transform)
        mrml_node.SetName(node_name)
        return mrml_node

    @staticmethod
    def getMRMLNode(node_name, mrml_type, copy_node=None, transform=None):
        mrml_node = slicer.util.getNode(node_name)
        if mrml_node is None:
            mrml_node = MRMLUtility.createNewMRMLNode(node_name, mrml_type, copy_node, transform)
            already_exists = False
        else:
            already_exists = True
        return (mrml_node, already_exists)

    @staticmethod
    def isMRMLNodeEmpty(mrml_node, mrml_type):
        node_empty = True
        if mrml_node is not None:
            if mrml_type == 'vtkMRMLModelNode':
                if mrml_node.GetPolyData() is not None:
                    node_empty = False
                    print "***", mrml_node.GetName(), "already has a polyData attribute"
            if mrml_type == 'vtkMRMLModelHierarchyNode':
                if mrml_node.GetNumberOfChildrenNodes() != 0:
                    node_empty = False
                    print "***", mrml_node.GetName(), "already has children models"
            elif mrml_type == 'vtkMRMLTransformNode' or mrml_type == 'vtkMRMLLinearTransformNode':
                if mrml_node.GetTransformToParent() is not None:
                    node_empty = False
                    print "***", mrml_node.GetName(), "already has a transform attribute"
            elif mrml_type == 'vtkMRMLScalarVolumeNode' or mrml_type == 'vtkMRMLLabelMapVolumeNode':
                if mrml_node.GetImageData() is not None:
                    node_empty = False
                    print "***", mrml_node.GetName(), "already has an image attribute"
        return node_empty

    @staticmethod
    def saveMRMLNodes(nodes, case_dir):
        for i in range(len(nodes)):
            MRMLUtility.saveMRMLNode(nodes[i], case_dir)

    @staticmethod
    def saveMRMLNode(node, case_dir):
        if slicer.util.getNode(node.GetName()):
            file_name = node.GetName().split("_")[0]
            class_name = node.GetClassName()
            if class_name == 'vtkMRMLScalarVolumeNode' or class_name == 'vtkMRMLLabelMapVolumeNode':
                file_name += '.nrrd'
            elif class_name == 'vtkMRMLModelNode':
                file_name += '.vtk'
            elif class_name == 'vtkMRMLLinearTransformNode' or class_name == 'vtkMRMLTransformNode':
                file_name += '.mat'
            elif class_name == 'vtkMRMLMarkupsFiducialNode':
                file_name += '.fcsv'
            elif class_name == 'vtkMRMLDoubleArrayNode':
                file_name += '.mcsv'
            file_path = os.path.join(case_dir, file_name)
            logging.info("Saving %s in %s", file_name, case_dir)
            slicer.util.saveNode(node, file_path)

    @staticmethod
    def removeMRMLNodes(nodes):
        for i in range(len(nodes)):
            MRMLUtility.removeMRMLNode(nodes[i])

    @staticmethod
    def removeMRMLNode(node):
        if slicer.util.getNode(node.GetName()):

            slicer.mrmlScene.RemoveNode(node)

            
