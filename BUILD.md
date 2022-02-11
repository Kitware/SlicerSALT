Build and Package SlicerSALT
============================

This document summarizes how to build and package SlicerSALT on Linux, macOS and Windows.

SlicerSALT is a custom Slicer application. Reading the [3D Slicer Developer Documentation](https://slicer.readthedocs.io/en/latest/developer_guide/index.html) may help answer additional questions.

The initial source files were created using [KitwareMedical/SlicerCustomAppTemplate](https://github.com/KitwareMedical/SlicerCustomAppTemplate).


Prerequisites
-------------

* Install the Fortran compiler

  * [GNU/Linux systems](https://www.slicer.org/wiki/Documentation/Nightly/Developers/Fortran#Linux)
  * [macOS](https://www.slicer.org/wiki/Documentation/Nightly/Developers/Fortran#macOS)
  * [Windows](https://www.slicer.org/wiki/Documentation/Nightly/Developers/Fortran#Windows)

* Review and install the `3D Slicer` prerequisites

  * [GNU/Linux systems](https://slicer.readthedocs.io/en/latest/developer_guide/build_instructions/linux.html)
  * [macOS](https://slicer.readthedocs.io/en/latest/developer_guide/build_instructions/macos.html)
  * [Windows](https://slicer.readthedocs.io/en/latest/developer_guide/build_instructions/windows.html)

* Setup your git account:

  * Create a [Github](https://github.com) account.

  * Setup your SSH keys following [these](https://help.github.com/articles/generating-ssh-keys) instructions at the
  exception of `step 2` where you should __NOT__ enter a passphrase.

  * Setup [your git username](https://help.github.com/articles/setting-your-username-in-git) and [your git email](https://help.github.com/articles/setting-your-email-in-git).


Checkout
--------

### GNU/Linux systems & macOS

```bash
mkdir ~/Projects
cd ~/Projects
git clone https://github.com/Kitware/SlicerSALT.git SS
```

### Windows

1. Start [Git Bash](https://help.github.com/articles/set-up-git#need-a-quick-lesson-about-terminalterminalgit-bashthe-command-line)
2. Checkout the source code into a directory `C:\W\` by typing the following commands:

```bat
cd /c
mkdir W
cd /c/W
git clone https://github.com/Kitware/SlicerSALT.git SS
```

_:warning: use short source and build directory names to avoid the [maximum path length limitation](http://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx#maxpath)._


Build
-----

### GNU/Linux systems

```bash
cd ~/Projects/SSR
cmake \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DQt5_DIR:PATH=/path/to/Qt/lib/cmake/Qt5 \
  ../SS
```

### macOS

```bash
mkdir ~/Projects
cd ~/Projects
cmake \
  -DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.13 \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DQt5_DIR:PATH=/path/to/Qt/lib/cmake/Qt5 \
  ../SS
```

### Windows

<b>Option 1: CMake GUI and Visual Studio (Recommended)</b>

1. Start [CMake GUI](https://cmake.org/runningcmake/), select source directory `C:\W\SS` and set build directory to `C:\W\SSR`.
2. Add an entry `Qt5_DIR` pointing to `C:/Qt/${QT_VERSION}/${COMPILER}/lib/cmake/Qt5`.
2. Generate the project.
3. Open `C:\W\SSR\{{cookiecutter.project_name}}.sln`, select `Release` and build the project.

<b>Option 2: Command Line</b>

1. Start the [Command Line Prompt](http://windows.microsoft.com/en-us/windows/command-prompt-faq)
2. Configure and build the project in `C:\W\SSR` by typing the following commands:

```bat
cd C:\W\
mkdir SSR
cd SSR
cmake -G "Visual Studio 16 2019" -A x64 -DQt5_DIR:PATH=`C:/Qt/${QT_VERSION}/${COMPILER}/lib/cmake/Qt5 ..\SS
cmake --build . --config Release -- /maxcpucount:4
```

Package
-------

_:warning: Creating distributable packages is only supported for `Release` builds._

### GNU/Linux systems & macOS

```
cd ~/Projects/SSR/Slicer-build
make package
```

### macOS

_:warning: SlicerSALT will only create a valid package that will run on machines other than it’s built on if Qt was built from source._

```
cd ~/Projects/SSR/Slicer-build
make package
```

### Windows

Install [NSIS 2](http://sourceforge.net/projects/nsis/files/)

<b>Option 1: CMake and Visual Studio</b>

1. In the `C:\W\SSR\Slicer-build` directory, open `Slicer.sln` and build the `PACKAGE` target

<b>Option 2: Command Line</b>

1. Start the [Command Line Prompt](http://windows.microsoft.com/en-us/windows/command-prompt-faq)
2. Build the `PACKAGE` target by typing the following commands:

```bat
cd C:\W\SSR\Slicer-build
cmake --build . --config Release --target PACKAGE
```

