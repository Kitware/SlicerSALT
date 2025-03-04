<span style="color:#ffffff">Shape Variation Analyzer</span>

<span style="color:#f2f2f2">User Tutorial</span>

<span style="color:#f2f2f2">Mateo lopez\, Priscille de Dumast\, Juan C\. Prieto\, Martin Styner\, Beatriz Paniagua </span>

<span style="color:#f2f2f2">December 2019</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_0.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_1.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_2.png)

<span style="color:#ffffff">ShapeVariationAnalyzer Tool Description</span>

<span style="color:#ffffff">Step 1: Create the different groups</span>

<span style="color:#ffffff">Step 2: Preview and group update  </span>

<span style="color:#ffffff">Step 3: Generate and explore models</span>

<span style="color:#ffffff">Step 4: Evaluate the models</span>

<span style="color:#366092">Description of ShapeVariationAnalyzer</span>

<span style="color:#595959"> __Shape Variation Analyzer \(SVA\)__ </span>  <span style="color:#595959"> allows the computation of PCA decomposition of groups of shapes in order be able to represent them in a lower dimensional space\. </span>  <span style="color:#595959"> __SVA__ </span>  <span style="color:#595959"> also allows the user to explore the generated PCA space and to evaluate the quality of the generated models\.</span>

<span style="color:#595959">The inputs meshes are vtk files\, they must have corresponding points to be processed by SVA\. If it is not the case\, SlicerSALT provides tools that are able to convert the data set\.</span>

<span style="color:#366092">Description of ShapeVariationAnalyzer</span>

<span style="color:#595959">The SVA tool consists on four steps: </span>

<span style="color:#595959"> _Input: 1 folder per group containing the vtk files_ </span>

<span style="color:#595959"> _Step 1_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Create the groups__ </span>  <span style="color:#595959"> </span>

<span style="color:#595959"> _Output: CSV file _ </span>

<span style="color:#595959"> _Step 2_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Preview and update__ </span>  <span style="color:#595959"> uses Shape Population Viewer</span>

<span style="color:#595959"> _Output: CSV file _ </span>

<span style="color:#595959"> _Step 3_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Computation and exploration__ </span>  <span style="color:#595959"> of the models</span>

<span style="color:#595959"> _Output: A mean shape for each group and a JSON file _ </span>

<span style="color:#595959"> _Step 4_ </span>  <span style="color:#595959"> : </span>  <span style="color:#595959"> __Evaluation__ </span>  <span style="color:#595959"> uses shapepca CLI</span>

<span style="color:#595959"> _Output: JSON file _ </span>

<span style="color:#366092">Step 1: Create the groups</span>

<span style="color:#595959"> _Input_ </span>  <span style="color:#595959">: Folders containing files  </span>

<span style="color:#595959">This step will generate a CSV file describing the location of each shape and their corresponding group\. To do so a folder per group should be created\. </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_3.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_4.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_5.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_6.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_7.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_8.png)

<span style="color:#595959"> _Output_ </span>  <span style="color:#595959">: CSV file</span>

<span style="color:#595959"> __Figure__ </span>  <span style="color:#595959">: Input/Output for the creation of groups</span>

<span style="color:#366092">Step 2: Preview and Update</span>

<span style="color:#595959">This step will allow the user to visualize the groups in Shape Population Viewer\. </span>

<span style="color:#595959">He will be able modify groups before computation\, if it is necessary\.</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_9.png)

<span style="color:#366092">Step 3: Generate and Explore Models </span>

<span style="color:#595959">Generating the PCA representation will:</span>

<span style="color:#595959">Compute the explained variance ratio and the cumulative sum of the explained variance ratio</span>

<span style="color:#595959">Project each group on the two first component</span>

<span style="color:#595959">Compute a mean shape for each group\.</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_10.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_11.png)

<span style="color:#366092">Step 3: Generate and Explore Models </span>

