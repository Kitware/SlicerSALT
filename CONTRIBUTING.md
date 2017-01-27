Contributing to slicerSALT
=====================

To contribute your changes to slicerSALT, you will need to follow the forking workflow.

1. [Fork the slicerSALT Repository] to your own github space, and add it to your git source directory

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
 
 [Fork the slicerSALT Repository]: https://help.github.com/articles/fork-a-repo/
