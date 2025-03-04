<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">Laura Pascal\, Jonathan Perdomo\, Martin Styner\, Hina Shah\, Beatriz Paniagua </span>

<span style="color:#f2f2f2">May 2017</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_0.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_1.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_2.png)

SPHARM\-PDM Tool Description

Step 1: Post Process Segmentation

Step 2: Generate Mesh Parameters

Step 3: Parameters to SPHARM Mesh

<span style="color:#366092">Description of SPHARM\-PDM</span>

<span style="color:#595959">Shape Analysis allows to precisely locate morphological changes between healthy and pathological structures\.</span>

<span style="color:#595959"> __Spherical Harmonic Representation Point Distribution Models \(SPHARM\-PDM\) tool __ </span>  <span style="color:#595959">is used to compute densely sampled correspondent point based models that allow performing 3D structural statistical shape analysis\.</span>

<span style="color:#595959">The inputs are </span>  <span style="color:#595959"> _binary segmentations_ </span>  <span style="color:#595959"> which are converted into corresponding </span>  <span style="color:#595959"> _spherical harmonic descriptions_ </span>  <span style="color:#595959"> \(SPHARM\) and then are sampled into </span>  <span style="color:#595959"> _triangulated surfaces_ </span>  <span style="color:#595959"> \(PDM\) </span>

<span style="color:#366092">Description of SPHARM\-PDM</span>

<span style="color:#595959">The SPHARM\-PDM tool consists on three steps: </span>

<span style="color:#595959"> _Input: Binary Segmentation_ </span>

<span style="color:#595959"> _Step 1_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Preprocessing__ </span>  <span style="color:#595959"> uses SegPostProcess CLI</span>

<span style="color:#595959"> _Output: Binary 3D Image _ </span>

<span style="color:#595959"> _Step 2_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Parameterization__ </span>  <span style="color:#595959"> uses GenParaMesh CLI</span>

<span style="color:#595959"> _Output: Surface Mesh \+ Parameterization sphere _ </span>

<span style="color:#595959"> _Step 3_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __SPHARM\-PDM__ </span>  <span style="color:#595959"> uses ParaToSPHARMMesh CLI</span>

<span style="color:#595959"> _Output: SPHARM Coefficients \+ Aligned Surface Meshes _ </span>

<span style="color:#366092">Step 1: Post Process Segmentation </span>

<span style="color:#595959">This step will:</span>

<span style="color:#595959">Ensure spherical topology of the segmentations by filling any interior holes and by applying two smoothing operations</span>

<span style="color:#595959">Extract a single label or a label range</span>

<span style="color:#595959">Re\-sample the label data to ensure an isotropic resolution and a relative fine resolution</span>  <span style="color:#595959"> </span>

<span style="color:#595959"> _Input_ </span>  <span style="color:#595959">: Binary Segmentation </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_3.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_4.png)

<span style="color:#595959"> _Output_ </span>  <span style="color:#595959">: Binary Segmentation  File: </span>  <span style="color:#595959"> _\*pp_ </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Input/Output of SegPostProcess CLI</span>

<span style="color:#366092">Step 2: Generate Mesh Parameters</span>

<span style="color:#595959">This step will: </span>

<span style="color:#595959"> </span>  <span style="color:#595959">Extract the surface of the input label segmentation</span>

<span style="color:#595959"> Create an area conforming mapping of the surface mesh to a unit sphere</span>

<span style="color:#595959"> _Note_ </span>  <span style="color:#595959">: If this step reports bad  Euler number\, it will mean that the extracted surface is not a spherical topology\. spherical topology has an Euler number of 2\.</span>

<span style="color:#595959"> _Input_ </span>  <span style="color:#595959">: Binary 3D Image File </span>  <span style="color:#595959"> _\*pp_ </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_5.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_6.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_7.png)

<span style="color:#595959"> _Outputs_ </span>  <span style="color:#595959">: Parametrization sphere \+ Surface Mesh</span>  <span style="color:#595959">Files: </span>  <span style="color:#595959"> _\*para\.vtk _ </span>  <span style="color:#595959">\+ </span>  <span style="color:#595959"> _\*surf\.vtk_ </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Input/Output of GenParaMesh CLI</span>

<span style="color:#366092">Step 2: Generate Mesh Parameters</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_8.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: </span>  <span style="color:#595959"> __\*surf\.vtk__ </span>  <span style="color:#595959"> is a surface approximation of the input file which represents the original voxel mesh: the cubes show the voxel delineation\. The surface will appear blocky because of it is the result of a marching cubes algorithm\.</span>  <span style="color:#595959">   </span>

