*Forked from https://github.com/goncalopp/git-utilities and converted to Python 3*

git-utilities
=============

[git-multi-rebase]

A script to rebase multiple branches onto a single base, preserving relations between branches (see [this stackoverflow question](https://stackoverflow.com/questions/23386318/how-can-i-rebase-multiple-branches-at-once) for an example).

This script will iteratively rebase each branch onto the 'newbase'.  

If confilicts arise the script will start a new shell instance, allowing the user to resolve the conflicts, or abort the conflicting rebase (using git rebase --abort). Once the conflicts have been resolved, the user must execute git rebase --continue, and then exit the shell. Once the shell exits the rest of the multi-rebase process will continue.  

usage: git-multi-rebase [options] newbase branch0 [branch1 ... branchN]

All options are passed directly through to each git rebase call

[git-completion.bash]

An updated version the standard git-completion.bash script that supports git-multi-rebase

[git_python.py]

A python module to wrap some standard git functions
