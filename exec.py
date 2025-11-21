#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import zipfile
import hashlib

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
parser.add_argument('-d', '--destroy', action='store_true')
parser.add_argument('sourcefile')

args = parser.parse_args()
if args.verbose:
    print(f"507 Labs EX Runner v 1.0.0. Running: {args.sourcefile}.")
try:
    shutil.copy(args.sourcefile, "./.507ex-runtime/exec.zip")
except FileNotFoundError:
    print("Source executable not found. Are you sure it exists?")
    exit(1)
if args.verbose:
    print(f"Copied {args.sourcefile} to {os.getcwd()}/.507ex-runtime/exec.zip.")
with zipfile.ZipFile('./.507ex-runtime/exec.zip', 'r') as zip_ref:
    if args.verbose:
        print("Extracting Source File")
    zip_ref.extractall(".507ex-runtime/exec")
try:
    file_hashes = []
    build_hashes = []
    os.chdir(".507ex-runtime/exec")
    sources_runtime = os.listdir("./")
    sources_runtime.sort()
    for file in sources_runtime:
        hash_func = hashlib.new('sha256')
        if file != ".hash":
            with open(file, 'rb') as f:
                # Read the file in chunks of 8192 bytes
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            file_hashes.append(hash_func.hexdigest())
    os.chdir("./.hash")
    sources = os.listdir("./")
    sources.sort()
    for file in sources:
        with open(file, 'r') as f:
            build_hashes.append(f.read())
    if len(file_hashes) != len(build_hashes):
        raise Exception("There are a different number of files in the build version of the package than the runtime version. Possible tampering detected.")
    for i in range(len(file_hashes)):
        if file_hashes[i] != build_hashes[i]:
            raise Exception("Checksums generated at build are not equivalent to the checksums generated at runtime. Possible tampering detected.")
    os.chdir("..")
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
    print(e)
    os.chdir("../..")
    if args.verbose:
        print(e)
if not args.keep_runtime:
    shutil.rmtree(".507ex-runtime")
if args.destroy:
    os.remove(args.sourcefile)