<span style="color:#366092">Step 2: Generate Mesh Parameters</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_9.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: </span>  <span style="color:#595959"> __\*para\.vtk__ </span>  <span style="color:#595959"> is a the  spherical mapping of the \*surf\.vtk file\. The sphere is an unit sphere \(diameter = 1\)</span>

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>



* <span style="color:#595959">This</span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">step will: </span>
* <span style="color:#595959">Compute the SPHARM\-PDM representation</span>
    * <span style="color:#595959">Compute the spherical harmonic description</span>
    * <span style="color:#595959">Sample into a triangulated surface</span>
    * <span style="color:#595959">The two main parameters for this step are: </span>
        * <span style="color:#595959">The degree for SPHARM computation </span>
        * <span style="color:#595959">The subdivision level for the icosahedron subdivision</span>
* <span style="color:#595959">Resolves issues of correspondence pose and alignment</span>


<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Input/Output of ParaToSPHARMMesh CLI</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_10.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_11.png)

<span style="color:#366092">ParaToSPHARMMesh</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_12.png)

<span style="color:#595959">Spherical mapping</span>

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Comparison between the surface mesh generated by the Generate Mesh Parameters step \(red\) and the SPHARM\-PDM output \*</span>  <span style="color:#595959"> _SPHARM\.vtk_ </span>  <span style="color:#595959"> \(blue\): </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_13.png)

<span style="color:#595959"> _Note_ </span>  <span style="color:#595959">: This figure shows how the final correspondent PDM represents the geometry of the structure without fitting the voxel mesh obtained from the binary segmentation</span>

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Visualization of </span>  <span style="color:#595959"> _\*SPHARMMedialAxis\.vtk _ </span>  <span style="color:#595959">\(red\) </span>  <span style="color:#595959">and </span>  <span style="color:#595959"> _\*SPHARMMedialMesh\.vtk_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">\(blue\): </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_14.png)

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_15.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: </span>  <span style="color:#595959"> __\*para\.vtk __ </span>  <span style="color:#595959">is a sphere with a icosahedron subdivision of 10\. </span>

<span style="color:#595959"> _Note: _ </span>  <span style="color:#595959">The sphere has 1002 points and the triangulated surface generated will have the same number of points that this sphere\. This file includes the spherical parameters \(</span>  <span style="color:#595959">φ\,θ</span>  <span style="color:#595959">\) at each point\.</span>

<span style="color:#595959">This sphere is also a unit sphere \(diameter = 1\)</span>

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Visualization of </span>  <span style="color:#595959"> _\*para\.vtk _ </span>  <span style="color:#595959">\(blue\)</span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">and </span>  <span style="color:#595959"> _\*SPHARM\_Ellalign\.vtk _ </span>  <span style="color:#595959">\(red\) </span>  <span style="color:#595959">which is aligned with the \*para\.vtk sphere:    </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_16.png)

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

<span style="color:#595959">Spherical parameters color map files</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_17.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Comparison of the spherical parameters color maps containing in the </span>  <span style="color:#595959"> _\*SPHARM\.vtk _ </span>  <span style="color:#595959">in ShapePopulationViewer tool: </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_18.png)

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#366092">Step 3: Parameters to SPHARM Mesh </span>

<span style="color:#595959"> Medial mesh parameter color map files</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_19.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Comparison of the Medial mesh parameter color maps containing in the </span>  <span style="color:#595959"> _\*_ </span>  <span style="color:#595959"> _SPHARMMedialMesh\.vtk_ </span>  <span style="color:#595959"> in ShapePopulationViewer tool:</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_20.png)

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARMMedialMesh\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARMMedialMesh\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARMMedialMesh\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARMMedialMesh\.vtk</span>

Installation of SPHARM\-PDM Tool



* SPHARM\-PDM tool can be used with two open\-source software platforms:
      * __SlicerSALT__ : which is the dissemination vehicle of powerful shape analysis methodology\. This software is a light\-weight\, customized version of 3D Slicer\. It contains SPHARM\-PDM  _as a module_ \.
      * __3D Slicer__ : which is an open\-source and free software platform for medical image informatics\, image processing\, and three\-dimensional visualization\. SPHARM\-PDM can be downloaded  _as an extension_ \.