<span style="color:#595959">The exploration of the models will allows to:	</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_12.png)

<span style="color:#595959">Generate new shapes with sliders representing each component of the PCA model</span>

<span style="color:#595959">Visualize the distance of the current shape compared to the mean shape of the group\.</span>

<span style="color:#595959">visualize a particular member of a group\, or the mean shape of a sub\-group</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_13.png)

<span style="color:#000000">Individual population shape</span>

<span style="color:#366092">Step 4: Evaluate the models  </span>

<span style="color:#595959">This</span>  <span style="color:#595959"> _ _ </span>  <span style="color:#595959">step will evaluate the models by computing three values:</span>

_Model compactness:_  __ __

__A compact model is one that has as little variance as__

__possible and requires as few parameters as possible to define an instance\. __

_Model generalization: _

__The generalization ability of a model measures its__

__capability to represent unseen instances of the object class\. This is a fundamental__

__property as it allows a model to learn the characteristics of an object class__

__from a limited training set\. __

_Model specificity: _

__A specific model should only generate instances of the__

__object class that are similar to those in the training set\. It is useful to assess__

__this qualitatively by generating a population of instances using the model and__

__comparing them to the members of the training set\. __

<span style="color:#ffffff">Installation of SVA Tool</span>



* <span style="color:#ffffff">SVA tool can be used with two open\-source software platforms: </span>
      * <span style="color:#ffffff"> __SlicerSALT__ </span>  <span style="color:#ffffff">: which is the dissemination vehicle of powerful shape analysis methodology\. This software is a light\-weight\, customized version of 3D Slicer\. It contains SVA </span>  <span style="color:#ffffff"> _as a module_ </span>  <span style="color:#ffffff">\. </span>
      * <span style="color:#ffffff"> __3D Slicer__ </span>  <span style="color:#ffffff">: which is an open\-source and free software platform for medical image informatics\, image processing\, and three\-dimensional visualization\. SVA can be downloaded </span>  <span style="color:#ffffff"> _as an extension_ </span>  <span style="color:#ffffff">\.  </span>


<span style="color:#366092">SVA Installation on SlicerSALT</span>

<span style="color:#595959">Download the SlicerSALT packages for your respective operating system from the </span>  _[SlicerSALT website](https://salt.slicer.org/)_  <span style="color:#595959"> and install it\. SVA will be ready to use then\. </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_14.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_15.png)

<span style="color:#595959">Powered by Girder</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_16.png)

<span style="color:#366092">SVA Installation on 3D Slicer</span>

<span style="color:#595959">  Download 3D Slicer packages for your respective operating system on the </span>  _[3D Slicer website](https://www.slicer.org/)_  <span style="color:#595959"> and install it\.</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_17.png)

<span style="color:#366092">SVA Installation on 3D Slicer</span>

<span style="color:#595959">  In 3D Slicer\, open the Extension Manager</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_18.png)

<span style="color:#366092">SVA Installation on 3D Slicer</span>

<span style="color:#595959">  In the </span>  <span style="color:#595959"> _Install Extension_ </span>  <span style="color:#595959"> tab\, select </span>  <span style="color:#595959"> _ShapeVariationAnalyzer_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>

<span style="color:#595959"> Under </span>  <span style="color:#595959"> __ShapeVariationAnalyzer__ </span>  <span style="color:#595959">\, select the </span>  <span style="color:#595959"> _Install_ </span>  <span style="color:#595959"> button and restart Slicer when prompted \!\!\!\!\!\!\!\!\!  </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_19.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_20.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_21.png)

<span style="color:#366092">SVA Installation on 3D Slicer</span>

<span style="color:#595959">To visualize groups before the computation\,SVA uses </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> extension\. Shape Population Viewer can be installed as a 3D Slicer extension or as an external binary\. This module is included as part of the SlicerSALT package\.  </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_22.png)

<span style="color:#366092">SVA Installation on 3D Slicer</span>



