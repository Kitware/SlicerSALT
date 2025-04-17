# Bundled Extensions

SlicerSALT integrates and bundles several extensions as part of its distribution.
The table below lists these bundled extensions, providing direct links to their
respective GitHub repositories and Quality Assurance dashboards (CDash) for monitoring
build, test, and packaging status.

* **Issue Reporting**: Report issues directly in the extension’s GitHub repository.

* If the repository is a fork, verify the issue exists upstream and report it there instead.

* Extensions bundled with SlicerSALT are also typically available individually through the
  regular Slicer Extensions Manager, unless otherwise indicated.

| Extension Name                                                        | Quality Assurance Dashboard (CDash)                                                               |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [MeshToLabelMap][gh-MeshToLabelMap]                                   | [stable][cdash-MeshToLabelMap] - [preview][cdash-prev-MeshToLabelMap]                             |
| [SlicerSkeletalRepresentation][gh-SlicerSkeletalRepresentation]       | [stable][cdash-SlicerSkeletalRepresentation] - [preview][cdash-prev-SlicerSkeletalRepresentation] |
| [GROUPS][gh-GROUPS]                                                   | Distributed as part of [SPHARM-PDM][gh-SPHARM-PDM] extension                                      |
| [MFSDA_Python][gh-MFSDA_Python]                                       | Bundled only; Historically distributed and retired on 2022-03-25                                  |
| [ShapeVariationAnalyzer][gh-ShapeVariationAnalyzer]                   | [stable][cdash-ShapeVariationAnalyzer] - [preview][cdash-prev-ShapeVariationAnalyzer]             |
| [ProcrustesRegistrationModule][gh-ProcrustesRegistrationModule]       | Bundled only; not distributed separately                                                          |
| [ModelToModelDistance][gh-ModelToModelDistance]                       | [stable][cdash-ModelToModelDistance] - [preview][cdash-prev-ModelToModelDistance]                 |
| [shape4D][gh-shape4D]                                                 | Distributed as part of [ShapeRegressionExtension][gh-ShapeRegressionExtension] extension          |
| [ShapePopulationViewer][gh-ShapePopulationViewer]                     | [stable][cdash-ShapePopulationViewer] - [preview][cdash-prev-ShapePopulationViewer]               |
| [ShapeRegressionExtension][gh-ShapeRegressionExtension]               | [stable][cdash-ShapeRegressionExtension] - [preview][cdash-prev-ShapeRegressionExtension]         |
| [SPHARM-PDM][gh-SPHARM-PDM]                                           | [stable][cdash-SPHARM-PDM] - [preview][cdash-prev-SPHARM-PDM]                                     |
| [RegistrationBasedCorrespondence][gh-RegistrationBasedCorrespondence] | Bundled only; not distributed separately                                                          |
| [SlicerDentalModelSeg][gh-SlicerDentalModelSeg]                       | [stable][cdash-SlicerDentalModelSeg] - [preview][cdash-prev-SlicerDentalModelSeg]                 |
| [SlicerDWD][gh-SlicerDWD]                                             | Bundled only; not distributed separately                                                          |
| [SlicerPipelines][gh-SlicerPipelines]                                 | [stable][cdash-SlicerPipelines] - [preview][cdash-prev-SlicerPipelines]                           |
| [SlicerSurfaceLearner][gh-SlicerSurfaceLearner]                       | [stable][cdash-SlicerSurfaceLearner] - [preview][cdash-prev-SlicerSurfaceLearner]                 |
| [SRepHypothesisTesting][gh-SRepHypothesisTesting]                     | Bundled only; not distributed separately                                                          |
| [HierarchicalGeodesicModeling][gh-HierarchicalGeodesicModeling]       | Bundled only; not distributed separately                                                          |
| [DifferenceStatistics][gh-DifferenceStatistics]                       | Bundled only; not distributed separately                                                          |

