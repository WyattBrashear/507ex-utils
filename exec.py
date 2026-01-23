"""
507 Labs .507ex Execution Utility
"""
#!/usr/bin/env python3
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
import requests
from requests import RequestException

# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def main():
    """Main execution function."""
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
                        help="Keeps '.507ex-runtime' after program execution. "
                             "Useful for debugging.")
    parser.add_argument('-d', '--destroy',
                        action='store_true',
                        help="Destroys the source file after execution. (Self destruct mode)")
    parser.add_argument('-i', '--infinite',
                        action='store_true',
                        help="Infinite mode. Keeps the program running even in "
                             "the event of an error.")

    parser.add_argument('sourcefile')

    args = parser.parse_args()
    source = args.sourcefile
    source = f"{path}/{source}"
    hashmode = ""
    exec_hash = ""
    exec_id = ""
    with open(source, 'rb') as f:
        binary_lines = [f.readline() for _ in range(6)]
        string_lines = [line.decode('utf-8').strip() for line in binary_lines]
        print(string_lines)
        for metadata in string_lines:
            if metadata.endswith("|507ex-id"):
                exec_id = metadata.split("|")[0]
                print(exec_id)
            if metadata.endswith("|507ex-hashmode"):
                hashmode = metadata.split("|")[0]
            if metadata.endswith("|507ex-hash"):
                exec_hash = metadata.split("|")[0]
    #Let the user know that verbose mode is broken
    is_remote = False
    if args.verbose:
        choice = input("Note: Verbose mode currently breaks utility. Proceed? (y/n)")
        if choice.lower() != "y":
            sys.exit(0)
    if args.destroy and args.keep_runtime:
        print("Invalid combination of arguments: --destroy and --keep-runtime "
              "cannot be used together.")
        sys.exit(1)

    #Handle CAR sources
    if 'http://' in source or 'https://' in source:
        is_remote = True
        try:
            r = requests.get(source, timeout=10)
            r.raise_for_status()
            with open(f'{exec_id}.507ex', 'wb') as f:
                f.write(r.content)
        except RequestException:
            sys.exit(1)
        source = f"{exec_id}.507ex"

    #Check if the sourcefile is a .507ex file
    if not source.endswith(".507ex"):
        print("Source file must be a .507ex file.")
        sys.exit(1)

    #Remove .507ex-runtime if it exists
    if not os.path.exists(".507ex-runtime"):
        os.mkdir(".507ex-runtime")
    print(path)
    os.mkdir(f"{path}/.507ex-runtime/{exec_id}")
    if args.verbose:
        print(f"507 Labs .507ex execution utility v 1.0.0. Running: {source}.")
    #Attempt to copy the source file to the runtime directory
    try:
        shutil.copy(source, f"{path}/.507ex-runtime/{exec_id}/exec.zip")
    except FileNotFoundError:
        #If it does not exist, let the user know and sys.exit.
        print("Source executable not found. Are you sure it exists?")
        sys.exit(1)
    if args.verbose:
        print(f"Copied {source} to {os.getcwd()}/.507ex-runtime/{exec_id}/exec.zip.")
    #Unzip the source file
    try:
        with zipfile.ZipFile(f'{path}/.507ex-runtime/{exec_id}/exec.zip', 'r') as zip_ref:
            if args.verbose:
                print("Extracting Source File")
            zip_ref.extractall(f"{path}/.507ex-runtime/{exec_id}/exec")
            if args.verbose:
                print("Source File Extracted.")
    except zipfile.BadZipFile:
        print("An error occurred while attempting to run the executable.")
    try:
        # Hashing time!
        with open(f"{path}/.507ex-runtime/{exec_id}/exec.zip", "rb") as exc:
            lines = exc.readlines()[6:]
            exec_file_content = b"".join(lines)
            runtime_hash = hashlib.new(hashmode, exec_file_content).hexdigest()
        if runtime_hash != exec_hash:
            print("Hash mismatch detected. Executable may have been tampered with.")
            sys.exit(1)
        # Change the directory to .507ex-runtime/exec and generate hashes
        # for files inside that directory.
        os.chdir(f"{path}/.507ex-runtime/{exec_id}/exec")
        os.listdir(f"{path}/.507ex-runtime/{exec_id}/exec/")
        sources = os.listdir("./")
        sources.sort()
        os.chdir(f"{path}/.507ex-runtime/{exec_id}/exec")
        # Open The runfile
        with open("./runfile", 'r', encoding='utf-8') as runfile:
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
                    print("Executable has crashed and/or run into an error. "
                          "Restarting script...")
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

    except Exception as e: # pylint: disable=broad-exception-caught
        #Cleanly handle exec errors.
        print(f"An Error occurred while executing {source}. "
              "Please contact the developer for help.")
        print("\nExiting 507ex Environment")
        os.chdir(path)
        print(e)
    if not args.keep_runtime:
        #Do this if we are not keeping the runtime directory.   j
        while ".507ex-runtime" in os.getcwd():
            #Ensure we are OUT of the .507ex-runtime directory. In the event that it is not.
            os.chdir("../")

        shutil.rmtree(f"{path}/.507ex-runtime/{exec_id}")
        #Clean up if nobody else is using the runtime.
        if len(os.listdir(f"{path}/.507ex-runtime")) == 0:
            shutil.rmtree(f"{path}/.507ex-runtime")
    if args.destroy or is_remote:
        #And optionally, destroy the source file.
        os.remove(source)

if __name__ == "__main__":
    main()
