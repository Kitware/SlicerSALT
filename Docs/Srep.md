<span style="color:#ffffff">Shape analysis via skeletal models</span>

<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">Zhiyuan Liu\, Stephen M\. Pizer\, Beatriz Paniagua\, Jared Vicory\, Junpyo Hong\, Connor Bowley</span>

<span style="color:#f2f2f2">May 2022</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_0.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_1.png)

# Introduction to skeletal representations

<span style="color:#366092">Skeletal representations</span>

<span style="color:#595959">Shape Analysis allows studying morphology in populations of anatomic structures\. A </span>  <span style="color:#595959"> __skeletal representation \(s\-rep\) is__ </span>  <span style="color:#595959"> used to model the structure of an object with no essential interior branches\, providing a rich geometric representation with correspondence across cases\. </span>

<span style="color:#595959">The S\-rep Extension \(short for </span>  <span style="color:#595959"> __Skeletal Representation Extension__ </span>  <span style="color:#595959">\) in SlicerSALT provides utilities to visualize\, initialize and refine s\-reps of 3\-dimensional objects\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_2.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_3.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_4.png)

<span style="color:#000000">Figure: Some examples have been researched via s\-rep</span>

<span style="color:#000000">Left: caudate nucleus Middle: hippocampus Right: cerebral ventricle </span>

<span style="color:#366092">The Slabular S\-rep</span>

<span style="color:#595959">A 3D object whose length is notably larger than its width which is notably larger than its thickness is suitable for modeling by a slabular s\-rep\.</span>

<span style="color:#595959">A slabular s\-rep \(from now on just referred to as an s\-rep\) </span>

<span style="color:#595959">consists first of a folded\, two\-sided quasi\-medial sheet inside the object\.  This sheet is called the “skeletal sheet”\. It is sampled into a network of skeletal positions\.</span>

<span style="color:#595959">Special skeletal samples are at positions where the sheet folds back onto itself\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_5.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_6.png)

<span style="color:#000000">Figure: A skeletal model for a hippocampus\.  </span>

<span style="color:#000000">Left: the surface mesh of hippocampus\.</span>

<span style="color:#000000">Right: the skeletal sheet of the s\-rep of this hippocampus</span>

<span style="color:#366092">The Slabular S\-rep</span>

<span style="color:#595959">From each sample point on the skeleton\, a vector to and approximately orthogonal to the boundary is provided as part of the s\-rep\. These vectors are called “spokes”\.</span>

<span style="color:#595959">The spokes emanating from the fold curve of the sheet \(yellow curve in the right figure\) meet the  object surface at crest points\. </span>

<span style="color:#595959">The spokes can be interpolated into a finer mesh\, and the spoke endpoints can be interpolated into a implied boundary for the object\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_7.jpg)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_8.png)

<span style="color:#000000">Figure: A skeletal model for a hippocampus\.  </span>

<span style="color:#000000">	     Left: implied boundary of hippocampus\.</span>

<span style="color:#000000">	     Right: the s\-rep of hippocampus</span>

# The SlicerSkeletalRepresentations extension

<span style="color:#366092">Modules Overview</span>

<span style="color:#595959"> __SRep:__ </span>  <span style="color:#595959"> Visualization and interpolation of existing s\-reps</span>

<span style="color:#595959"> __SRepCreator:__ </span>  <span style="color:#595959"> Initialize an s\-rep by mean curvature flow of an object boundary</span>

<span style="color:#595959"> __SRepRefinement:__ </span>  <span style="color:#595959"> Refine an s\-rep to more closely fit an object boundary</span>

<span style="color:#595959">All the s\-rep modules can be found in the category </span>  <span style="color:#595959"> _Skeleton\, topology_ </span>

<span style="color:#366092">S\-rep MRML Nodes</span>

<span style="color:#595959">3D Slicer uses Medical Reality Modeling Language \(MRML\) nodes as the data types for its processing\. The s\-rep extension adds a new MRML data node used to describe s\-reps\.</span>

<span style="color:#595959">These nodes can be saved and loaded as </span>  <span style="color:#595959">\.srep\.json</span>  <span style="color:#595959"> files using Slicer’s built in save and load facilities\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_9.png)

<span style="color:#366092">S\-rep modules workflow</span>

<span style="color:#000000">3D Visualization</span>

