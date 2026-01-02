"""
507 Labs .507ex Execution Utility
"""
#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import zipfile
import hashlib
import uuid
import sys
import requests
from requests import RequestException
path = os.getcwd()
#Parser Setup
parser = argparse.ArgumentParser(
                    prog='507 Labs .507ex Execution Utility',
                    description='Runs a .507ex executable.',
                    epilog='507 Labs')
#And Now the Args
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help="Prints verbose output.")
parser.add_argument('-k', '--keep-runtime',
                    action='store_true',
                    help="Keeps '.507ex-runtime' after program execution. Useful for debugging.")
parser.add_argument('-d', '--destroy',
                    action='store_true',
                    help="Destroys the source file after execution. (Self destruct mode)")
parser.add_argument('-i', '--infinite',
                    action='store_true',
                    help="Infinite mode. Keeps the program running even in the event of an error.")

parser.add_argument('sourcefile')

args = parser.parse_args()
source = args.sourcefile
source = f"{path}/{source}"
EXEC_ID = str(uuid.uuid4())

#Let the user know that verbose mode is broken
is_remote = False
if args.verbose:
    choice = input("Note: Verbose mode currently breaks utility. Proceed? (y/n)")
    if choice.lower() != "n":
        sys.exit(0)
if args.destroy and args.keep_runtime:
    print("Invalid combination of arguments: --destroy and --keep-runtime cannot be used together.")
    sys.exit(1)

#Handle CAR sources
if 'http://' in source or 'https://' in source:
    is_remote = True
    try:
        r = requests.get(source, timeout=10)
        r.raise_for_status()
        with open(f'{EXEC_ID}.507ex', 'wb') as f:
            f.write(r.content)
    except RequestException:
        sys.exit(1)
    source = f"{EXEC_ID}.507ex"

#Check if the sourcefile is a .507ex file
if not source.endswith(".507ex"):
    print("Source file must be a .507ex file.")
    sys.exit(1)

#Remove .507ex-runtime if it exists
if not os.path.exists(".507ex-runtime"):
    os.mkdir(".507ex-runtime")
os.mkdir(f"{path}/.507ex-runtime/{EXEC_ID}")
if args.verbose:
    print(f"507 Labs EX Runner v 1.0.0. Running: {source}.")
#Attempt to copy the source file to the runtime directory
try:
    shutil.copy(source, f"{path}/.507ex-runtime/{EXEC_ID}/exec.zip")
except FileNotFoundError:
    #If it does not exist, let the user know and sys.exit.
    print("Source executable not found. Are you sure it exists?")
    sys.exit(1)
if args.verbose:
    print(f"Copied {source} to {os.getcwd()}/.507ex-runtime/{EXEC_ID}/exec.zip.")
#Unzip the source file
try:
    with zipfile.ZipFile(f'{path}/.507ex-runtime/{EXEC_ID}/exec.zip', 'r') as zip_ref:
        if args.verbose:
            print("Extracting Source File")
        zip_ref.extractall(f"{path}/.507ex-runtime/{EXEC_ID}/exec")
        if args.verbose:
            print("Source File Extracted.")
except zipfile.BadZipFile:
    print("An error occurred while attempting to run the executable.")
try:
    #Setup hashes lists
    file_hashes = []
    build_hashes = []
    #Change the directory to .507ex-runtime/exec and generate hashes for files inside that directory.
    os.chdir(f"{path}/.507ex-runtime/{EXEC_ID}/exec")
    sources_runtime = os.listdir(f"{path}/.507ex-runtime/{EXEC_ID}/exec/")
    sources_runtime.sort()
    for file in sources_runtime:
        hash_func = hashlib.new('blake2s')
        #Ensure files inside .hash is not hashed
        if file != ".hash":
            try:
                with open(file, 'rb') as f:
                    # Read the file in chunks of 8192 bytes
                    while chunk := f.read(8192):
                        hash_func.update(chunk)
                #Append the hash to the list
                file_hashes.append(hash_func.hexdigest())
            except IsADirectoryError:
                #If it is a directory, ignore it
                pass
    #Change directory to .hash and get hashes from files inside that directory.
    os.chdir(f"{path}/.507ex-runtime/{EXEC_ID}/exec/.hash")
    sources = os.listdir("./")
    sources.sort()
    for file in sources:
        try:
            with open(file, 'r') as f:
                #All hashes in the .hash directory are in plain text just read them as normal text.
                build_hashes.append(f.read())
        except IsADirectoryError:
            pass
    #Check if there are any file count discrepancies between build and runtime hashes.
    if len(file_hashes) != len(build_hashes):
        raise Exception("File hash amount mismatch. Possible tampering detected.")
    #Check if hashes are equivalent.
    for i in range(len(file_hashes)):
        if file_hashes[i] != build_hashes[i]:
            raise Exception("File hash mismatch. Possible tampering detected.")
    os.chdir(f"{path}/.507ex-runtime/{EXEC_ID}/exec")
    #Open The runfile
    with open(f"./runfile", 'r') as runfile:
        if args.verbose:
            print("Changed working directory to .507ex-runtime/exec")
            print(f"Runfile Contents: {runfile.read()}")
            print("Executing!")
        #Check if infinite mode is enabled.
        if args.infinite:
            #If it is, initialize the while True: Loop.
            while True:
                #Read runfile
                execfile = f"{runfile.read()}"
                #Execute!
                subprocess.run(execfile, shell=True, check=False)
                print("Executable has crashed and/or run into an error. Restarting script...")
        else:
            #If infinite mode is not enabled, do the same except not in a while True: Loop.
            execfile = f"{runfile.read()}"
            subprocess.run(execfile, shell=True, check=False)
        #Once done, exit the .507ex environment.
        os.chdir(path)
except KeyboardInterrupt:
    #Cleanly handle KeyboardInterrupts.
    print("\nExiting 507ex Environment")
    os.chdir(path)

except Exception as e:
    #Cleanly handle exec errors.
    print(f"An Error occurred while executing {source}. Please contact the developer for help.")
    print("\nExiting 507ex Environment")
    os.chdir(path)
    #print(e)
if not args.keep_runtime:
    #Do this if we are not keeping the runtime directory.   j
    while ".507ex-runtime" in os.getcwd():
        #Ensure we are OUT of the .507ex-runtime directory. In the event that it is not.
        os.chdir("../")

    shutil.rmtree(f"{path}/.507ex-runtime/{EXEC_ID}")
    #Clean up if nobody else is using the runtime.
    if len(os.listdir(f"{path}/.507ex-runtime")) == 0:
        shutil.rmtree(f"{path}/.507ex-runtime")
if args.destroy or is_remote:
    #And optionally, destroy the source file.
    os.remove(source)
