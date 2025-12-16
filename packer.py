#!/usr/bin/env python3
#507 Labs .507ex Packer.
import shutil
import argparse
import os
import subprocess
import hashlib
import requests

parser = argparse.ArgumentParser(
                    prog='507 Labs EX Packer',
                    description='Packs a source directory into a .507ex executable.',
                    epilog='[/|\]')
parser.add_argument('source')
parser.add_argument('packname')
parser.add_argument('-r', '--run',
                    action='store_true')
parser.add_argument('-t', '--temp', action='store_true')
parser.add_argument('--url', help='URL for Auto upload to a CAR repository.')
args = parser.parse_args()
try:
    source = args.source
    if os.path.exists(f"{source}/runfile"):
        os.chdir(f"{source}")
        sources = os.listdir(f"./")
        sources.sort()
        os.mkdir(".hash")
        for file in sources:
            hash_func = hashlib.new('blake2s')
            try:
                with open(file, 'rb') as file:
                    while chunk := file.read(8192):
                        hash_func.update(chunk)
                with open(f"./.hash/{str(file.name)}.blake2s", 'x') as f:
                    f.write(hash_func.hexdigest())
            except IsADirectoryError:
                pass
        print("Build checksums generated.")
        os.chdir("../")
        print("Creating archive...")
        shutil.make_archive(f"{args.packname}", "zip", f"{source}")
        print("Archive creation complete.")
        os.rename(f"{args.packname}.zip", f"{args.packname}.507ex")
        os.chdir(f"{source}")
        shutil.rmtree("./.hash")
        os.chdir("../")
        print(f"Packed {args.packname}.507ex!")
    else:
        print("Runfile not found or source directory doesn't exist.")
    for file in os.listdir(f"{source}"):
        if file.endswith("hash"):
            os.remove(f"{source}/{file}")
except KeyboardInterrupt:
    print("Cancelling Build...")
    if os.path.exists(f"{source}/.hash"):
        shutil.rmtree(f"{source}/.hash")
    if os.path.exists(f"{args.packname}.507ex"):
        os.remove(f"{args.packname}.507ex")
    if os.path.exists(f"{args.packname}.zip"):
        os.remove(f"{args.packname}.zip")
    exit(0)
except Exception as e:
    print(f"An error has occured while attempting to pack {source}. Please try again later.")
    if os.path.exists(f"{source}/.hash"):
        shutil.rmtree(f"{source}/.hash")
    if os.path.exists(f"{args.packname}.507ex"):
        os.remove(f"{args.packname}.507ex")
    if os.path.exists(f"{args.packname}.zip"):
        os.remove(f"{args.packname}.zip")
    print(e)
    exit(1)

if args.url:
    if not args.url.endswith(":507"):
        args.url = f"{args.url}:507"
    print(f"Uploading {args.packname}.507ex to CAR repository located at: {args.url}...")
    executable = {'executable': open(f"{args.packname}.507ex", 'rb')}
    r = requests.post(f'{args.url}/push', files=executable)
    print("Uploaded executable!")
    print(f"Executable URL: {r.json()['url']}")
if args.run:
    try:
        if args.temp:
            subprocess.run(f"python3 {os.getcwd()}/exec.py -d {args.packname}.507ex", shell=True)
        else:
            subprocess.run(f"python3 {os.getcwd()}/exec.py {args.packname}.507ex", shell=True)
    except KeyboardInterrupt:
        print("")