<span style="color:#366092">SPHARM\-PDM Installation on SlicerSALT</span>

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  _[SlicerSALT website](http://salt.slicer.org/)_  <span style="color:#595959"> and install it\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_21.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_22.png)

<span style="color:#595959">Powered by Girder</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_23.png)

<span style="color:#366092">SPHARM\-PDM Installation on 3D Slicer</span>

<span style="color:#595959">  Download 3D Slicer packages for your respective operating system on the </span>  _[3D Slicer website](https://www.slicer.org/)_  <span style="color:#595959"> and install it\.</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_24.png)

<span style="color:#366092">SPHARM\-PDM Installation on 3D Slicer</span>

<span style="color:#595959">  In 3D Slicer\, open the Extension Manager</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_25.png)

<span style="color:#366092">SPHARM\-PDM Installation on 3D Slicer</span>

<span style="color:#595959">  In the </span>  <span style="color:#595959"> _Install Extension_ </span>  <span style="color:#595959"> tab\, select </span>  <span style="color:#595959"> _SPHARM_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>

<span style="color:#595959"> Under </span>  <span style="color:#595959"> __SPHARM\-PDM__ </span>  <span style="color:#595959">\, select the </span>  <span style="color:#595959"> _Install_ </span>  <span style="color:#595959"> button and restart Slicer when prompted   </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_26.png)

<span style="color:#366092">SPHARM\-PDM Installation on 3D Slicer</span>

<span style="color:#595959">For quality control\, we analyze our SPHARM\-PDM outputs with </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> extension\. Shape Population Viewer can be installed as a 3D Slicer extension or as an external binary\. This module is included as part of the SlicerSALT package\.  </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_27.png)

<span style="color:#366092">SPHARM\-PDM Installation on 3D Slicer</span>



* <span style="color:#595959">To install </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> as </span>  <span style="color:#595959"> _a 3D Slicer extension_ </span>  <span style="color:#595959">: </span>
    * <span style="color:#595959">Open </span>  <span style="color:#595959"> _Extension Manager_ </span>  <span style="color:#595959">\, in the </span>  <span style="color:#595959"> _Install Extensions _ </span>  <span style="color:#595959">tab\, select ‘</span>  <span style="color:#595959"> _Shape Analysis’_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>
    * <span style="color:#595959"> Select the appropriate </span>  <span style="color:#595959"> _Install _ </span>  <span style="color:#595959">button and restart 3D Slicer when prompted</span>


![](img/SlicerSALT-SPHARM-PDM-Tutorial_28.png)

<span style="color:#366092">SPHARM\-PDM Installation on 3D Slicer</span>



* <span style="color:#595959">To install </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> as an </span>  <span style="color:#595959"> _external binary_ </span>  <span style="color:#595959">: </span>
    * <span style="color:#595959"> Download ShapePopulationViewer package for your respective operating system on </span>  _[NITRC website](https://www.nitrc.org/projects/shapepopviewer/)_
    * <span style="color:#595959"> In 3D Slicer\, open </span>  <span style="color:#595959"> _Application Settings _ </span>  <span style="color:#595959">in the </span>  <span style="color:#595959"> _Edit _ </span>  <span style="color:#595959">Menu\.  On the tab </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959">\, </span>  <span style="color:#595959"> __Add __ </span>  <span style="color:#595959">the folder where  ShapePopulationViewer is stored</span>
    * <span style="color:#595959"> Restart 3D Slicer</span>


![](img/SlicerSALT-SPHARM-PDM-Tutorial_29.png)



  * SPHARM\-PDM tool can be used by two different ways:
      * As  __command\-line__   __tool__  through the terminal thanks to SlicerSALT
      * As a  __module__  of SlicerSALT or 3DSlicer


<span style="color:#366092">SPHARM\-PDM Command\-Line Tool</span>



* <span style="color:#595959">SPHARM\-PDM method can be run on several cases through a terminal thanks to two files included in the SlicerSALT package: </span>
* <span style="color:#595959">SPHARM\-PDM\-parameters\.ini which allows the user to specify the inputs\, outputs and the parameters of the SPHARM\-PDM tool</span>
* <span style="color:#595959">SPHARM\-PDM\.py python script which will apply SPHARM\-PDM method on the given input cases with the parameters specified in the SPHARM\-PDM\-parameters\.ini file</span>
* <span style="color:#595959"> _Location of the SPHARM\-PDM\.py_ </span>  <span style="color:#595959"> and </span>  <span style="color:#595959"> _SPHARM\-PDM\-parameters\.ini files: _ </span>
  * <span style="color:#595959"> _On Linux and Windows: share/Slicer\-4\.7/CommandLineTool_ </span>
  * <span style="color:#595959"> _On MacOs: Open the SlicerSALT Contents 			 _ </span>
  * <span style="color:#595959"> _🡪 Contents/share/Slicer\-4\.7/CommandLineTool_ </span>


![](img/SlicerSALT-SPHARM-PDM-Tutorial_30.png)

<span style="color:#366092">SPHARM\-PDM Command\-Line Tool</span>

<span style="color:#595959"> __Step 1__ </span>  <span style="color:#595959">: Modification of the </span>  <span style="color:#595959"> _SPHARM\-PDM\-parameters\.ini_ </span>  <span style="color:#595959"> file by specifying the </span>  <span style="color:#595959"> __input directory path __ </span>  <span style="color:#595959">containing the input cases and </span>  <span style="color:#595959"> __the output directory path __ </span>  <span style="color:#595959">where the SPHARM\-PDM outputs will be stored\.</span>

<span style="color:#595959">The others parameters can also be modified to apply SPHARM\-PDM to a particular case\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_31.png)