<span style="color:#366092">S\-rep Extension in SlicerSALT</span>

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  <span style="color:#0000ff"> _[SlicerSALT website](http://salt.slicer.org/)_ </span>  <span style="color:#595959"> and install it\. The </span>  <span style="color:#595959"> _SlicerSkeletalRepresentation_ </span>  <span style="color:#595959"> extension will be ready to use\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_10.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_11.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_12.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_13.png)

<span style="color:#595959">Powered by Girder</span>

<span style="color:#366092">S\-rep Extension Installation on 3D Slicer</span>

<span style="color:#595959">Download 3D Slicer at </span>  _[https://download\.slicer\.org/](https://download.slicer.org/)_  <span style="color:#595959"> </span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_14.png)

<span style="color:#366092">S\-rep Extension Installation on 3D Slicer</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_15.png)

<span style="color:#595959">From 3D Slicer\, open the extension manager</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_16.png)

<span style="color:#366092">S\-rep Extension Installation on 3D Slicer</span>

<span style="color:#595959">Search for “SkeletalRepresentation”\, press Install\, then press Restart in the bottom right corner\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_17.png)

![](img/SlicerSALT-SrepMRMLModule-Tutorial_18.png)

# SRep Module

<span style="color:#366092">SRep: Visualization</span>

<span style="color:#595959">Can visualize the SRep \(or pieces thereof\) </span>

<span style="color:#595959">Can see basic information\, such as number of spokes</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_19.png)

<span style="color:#366092">SRep: Interpolation</span>

<span style="color:#595959">Can interpolate skeletal grid and spoke points</span>

<span style="color:#595959">Will increase number of spokes by 2</span>  <span style="color:#595959">\(Interpolation level\)</span>  <span style="color:#595959"> times</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_20.png)

<span style="color:#000000">Both original and interpolate s\-reps displayed\. The original s\-rep was given thicker lines for visualization purposes\.</span>

# SRepCreator Module

<span style="color:#595959">Create s\-reps from Models \(\.vtk\, \.stl\, \.ply\, etc\) in 2 steps</span>

<span style="color:#595959">Forward Flow: creates an ellipsoid that best fits the input model and creates an SRep to fit that ellipsoid\. The model is "flowed" toward an ellipsoidal shape for a number of iterations\, then a best fit ellipsoid is made on the flowed shaped\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_21.png)

<span style="color:#000000">Example forward flow to ellipsoid</span>

<span style="color:#595959">Backward Flow: adjusts the SRep created from the ellipsoid to fit the original model by reversing the flow transformations made during the forward flow\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_22.png)

<span style="color:#000000">Example backward flow to fit original model</span>

<span style="color:#366092">SRepCreator Parameters</span>



* <span style="color:#595959">S\-rep creation parameters \(also see “Help” in the module\)</span>
  * <span style="color:#595959"> _Input Mesh: _ </span>  <span style="color:#595959">model to create the SRep of\. </span>
  * <span style="color:#595959"> _Max iterations:_ </span>  <span style="color:#595959"> the number of iterations to run in the forward flow\. </span>
  * <span style="color:#595959"> _Step size:_ </span>  <span style="color:#595959"> the size of step to take in during the forward flow\. </span>
  * <span style="color:#595959"> _Smooth amount:_ </span>  <span style="color:#595959"> the amount of smoothing that should be applied to the model while flowing toward the ellipsoidal shape\. The algorithm doesn't work well with sharp edges or points\, so smoothing can help with that\. </span>
  * <span style="color:#595959"> _\# Fold Points:_ </span>  <span style="color:#595959"> The number of fold \(aka crest\) points in the generated SRep\. </span>
  * <span style="color:#595959"> _\# Steps to Fold:_ </span>  <span style="color:#595959"> The number of steps from the spine to outer boundary of the skeletal sheet\. The point on the spine is not included in this number\.</span>


<span style="color:#366092">Running SRepCreator</span>

<span style="color:#595959">Set the desired parameters and press run\. During the creation of the s\-rep you will see a progress bar\, but be unable to do anything else in Slicer\.</span>

<span style="color:#595959">After a couple minutes an SRep will be created with the name </span>  <span style="color:#595959">\<Model\-name>\-srep</span>  <span style="color:#595959">\.</span>

<span style="color:#595959">You can then use the </span>  <span style="color:#595959"> _Data_ </span>  <span style="color:#595959"> or </span>  <span style="color:#595959"> _SRep_ </span>  <span style="color:#595959"> modules to visualize the SRep\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_23.png)

# SRepRefinement Module

<span style="color:#595959">The goal of refinement is to better fit an s\-rep’s spokes to the boundary of the model it was created from\. There are three factors we consider when defining the objective function for fit\.</span>

<span style="color:#595959">The distance from s\-rep implied boundary \(the ends of the spokes\) to actual model boundary\.</span>

