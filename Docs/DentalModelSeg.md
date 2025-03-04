<span style="color:#ffffff">SlicerDentalModelSeg</span>

<span style="color:#ffffff"> Automated teeth segmentation on Intra\-Oral Scans</span>

<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">Mathieu Leclercq\, Juan Carlos Prieto\, Martin Styner\, Connor Bowley\, Beatriz Paniagua </span>

<span style="color:#f2f2f2">September 2022</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_0.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_1.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_2.png)

_Intra\-Oral Scanners \(IOS\)_

<span style="color:#595959"> __IOS \(intra oral scanner\): __ </span>  <span style="color:#595959">A device that projects light to produce a 3D model of a lower or upper jaw</span>

<span style="color:#595959">Those 3D IOS scans are the inputs of our automated teeth segmentation method</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_3.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_4.png)

# Architecture of the algorithm

# Read 3D scan, apply random rotation and extract point features.

Capture 2D rendering from random viewpoints on a sphere, or viewpoints following an  icosahedron subdivision. Rendering is done with Pytorch3D.

The Pytorch3D rendering engine provides a map that relates pixels in the images to faces in the mesh and allows rapid extraction of point data (normals, curvatures, labels, etc).

Feed the 2D views to a neural network (UNET).

Put the information back into the 3D surface.

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_5.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_6.png)

# Teeth segmentation

<span style="color:#7f7f7f"> __Training__ </span>

<span style="color:#7f7f7f">Network: MONAI UNET \(Convolutional network used for medical image segmentation\) with residual connections\.</span>

<span style="color:#7f7f7f">Loss function: MONAI DiceCELoss\. Weighted sum of Dice and Cross\-Entropy loss\.</span>

<span style="color:#7f7f7f">Adam Optimizer\.</span>

<span style="color:#7f7f7f">Trained on approximately 1000 scans\.</span>

<span style="color:#7f7f7f">Use of the early\-stopping criteria to stop the training when the validation loss has stopped decreasing\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_7.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_8.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_9.png)

# Extension Overview

<span style="color:#7f7f7f">The extension consists of one module \(and its associated CLI module\):</span>

<span style="color:#7f7f7f"> __CrownSegmentation__ </span>  <span style="color:#7f7f7f">: GUI for dental crown segmentation\. The user has the option to use either </span>  <span style="color:#7f7f7f"> _[Universal Numbering System](https://en.wikipedia.org/wiki/Universal_Numbering_System)_ </span>  <span style="color:#7f7f7f"> or </span>  <span style="color:#7f7f7f"> _[FDI notation](https://en.wikipedia.org/wiki/FDI_World_Dental_Federation_notation)_ </span>  <span style="color:#7f7f7f">\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_10.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_11.png)

_SlicerJawSegmentation Installation on SlicerSALT_

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  _[SlicerSALT website ](http://salt.slicer.org)_  <span style="color:#595959">and install it\. </span>  <span style="color:#595959">The module </span>  <span style="color:#595959">will be ready to use then\. </span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_12.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_13.png)

<span style="color:#595959">Powered by Girder</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_14.png)

_JawSegmentation Installation on 3D Slicer_

<span style="color:#595959">  Download 3D Slicer packages for your respective operating system on the </span>  _[3D Slicer website ](http://www.slicer.org)_  <span style="color:#595959">and install it\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_15.png)

_SlicerJawSegmentation Installation on 3D Slicer_

<span style="color:#595959">  In 3D Slicer\, open the Extension Manager</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_16.png)

<span style="color:#366092">SlicerJawSegmentation Installation on 3D Slicer</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_17.png)

<span style="color:#7f7f7f">Search for </span>  <span style="color:#7f7f7f"> __SlicerJawSegmentation__ </span>  <span style="color:#7f7f7f"> in the </span>  <span style="color:#7f7f7f"> _Install Extensions_ </span>  <span style="color:#7f7f7f"> tab\.</span>

<span style="color:#7f7f7f">Click </span>  <span style="color:#7f7f7f"> _Install_ </span>  <span style="color:#7f7f7f">\.</span>

<span style="color:#7f7f7f">Slicer needs to </span>  <span style="color:#7f7f7f"> __restart__ </span>  <span style="color:#7f7f7f"> after installation\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_18.png)

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_19.png)

