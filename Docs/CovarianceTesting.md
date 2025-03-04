<span style="color:#ffffff">Covariate Significance Testing</span>

<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">Mahmoud Mostapha\, Jared Vicory\, Chao Huang\, Martin Styner\, Beatriz Paniagua </span>

<span style="color:#f2f2f2">July 2020</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_0.png)

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_1.png)

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_2.png)

<span style="color:#ffffff">Covariate Significance Testing</span>  <span style="color:#000000"> </span> Description



* This module provides the following functions:
  * Model Fitting & Hypothesis Testing
  * Visualize Statistical Results
* _Important note:_  __ If you are downloading this module as part of the Slicer Extension mechanism \(slides 7\-9\) then it will be named multivariate functional shape data analysis \(MFSDA\)__


<span style="color:#366092">Description of Covariate Significance Testing</span>

<span style="color:#595959"> __Covariate Significance Testing __ </span>  <span style="color:#595959">provides an interface for MFSDA \(Multivariate Functional Shape Data Analysis\) method\, which is a Python based tool for statistical shape analysis\. </span>

<span style="color:#595959">A multivariate varying coefficient model is introduced to build the association between the multivariate shape measurements and demographic information and other clinical variables\. </span>

<span style="color:#595959">Statistical inference\, i\.e\.\, hypothesis testing\, is also included in this tool\, which can be used in investigating whether some covariates of interest are significantly associated with the shape information\. The hypothesis testing results are further used in clustering based analysis\, i\.e\.\, significant suregion detection\.</span>

<span style="color:#366092">Description of Covariate Significance Testing</span>

<span style="color:#595959">The Covariate Significance Testing tool has of the following structure: </span>

<span style="color:#595959">A VTK file providing a shape template for visualizing p\-values</span>

<span style="color:#595959">A single CSV file containing the location of the surface meshes and the corresponding covariates to be tested</span>

<span style="color:#595959">A VTK file providing a common coordinates for input surfaces</span>

<span style="color:#595959"> _Inputs: Surface Meshes \+ Covariate Matrix \+ Spherical Template \+ Shape Template _ </span>

<span style="color:#595959"> __Covariate Significance Testing __ </span>  <span style="color:#595959">uses MFSDA\_run & MFSDA\_createShapes CLIs</span>

<span style="color:#595959"> _Output: Fitted Model Parameters \+ P\-Values \+ Shape Template Mesh with Scalars_ </span>

<span style="color:#595959">A JSON file containing the parameters of the fitted statistical model</span>

<span style="color:#595959">A JSON file containing the resultant p\-values</span>

<span style="color:#595959">A VTK file of the input shape template with fitted model parameters and p\-values as point data scalars for visualization</span>

Installation of Covariate Significance Testing Tool

Covariate Significance Testing tool can be used with  __SlicerSALT__  platform as a  _module_ \, which is the dissemination vehicle of powerful shape analysis methodology\. This software is a light\-weight\, customized version of 3D Slicer\.

<span style="color:#366092">Covariate Significance Testing Installation on SlicerSALT</span>

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  <span style="color:#0000ff"> _[SlicerSALT website](http://salt.slicer.org/)_ </span>  <span style="color:#595959"> and install it\. Covariate Significance Testing will be ready to use as a module\.</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_3.png)

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_4.png)

<span style="color:#595959">Powered by Girder</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_5.png)

<span style="color:#366092">MFSDA Installation on 3D Slicer</span>

<span style="color:#595959">  Download 3D Slicer packages for your respective operating system on the </span>  _[3D Slicer website](https://www.slicer.org/)_  <span style="color:#595959"> and install it\.</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_6.png)

<span style="color:#366092">MFSDA Installation on 3D Slicer</span>

<span style="color:#595959">  In 3D Slicer\, open the Extension Manager</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_7.png)

<span style="color:#366092">MFSDA Installation on 3D Slicer</span>

<span style="color:#595959">  In the </span>  <span style="color:#595959"> _Install Extension_ </span>  <span style="color:#595959"> tab\, select </span>  <span style="color:#595959"> _MFSDA_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>

