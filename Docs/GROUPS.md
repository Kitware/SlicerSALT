<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">Mahmoud Mostapha\, Ilwoo Lyu\, Martin Styner\, Beatriz Paniagua </span>

<span style="color:#f2f2f2">August 2018</span>

![](img/SlicerSALT-GROUPS-Tutorial_0.png)

![](img/SlicerSALT-GROUPS-Tutorial_1.png)

![](img/SlicerSALT-GROUPS-Tutorial_2.png)

GROUPS Tool Description

Step 1: Landmark\-based Rigid Alignment

Step 2: Group\-wise Shape Registration

<span style="color:#366092">Description of GROUPS</span>

<span style="color:#595959">Consistent shape correspondence is a prerequisite any group analysis investigating disease patterns and group variability</span>

<span style="color:#595959"> __Group\-wise Registration For Shape Correspondence \(GROUPS\) tool __ </span>  <span style="color:#595959">is a general framework for establishing correspondence of 3D models that employs group\-wise registration in a spherical parametrization space</span>

<span style="color:#595959">The inputs are spherical harmonics \(SPHARM\) point distribution models \(PDM\)  in addition to user\-defined geometrical features and landmarks\. The output is SPHARM\-PDM models with optimized correspondence obtained by minimizing the entropy of the joint distribution of features and landmarks at corresponding point locations</span>

<span style="color:#366092">Description of GROUPS</span>

<span style="color:#595959">The GROUPS tool consists of the following detailed steps: </span>

<span style="color:#595959"> _Inputs: Surface Meshs \+ Landmarks \+ Common Sphere_ </span>

<span style="color:#595959"> _Step 1 \(a\)_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Rigid Alignment __ </span>  <span style="color:#595959">uses RigidWrapper CLI</span>

<span style="color:#595959"> _Output: Rotated Parameterization Spheres _ </span>

<span style="color:#595959"> _Inputs: Surface Mesh \+ Parameterization Sphere \+ Common Sphere _ </span>

<span style="color:#595959"> _Step 1 \(b\)_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Surface Remeshing __ </span>  <span style="color:#595959">uses SurfRemesh CLI</span>

<span style="color:#595959"> _Output: Remeshed Surface _ </span>

<span style="color:#595959"> _Inputs: Surface Meshs \+ Parameterization Spheres \+ Surface Features \+ landmarks_ </span>

<span style="color:#595959"> _Step 2 \(a\)_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Group\-Wise Registration __ </span>  <span style="color:#595959">uses Groups CLI</span>

<span style="color:#595959"> _Output: Aligned SPHARM Coefficients _ </span>

<span style="color:#595959"> _Inputs: Surface Mesh \+ Parameterization Sphere \+ Common Sphere \+ SPHARM Coefficients _ </span>

<span style="color:#595959"> _Step 2_ </span>  <span style="color:#595959"> \(b\) : </span>  <span style="color:#595959"> __Surface Remeshing __ </span>  <span style="color:#595959">uses SurfRemesh CLI</span>

<span style="color:#595959"> _Output: Remeshed Surface _ </span>

<span style="color:#366092">Step 1 : Landmark\-based Rigid Alignment</span>

<span style="color:#595959">This step will:</span>

<span style="color:#595959">Improve the SPHARM\-PDM initial correspondence using a set of user placed landmarks</span>

<span style="color:#595959">Landmarks are defined in terms of 3D Slicer Fiducials \(\*\.fcsv\)</span>

<span style="color:#595959">Minimize the landmark distance errors on the sphere in terms of rigid alignment transformation</span>

<span style="color:#595959">Surfaces are Remeshed using rotated parametrization spheres</span>

![](img/SlicerSALT-GROUPS-Tutorial_3.jpg)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: \(a\) initial landmarks of the SPHARM\-PDM surfaces\, and \(b\) aligned landmarks after rigid transformation on the sphere</span>

<span style="color:#366092">Step 1 : Landmark\-based Rigid Alignment</span>

![](img/SlicerSALT-GROUPS-Tutorial_4.png)

