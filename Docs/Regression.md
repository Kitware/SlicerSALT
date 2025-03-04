<span style="color:#ffffff">Shape Regression</span>

<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">James Fishbaugh\, Guido Gerig\, Laura Pascal\, Jared Vicory\, Beatriz Paniagua</span>

<span style="color:#f2f2f2">January 2019</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_0.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_1.png)

<span style="color:#366092">Table of Contents</span>

<span style="color:#595959"> __1\) __ </span>  <span style="color:#595959">Description of Shape Regression…………\.\.…\.3</span>

<span style="color:#595959"> __2\)__ </span>  <span style="color:#595959"> Installing the Software…………………………\.\.8</span>

<span style="color:#595959"> __3\)__ </span>  <span style="color:#595959"> Shape Regression Workflow………………\.…13</span>

<span style="color:#595959"> __4\) __ </span>  <span style="color:#595959">Debugging and Quality Control………………\.46</span>

<span style="color:#595959"> __5\)__ </span>  <span style="color:#595959"> Acknowledgments and Resources…………\.\.\.51</span>

<span style="color:#ffffff">Description of Shape Regression</span>

<span style="color:#366092">Description of Shape Regression</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_2.png)

<span style="color:#595959">Shape regression consists of estimating a continuous shape sequence which best matches a set of observed shapes </span>

<span style="color:#366092"> __What growth model?__ </span>  <span style="color:#595959"> Model anatomical evolution by a continuous deformation of space</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_3.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_4.jpg)

![](img/SlicerSALT-ShapeRegression-Tutorial_5.jpg)

<span style="color:#366092">Acceleration Controlled Shape Regression</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_6.png)

<span style="color:#366092"> __How to parameterize deformations?__ </span>

<span style="color:#366092"> __Key Idea: __ </span>  <span style="color:#595959">Parameterize a flow of deformations by </span>  <span style="color:#595959"> __acceleration__ </span>  <span style="color:#595959"> vectors\, which produce velocity\, which in turn results in a change of position\.</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_7.png)

<span style="color:#366092">Acceleration Controlled Shape Regression</span>

<span style="color:#595959">We define the acceleration field a\(x\(t\)\)</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_8.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_9.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_10.png)

<span style="color:#595959">the shape points carrying a point force vector α</span>  <span style="color:#595959">i</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_11.png)

<span style="color:#595959">kernel with standard deviation λ</span>  <span style="color:#595959">V</span>

<span style="color:#595959">Time varying deformation </span>

![](img/SlicerSALT-ShapeRegression-Tutorial_12.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_13.png)

<span style="color:#595959"> initial position</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_14.png)

<span style="color:#595959"> initial velocity</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_15.png)

<span style="color:#366092">Impact of Parameters</span>

<span style="color:#366092"> __Size of deformation kernel:__ </span>  <span style="color:#366092"> T</span>  <span style="color:#595959">he  distance  at  which  neighboring  points  move  in  correlation\. Higher values result in mostly rigid deformation\, while lower values allow points a greater degree of independent movement\. </span>

<span style="color:#366092"> __Size of shape matching kernel:__ </span>  <span style="color:#366092"> T</span>  <span style="color:#595959">he scale at which shape differences are considered noise\.  For matching very detailed shape features\, choose a small value\.  For noisy observations with spurious features\, set this value larger than the size of the features\.</span>

<span style="color:#366092"> __Regularity weight:__ </span>  <span style="color:#366092">  </span>  <span style="color:#595959">A low weight on regularity results in models which closely match observed data\, tending towards interpolation \(rather than regression\) the weight goes to zero\.</span>

<span style="color:#595959">See </span>  <span style="color:#595959"> __“Model selection for spatiotemporal modeling of early childhood sub\-cortical development” SPIE Medical Imaging \(2019\)__ </span>  <span style="color:#595959"> for more detail</span>

<span style="color:#ffffff">Installing the Software</span>

<span style="color:#366092">Installation of ShapeRegression Module in SlicerSALT</span>

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  _[SlicerSALT website](http://salt.slicer.org/)_  <span style="color:#595959"> and install it\. </span>

![](img/SlicerSALT-ShapeRegression-Tutorial_16.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_17.png)

<span style="color:#595959">Powered by Girder</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_18.png)

<span style="color:#366092">Installation of ShapeRegression Module in SlicerSALT</span>

<span style="color:#595959">  Download 3D Slicer packages for your respective operating system on the </span>  _[3D Slicer website](https://www.slicer.org/)_  <span style="color:#595959"> and install it\.</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_19.png)

<span style="color:#366092">Installation of ShapeRegression Module In 3D Slicer</span>

<span style="color:#595959">  In 3D Slicer\, open the Extension Manager</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_20.png)