<!-- ---------------------------------------------------------------------- -->
[gh-MeshToLabelMap]: https://github.com/DCBIA-OrthoLab/AnglePlanes-Extension
[gh-SlicerSkeletalRepresentation]: https://github.com/KitwareMedical/SlicerSkeletalRepresentation
[gh-GROUPS]: https://github.com/slicersalt/GROUPS
[gh-MFSDA_Python]: https://github.com/slicersalt/MFSDA_Python
[gh-ShapeVariationAnalyzer]: https://github.com/slicersalt/ShapeVariationAnalyzer
[gh-ProcrustesRegistrationModule]: https://github.com/slicersalt/ProcrustesRegistrationModule
[gh-ModelToModelDistance]: https://github.com/slicersalt/3DMetricTools
[gh-shape4D]: https://github.com/slicersalt/shape4D
[gh-ShapePopulationViewer]: https://github.com/slicersalt/ShapePopulationViewer
[gh-ShapeRegressionExtension]: https://github.com/KitwareMedical/ShapeRegressionExtension
[gh-SPHARM-PDM]: https://github.com/slicersalt/SPHARM-PDM
[gh-RegistrationBasedCorrespondence]: https://github.com/slicersalt/RegistrationBasedCorrespondence
[gh-SlicerDentalModelSeg]: https://github.com/slicersalt/SlicerDentalModelSeg
[gh-SlicerDWD]: https://github.com/slicersalt/SlicerDWD
[gh-SlicerPipelines]: https://github.com/KitwareMedical/SlicerPipelines
[gh-SlicerSurfaceLearner]: https://github.com/KitwareMedical/SlicerSurfaceLearner
[gh-SRepHypothesisTesting]: https://github.com/slicersalt/SRepHypothesisTesting
[gh-HierarchicalGeodesicModeling]: https://github.com/KitwareMedical/HierarchicalGeodesicModeling
[gh-DifferenceStatistics]: https://github.com/slicersalt/DifferenceStatistics

<!-- ---------------------------------------------------------------------- -->
[cdash-MeshToLabelMap]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=MeshToLabelMap
[cdash-SlicerSkeletalRepresentation]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SkeletalRepresentation
<!-- GROUPS -->
<!-- MFSDA_Python -->
[cdash-ShapeVariationAnalyzer]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ShapeVariationAnalyzer
[cdash-ModelToModelDistance]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ModelToModelDistance
<!-- ProcrustesRegistrationModule -->
<!-- shape4D -->
[cdash-ShapePopulationViewer]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ShapePopulationViewer
[cdash-ShapeRegressionExtension]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ShapeRegressionExtension
[cdash-SPHARM-PDM]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SPHARM-PDM
<!-- RegistrationBasedCorrespondence -->
[cdash-SlicerDentalModelSeg]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SlicerDentalModelSeg
<!-- SlicerDWD -->
[cdash-SlicerPipelines]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SlicerPipelines
[cdash-SlicerSurfaceLearner]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SurfaceLearner
<!-- SRepHypothesisTesting -->
<!-- HierarchicalGeodesicModeling -->
<!-- DifferenceStatistics -->

<!-- ---------------------------------------------------------------------- -->
[cdash-prev-MeshToLabelMap]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=MeshToLabelMap
[cdash-prev-SlicerSkeletalRepresentation]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SkeletalRepresentation
<!-- GROUPS -->
<!-- MFSDA_Python -->
[cdash-prev-ShapeVariationAnalyzer]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ShapeVariationAnalyzer
[cdash-prev-ModelToModelDistance]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ModelToModelDistance
<!-- ProcrustesRegistrationModule -->
<!-- shape4D -->
[cdash-prev-ShapePopulationViewer]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ShapePopulationViewer
[cdash-prev-ShapeRegressionExtension]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=ShapeRegressionExtension
[cdash-prev-SPHARM-PDM]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SPHARM-PDM
<!-- RegistrationBasedCorrespondence -->
[cdash-prev-SlicerDentalModelSeg]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SlicerDentalModelSeg
[cdash-prev-SlicerPipelines]: https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SlicerPipelines
[cdash-prev-SlicerSurfaceLearner]: https://slicer.cdash.org/index.php?project=SlicerStable&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=SurfaceLearner
<!-- SRepHypothesisTesting -->
<!-- HierarchicalGeodesicModeling -->
<!-- DifferenceStatistics -->