<span style="color:#595959"> _Input: _ </span>  <span style="color:#595959">Surface Meshs </span>

<span style="color:#595959">RigidWrapper CLI</span>

![](img/SlicerSALT-GROUPS-Tutorial_5.png)

<span style="color:#595959"> _Output_ </span>  <span style="color:#595959"> __: __ </span>  <span style="color:#595959">Rotated Parameterization Spheres </span>

![](img/SlicerSALT-GROUPS-Tutorial_6.png)

<span style="color:#595959"> _Output_ </span>  <span style="color:#595959"> __: __ </span>  <span style="color:#595959">Remeshed Surface </span>

<span style="color:#366092">Step 1 : Landmark\-based Rigid Alignment</span>

![](img/SlicerSALT-GROUPS-Tutorial_7.png)

![](img/SlicerSALT-GROUPS-Tutorial_8.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: SPHARM\-PDM Meshs \(\*</span>  <span style="color:#595959"> _SPHARM\.vtk\) with user placed fiducals \(\*\.fcsv\) for each subject_ </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Common parametrization sphere obtained from the SPHARM\-PDM pipeline  \(\*</span>  <span style="color:#595959"> _surf\_para\.vtk\)_ </span>

<span style="color:#366092">Step 1 : Landmark\-based Rigid Alignment</span>

![](img/SlicerSALT-GROUPS-Tutorial_9.png)

![](img/SlicerSALT-GROUPS-Tutorial_10.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Remeshed Surface using SurfRemesh CLI</span>  <span style="color:#000000">               </span>  <span style="color:#595959">\(\* aligned\.vtk\)</span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Rotated parametrization sphere using RigidWrapper CLI \(\*</span>  <span style="color:#595959"> _rotSphere\.vtk\)_ </span>

<span style="color:#366092">Step 2: Group\-wise Shape Registration </span>

<span style="color:#595959">This step will:</span>

<span style="color:#595959">Further improve correspondence  using group\-wise registration in a spherical parametrization space</span>

<span style="color:#595959">Optimizing landmarks \(local\) and multidimensional features \(global\) by minimizing the joint entropy </span>

<span style="color:#595959">Features are pre\-computed by the user and saved in SPHARM vtk files as point data arrays</span>

<span style="color:#595959">Surfaces are Remeshed using aligned SPHARM coefficients </span>

![](img/SlicerSALT-GROUPS-Tutorial_11.jpg)

![](img/SlicerSALT-GROUPS-Tutorial_12.jpg)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: \(a\) landmarks after rigid transformation on the sphere\, and \(b\) final landmark alignment using group\-wise shape registration </span>

<span style="color:#366092">Step 2: Group\-wise Shape Registration </span>

![](img/SlicerSALT-GROUPS-Tutorial_13.png)

<span style="color:#595959"> _Input: _ </span>  <span style="color:#595959">Surface Meshs </span>

<span style="color:#595959">Groups </span>

<span style="color:#595959">\+ SurfRemesh CLIs</span>

![](img/SlicerSALT-GROUPS-Tutorial_14.png)

<span style="color:#595959"> _Output_ </span>  <span style="color:#595959"> __: __ </span>  <span style="color:#595959">Remeshed Surface </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Examples of geometrical features generated by the user and stored in the \(\*SPHARM\.vtk\) Surfaces as point data arrays\. \(a\) Curvedness generated using the SpharmTool in the SPHARM\-PDM pipeline</span>

<span style="color:#366092">Step 2 : Group\-wise Shape Registration </span>

![](img/SlicerSALT-GROUPS-Tutorial_15.png)

![](img/SlicerSALT-GROUPS-Tutorial_16.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Examples of geometrical features generated by the user and stored in the \(\*SPHARM\.vtk\) Surfaces as point data arrays\. \(a\) Curvedness generated using the SpharmTool in the SPHARM\-PDM pipeline\. \(b\) Partial radius \(thickness\) generated when medial mesh is generated in the SPHARM\-PDM pipeline If landmarks to be used\, the user need to save landmarks as binary array of the Vertex IDs saved as an array called “Landmarks”</span>

<span style="color:#366092">Step 2 : Group\-wise Shape Registration </span>

![](img/SlicerSALT-GROUPS-Tutorial_17.png)

![](img/SlicerSALT-GROUPS-Tutorial_18.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: \(a\) SPHARM deformation coefficients \(\*coeff\) produced by the Groups CLI\. \(b\) The input surface is then remeshed \(\*SPHARM\.vtk\) using SurfRemesh CLI</span>

Installation of GROUPS Tool



* GROUPS tool can be used with two open\-source software platforms:
      * __SlicerSALT__ : which is the dissemination vehicle of powerful shape analysis methodology\. This software is a light\-weight\, customized version of 3D Slicer\. It contains GROUPS  _as modules_
      * __3D Slicer__ : which is an open\-source and free software platform for medical image informatics\, image processing\, and three\-dimensional visualization\. GROUPS can be downloaded  _as an extension_


<span style="color:#366092">GROUPS Installation on SlicerSALT</span>

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  _[SlicerSALT website](http://salt.slicer.org/)_  <span style="color:#595959"> and install it\. </span>

![](img/SlicerSALT-GROUPS-Tutorial_19.png)

![](img/SlicerSALT-GROUPS-Tutorial_20.png)

<span style="color:#595959">Powered by Girder</span>

![](img/SlicerSALT-GROUPS-Tutorial_21.png)

<span style="color:#366092">GROUPS Installation on 3D Slicer</span>

<span style="color:#595959">  Download 3D Slicer packages for your respective operating system on the </span>  _[3D Slicer website](https://www.slicer.org/)_  <span style="color:#595959"> and install it</span>

![](img/SlicerSALT-GROUPS-Tutorial_22.png)

<span style="color:#366092">GROUPS Installation on 3D Slicer</span>

<span style="color:#595959">  In 3D Slicer\, open the Extension Manager</span>

![](img/SlicerSALT-GROUPS-Tutorial_23.png)

<span style="color:#366092">GROUPS Installation on 3D Slicer</span>

<span style="color:#595959"> In the </span>  <span style="color:#595959"> _Install Extension_ </span>  <span style="color:#595959"> tab\, select </span>  <span style="color:#595959"> _Shape Analysis_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>

<span style="color:#595959"> Under </span>  <span style="color:#595959"> __SPHARM\-PDM__ </span>  <span style="color:#595959">\, select the </span>  <span style="color:#595959"> _Install_ </span>  <span style="color:#595959"> button and restart Slicer when prompted   </span>

![](img/SlicerSALT-GROUPS-Tutorial_24.png)

![](img/SlicerSALT-GROUPS-Tutorial_25.png)

__GROUPS__

<span style="color:#7f7f7f">Mahmoud Mostapha </span>

<span style="color:#366092">GROUPS Installation on 3D Slicer</span>

<span style="color:#595959">For quality control\, we analyze our GROUPS outputs with </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> extension\. Shape Population Viewer can be installed as a 3D Slicer extension or as an external binary\. This module is included as part of the SlicerSALT package </span>

![](img/SlicerSALT-GROUPS-Tutorial_26.png)

<span style="color:#366092">GROUPS Installation on 3D Slicer</span>



* <span style="color:#595959">To install </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> as </span>  <span style="color:#595959"> _a 3D Slicer extension_ </span>  <span style="color:#595959">: </span>
    * <span style="color:#595959">Open </span>  <span style="color:#595959"> _Extension Manager_ </span>  <span style="color:#595959">\, in the </span>  <span style="color:#595959"> _Install Extensions _ </span>  <span style="color:#595959">tab\, select ‘</span>  <span style="color:#595959"> _Shape Analysis’_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>
    * <span style="color:#595959"> Select the appropriate </span>  <span style="color:#595959"> _Install _ </span>  <span style="color:#595959">button and restart 3D Slicer when prompted</span>


![](img/SlicerSALT-GROUPS-Tutorial_27.png)

<span style="color:#366092">GROUPS Installation on 3D Slicer</span>



* <span style="color:#595959">To install </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> as an </span>  <span style="color:#595959"> _external binary_ </span>  <span style="color:#595959">: </span>
    * <span style="color:#595959"> Download ShapePopulationViewer package for your respective operating system on </span>  _[NITRC website](https://www.nitrc.org/projects/shapepopviewer/)_
    * <span style="color:#595959"> In 3D Slicer\, open </span>  <span style="color:#595959"> _Application Settings _ </span>  <span style="color:#595959">in the </span>  <span style="color:#595959"> _Edit _ </span>  <span style="color:#595959">Menu\.  On the tab </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959">\, </span>  <span style="color:#595959"> __Add __ </span>  <span style="color:#595959">the folder where  ShapePopulationViewer is stored</span>
    * <span style="color:#595959"> Restart 3D Slicer</span>


![](img/SlicerSALT-GROUPS-Tutorial_28.png)

Rigid Alignment Use



  * Rigid Alignment tool can be used by two different ways:
      * As  __command\-line__   __tool__  through the terminal thanks to SlicerSALT
      * As a  __module__  of SlicerSALT or 3D Slicer


<span style="color:#366092">Rigid Alignment Command\-Line Tool</span>



* <span style="color:#595959">Rigid Alignment method can be run on several cases through a terminal thanks to two files included in the SlicerSALT package: </span>
* <span style="color:#595959">RigidAlignment\-parameters\.ini which allows the user to specify the inputs\, outputs and the parameters of the RigidAlignment tool</span>
* <span style="color:#595959">RigidAlignment\.py python script which will apply RigidAlignment method on the given input cases with the parameters specified in the RigidAlignment\-parameters\.ini file</span>
* <span style="color:#595959"> _RigidAlignment\.py_ </span>  <span style="color:#595959"> and </span>  <span style="color:#595959"> _RigidAlignment\-parameters\.ini files location: _ </span>
  * <span style="color:#595959"> _On Linux and Windows: share/Slicer\-4\.7/CommandLineTool_ </span>
  * <span style="color:#595959"> _On MacOs: Open the SlicerSALT Contents 			 _ </span>
  * <span style="color:#595959"> _🡪 Contents/share/Slicer\-4\.7/CommandLineTool_ </span>


![](img/SlicerSALT-GROUPS-Tutorial_29.png)

<span style="color:#366092">Rigid Alignment Command\-Line Tool</span>



* <span style="color:#595959"> __Step 1__ </span>  <span style="color:#595959">: Modification of the </span>  <span style="color:#595959"> _RigidAlignment\-parameters\.ini_ </span>  <span style="color:#595959"> file by specifying the </span>  <span style="color:#595959"> __directories __ </span>  <span style="color:#595959">needed for tool CLIs</span>
* <span style="color:#595959"> __Step 2__ </span>  <span style="color:#595959">: Launch Rigid Alignment  method with the following command\-lines: </span>
* <span style="color:#595959">On Linux and Windows: </span>
  * <span style="color:#595959"> _$cd path\-to\-the\-SlicerSALT\-package_ </span>
  * <span style="color:#595959"> _$\./SlicerSALT \-\-no\-main\-window \-\-python\-script share/Slicer\-4\.7/CommandLineTool/RigidAlignment\.py   share/Slicer\-4\.7/CommandLineTool/RigidAlignment\-parameters\.ini_ </span>
* <span style="color:#595959">On MacOs: </span>
  * <span style="color:#595959"> _$cd path\-to\-the\-SlicerSALT\-package/SlicerSALT\.app/Contents/MacOS_ </span>
  * <span style="color:#595959"> _$\./SlicerSALT \-\-no\-main\-window \-\-python\-script \.\./share/Slicer\-4\.7/CommandLineTool/RigidAlignment\.py \.\./share/Slicer\-4\.7/CommandLineTool/RigidAlignment\-parameters\.ini_ </span>


<span style="color:#366092">Rigid Alignment Module </span>

<span style="color:#595959">In 3D Slicer or in SlicerSALT\, select </span>  <span style="color:#595959"> _Rigid Alignment Module _ </span>

<span style="color:#595959">from the </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959"> drop\-down menu \(</span>  <span style="color:#595959"> _Category:_ </span>  <span style="color:#595959"> Shape Analysis\) or on the Search bar </span>

![](img/SlicerSALT-GROUPS-Tutorial_30.png)

<span style="color:#366092">Setting up Input Directories</span>

<span style="color:#595959"> __RigidAlignment tab__ </span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Models Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the folder which contains the input surface meshs \(\*\.vtk\)</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Fiducial Files Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> select the folder where the landmarks \(fiducials\) files are stored \(\*\.fcsv\)</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Common Unit Sphere_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> select the folder where the common parametrization sphere is stored \(\*\.vtk\)</span>

![](img/SlicerSALT-GROUPS-Tutorial_31.png)

<span style="color:#366092">Setting up Output Directories</span>

<span style="color:#595959"> __RigidAlignment tab__ </span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Output Spherical Models Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the folder where the output of the RigidWrapper CLI will be stored \(\*\.vtk\)</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Output Models Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> select the folder where the output of the SurfRemesh CLI will be stored \(\*\.vtk\)</span>

![](img/SlicerSALT-GROUPS-Tutorial_32.png)

<span style="color:#366092">Running Rigid Alignment Module </span>

![](img/SlicerSALT-GROUPS-Tutorial_33.png)

<span style="color:#595959">Click on the </span>

<span style="color:#595959"> _Run_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959"> _RigidAlignment _ </span>  <span style="color:#595959">button\, to run the CLIs on the provided inputs</span>

<span style="color:#366092">Running Rigid Alignment Module </span>

<span style="color:#595959">Shape Population Viewer will pop up to preview the input meshes giving the user the chance to inspect the input data before running the tool</span>

![](img/SlicerSALT-GROUPS-Tutorial_34.jpg)

<span style="color:#366092">Running Rigid Alignment Module </span>

<span style="color:#595959">Shape Population Viewer will pop up also after the module finished processing giving the user the chance to check the remeshed surfaces</span>

![](img/SlicerSALT-GROUPS-Tutorial_35.jpg)

<span style="color:#595959"> _3D Slicer’s Error Log_ </span>  <span style="color:#595959"> can also be used for debugging if the module was completed with errors\. To open it\, click on the red icon at the bottom right\. </span>

![](img/SlicerSALT-GROUPS-Tutorial_36.png)

<span style="color:#595959"> _3D Slicer’s Error Log_ </span>  <span style="color:#595959"> can also be used for debugging if the module was completed with errors\. To open it\, click on the red icon at the bottom right\. </span>

![](img/SlicerSALT-GROUPS-Tutorial_37.png)

<span style="color:#595959">The outputs files for the two sub\-steps of Rigid Alignment Module  are stored in the two folders specified by the user: </span>

![](img/SlicerSALT-GROUPS-Tutorial_38.png)

![](img/SlicerSALT-GROUPS-Tutorial_39.png)

![](img/SlicerSALT-GROUPS-Tutorial_40.png)

<span style="color:#ffffff">Group\-wise Registration Use</span>



  * Group\-wise Registration  <span style="color:#ffffff">tool can be used by two different ways: </span>
      * <span style="color:#ffffff">As </span>  <span style="color:#ffffff"> __command\-line__ </span>  <span style="color:#ffffff"> </span>  <span style="color:#ffffff"> __tool__ </span>  <span style="color:#ffffff"> through the terminal thanks to SlicerSALT</span>
      * <span style="color:#ffffff">As a </span>  <span style="color:#ffffff"> __module__ </span>  <span style="color:#ffffff"> of SlicerSALT or 3DSlicer</span>


<span style="color:#366092">Group\-wise Registration Command\-Line Tool</span>



* <span style="color:#595959">Group\-wise Registration method can be run on several cases through a terminal thanks to two files included in the SlicerSALT package: </span>
* <span style="color:#595959">GroupWiseRegistration\-parameters\.ini which allows the user to specify the inputs\, outputs and the parameters of the Group\-wise Registration tool</span>
* <span style="color:#595959">GroupWiseRegistration\.py python script which will apply GroupWiseRegistration method on the given input cases with the parameters specified in the GroupWiseRegistration \-parameters\.ini file</span>
* <span style="color:#595959"> _GroupWiseRegistration\.py_ </span>  <span style="color:#595959"> and </span>  <span style="color:#595959"> _GroupWiseRegistration \-parameters\.ini files location: _ </span>
  * <span style="color:#595959"> _On Linux and Windows: share/Slicer\-4\.7/CommandLineTool_ </span>
  * <span style="color:#595959"> _On MacOs: Open the SlicerSALT Contents 			 _ </span>
  * <span style="color:#595959"> _🡪 Contents/share/Slicer\-4\.7/CommandLineTool_ </span>


![](img/SlicerSALT-GROUPS-Tutorial_41.png)

<span style="color:#366092">Group\-wise Registration Command\-Line Tool</span>



* <span style="color:#595959"> __Step 1__ </span>  <span style="color:#595959">: Modification of the </span>  <span style="color:#595959"> _GroupWiseRegistration\-parameters\.ini_ </span>  <span style="color:#595959"> file by specifying the </span>  <span style="color:#595959"> __directories and parameters __ </span>  <span style="color:#595959">needed for tool CLIs</span>
* <span style="color:#595959"> __Step 2__ </span>  <span style="color:#595959">: Launch Group Wise Registration method with the following command\-lines: </span>
* <span style="color:#595959">On Linux and Windows: </span>
  * <span style="color:#595959"> _$cd path\-to\-the\-SlicerSALT\-package_ </span>
  * <span style="color:#595959"> _$\./SlicerSALT \-\-no\-main\-window \-\-python\-script share/Slicer\-4\.7/CommandLineTool/GroupWiseRegistration\.py   share/Slicer\-4\.7/CommandLineTool/GroupWiseRegistration\-parameters\.ini_ </span>
* <span style="color:#595959">On MacOs: </span>
  * <span style="color:#595959"> _$cd path\-to\-the\-SlicerSALT\-package/SlicerSALT\.app/Contents/MacOS_ </span>
  * <span style="color:#595959"> _$\./SlicerSALT \-\-no\-main\-window \-\-python\-script \.\./share/Slicer\-4\.7/CommandLineTool/GroupWiseRegistration\.py \.\./share/Slicer\-4\.7/CommandLineTool/GroupWiseRegistration\-parameters\.ini_ </span>


<span style="color:#366092">Group\-wise Registration Module </span>

<span style="color:#595959">In 3D Slicer or in SlicerSALT\, select </span>  <span style="color:#595959"> _Group\-wise Registration Module _ </span>  <span style="color:#595959">from the </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959"> drop\-down menu \(</span>  <span style="color:#595959"> _Category:_ </span>  <span style="color:#595959"> Shape Analysis\) or on the Search bar </span>

![](img/SlicerSALT-GROUPS-Tutorial_42.png)

<span style="color:#366092">Setting up Input Directories</span>

<span style="color:#595959"> __Groups tab__ </span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Models Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the folder which contains the input surface meshs \(\*SPHARM\.vtk\)</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Spherical Models Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> select the folder where the spherical parametrization files are stored \(\*\_para\.vtk\)</span>

![](img/SlicerSALT-GROUPS-Tutorial_43.png)

<span style="color:#366092">Setting up Output Directories</span>

<span style="color:#595959"> __Groups tab__ </span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Output Coefficents Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the folder where the output of the Groups CLI will be stored \(\*\.Coeff\)</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Output Models Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> select the folder where the output of the SurfRemesh CLI will be stored \(\*\.vtk\)</span>

![](img/SlicerSALT-GROUPS-Tutorial_44.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> __Groups Parameters tab__ </span>

<span style="color:#595959">Once the user specify the input models directory\, the geometrical features/prosperities stored in the vtk files are dynamically populated into a list where the user can select what features to include \(Weight >0\)</span>

![](img/SlicerSALT-GROUPS-Tutorial_45.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> __Groups Parameters tab__ </span>

<span style="color:#595959">Enable Use of Landmarks: Option for the user to select if landmarks will be included in improving the correspondence</span>

<span style="color:#595959"> If enabled\, the user need to store the landmarks as a point data array called “Landmarks” indicating Vertex IDs to be selected \(Value > 0\)</span>

![](img/SlicerSALT-GROUPS-Tutorial_46.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: </span>  <span style="color:#595959"> _Example of Landmarks stored in \*SPHARM\.vtk files _ </span>

![](img/SlicerSALT-GROUPS-Tutorial_47.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> __Groups Parameters tab__ </span>

<span style="color:#595959">Degree of SPHARM Decomposition: Degree value represents the degree of the spherical harmonic decomposition used to represent the computed deformation field</span>

<span style="color:#595959">Changing this value results in different levels of detail of the deformation field that will be used to transform the input SPHARM mesh </span>

![](img/SlicerSALT-GROUPS-Tutorial_48.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> __Groups Parameters tab__ </span>

<span style="color:#595959">Maximum Number of Iterations: Number of iterations before the energy minimization optimization stops</span>

<span style="color:#595959"> A higher number of iterations usually needed with increasing the number of subjects sin the dataset\, number of properties selected for the optimization procedure\, or with higher deformation field SPHARM degree</span>

![](img/SlicerSALT-GROUPS-Tutorial_49.png)

<span style="color:#366092">Running Group\-wise Registration Module </span>

![](img/SlicerSALT-GROUPS-Tutorial_50.png)

<span style="color:#595959">Click on the </span>

<span style="color:#595959"> _Run_ </span>  <span style="color:#595959"> _  _ </span>  <span style="color:#595959"> _Groups  _ </span>  <span style="color:#595959">button\, </span>

<span style="color:#595959">to run the CLIs on the provided inputs</span>

<span style="color:#366092">Running Group\-wise Registration Module </span>

<span style="color:#595959">Shape Population Viewer will be used again for quality control of the input meshs before running the tool\, in particular\, features planned to be included should be inspected by the user carefully </span>

![](img/SlicerSALT-GROUPS-Tutorial_51.jpg)

<span style="color:#366092">Running Group\-wise Registration Module </span>

<span style="color:#595959">Also\, Shape Population Viewer will be used to inspect the final correspondence established by the Group\-wise Registration tool</span>

![](img/SlicerSALT-GROUPS-Tutorial_52.jpg)

<span style="color:#595959"> _3D Slicer’s Error Log_ </span>  <span style="color:#595959"> can also be used for debugging if the module was completed with errors\. To open it\, click on the red icon at the bottom right\. </span>

![](img/SlicerSALT-GROUPS-Tutorial_53.png)

<span style="color:#595959">The outputs files for the two sub\-steps of Group\-wise Registration Module  are stored in the two folders specified by the user: </span>

![](img/SlicerSALT-GROUPS-Tutorial_54.png)

![](img/SlicerSALT-GROUPS-Tutorial_55.png)

![](img/SlicerSALT-GROUPS-Tutorial_56.png)

Acknowledgements \- Resources \- Questions



* The GROUPS developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.
* Github repository:
      * _[Groups](https://github.com/NIRALUser/GROUPS)_  _ _
      * _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_
      * _[3D Slicer](https://github.com/Slicer/Slicer)_
* Forums:
      * _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_
      * _[3D Slicer](https://discourse.slicer.org/)_
* Papers:
      * _[Robust estimation of group\-wise cortical correspondence with an  application to macaque and human neuroimaging studies](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4462677/)_
      * _[Group\-wise shape correspondence of variable and complex objects ](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/10574/105742T/Group-wise-shape-correspondence-of-variable-and-complex-objects/10.1117/12.2293273.full?SSO=1)_
* For other remarks or questions\, please email:
* beatriz\.paniagua@kitware\.com


![](img/SlicerSALT-GROUPS-Tutorial_57.png)