<span style="color:#595959">The deviation of the spokes from being perpendicular to the model boundary\.</span>

<span style="color:#595959">The geometric illegality of the spokes\, i\.e\. the spokes are not allowed to cross each other\.</span>

<span style="color:#366092">SRepRefinement Parameters</span>

<span style="color:#595959"> _Input Model:_ </span>  <span style="color:#595959"> the model to refine the SRep to </span>

<span style="color:#595959"> _Input SRep:_ </span>  <span style="color:#595959"> the SRep to be refined </span>

<span style="color:#595959"> _Output SRep:_ </span>  <span style="color:#595959"> the SRep object to put the refined SRep into </span>

<span style="color:#595959"> _Interpolation level:_ </span>  <span style="color:#595959"> how much to interpolate between spokes\. The interpolated spokes are used to define the implied boundary used by the objective function\. Interpolated spokes are produced at 2</span>  <span style="color:#595959">level</span>  <span style="color:#595959"> times the original density\. </span>

<span style="color:#595959"> _Initial region size:_ </span>  <span style="color:#595959"> the initial value of the newuoa trust region radius\. </span>

<span style="color:#595959"> _Final region size:_ </span>  <span style="color:#595959"> the final value of the newuoa trust region radius\. Typically this is around one tenth the greatest expected change to a variable\. </span>

<span style="color:#595959"> _Max iterations:_ </span>  <span style="color:#595959"> the maximum amount of iterations to run </span>

<span style="color:#366092">SRepRefinement Parameters</span>

<span style="color:#595959"> _Image match weight:_ </span>  <span style="color:#595959"> the amount of weight to place on the L0 penalty for not being on the model boundary</span>

<span style="color:#595959"> _Normal match weight:_ </span>  <span style="color:#595959"> the amount of weight to place on the L1 penalty for not being normal to the model boundary</span>

<span style="color:#595959"> _Geometric illegality weight: _ </span>  <span style="color:#595959">the amount of weight to place on the L2 penalty for having illegally crossing spokes</span>

<span style="color:#366092">Running SRepRefinement</span>

<span style="color:#595959">Set the desired parameters and press run\. During the refinement of the s\-rep you will see a progress bar\, but be unable to do anything else in Slicer\.</span>

<span style="color:#595959">After a few minutes the refined s\-rep will be available in the </span>  <span style="color:#595959"> _Output SRep_ </span>  <span style="color:#595959"> node\.</span>

<span style="color:#595959">You can then use the </span>  <span style="color:#595959"> _Data_ </span>  <span style="color:#595959"> or </span>  <span style="color:#595959"> _SRep_ </span>  <span style="color:#595959"> modules to visualize the SRep\.</span>

![](img/SlicerSALT-SrepMRMLModule-Tutorial_24.png)

<span style="color:#ffffff">Acknowledgements \-</span>

<span style="color:#ffffff"> Resources \- Questions</span>



* <span style="color:#ffffff">The S\-rep module developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.</span>
* <span style="color:#ffffff">Github repository: </span>
      * <span style="color:#0000ff"> _[SkeletalRepresentation](https://github.com/KitwareMedical/SRepExtension)_ </span>  <span style="color:#ffffff"> _ _ </span>
      * <span style="color:#0000ff"> _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_ </span>
      * <span style="color:#0000ff"> _[3D Slicer](https://github.com/Slicer/Slicer)_ </span>
* <span style="color:#ffffff">Forums:</span>
      * <span style="color:#0000ff"> _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_ </span>
      * <span style="color:#0000ff"> _[3D Slicer](https://discourse.slicer.org/)_ </span>  <span style="color:#ffffff"> </span>
* <span style="color:#ffffff">Papers & manuals: </span>
      * _[Fitting Unbranching Skeletal Structures to Objects](http://midag.cs.unc.edu/pubs/papers/srep_fitting_media_final_accept.pdf)_
      * <span style="color:#0000ff"> _[Object Shape Representation via Skeletal Models \(s\-reps\) and Statistical Analysis](http://midag.cs.unc.edu/pubs/papers/xavier_book_2019.pdf)_ </span>
      * <span style="color:#0000ff"> _[Skeletal shape correspondence through entropy](http://midag.cs.unc.edu/pubs/papers/Tu_TMI_2016.pdf)_ </span>
* <span style="color:#ffffff">For other remarks or questions\, please email: </span>
* _[beatriz\.paniagua@kitware\.com](mailto:beatriz.paniagua@kitware.com)_


![](img/SlicerSALT-SrepMRMLModule-Tutorial_25.png)

