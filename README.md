SlicerSALT
======================

![SlicerSALT by Kitware.](https://www.nitrc.org/project/screenshot.php?group_id=308&screenshot_id=553)

Prerequisites
-------------


Checkout
--------


Build
-----

* Make sure that you can compile Slicer. Instructions can be found [here](https://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions)
* Register [Gitlab Access]() to create an account
* To create SSH keys associated to your account follow instructions [here](https://gitlab.kitware.com/help/ssh/README)
* Clone the repository and follow platform specific instructions below:

        $ git clone git@github.com:Kitware/slicerSALT.git

Windows
-------
Tested Development environment: as specified [here](https://www.slicer.org/wiki/Documentation/Nightly/Developers/Build_Instructions#Windows)

1. Run CMake (cmake-gui) from the Windows Start Menu
    * Set the build directory `C:\slicerSALT-Debug` or `C:\slicerSALT-Release`
    * Select your compiler: Visual Studio 12 2013 Win64
    * Configure using default options. You may get a configuration error that `QT_QMAKE_EXECUTABLE` is not set, which is normal.
    * Verify that `QT_QMAKE_EXECUTABLE` is set to the QT version that was used to compile Slicer
    * Click generate the close cmake-gui
2. Build (be prepared to wait for some hours!)
    * Open the top-level slicerSALT.sln in the build directory
    * If you're trying to build Release mode, make sure to set the active configuration to Release 
    * Build Solution!
3. slicerSALT executable lives in `path/to/slicerSALT-build/S-bld/Slicer-build/`

Unix-like
---------
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

To contribute your changes to slicerSALT, you will need to follow the forking workflow.

1. [Fork the slicerSALT repository] to your own github space, and add it to your git source directory

```sh
 git remote add custom-remote-name git@github.com:{github-space-name}/slicerSALT.git
 ```

2. Create an issue on slicerSALT's issue tracker (optional step for minor changes)
>
> https://github.com/Kitware/slicerSALT/issues
 
3. Create a new branch named `<issuer_number>-a-descriptive-topic-name`. Example:

 ```sh
 git checkout -b 101-add-surface-preprocess-extension
 ```
4. Fix the code or implement your feature, then commit your change(s)
>
> Make sure to read the [Slicer Coding and Commit Style Guide]

5. Push your branch to your fork of slicerSALT

 ```sh
 git push custom-remote-name 101-add-surface-preprocess-extension
 ```

6. Once your branch is ready for merging, create a pull request
>
> https://help.github.com/articles/creating-a-pull-request/

7. Once your changes have been reviewed and merged into the `master` branch of slicerSALT, you may get rid of your development branch and pull the latest commits from the master branch, then repeat from step 2 for further development
 
 ```sh
 git branch -d 101-add-surface-preprocess-extension
 git checkout master
 git pull origin master
 ```

Package
-------


Resources
---------
* [3D Slicer Developer Wiki](http://wiki.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers)


[Fork the slicerSALT repository]: https://help.github.com/articles/fork-a-repo/
[Slicer Coding and Commit Style Guide]: https://www.slicer.org/wiki/Documentation/Nightly/Developers/Style_Guide