* <span style="color:#595959">To install </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> as </span>  <span style="color:#595959"> _a 3D Slicer extension_ </span>  <span style="color:#595959">: </span>
    * <span style="color:#595959">Open </span>  <span style="color:#595959"> _Extension Manager_ </span>  <span style="color:#595959">\, in the </span>  <span style="color:#595959"> _Install Extensions _ </span>  <span style="color:#595959">tab\, select ‘</span>  <span style="color:#595959"> _Shape Analysis’_ </span>  <span style="color:#595959"> under </span>  <span style="color:#595959"> _Categories_ </span>
    * <span style="color:#595959"> Select the appropriate </span>  <span style="color:#595959"> _Install _ </span>  <span style="color:#595959">button and restart 3D Slicer when prompted</span>


![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_23.png)

<span style="color:#366092">SVA Installation on 3D Slicer</span>



* <span style="color:#595959">To install </span>  <span style="color:#595959"> __Shape Population Viewer__ </span>  <span style="color:#595959"> as an </span>  <span style="color:#595959"> _external binary_ </span>  <span style="color:#595959">: </span>
    * <span style="color:#595959"> Download ShapePopulationViewer package for your respective operating system on </span>  <span style="color:#009cff"> _NITRC website_ </span>
    * <span style="color:#595959"> In 3D Slicer\, open </span>  <span style="color:#595959"> _Application Settings _ </span>  <span style="color:#595959">in the </span>  <span style="color:#595959"> _Edit _ </span>  <span style="color:#595959">Menu\.  On the tab </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959">\, </span>  <span style="color:#595959"> __Add __ </span>  <span style="color:#595959">the folder where  ShapePopulationViewer is stored</span>
    * <span style="color:#595959"> Restart 3D Slicer</span>


![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_24.png)

<span style="color:#ffffff">ShapeVariationAnalyzer</span>

<span style="color:#595959">In 3D Slicer or in SlicerSALT\, select </span>  <span style="color:#595959"> _ShapeVariationAnalyzer_ </span>  <span style="color:#595959"> from the </span>  <span style="color:#595959"> _Modules_ </span>  <span style="color:#595959"> drop\-down menu \(</span>  <span style="color:#595959"> _Category:_ </span>  <span style="color:#595959"> Decomposition\) or on the Search bar\.  </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_25.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_26.png)

<span style="color:#366092">Setting up the input directories</span>



* <span style="color:#000000">The SVA tool process PCA models for different groups at the same time</span>
* <span style="color:#000000"> and a general model that combine all the groups\. To do so\, the input files should be </span>
* <span style="color:#000000">organized in folders\, one folder per group\. </span>
* <span style="color:#000000">Remember:</span>
  * <span style="color:#000000">Every file must have corresponding points</span>
  * <span style="color:#000000">Only \.vtk files are supported</span>


![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_27.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_28.png)

<span style="color:#366092">Create the Groups</span>

<span style="color:#000000"> __Tab: Creation of CSV file__ </span>  <span style="color:#000000"> </span>

<span style="color:#595959">To add a group\, select the desired folder and click the ‘Add Group’ Button to add it\. Note that adding a group will  give it a group  number</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_29.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_30.png)

<span style="color:#000000"> _/data_ </span>  <span style="color:#000000">/population/group1</span>

<span style="color:#366092">Edit a group folder</span>

<span style="color:#595959"> __Tab: Creation of CSV file __ </span>

<span style="color:#595959">To edit a group\, select the desired group number in the spin box\, two new options appears:</span>



    * <span style="color:#595959">Remove group: remove the current group from the list of groups</span>
    * <span style="color:#595959">Modify group: This option update the current group by associating it with the current selected folder  </span>


![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_31.png)

<span style="color:#000000"> _/data_ </span>  <span style="color:#000000">/population/group0</span>

<span style="color:#366092">Export the groups file</span>