<span style="color:#366092">SPHARM\-PDM Command\-Line Tool</span>



* <span style="color:#595959"> __Step 2__ </span>  <span style="color:#595959">: Launch SPHARM\-PDM method with the following command\-lines: </span>
* <span style="color:#595959">On Linux and Windows: </span>
  * <span style="color:#595959"> _$cd path\-to\-the\-SlicerSALT\-package_ </span>
  * <span style="color:#595959"> _$\./SlicerSALT \-\-no\-main\-window \-\-python\-script share/Slicer\-4\.7/CommandLineTool/SPHARM\-PDM\.py   share/Slicer\-4\.7/CommandLineTool/SPHARM\-PDM\-parameters\.ini_ </span>
* <span style="color:#595959">On MacOs: </span>
  * <span style="color:#595959"> _$cd path\-to\-the\-SlicerSALT\-package/SlicerSALT\.app/Contents/MacOS_ </span>
  * <span style="color:#595959"> _$\./SlicerSALT \-\-no\-main\-window \-\-python\-script \.\./share/Slicer\-4\.7/CommandLineTool/SPHARM\-PDM\.py \.\./share/Slicer\-4\.7/CommandLineTool/SPHARM\-PDM\-parameters\.ini_ </span>


<span style="color:#366092">SPHARM\-PDM Module </span>

<span style="color:#595959">In 3D Slicer or in SlicerSALT\, select </span>  <span style="color:#595959"> _Shape Analysis Module_ </span>  <span style="color:#595959"> from the </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959"> drop\-down menu \(</span>  <span style="color:#595959"> _Category:_ </span>  <span style="color:#595959"> SPHARM\) or on the Search bar\.  </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_32.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_33.png)

<span style="color:#366092">Setting up Input/Output Directories</span>

<span style="color:#595959"> _Group Project IO _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the folder which contains the input data</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Output Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> select the folder where the outputs of each step will be stored</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_34.png)

<span style="color:#000000">/path/to/InputDirectory</span>

<span style="color:#000000">/path/to/OutputDirectory</span>

<span style="color:#366092">Input/Output Data</span>



* <span style="color:#595959">The </span>  <span style="color:#595959"> _input directory_ </span>  <span style="color:#595959"> contains the input data which can be:  </span>
  * <span style="color:#595959">Label map volumes \(\.gipl\, \.gipl\.gz\, \.nii\, \.nii\.gz\, \.nrrd\, \.mgh\, \.mgh\.gz\, \.mhd\, or \.hdr\) </span>
  * <span style="color:#595959">Models \(\.vtk\, or \.vtp\)</span>
* <span style="color:#595959">The </span>  <span style="color:#595959"> _output directory_ </span>  <span style="color:#595959"> will contain SPHARM output data sorted in three different folders for each of the three steps:</span>
    * <span style="color:#595959"> _Step1\_SegPostProcess_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">for the </span>  <span style="color:#595959"> _Post Processed Segmentation _ </span>  <span style="color:#595959">step</span>
    * <span style="color:#595959"> _Step2\_GenMeshPara_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">for the </span>  <span style="color:#595959"> _Generate Mesh Parameters_ </span>  <span style="color:#595959"> step</span>
    * <span style="color:#595959"> _Step3\_ParaToSPHARMMesh_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">for the </span>  <span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959">step</span>  <span style="color:#595959"> </span>


