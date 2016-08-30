Ninja by Kitware, Inc.
======================

![Ninja by Kitware, Inc.](https://kwgitlab.kitware.com/slicer/slicertemplateproject/raw/latest/Applications/App/Resources/Images/LogoFull.png)

Prerequisites
-------------

* Microsoft Windows 7 or above recommended

* Supported Microsoft Visual Studio versions:
    * Visual Studio 2013
    * Visual Studio 2010 Professional
    * Visual Studio 2008 Professional + SP1
    * [Visual Studio 2010 Express](http://www.visualstudio.com/downloads/download-visual-studio-vs#d-2010-express) + [hot-fix KB2280741](http://archive.msdn.microsoft.com/KB2280741) + [Windows SDK 7](http://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=8279)

* [CMake](http://cmake.org/cmake/resources/software.html), version 2.8.12 or above

* Qt, version 4.8.7: [one line build](https://github.com/jcfr/qt-easy-build).

* [Git](http://git-scm.com/downloads)

* [Subversion](http://www.sliksvn.com/en/download)

* Setting up your git account:

    * Create a [Github](https://github.com) account.

    * Setup your SSH keys following [these](https://help.github.com/articles/generating-ssh-keys) instructions at the
    exception of `step 2` where you should __NOT__ enter a passphrase.

    * Setup [your git username](https://help.github.com/articles/setting-your-username-in-git) and [your git email](https://help.github.com/articles/setting-your-email-in-git).

    * If not already done, email `Jean-Christophe Fillion-Robin <jchris.fillionr@kitware.com>` to be granted access to
    the [slicer/slicertemplateproject](https://kwgitlab.kitware.com/slicer/slicertemplateproject) repository.

Checkout
--------

1. Start [Git Bash](https://help.github.com/articles/set-up-git#need-a-quick-lesson-about-terminalterminalgit-bashthe-command-line)
2. Checkout the source code into a directory `C:\W\` by typing the following commands:

```bat
cd /c
mkdir W
cd /c/W
git clone https://github.com/Ninja/Ninja.git Ninja
```

Note: use short source and build directory names to avoid the [maximum path length limitation](http://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx#maxpath).

Build
-----
Note: The build process will take approximately 3 hours.

<b>Option 1: CMake GUI and Visual Studio (Recommended)</b>

1. Start [CMake GUI](https://cmake.org/runningcmake/), select source directory `C:\W\Ninja` and set build directory to `C:\W\Ninja-rel`.
2. Add an entry `QT_QMAKE_EXECUTABLE` pointing to `C:\D\Support\qt-4.8.7-64-vs2013-rel`.
2. Generate the project.
3. Open `C:\W\Ninja-rel\Ninja.sln`, select `Release` and build the project.

<b>Option 2: Command Line</b>

1. Start the [Command Line Prompt](http://windows.microsoft.com/en-us/windows/command-prompt-faq)
2. Configure and build the project in `C:\W\Ninja-rel` by typing the following commands:

```bat
cd C:\W\
mkdir Ninja-rel
cd Ninja-rel
cmake -G "Visual Studio 9 2008 (Win64)" -DQT_QMAKE_EXECUTABLE:PATH=C:\D\Support\qt-4.8.7-64-vs2013-rel\bin\qmake.exe ..\Ninja
cmake --build . --config Release
```

Package
-------

Install [NSIS 2](http://sourceforge.net/projects/nsis/files/)

<b>Option 1: CMake and Visual Studio (Recommended)</b>

1. In the `C:\W\Ninja-rel\S-bld\Slicer-build` directory, open `Slicer.sln` and build the `PACKAGE` target

<b>Option 2: Command Line</b>

1. Start the [Command Line Prompt](http://windows.microsoft.com/en-us/windows/command-prompt-faq)
2. Build the `PACKAGE` target by typing the following commands:

```bat
cd C:\W\Ninja-rel\S-bld\Slicer-build
cmake --build . --config Release --target PACKAGE
```

Resources
---------
* [3D Slicer Developer Wiki](http://wiki.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers)