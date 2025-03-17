# SurfacePlaneMapper User tutorial

Authors: Martin Styner\, Beatriz Paniagua 

Collaborators:

![](img/SlicerSALT-SPM-Tutorial_0.png)
![](img/SlicerSALT-SPM-Tutorial_1.png)
![](img/SlicerSALT-SPM-Tutorial_2.png)


## Surface Plane Mapper

SurfacePlaneMapper is a module to flatten a surface (such as brain surface or hippocampus) into a 2D image. 
This functionality allows us to utilize various deep learning architectures, such as ResNet and EfficientNet, which are commonly used for 2D image classification, with surface data.
This is implemented using a technique called Geometry image proposed by Gu et al. (https://hhoppe.com/gim.pdf) where geometry is resampled into a completely regular 2D grid.
The process involves cutting the surface into a disk using a network of cut paths, and then mapping the boundary of this disk to a square. 
Both geometry and other signals are stored as 2D grids, with grid samples in implicit correspondence. 

![](img/SlicerSALT-SPM-Tutorial_3.png)


## Input

![](img/SlicerSALT-SPM-Tutorial_4.png)


### Input Directory Structure

The module assumes that the input directory is organized in one of the following two manners:

#### Option 1: Features in `.txt` files

input_directory
| ---- subject_id
       | ---- session
              | ---- modality
                     | ---- *.txt

- The `.txt` files contain the features at each point on the surface.

#### Option 2: Features in `.vtk` files

input_directory
| ---- subject_id
       | ---- session
              | ---- *.vtk

### Sphere Template

- A `.vtk` or `.obj` file containing the icosahedron subdivision of the sphere where the surface is mapped.

## Output Directory Structure

The output directory where the results will be saved. The module will create a similar folder hierarchy as the input directory.

output_directory
| ---- subject_id
       | ---- session
              | ---- modality
                     | ---- *.png

- The results are saved in `.png` format. In the dimension you asked for.