![](img/SlicerSALT-SPHARM-PDM-Tutorial_35.png)

<span style="color:#366092">Features and Parameters</span>



* <span style="color:#595959"> _Common to all _ </span>  <span style="color:#595959"> __tabs__ </span>
* <span style="color:#595959">The </span>  <span style="color:#595959"> _Overwrite_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">option: this option is available for the three steps of </span>  <span style="color:#595959"> _Shape Analysis Module_ </span>  <span style="color:#595959">: </span>
* <span style="color:#595959">If this option </span>  <span style="color:#595959"> __is not selected__ </span>  <span style="color:#595959"> for one step\, it will skip the step if the output data were previously computed and stored in the output folder of this step: </span>
    * <span style="color:#595959">Folder </span>  <span style="color:#595959"> _Step1\_SegPostProcess_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">for the </span>  <span style="color:#595959"> _Post Processed Segmentation _ </span>  <span style="color:#595959">step</span>
    * <span style="color:#595959">Folder </span>  <span style="color:#595959"> _Step2\_GenMeshPara_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">for the </span>  <span style="color:#595959"> _Generate Mesh Parameters_ </span>  <span style="color:#595959"> step</span>
    * <span style="color:#595959">Folder </span>  <span style="color:#595959"> _Step3\_ParaToSPHARMMesh_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">for the </span>  <span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959">step</span>
* <span style="color:#595959">If this option </span>  <span style="color:#595959"> __is selected __ </span>  <span style="color:#595959">for one step\, all the files in the output folder of this step will be removed and the step won’t be skipped\. </span>


<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Post Processed Segmentation tab_ </span>

<span style="color:#595959"> _Rescale option_ </span>  <span style="color:#595959">: The X\, Y and Z spacing parameters \(sx/sy/sz\) determine the resolution in which the data will be processed for each axis \(in millimeters\)</span>

<span style="color:#595959"> _Label Number option_ </span>  <span style="color:#595959">: First extraction of the specified label before to apply the post processing step</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_36.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Generate Mesh Parameters _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Number of iterations_ </span>  <span style="color:#595959">: Higher number of iterations will improve the accuracy of the mapping of the surface mesh to a parameterization sphere</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_37.png)

| <span style="color:#ffffff">Number of iterations</span> |
| :-: |
| <span style="color:#ffffff">5</span> |
| <span style="color:#ffffff">1000</span> |

![](img/SlicerSALT-SPHARM-PDM-Tutorial_38.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: </span>  <span style="color:#595959"> _\*SPHARM\.vtk_ </span>  <span style="color:#595959"> generated with 5 iterations \(top\) and 1000 iterations \(bottom\)</span>  <span style="color:#808080"> </span>

<span style="color:#595959"> _Note_ </span>  <span style="color:#595959">: Higher number of iterations will produce better representation results\.</span>

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Subdivision Level value_ </span>  <span style="color:#595959">: Icosahedron subdivision allows for linear\, uniform sampling of the object by referring to its spherical parameterization\. The </span>  <span style="color:#595959"> _SubdivLevel_ </span>  <span style="color:#595959"> value sets the level of the subdivision factor that will be used\. Improving this value results in a SPHARM mesh with more points\.   </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_39.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Subdivision Level value_ </span>  <span style="color:#595959">:    </span>

<span style="color:#595959"> __Figure: __ </span>  <span style="color:#595959"> _\*para\.vtk _ </span>  <span style="color:#595959">generated with 5 subdivision different </span>  <span style="color:#595959">\(left to right : 2 – 4 – 6 – 10 \- 20\)     </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_40.png)

| <span style="color:#ffffff">Subdivision Level</span> | <span style="color:#ffffff">2</span> | <span style="color:#ffffff">4</span> | <span style="color:#ffffff">6</span> | <span style="color:#ffffff">10</span> | <span style="color:#ffffff">20</span> |
| :-: | :-: | :-: | :-: | :-: | :-: |
| <span style="color:#ffffff">Number of Points</span> | <span style="color:#ffffff">42</span> | <span style="color:#ffffff">162</span> | <span style="color:#ffffff">362</span> | <span style="color:#ffffff">1002</span> | <span style="color:#ffffff">4002</span> |

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Subdivision Level value_ </span>  <span style="color:#595959">:    </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_41.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959"> _: \*SPHARM\.vtk _ </span>  <span style="color:#595959">generated with a subdivision level of 2 \(left\) and 10 \(right\)</span>