<span style="color:#595959"> __Tab: Creation of CSV file __ </span>

<span style="color:#595959">When all the groups have been created\, use the Export button to save the CSV file describing the groups\. The path of this file is automatically passed to the other tabs of the module\. </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_32.png)

<span style="color:#366092">Visualize and update Groups</span>

<span style="color:#595959"> __Tab: Preview/Update Group__ </span>

<span style="color:#595959">To make sure that the groups are correctly defined\, SVA offers the possibility to visualize each element of a group using the Shape Population Viewer \(SPV\) module:</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_33.png)



    * <span style="color:#595959">Select all the shapes that you want to visualize by marking the corresponding check box</span>
    * <span style="color:#595959">Use the preview button to launch SPV</span>


<span style="color:#366092">Visualize and update Groups</span>

<span style="color:#595959"> __Tab: Preview/Update Group__ </span>

<span style="color:#595959">If a shape is identified as being part of the wrong group\, change his group number and use the Export button to update the csv file\. </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_34.png)

<span style="color:#366092">Generate and Explore</span>

<span style="color:#595959"> __Tab: Exploration__ </span>

<span style="color:#000000"> 1\): Generate the models</span>

<span style="color:#000000">Select the desired CSV file previously generated and use the Process and Export button to generate the models and import them in the explorer\. The exploration interface will appear:</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_35.png)

<span style="color:#000000">Generate and</span>

<span style="color:#000000"> load models</span>

<span style="color:#000000">Number of </span>

<span style="color:#000000">eigenvalues</span>

<span style="color:#000000">Hide / show </span>

<span style="color:#000000">the mean shape</span>

<span style="color:#000000">Evaluation parameter</span>

<span style="color:#000000">and launching</span>

<span style="color:#000000">Color mode </span>

<span style="color:#000000">selection</span>

<span style="color:#366092">Generate and Explore</span>

<span style="color:#595959"> __Tab: Exploration__ </span>



* <span style="color:#000000">2\): Save and load a model:</span>
* <span style="color:#000000">We recommend to save your models before starting the exploration by using the save button: specify a \.json file \(ex: exploration\.json\) where the exploration should be saved\. </span>
* <span style="color:#000000">The following files will be generated:</span>
    * __The specified JSON file  __
    * __A VTK file per group representing the mean shape of the group__
    * __A PYC file necessary for pca computation__
* __To load an existing exploration\, select a previously generated json file in the ‘JSON file’ field\.__


![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_36.png)

<span style="color:#366092">Generate and Explore</span>

<span style="color:#595959"> __Tab: Exploration__ </span>

<span style="color:#000000">3\)Exploration: Groups</span>

<span style="color:#000000">	Define colors for each groups\, navigate between groups using the 	group option\.   </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_37.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_38.png)

<span style="color:#366092">Generate and Explore</span>

<span style="color:#000000">Tab: Exploration</span>

<span style="color:#000000">3\)exploration: Eigenvalues</span>

<span style="color:#000000">	To start exploring the PCA space\, use the eigenvalues sliders</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_39.png)

<span style="color:#000000">	If you want to play with more sliders\, you can use the minimum explained variance and the maximum number of eigenvalues to add more sliders </span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_40.png)

<span style="color:#366092">Generate and Explore</span>

<span style="color:#000000">Tab: Exploration</span>

<span style="color:#000000">3\)exploration: Visualization of the distance </span>

<span style="color:#000000">It is possible to visualize the distance between the current shape and the mean shape by changing the color mode in the SVA interface\, keep in mind that the distance is computed using the corresponding points of the shape\, not the closest point\. </span>

<span style="color:#000000"> _Signed distance to mean shape_ </span>

<span style="color:#000000">From blue\(\<0\) to white\(0\) to red\(>0\)\. The Maximum and Minimum distance parameter allows to change the color range\. The white is fixed to 0\.</span>

<span style="color:#000000"> _Unsigned distance to mean shape_ </span>

