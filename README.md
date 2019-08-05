
<img src="SlicerSALT.png" width="512">


Introduction
------------
SlicerSALT is an open-source, free comprehensive software that will allow biomedical scientists to precisely locate shape changes in their imaging studies. This software called Slicer Shape AnaLysis Toolbox (SlicerSALT), will enhance the intuitiveness and ease of use for such studies, as well as allow researchers to find shape changes with higher statistical power. Altogether this constitutes a crucial resource for the imaging field that will enable many and important new findings in biomedical imaging studies.

Prerequisites
-------------
* [Slicer Prerequisites]
* [Fortran Compiler]

Checkout
--------
* Register [Github Access]() to create an account
* Create SSH keys associated to your account: [SSH Key Generation Instructions].
    * Recommended: keep the passphrase empty for your SSH key to let the Superbuild work without interruptions
* Add the SSH key to your Github account: [Steps to add SSH Key to Github].
* Clone the repository and follow platform specific instructions below:

        $ git clone git@github.com:Kitware/slicerSALT.git

Build
-----

Make sure that you can compile Slicer OR have the Prerequisites for Slicer: [Slicer Build Instructions].

### Windows

Tested Development environment: [Slicer Windows Dev Environment].

1. Run CMake (cmake-gui) from the Windows Start Menu
    * Set the build directory `C:\slicerSALT-Debug` or `C:\slicerSALT-Release`
    * Select your compiler: Visual Studio 14 2015 Win64
    * If using a newer version of Visual Studio, be sure to specify the 2015 toolset (v140)
    * Configure using default options. You may get a configuration error that `QT_QMAKE_EXECUTABLE` is not set, which is normal.
    * Verify that `QT_QMAKE_EXECUTABLE` is set to the QT version that was used to compile Slicer
    * Click generate the close cmake-gui
2. Build (be prepared to wait for some hours!)
    * Open the top-level slicerSALT.sln in the build directory
    * If you're trying to build Release mode, make sure to set the active configuration to Release 
    * Build Solution!
3. slicerSALT executable lives in `path/to/slicerSALT-build/S-bld/Slicer-build/`

### Unix-like

***MacOSX Note:*** Beginning XCode 7 support for OpenMP has been removed. So if you're using XCode 7 or above OpenMP will be bypassed during build process.

        $ mkdir slicerSALT-build
        $ cd slicerSALT-build

1. Configure CMake
    *       $ ccmake ../slicerSALT
    * Point CMake to the QT version that was used to compile Slicer
    * ___MacOSX:___ Set variable CMAKE_OSX_DEPLOYMENT_TARGET to 10.9 (Mavericks) / 10.10 (Yosemite) / 10.11 (El Capitan)
2. Build (be prepared to wait for some hours!)

        $ make -j4
3. slicerSALT executable lives in `path/to/slicerSALT-build/S-bld/Slicer-build/`

Contribute
----------
See [CONTRIBUTING.md][] for instructions to contribute.

[CONTRIBUTING.md]: CONTRIBUTING.md

Package
-------


Resources
---------
* [3D Slicer Developer Wiki](http://wiki.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers)


[Fork the slicerSALT Repository]: https://help.github.com/articles/fork-a-repo/
[Slicer Coding and Commit Style Guide]: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Style_Guide
[Slicer Prerequisites]: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Build_Instructions#PREREQUISITES
[Fortran Compiler]: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Fortran
[Slicer Build Instructions]: https://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions
[SSH Key Generation Instructions]: https://gitlab.kitware.com/help/ssh/README
[Steps to add SSH Key to Github]: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/
[Slicer Windows Dev Environment]: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Build_Instructions#Windows