<span style="color:#366092">Installation of ShapeRegression Module In 3D Slicer</span>

<span style="color:#595959"> In the </span>  <span style="color:#595959"> _Install Extension_ </span>  <span style="color:#595959"> tab\, select </span>  <span style="color:#595959"> _Shape Regression_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>

<span style="color:#595959"> Under </span>  <span style="color:#595959"> __ShapeRegressionExtension__ </span>  <span style="color:#595959">\, select the </span>  <span style="color:#595959"> _Install_ </span>  <span style="color:#595959"> button and restart Slicer when prompted   </span>

![](img/SlicerSALT-ShapeRegression-Tutorial_21.png)

<span style="color:#ffffff">Shape Regression Workflow</span>

<span style="color:#ffffff">1\) </span>  <span style="color:#ffffff"> __Regression Computation__ </span>  <span style="color:#ffffff"> – Model estimation</span>

<span style="color:#ffffff">2\) </span>  <span style="color:#ffffff"> __Regression Visualization__ </span>  <span style="color:#ffffff"> – Visualization of estimated shape change</span>

<span style="color:#366092">Shape Regression Model Estimation</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_22.png)

<span style="color:#ffffff">Begin by selecting ‘</span>  <span style="color:#ffffff"> __Regression Computation__ </span>  <span style="color:#ffffff">’</span>

<span style="color:#366092">Downloading </span>  <span style="color:#366092">tutorial sample data</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_23.png)

<span style="color:#ffffff">Download tutorial </span>  <span style="color:#ffffff">sample data </span>

<span style="color:#ffffff">to a directory of your choice</span>

<span style="color:#366092">Setting up Input Data</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_24.png)

<span style="color:#ffffff">Click the button to select the directory with input vtk shapes</span>

<span style="color:#366092">Setting up Input Data</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_25.png)

<span style="color:#ffffff">Navigate to the directory containing the tutorial shapes</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_26.png)

<span style="color:#ffffff"> _Time point_ </span>  <span style="color:#ffffff"> automatically populated if shape names have time\-suffix</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_27.png)

<span style="color:#ffffff"> _Kernel width_ </span>  <span style="color:#ffffff"> initialized as 50% of the smallest extent of the shape</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_28.png)

<span style="color:#ffffff"> _Shape index_ </span>  <span style="color:#ffffff"> indicates shape correspondence in multi\-objects</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_29.png)

<span style="color:#ffffff">Weight controls the importance of each shape in model estimation</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_30.png)

<span style="color:#ffffff">Leave all settings at default and expand </span>  <span style="color:#ffffff"> _‘Time Parameters’_ </span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_31.png)

<span style="color:#ffffff">Time point range is set using the min and max from input shapes</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_32.png)

<span style="color:#ffffff">Leave all settings at default and expand </span>  <span style="color:#ffffff"> _‘Deformation Parameters’_ </span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_33.png)

<span style="color:#ffffff">The width of the deformation kernel\. Lower values result in more non\-linear changes\, higher values tend towards rigid deformation\.</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_34.png)

<span style="color:#ffffff">For shape inputs with only a few hundred vertices\, chose ‘exact’\, otherwise ‘p3m’ usualy results in faster model estimation\.</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_35.png)

<span style="color:#ffffff">Balances data\-matching and regularity\. Lower values favor accurate data\-matching\.</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_36.png)

<span style="color:#ffffff">Leave all settings at default and expand </span>  <span style="color:#ffffff"> _‘Output Parameters’_ </span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_37.png)

<span style="color:#ffffff">Click to choose an output directory for the estimated model</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_38.png)

<span style="color:#ffffff">Create a new folder called ‘output’</span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_39.png)

<span style="color:#ffffff">Leave all settings at default and expand </span>  <span style="color:#ffffff"> _‘Optional Parameters’_ </span>

<span style="color:#366092">Setting Parameters</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_40.png)

<span style="color:#ffffff">Change the maximum number of iterations to ‘200’</span>

<span style="color:#366092">Model Estimation</span>

<span style="color:#366092">Model Estimation</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_41.png)

<span style="color:#ffffff">Click ‘Run Shape4D’</span>

<span style="color:#366092">Model Estimation</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_42.png)

<span style="color:#ffffff">Estimation may take several minutes to finish</span>

<span style="color:#366092">Model Estimation</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_43.png)

<span style="color:#ffffff">Estimation has converged when </span>  <span style="color:#ffffff"> _‘Status: Completed’_ </span>  <span style="color:#ffffff"> is displayed</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_44.png)