# CrownSegmentation Module

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_20.png)

# Inputs



* <span style="color:#7f7f7f"> __Input type\. IOS scan\(s\)\, either: __ </span>
  * <span style="color:#7f7f7f"> \.vtk file\.</span>
  * <span style="color:#7f7f7f">vtkMRMLModelNode of an IOS scan\.</span>
  * <span style="color:#7f7f7f">Folder containing IOS scans\. </span>
* <span style="color:#7f7f7f"> __Number of views:__ </span>  <span style="color:#7f7f7f"> this sets the number of 2D views used for one prediction\. A low number takes less time to compute\, but results can be inaccurate\. Generally 45 views is good\.</span>
* <span style="color:#7f7f7f"> __Model for segmentation: __ </span>  <span style="color:#7f7f7f">this is the path for the neural network model\. You can look for the latest version of the network on the github repo by clicking the corresponding button\.</span>


![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_21.png)

# Advanced

<span style="color:#7f7f7f"> __Resolution: __ </span>  <span style="color:#7f7f7f">This sets the resolution of the 2D views used for the prediction\.</span>  <span style="color:#7f7f7f"> __ __ </span>  <span style="color:#7f7f7f">Should stay at 320 unless the selected model explicitly works with another Resolution\.</span>

<span style="color:#7f7f7f"> __Name of the predicted labels: __ </span>  <span style="color:#7f7f7f">The name of the VTK array that stores the labels for each vertex in the output surface file\.</span>

<span style="color:#7f7f7f"> __Install/Check dependencies__ </span>  <span style="color:#7f7f7f">: This forces the installation of all dependencies\. You do not need to use this button as the module will automatically install all dependencies before the first prediction\.</span>

<span style="color:#7f7f7f"> __Create one output file for each label__ </span>  <span style="color:#7f7f7f">: Check this box if you want one separate output file for each tooth\.</span>

<span style="color:#7f7f7f">Numbering system: Choose between </span>  <span style="color:#7f7f7f"> _[Universal Numbering System](https://en.wikipedia.org/wiki/Universal_Numbering_System)_ </span>  <span style="color:#7f7f7f"> and </span>  <span style="color:#7f7f7f"> _[FDI notation](https://en.wikipedia.org/wiki/FDI_World_Dental_Federation_notation)_ </span>  <span style="color:#7f7f7f">\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_22.png)

# Outputs

<span style="color:#7f7f7f">Once prediction is over\, click </span>  <span style="color:#7f7f7f"> _open output surface _ </span>  <span style="color:#7f7f7f">to open the model in the scene\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_23.png)

<span style="color:#7f7f7f">Go to the </span>  <span style="color:#7f7f7f"> _Models_ </span>  <span style="color:#7f7f7f"> module to check the output\.</span>

<span style="color:#7f7f7f">The scalar for the prediction is turned on when you click "Open output surface"\.</span>

<span style="color:#7f7f7f">You can change the Color Table \(the random colors table can be useful to better distinguish close labels\)</span>

<span style="color:#7f7f7f">You can enable the Threshold to hide some labels\.</span>

![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_24.png)

<span style="color:#ffffff">Acknowledgements \-</span>

<span style="color:#ffffff"> Resources \- Questions</span>



* <span style="color:#ffffff">The S\-rep module developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.</span>
* <span style="color:#ffffff">Github repository: </span>
      * _[DentalModelSeg](https://github.com/DCBIA-OrthoLab/SlicerDentalModelSeg.git)_  <span style="color:#ffffff"> _ _ </span>
      * <span style="color:#0000ff"> _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_ </span>
      * <span style="color:#0000ff"> _[3D Slicer](https://github.com/Slicer/Slicer)_ </span>
* <span style="color:#ffffff">Forums:</span>
      * <span style="color:#0000ff"> _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_ </span>
      * <span style="color:#0000ff"> _[3D Slicer](https://discourse.slicer.org/)_ </span>
* <span style="color:#ffffff">For other remarks or questions\, please email: </span>
* _[beatriz\.paniagua@kitware\.com](mailto:beatriz.paniagua@kitware.com)_


![](img/SlicerSALT-SlicerDentalModelSeg-Tutorial_25.png)

