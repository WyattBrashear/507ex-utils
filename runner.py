#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import zipfile

if os.path.exists(".507ex-runtime"):
    shutil.rmtree(".507ex-runtime")
os.mkdir(".507ex-runtime")
parser = argparse.ArgumentParser(
                    prog='507 Labs EX Runner',
                    description='Runs a .507ex executable.',
                    epilog='[/|\]')


parser.add_argument('-v', '--verbose',
                    action='store_true')
parser.add_argument('-k', '--keep-runtime',
                    action='store_true')
parser.add_argument('sourcefile')

args = parser.parse_args()
if args.verbose:
    print(f"507 Labs EX Runner v 1.0.0. Running: {args.sourcefile}.")
shutil.copy(args.sourcefile, "./.507ex-runtime/exec.zip")
if args.verbose:
    print(f"Copied {args.sourcefile} to {os.getcwd()}/.507ex-runtime/exec.zip.")
with zipfile.ZipFile('./.507ex-runtime/exec.zip', 'r') as zip_ref:
    if args.verbose:
        print("Extracting Source File")
    zip_ref.extractall(".507ex-runtime/exec")
try:
    os.chdir(".507ex-runtime/exec")
    with open(f"./runfile", 'r') as runfile:
        if args.verbose:
            print("Changed working directory to .507ex-runtime/exec")
            print(f"Runfile Contents: {runfile.read()}")
            print("Executing!")
        execfile = f"{runfile.read()}"
        subprocess.run(execfile, shell=True)
        os.chdir("../..")
except KeyboardInterrupt:
    print("\nExiting 507ex Enviornment")
    os.chdir("../..")

except Exception as e:
    print(f"An Error occured while attempting to run {args.sourcefile}. Please contact the developer for assistance.")
    os.chdir("../..")
    if args.verbose:
        print(e)
if not args.keep_runtime:
    shutil.rmtree(".507ex-runtime")