<span style="color:#595959"> _Note_ </span>  <span style="color:#595959">: Higher subdivision level value will result in a smoother surface mesh\.</span>  <span style="color:#595959">    </span>

| <span style="color:#ffffff">Subdivision Level</span> | <span style="color:#ffffff">2</span> | <span style="color:#ffffff">10</span> |
| :-: | :-: | :-: |
| <span style="color:#ffffff">Number of points</span> | <span style="color:#ffffff">42</span> | <span style="color:#ffffff">1002</span> |

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _SPHARM Degree value_ </span>  <span style="color:#595959"> represents the degree of the spherical harmonic series used on the data\. Changing this value results in different levels of detail of the object\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_42.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _SPHARM Degree_ </span>  <span style="color:#595959">: </span>

| <span style="color:#ffffff">SPHARM degree</span> |
| :-: |
| <span style="color:#ffffff">1</span> |
| <span style="color:#ffffff">3</span> |
| <span style="color:#ffffff">5</span> |
| <span style="color:#ffffff">10</span> |
| <span style="color:#ffffff">25</span> |

![](img/SlicerSALT-SPHARM-PDM-Tutorial_43.png)

<span style="color:#595959"> __Figure: __ </span>  <span style="color:#595959"> _\*SPHARM\.vtk_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">generated with different SPHARM degree \(left to right: 1 – 3 – 5 – 10 – 25\)  </span>

<span style="color:#595959"> _Note_ </span>  <span style="color:#595959">: A higher SPHARM degree value will result in a surface mesh with more details\. </span>

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Build the medial mesh:_ </span>  <span style="color:#595959"> This option will compute the mean latitude axis associated with the data if checked\. The Number of theta/phi iterations corresponds to the number of samples used in the medial mesh computation</span>  <span style="color:#595959">1</span>  <span style="color:#595959">\.</span>  <span style="color:#595959"> </span>

<span style="color:#595959">1\. Paniagua B1\, Lyall A\, Berger JB\, Vachet C\, Hamer RM\, Woolson S\, Lin W\, Gilmore J\, Styner M\. \(2013\)\. Lateral ventricle morphology analysis via mean latitude axis\. Proc SPIE Int Soc Opt Eng\. 2013 Mar 29;8672\. pii: 2006846\. \<http://www\.ncbi\.nlm\.nih\.gov/pubmed/23606800></span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_44.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Post Processed Segmentation _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Gaussian filtering_ </span>  <span style="color:#595959">: A Gaussian filter will be applied during the preprocessing step if this option is checked\.</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_45.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Registration template Options_ </span>  <span style="color:#595959">: This option allows to have a rigid\-body Procrustes alignment i\.e\. the </span>  <span style="color:#595959"> _\*SPHARM\_procalign _ </span>  <span style="color:#595959">mesh generated by the tool will be aligned with the registration template \(VTK file\) by applying\, if needed\, a rigid transformation \(which uses only translation and/or a rotation\)\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_46.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Flip template Options_ </span>  <span style="color:#595959">: If </span>  <span style="color:#595959"> _Use Flip Template_ </span>  <span style="color:#595959"> is checked\, a </span>  <span style="color:#595959"> _Flip Template _ </span>  <span style="color:#595959">is used to test all possible flips of the parametrization along the first order ellipsoid axis and select the one whose reconstruction has minimal distance to the flip\-template\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_47.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Flip Options_ </span>  <span style="color:#595959">: This option allows an optional flipping of the parametrization specified by the user\.</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_48.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Flip Options_ </span>  <span style="color:#595959">: To apply the same flip option for each case\, check </span>  <span style="color:#595959"> _Same Flip for all the outputs_ </span>  <span style="color:#595959">\. </span>

<span style="color:#595959">Select </span>  <span style="color:#595959"> __one flip along an axis__ </span>  <span style="color:#595959"> or choose to apply </span>  <span style="color:#595959"> __all the flips__ </span>  <span style="color:#595959"> to determine the best flip\.</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_49.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Flip Options_ </span>  <span style="color:#595959">: To apply different flip options for each case\, uncheck </span>  <span style="color:#595959"> _Same Flip for all the outputs_ </span>  <span style="color:#595959">\. </span>

<span style="color:#595959">As previously\, select a flip option for each case\.</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_50.png)

<span style="color:#366092">Features and Parameters</span>

<span style="color:#595959"> _Advanced Parameters to SPHARM Mesh _ </span>  <span style="color:#595959"> __tab__ </span>