<span style="color:#000000">From white\(0\) to red\. The Maximum distance parameter allows to change the color range</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_41.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_42.png)

<span style="color:#366092">Generate and Explore</span>

<span style="color:#000000">Tab: Exploration</span>

<span style="color:#000000">3\)exploration: Plot Visualization and interaction</span>

<span style="color:#000000">	By default\, the Explained Variance Ratio plot appears when a model is generated or loaded\. It shows\, for the selected group\, the explained variance for each eigenvalue in a bar plot\, and the cumulative sum of the explained variance\.</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_43.png)

<span style="color:#366092">Generate and Explore</span>

<span style="color:#000000">Tab: Exploration</span>

<span style="color:#000000">3\)exploration: Plot Visualization and interaction</span>

<span style="color:#000000">To see the projection of the group on the 2 first component of the PCA model\, select the 'PCA projection plot chart' plot using the top left menu of the plot area:</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_44.png)

<span style="color:#000000">Use interaction mode to select point on the plot</span>

__On this plot\, you can select a point\, the corresponding shape will be displayed by updating the sliders value\. If you select a group of points\, the mean shape of those points will be displayed\. __

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_45.png)

<span style="color:#366092">Evaluate the models</span>

<span style="color:#000000">Tab: Exploration</span>

<span style="color:#000000">4\) Evaluation:</span>

<span style="color:#000000">	To make sure that the generated models are well defined\, SVA can evaluate the models by computing the compactness\, specificity and generalization and visualize them in the plot area\.</span>



* <span style="color:#000000">Parameters: 	</span>
  * <span style="color:#000000">The number of eigenvalues are determined by the number of sliders available when the evaluation is launched\.</span>
  * <span style="color:#000000">The number of random shapes parameter allow to choose how many shapes should be generated to compute the specificity\. </span>


<span style="color:#000000">	To launch the evaluation\, use the Evaluate models button\. The evaluation is a long process\, if you want to abort it\, you can use the same button\.</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_46.png)

<span style="color:#366092">Evaluate the models</span>

<span style="color:#000000">Tab: Exploration</span>

<span style="color:#000000">4\) Visualize the evaluation:</span>

<span style="color:#000000">	When the evaluation is done\, you can visualize the results by selecting in the plot area menu the PCA Specificity plot chart\, the PCA Compactness plot chart or the PCA Generalization plot chart\.</span>

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_47.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_48.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_49.png)

![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_50.png)

<span style="color:#ffffff">Acknowledgements \-</span>

<span style="color:#ffffff"> Resources \- Questions</span>



* <span style="color:#ffffff">The ShapeVariationAnalyzer developers gratefully acknowledge funding for this project provided by NIH NIBIB R01EB021391 \(Shape Analysis Toolbox for Medical Image Computing Projects\)\, as well as the Slicer community\.</span>
* <span style="color:#ffffff">Github repository: </span>
      * _[ShapeVariationAnalyzer](https://github.com/DCBIA-OrthoLab/ShapeVariationAnalyzer)_  <span style="color:#ffffff"> _ _ </span>
      * _[SlicerSALT](https://github.com/Kitware/SlicerSALT)_
      * _[3D Slicer](https://github.com/Slicer/Slicer)_
* <span style="color:#ffffff">Forums:</span>
      * _[SlicerSALT](https://discourse.slicer.org/t/about-the-slicersalt-category/47)_
      * _[3D Slicer](https://discourse.slicer.org/)_  <span style="color:#ffffff"> </span>
* <span style="color:#ffffff">For other remarks or questions\, please email: </span>
* _[beatriz\.paniagua@kitware\.com](mailto:beatriz.paniagua@kitware.com)_
* _[Juanprietob@gmail\.com](mailto:Juanprietob@gmail.com)_


![](img/SlicerSALT-ShapeVariationAnalyzer-Tutorial_51.png)