<span style="color:#ffffff">We can now visualize the model by selecting ‘</span>  <span style="color:#ffffff"> __RegressionVisualization’__ </span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_45.png)

<span style="color:#ffffff">Click to choose the directory containing the estimated model</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_46.png)

<span style="color:#ffffff">Choose the output directory from ‘</span>  <span style="color:#ffffff"> __Regression Computation__ </span>  <span style="color:#ffffff">’</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_47.png)

<span style="color:#ffffff">The rootname is automatically populated if a final model is found in the directory\. Otherwise rootname has to be specified\.</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_48.png)

<span style="color:#ffffff">Click ‘</span>  <span style="color:#ffffff"> _Create Sequence_ </span>  <span style="color:#ffffff">’ button to load the model sequence</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_49.png)

<span style="color:#ffffff">Hold right mouse button to zoom\. Hold left button to rotate\.</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_50.png)

<span style="color:#ffffff">Expand ‘</span>  <span style="color:#ffffff"> _Sequence Visualization Options’_ </span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_51.png)

<span style="color:#ffffff">Change the color map to </span>  <span style="color:#ffffff"> _‘velocity’ _ </span>  <span style="color:#ffffff">to visualize speed of shape change</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_52.png)

<span style="color:#ffffff">The </span>  <span style="color:#ffffff"> _‘Sequence Browser’_ </span>  <span style="color:#ffffff"> section allows for playback of the model</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_53.png)

<span style="color:#ffffff">Expand ‘Regression Volume Plot’ and click the plot button</span>

<span style="color:#366092">Visualizing Shape Regression Results</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_54.png)

<span style="color:#ffffff">A volume plot shows the estimated volume from shape regression along with the volume of the original shape observations</span>

<span style="color:#ffffff">Shape Regression Debugging and Quality Control</span>

![](img/SlicerSALT-ShapeRegression-Tutorial_55.png)

<span style="color:#595959">If an error occurred\, you will be </span>

<span style="color:#595959">presented with a notification</span>

<span style="color:#595959">Error details may be viewed in the </span>  <span style="color:#595959"> __Error Log __ </span>  <span style="color:#595959">under </span>  <span style="color:#595959"> _View_ </span>

![](img/SlicerSALT-ShapeRegression-Tutorial_56.png)



* <span style="color:#595959">If RegressionComputation experiences an error\, carefully check parameter settings\, including:</span>
  * <span style="color:#595959">Input shapes 'Time Point' \- make sure all time points are within the 'Time point range'</span>
  * <span style="color:#595959">Check the input \.vtk shapes exist at the path selected and verify all \.vtk files are valid</span>
  * <span style="color:#595959">In some cases\, it may be necessary to reorient the surface normals of input shapes before model estimation</span>
* <span style="color:#595959">Use the RegressionVisualization module to view the estimated shape trajectory as an animation</span>
  * <span style="color:#595959">It is helpful to load the original observations displayed with transparency to visually assess model fit</span>


![](img/SlicerSALT-ShapeRegression-Tutorial_57.png)



* <span style="color:#595959">Use the RegressionVisualization module to view the volume measured after shape regression</span>
  * <span style="color:#595959">The volume plot can help to assess model fit and inform about possible overfitting</span>


![](img/SlicerSALT-ShapeRegression-Tutorial_58.png)

<span style="color:#ffffff">Acknowledgements \- Resources \- Questions</span>



* <span style="color:#ffffff">The ShapeRegressionExtension developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.</span>
* <span style="color:#ffffff">Github repository: </span>
      * _[ShapeRegression](https://github.com/KitwareMedical/ShapeRegressionExtension)_  <span style="color:#ffffff"> _ _ </span>
      * _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_
      * _[3D Slicer](https://github.com/Slicer/Slicer)_
* <span style="color:#ffffff">Forums:</span>
      * _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_
      * _[3D Slicer](https://discourse.slicer.org/)_  <span style="color:#ffffff"> </span>
* <span style="color:#ffffff">Papers: </span>
      * _[Estimation of Smooth Growth Trajectories with Controlled Accelerationo from Time Series Shape Data](https://www.ncbi.nlm.nih.gov/pubmed/21995054)_
      * _[Model Selection for Spatiotemporal Modeling of Early Childhood Sub\-cortical Development](http://research.engineering.nyu.edu/~fishbaugh/docs/fishbaugh_spie_2019.pdf)_
* <span style="color:#ffffff">For other remarks or questions\, please email: </span>
* <span style="color:#ffffff">james\.fishbaugh@</span>  <span style="color:#ffffff">kitware\.com</span>


![](img/SlicerSALT-ShapeRegression-Tutorial_59.png)

