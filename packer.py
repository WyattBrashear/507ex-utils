#!/usr/bin/env python3
"""
507 Labs .507ex Packer.
"""
import shutil
import argparse
import os
import subprocess
import hashlib
import uuid
import sys
import requests

# pylint: disable=too-many-branches,too-many-statements
def main():
    """Main function for packing .507ex files."""
    parser = argparse.ArgumentParser(
                        prog='507 Labs EX Packer',
                        description='Packs a source directory into a .507ex executable.',
                        epilog=r'[/|\]')
    parser.add_argument('source')
    parser.add_argument('packname')
    parser.add_argument('-r', '--run',
                        action='store_true')
    parser.add_argument('-t', '--temp', action='store_true')
    parser.add_argument('-u', '--url', help='URL for Auto upload to a CAR repository.')
    args = parser.parse_args()
    source = args.source
    try:
        if os.path.exists(f"{source}/runfile"):
            os.chdir(f"{source}")
            sources = os.listdir("./")
            sources.sort()
            print("Build checksums generated.")
            os.chdir("../")
            print("Creating archive...")
            shutil.make_archive(f"{args.packname}", "zip", f"{source}")
            print("Archive creation complete.")
            os.rename(f"{args.packname}.zip", f"{args.packname}.507ex")
            os.chdir(f"{source}")
            os.chdir("../")
            hash_func = hashlib.new('blake2s')
            with open(f"./{args.packname}.507ex", 'rb') as f:
                # Read the file in chunks of 8192 bytes
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            with open(f"./{args.packname}.507ex", 'rb') as f:
                exec_contents = f.read()
            with open(f"./{args.packname}.507ex", 'w', encoding='utf-8') as f:
                f.write("!507EX-METADATA")
                f.write(f"\n{hash_func.hexdigest()}|507ex-hash")
                f.write(f"\n{uuid.uuid4()}|507ex-id")
                f.write("\nblake2s|507ex-hashmode")
                f.write("\n#This File Was Created using 507ex-utils on github "
                        "(https://github.com/WyattBrashear/507ex-utils). Check it out!")
                f.write("\n!EXEC_CONTENTS\n")
            with open(f"./{args.packname}.507ex", 'ab') as f:
                f.write(exec_contents)
            print(f"Packed {args.packname}.507ex!")
        else:
            print("Runfile not found or source directory doesn't exist.")
    except KeyboardInterrupt:
        print("Cancelling Build...")
        if os.path.exists(f"{args.packname}.507ex"):
            os.remove(f"{args.packname}.507ex")
        if os.path.exists(f"{args.packname}.zip"):
            os.remove(f"{args.packname}.zip")
        sys.exit(0)
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"An error has occured while attempting to pack {source}. "
              "Please try again later.")
        if os.path.exists(f"{args.packname}.507ex"):
            os.remove(f"{args.packname}.507ex")
        if os.path.exists(f"{args.packname}.zip"):
            os.remove(f"{args.packname}.zip")
        print(e)
        sys.exit(1)

    if args.url:
        if not args.url.endswith(":507"):
            args.url = f"{args.url}:507"
        print(f"Uploading {args.packname}.507ex to CAR repository located at: {args.url}...")
        with open(f"{args.packname}.507ex", 'rb') as f:
            files = {'executable': f}
            r = requests.post(f'{args.url}/push', files=files, timeout=60)
        print("Uploaded executable!")
        print(f"Executable URL: {r.json()['url']}")
    if args.run:
        try:
            if args.temp:
                subprocess.run(f"python3 {os.getcwd()}/exec.py -d {args.packname}.507ex",
                               shell=True, check=False)
            else:
                subprocess.run(f"python3 {os.getcwd()}/exec.py {args.packname}.507ex",
                               shell=True, check=False)
        except KeyboardInterrupt:
            print("")

if __name__ == "__main__":
    main()
