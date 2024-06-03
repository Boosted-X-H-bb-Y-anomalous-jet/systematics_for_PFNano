Requires [TIMBER](https://github.com/JHU-Tools/TIMBER/tree/master) installation.
Before submitting jobs to condor, make sure to edit the paths in the `timber_tar.sh` and the `exe.sh` scripts. Likewise, the `timber_tar.sh` will need to be executed in order to bundle the TIMBER installation and have it available for condor nodes.
`submitToCondor.py` contains the datasets against which the script tries to find matching systematic trees. In this script, one needs to change the `root_dir` path that will contain the output systematic trees.