<span style="color:#595959"> Under </span>  <span style="color:#595959"> __MFSDA__ </span>  <span style="color:#595959">\, select the </span>  <span style="color:#595959"> _Install_ </span>  <span style="color:#595959"> button and restart Slicer when prompted   </span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_8.png)

<span style="color:#366092">Covariate Significance Testing Module </span>

<span style="color:#595959">In SlicerSALT\, select </span>  <span style="color:#595959"> _Covariate Significance Testing Module _ </span>  <span style="color:#595959">\(in Slicer\, select </span>  <span style="color:#595959"> __MFSDA__ </span>  <span style="color:#595959">\) from the </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959"> drop\-down menu \(</span>  <span style="color:#595959"> _Category:_ </span>  <span style="color:#595959"> Shape Analysis\) or on the Search bar </span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_9.png)

<span style="color:#366092">Setting up Input Files</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input CSV File_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the csv file which contains the location of input surface meshes \(\*\.vtk\) and corresponding covariates</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_10.png)

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_11.png)

<span style="color:#000000">First column contains the location of input surface vtk files </span>

<span style="color:#000000">Each additional column represent a covariate to be tested\, which can be categorical or continuous</span>

<span style="color:#000000">Example of an input CSV file with one categorical covariate</span>

<span style="color:#366092">Input Surface Meshes Visualization</span>

<span style="color:#595959">Shape Population Viewer can be used to check the input surface meshes\, where the same CSV file as its input</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_12.png)

<span style="color:#366092">Input Surface Meshes Visualization</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_13.png)

<span style="color:#366092">Setting up Input Files</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Spherical Template_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the vtk file which provides a common coordinates for the of input surface meshes</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_14.png)

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_15.png)

<span style="color:#000000">Example of an input spherical template file\, which can be an average surface or one of the input surfaces</span>

<span style="color:#366092">Setting up Input Files</span>

<span style="color:#595959">For </span>  <span style="color:#595959"> _Input Shape for p\-values_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the vtk file which will be used to visualize the fitted model parameters and the resulted p\-values</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_16.png)

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_17.png)

<span style="color:#000000">Example of an input shape for p\-values file\, which can be an average surface or one of the input surfaces</span>

<span style="color:#366092">Setting up Output Directory</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_18.png)

<span style="color:#595959">For </span>  <span style="color:#595959"> _Output Files Directory_ </span>  <span style="color:#595959"> _\,_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">select the folder where the module will store the output files</span>

<span style="color:#366092">Running Covariate Significance Testing Module </span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_19.png)

<span style="color:#595959">Click on the </span>  <span style="color:#595959"> _Run_ </span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">button\, to run the MFSDA\_run & MFSDA\_createShapes CLIs on the provided inputs files</span>

<span style="color:#595959"> _SlicerSALT Error Log_ </span>  <span style="color:#595959"> can also be used for debugging if the module was completed with errors\. </span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_20.png)

<span style="color:#595959"> _SlicerSALT Error Log_ </span>  <span style="color:#595959"> can also be used for debugging if the module was completed with errors\. </span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_21.png)

<span style="color:#595959">The outputs files for the Covariate Significance Testing Module  are stored in the output folder specified by the user: </span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_22.png)

<span style="color:#000000">Fitted model parameters</span>

<span style="color:#000000">Shape template with Scalars</span>

<span style="color:#000000">Hypothesis testing p\-values</span>

<span style="color:#000000">The output files generated by running Covariate Significance Testing </span>

<span style="color:#366092">Output Shape Template Visualization</span>

<span style="color:#595959">Shape Population Viewer can be used also to visualize the output shape template with fitted model parameters and p\-values as scalars</span>

![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_23.png)

Acknowledgements \- Resources \- Questions



* The MFSDA developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.
* Github repository:
      * _[MFSDA](https://github.com/DCBIA-OrthoLab/MFSDA_Python)_  _ _
      * _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_
      * _[3D Slicer](https://github.com/Slicer/Slicer)_
* Forums:
      * _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_
      * _[3D Slicer](https://discourse.slicer.org/)_
* For other remarks or questions\, please email:
* beatriz\.paniagua@kitware\.com


![](img/SlicerSALT-CovarianceSignificanceTesting-Tutorial_24.png)

