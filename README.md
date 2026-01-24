# 507ex-utils
## Overview
The .507ex file format is pretty much a zip file but, with a little extra magic behind the scenes.
It allows you to easily turn your program into an app that you can share with the world!

## Runfile
The Runfile is a file that is required to be in any source directory that is being packed as a .507ex. It contains the shell command in order to run your app. For multi-step application boots, have the runfile point to a boot script (e.g. start.sh).

## Hashing
For security reasons, all core/top level files in an executable are hashed. This is done to prevent unathorized tampering to the executable.
All hashes are stored in the .hash directory that is created at build and included only in the executeable and does not exist in the source folder.
It's format is {source file name}.hash and is in the blake2s format.

## Metadata
507ex metadata is stored at the top of the file and is handled like this:
```507ex-metadata
!507EX-METADATA
1b13618e5c5e4b77a40794cd6014b0e6d8a525fb6203bbeeeb60fe12b3bcbd61|507ex-hash
e6830510-1d6f-420d-9ceb-664cafec2d54|507ex-id
blake2s|507ex-hashmode
#This File Was Created using 507ex-utils on github (https://github.com/WyattBrashear/507ex-utils). Check it out!
!EXEC_CONTENTS
```


# CAR (Central App Repository)
CAR is a server system that allows hosting of 507ex executables for easy download. it provides (Once uploaded) a url with the .507ex file on it.
