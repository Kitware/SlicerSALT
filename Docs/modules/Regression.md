# Shape Regression User Tutorial

Authors: James Fishbaugh\, Guido Gerig\, Laura Pascal\, Jared Vicory\, Beatriz Paniagua

Collaborators: 

![](img/SlicerSALT-ShapeRegression-Tutorial_0.png)
![](img/SlicerSALT-ShapeRegression-Tutorial_1.png)

## Outline

 1\)    Description of Shape Regression

 2\)    Installing the Software

 3\)    Shape Regression Workflow

 4\)    Debugging and Quality Control

 5\)    Acknowledgments and Resources

## Description of Shape Regression

![](img/SlicerSALT-ShapeRegression-Tutorial_2.png)

Shape regression consists of estimating a continuous shape sequence which best matches a set of observed shapes. We use a growth model that represents anatomical evolution by a continuous deformation of space.

![](img/SlicerSALT-ShapeRegression-Tutorial_3.png)

This was done before by Thomas D'Arcy Thompson.

![](img/SlicerSALT-ShapeRegression-Tutorial_4.jpg)

![](img/SlicerSALT-ShapeRegression-Tutorial_5.jpg)

### Acceleration Controlled Shape Regression

 Deformations are parameterized by a flow of deformations by    acceleration    vectors\, which produce velocity\, which in turn results in a change of position\.

![](img/SlicerSALT-ShapeRegression-Tutorial_8.png)

We define the acceleration field $a(x(t))$

Where $x_i$ is the shape points carrying a point force vector $\alpha_i$

Where $K(x,y)$ is a kernel with standard deviation $\lambda_V$

![](img/SlicerSALT-ShapeRegression-Tutorial_11.png)

The time varying deformation $\phi_t(x_i)$ is given by the equation below, with initial position $x_i(0)$ and initial velocity $\dot{x}_i(0)$

![](img/SlicerSALT-ShapeRegression-Tutorial_13.png)

### Impact of Parameters

 Size of deformation kernel: The  distance  at  which  neighboring  points  move  in  correlation\. Higher values result in mostly rigid deformation\, while lower values allow points a greater degree of independent movement\. 

 Size of shape matching kernel: The scale at which shape differences are considered noise\.  For matching very detailed shape features\, choose a small value\.  For noisy observations with spurious features\, set this value larger than the size of the features\.

 Regularity weight: A low weight on regularity results in models which closely match observed data\, tending towards interpolation \(rather than regression\) the weight goes to zero\.

See    “Model selection for spatiotemporal modeling of early childhood sub\-cortical development” SPIE Medical Imaging \(2019\)    for more detail

## Installing the Software

### Installation of ShapeRegression Module through SlicerSALT

Download the SlicerSALT packages for your respective operating system from the   _[SlicerSALT website](http://salt.slicer.org/)_   and install it\. 

![](img/SlicerSALT-ShapeRegression-Tutorial_16.png)

![](img/SlicerSALT-ShapeRegression-Tutorial_17.png)

### Installation of ShapeRegression Module through 3D Slicer

  In 3D Slicer\, open the Extension Manager

![](img/SlicerSALT-ShapeRegression-Tutorial_20.png)

Installation of ShapeRegression Module In 3D Slicer

 In the    _Install Extension_    tab\, select    _Shape Regression_    under    _Categories_ 

 Under    ShapeRegressionExtension   \, select the    _Install_    button and restart Slicer when prompted   

![](img/SlicerSALT-ShapeRegression-Tutorial_21.png)

## Shape Regression Workflow

1\)    Regression Computation    – Model estimation

2\)    Regression Visualization    – Visualization of estimated shape change

### Shape Regression Model Estimation

After installing, begin by selecting ‘   Regression Computation   ’

![](img/SlicerSALT-ShapeRegression-Tutorial_22.png)

Then download sample data to a directory of your choice

![](img/SlicerSALT-ShapeRegression-Tutorial_23.png)

Click the button to select the directory with input vtk shapes

![](img/SlicerSALT-ShapeRegression-Tutorial_24.png)


Navigate to the directory containing the tutorial shapes

![](img/SlicerSALT-ShapeRegression-Tutorial_25.png)

**Setting Parameters**

_Time point_    automatically populated if shape names have time\-suffix

![](img/SlicerSALT-ShapeRegression-Tutorial_26.png)

 _Kernel width_    initialized as 50% of the smallest extent of the shape

![](img/SlicerSALT-ShapeRegression-Tutorial_27.png)

 _Shape index_    indicates shape correspondence in multi\-objects

![](img/SlicerSALT-ShapeRegression-Tutorial_28.png)

_Weight_ controls the importance of each shape in model estimation

![](img/SlicerSALT-ShapeRegression-Tutorial_29.png)

Leave all settings at default and expand    _‘Time Parameters’_ 

![](img/SlicerSALT-ShapeRegression-Tutorial_30.png)

_Time point range_ is set using the min and max from input shapes

![](img/SlicerSALT-ShapeRegression-Tutorial_31.png)

Leave all settings at default and expand    _‘Deformation Parameters’_ 

![](img/SlicerSALT-ShapeRegression-Tutorial_32.png)

_The width of the deformation kernel_ lowers values result in more non\-linear changes\, higher values tend towards rigid deformation\.

![](img/SlicerSALT-ShapeRegression-Tutorial_33.png)

For shape inputs with only a few hundred vertices\, chose ‘exact’\, otherwise ‘p3m’ usualy results in faster model estimation\.

