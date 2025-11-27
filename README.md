# 507ex-utils
## Overview
The .507ex file format is pretty much a zip file but, with a little extra magic behind the scenes.
It allows you to easily turn your program into an app that you can share with the world!

## Runfile
The Runfile is a file that is required to be in any source directory that is being packed as a .507ex. It contains the shell command in order to run your app.

## Hashing
For security reasons, all core/top level files in an executable are hashed. This is done to prevent unathorized tampering to the executable.
All hashes are stored in the .hash directory that is created at build and included only in the executeable and does not exist in the source folder.
It's format is {source file name}.hash and is in the sha256 format.