<span style="color:#595959"> _Flip Options_ </span>  <span style="color:#595959">: Example of an application of all the flips on one case by iterating 7 times </span>  <span style="color:#595959"> _ParaToSPHARMMesh_ </span>  <span style="color:#595959"> CLI\. This figure shows a comparison of different flips in </span>  <span style="color:#595959"> _Shape Population Viewer\._ </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_51.png)

<span style="color:#595959"> _Flip Along X Axis_ </span>

<span style="color:#595959"> _Flip Along Y Axis_ </span>

<span style="color:#595959"> _Flip Along Z Axis_ </span>

<span style="color:#595959"> _Flip Along _ </span>  <span style="color:#595959"> _X and Y Axis_ </span>

<span style="color:#595959"> _Flip Along _ </span>  <span style="color:#595959"> _X and Z Axis_ </span>

<span style="color:#595959"> _Flip Along _ </span>  <span style="color:#595959"> _Y and Z Axis_ </span>

<span style="color:#595959"> _Flip Along X\, Y and Z Axis_ </span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Visualization in ShapePopulationViewer of the different flips applied on </span>  <span style="color:#595959"> _\*SPHARM_ </span>  <span style="color:#595959"> model\.   </span>

<span style="color:#366092">Running SPHARM\-PDM</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_52.png)

<span style="color:#595959">Click on the Run </span>  <span style="color:#595959"> _ShapeAnalysisModule_ </span>  <span style="color:#595959"> button\, to run the three steps on the provided inputs\. </span>

<span style="color:#366092">Running SPHARM\-PDM</span>

<span style="color:#595959">Progress bars will indicate when the computation is done and if the computation for each case was completed with or without error\.</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_53.png)

<span style="color:#595959">If the module was completed with errors\, the step which was completed with errors is indicated and the errors can be displayed by clicking on the little arrows:</span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_54.png)

<span style="color:#595959"> _3D Slicer’s Error Log_ </span>  <span style="color:#595959"> can also be used for debugging if the module was completed with errors\. To open it\, click on the red icon at the bottom right\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_55.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_56.png)

<span style="color:#595959">The outputs files for each step of SPHARM\-PDM are stored in three folders in the output directory previously selected: </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_57.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_58.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_59.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_60.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>

<span style="color:#595959">If </span>  <span style="color:#595959"> _Shape Population Viewer _ </span>  <span style="color:#595959">is installed\, the Visualization tab will be enabled: </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_61.png)

<span style="color:#595959"> __Note__ </span>  <span style="color:#595959">: </span>  <span style="color:#595959"> _ShapePopulationViewer_ </span>  <span style="color:#595959"> is installed by default in SlicerSALT </span>

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>

<span style="color:#595959">The selection of the SPHARM outputs which will be displayed in </span>  <span style="color:#595959"> _Shape Population Viewer _ </span>  <span style="color:#595959">can be done thanks to the checkable combobox or with the checkbox corresponding to them: </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_62.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>

<span style="color:#595959">Run </span>  <span style="color:#595959"> _Shape Population Viewer _ </span>  <span style="color:#595959">by clicking on the </span>  <span style="color:#595959"> _Shape Population Viewer _ </span>  <span style="color:#595959">button: </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_63.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>

<span style="color:#595959">To display the selected models in </span>  <span style="color:#595959"> _Shape Population Viewer_ </span>  <span style="color:#595959">\, click on </span>  <span style="color:#595959"> _VTK Files_ </span>  <span style="color:#595959"> and then </span>  <span style="color:#595959"> _Ok_ </span>  <span style="color:#595959">: </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_64.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>

<span style="color:#595959">To display the different color maps on the meshes\, use the comboBox Attributes:  </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_65.png)

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Visualization in ShapePopulationViewer of two \*SPHARM models with the phi spherical parameter representation</span>

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>



* <span style="color:#595959">Example: This view shows the phi correspondences between the files\.</span>
  * <span style="color:#595959">Quality control of the correspondences is performed using the color\-coded parameterization information\.</span>
  * <span style="color:#595959">Equally colored areas represent equal corresponding area\.  </span>


![](img/SlicerSALT-SPHARM-PDM-Tutorial_66.png)

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#000000">groupA\_01\_hippo\_pp\_surf\_SPHARM\.vtk</span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Visualization in ShapePopulationViewer of multiples </span>  <span style="color:#595959"> _\*SPHARM_ </span>  <span style="color:#595959"> shapes displaying paraPhi color map</span>

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>