![](img/SlicerSALT-ShapeRegression-Tutorial_34.png)

_Regularity weight_ balances data\-matching and regularity\. Lower values favor accurate data\-matching\.

![](img/SlicerSALT-ShapeRegression-Tutorial_35.png)


Leave all settings at default and expand    _‘Output Parameters’_ 

![](img/SlicerSALT-ShapeRegression-Tutorial_36.png)


Click to choose an output directory for the estimated model

![](img/SlicerSALT-ShapeRegression-Tutorial_37.png)


Create a new folder called ‘output’

![](img/SlicerSALT-ShapeRegression-Tutorial_38.png)

Leave all settings at default and expand    _‘Optional Parameters’_ 

![](img/SlicerSALT-ShapeRegression-Tutorial_39.png)


Change the maximum number of iterations to ‘200’

![](img/SlicerSALT-ShapeRegression-Tutorial_40.png)

**Model Estimation**

Click ‘Run Shape4D’

![](img/SlicerSALT-ShapeRegression-Tutorial_41.png)

Estimation may take several minutes to finish

![](img/SlicerSALT-ShapeRegression-Tutorial_42.png)

Estimation has converged when    _‘Status: Completed’_    is displayed

![](img/SlicerSALT-ShapeRegression-Tutorial_43.png)

**Visualizing Shape Regression Results**

We can now visualize the model by selecting ‘   RegressionVisualization’ 

![](img/SlicerSALT-ShapeRegression-Tutorial_44.png)

Click to choose the directory containing the estimated model

![](img/SlicerSALT-ShapeRegression-Tutorial_45.png)

Choose the output directory from ‘   Regression Computation   ’

![](img/SlicerSALT-ShapeRegression-Tutorial_46.png)

The rootname is automatically populated if a final model is found in the directory\. Otherwise rootname has to be specified\.

![](img/SlicerSALT-ShapeRegression-Tutorial_47.png)

Click ‘   _Create Sequence_   ’ button to load the model sequence

![](img/SlicerSALT-ShapeRegression-Tutorial_48.png)

Hold right mouse button to zoom\. Hold left button to rotate\.

![](img/SlicerSALT-ShapeRegression-Tutorial_49.png)

Expand ‘   _Sequence Visualization Options’_ 

![](img/SlicerSALT-ShapeRegression-Tutorial_50.png)

Change the color map to    _‘velocity’ _   to visualize speed of shape change

![](img/SlicerSALT-ShapeRegression-Tutorial_51.png)

The    _‘Sequence Browser’_    section allows for playback of the model

![](img/SlicerSALT-ShapeRegression-Tutorial_52.png)

Expand ‘Regression Volume Plot’ and click the plot button

![](img/SlicerSALT-ShapeRegression-Tutorial_53.png)

A volume plot shows the estimated volume from shape regression along with the volume of the original shape observations

![](img/SlicerSALT-ShapeRegression-Tutorial_54.png)

### Shape Regression Debugging and Quality Control

If an error occurred\, you will be presented with a notification. You can visualize error details in the    Error Log    under    _View_ 

![](img/SlicerSALT-ShapeRegression-Tutorial_55.png)



![](img/SlicerSALT-ShapeRegression-Tutorial_56.png)



* If RegressionComputation experiences an error\, carefully check parameter settings\, including:
  * Input shapes 'Time Point' \- make sure all time points are within the 'Time point range'
  * Check the input \.vtk shapes exist at the path selected and verify all \.vtk files are valid
  * In some cases\, it may be necessary to reorient the surface normals of input shapes before model estimation
* Use the RegressionVisualization module to view the estimated shape trajectory as an animation
  * It is helpful to load the original observations displayed with transparency to visually assess model fit


![](img/SlicerSALT-ShapeRegression-Tutorial_57.png)



* Use the RegressionVisualization module to view the volume measured after shape regression
  * The volume plot can help to assess model fit and inform about possible overfitting


![](img/SlicerSALT-ShapeRegression-Tutorial_58.png)


## Acknowledgements \- Resources \- Questions

<ul>
  <li> The ShapeRegressionExtension developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 (Shape Analysis Toolbox for Medical Image Computing Projects), as well as the Slicer community.</li>
  <li>Github repository:</li>
      <ul>
            <li><a href="https://github.com/KitwareMedical/ShapeRegressionExtension">ShapeRegression</a></li>
            <li><a href="https://salt.slicer.org">SlicerSALT</a></li>
            <li><a href="https://github.com/Slicer/Slicer">3D Slicer</a></li>
      </ul>
  <li>Forums:</li>
      <ul>
            <li><a href="https://discourse.slicer.org/t/about-the-slicersalt-category/47">SlicerSALT</a></li>
            <li><a href="https://discourse.slicer.org/">3D Slicer</a></li>
      </ul>
  <li>Papers:</li>
      <ul>
            <li><a href="https://www.ncbi.nlm.nih.gov/pubmed/21995054">Estimation of Smooth Growth Trajectories with Controlled Accelerationo from Time Series Shape Data.</a></li>
            <li><a href="http://research.engineering.nyu.edu/~fishbaugh/docs/fishbaugh_spie_2019.pdf">Model Selection for Spatiotemporal Modeling of Early Childhood Sub\-cortical Development</a></li>
      </ul>  
  <li>For other remarks or questions, please email: beatriz.paniagua@kitware.com</li>
</ul>