* <span style="color:#595959">Only data sets with Procrustes alignment information are automatically aligned in </span>  <span style="color:#595959"> _Shape Population Viewer_ </span>  <span style="color:#595959">\.</span>
* <span style="color:#595959">For data sets without Procrustes alignment:</span>
  * <span style="color:#595959">Under </span>  <span style="color:#595959"> _View Options_ </span>  <span style="color:#595959">\, set </span>  <span style="color:#595959"> _Aligned_ </span>  <span style="color:#595959"> to </span>  <span style="color:#595959"> __On __ </span>  <span style="color:#595959">to align the data set using file information\.  </span>


![](img/SlicerSALT-SPHARM-PDM-Tutorial_67.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092">ShapePopulationViewer</span>

<span style="color:#595959">For more information about using </span>  <span style="color:#595959"> _Shape Population Viewer _ </span>  <span style="color:#595959">tool\, consult the </span>  _[ShapePopulationViewer tutorial](https://www.nitrc.org/docman/view.php/759/1339/User%20Tutorial%20v1.3.2)_  <span style="color:#595959"> by Alexis Girault\.</span>

<span style="color:#366092">Quality control using</span>  <span style="color:#366092"> _Models _ </span>  <span style="color:#366092">module</span>

<span style="color:#595959">Models can be viewed in </span>  <span style="color:#595959"> _3D Slicer_ </span>  <span style="color:#595959"> or </span>  <span style="color:#595959"> _SlicerSALT _ </span>  <span style="color:#595959">by dragging and dropping the files or by using the </span>  <span style="color:#595959"> _Data _ </span>  <span style="color:#595959">button in the toolbar to search for the file\.</span>

<span style="color:#595959">When importing the VTK file\, select the </span>  <span style="color:#595959"> _Model _ </span>  <span style="color:#595959">Option : </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_68.png)

![](img/SlicerSALT-SPHARM-PDM-Tutorial_69.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092"> _Models _ </span>  <span style="color:#366092">module</span>

<span style="color:#595959">When the VTK file has been imported\, it will be visualized in the </span>  <span style="color:#595959"> _Scene View_ </span>  <span style="color:#595959"> \(or the 3D View\)\. Switch to the </span>  <span style="color:#595959"> _Models_ </span>  <span style="color:#595959"> Module to change the display settings of the VTK model\. </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_70.png)

<span style="color:#366092">Quality control using</span>  <span style="color:#366092"> _Models _ </span>  <span style="color:#366092">module</span>

<span style="color:#595959"> _Hide/show_ </span>  <span style="color:#595959"> the model by clicking on the eye icon</span>

<span style="color:#595959">To change the display properties of the VTK file\, first </span>  <span style="color:#595959"> _select_ </span>  <span style="color:#595959"> the file from the </span>  <span style="color:#595959"> _Scene window_ </span>  <span style="color:#595959"> in the </span>  <span style="color:#595959"> _Models_ </span>  <span style="color:#595959"> Module</span>

<span style="color:#595959">Change the </span>  <span style="color:#595959"> _representation_ </span>  <span style="color:#595959"> __ __ </span>  <span style="color:#595959">of the model mesh\. For example\, </span>  <span style="color:#595959"> _Wireframe_ </span>  <span style="color:#595959"> representation will display the meshing of the model</span>

<span style="color:#595959">Change the </span>  <span style="color:#595959"> _color_ </span>  <span style="color:#595959"> of the mesh from the default gray color</span>

<span style="color:#595959">Change the </span>  <span style="color:#595959"> _opacity_ </span>  <span style="color:#595959"> of the mesh  </span>

![](img/SlicerSALT-SPHARM-PDM-Tutorial_71.png)

Acknowledgements \- Resources \- Questions



* The SPHARM\-PDM developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.
* Github repository:
      * _[SPHARM\-PDM](https://github.com/NIRALUser/SPHARM-PDM)_  _ _
      * _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_
      * _[3D Slicer](https://github.com/Slicer/Slicer)_
* Forums:
      * _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_
      * _[3D Slicer](https://discourse.slicer.org/)_
* Papers:
      * _[Lateral ventricle morphology analysis via mean latitude axis\.](https://www.ncbi.nlm.nih.gov/pubmed/23606800)_
      * _[Framework for the Statistical Shape Analysis of Brain Structures using SPHARM\-PDM](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3062073/)_
* For other remarks or questions\, please email:
* beatriz\.paniagua@kitware\.com


![](img/SlicerSALT-SPHARM-PDM-Tutorial_72.png)

