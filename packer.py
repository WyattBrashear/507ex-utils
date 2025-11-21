#!/usr/bin/env python3
#507 Labs .507ex Packer.
import shutil
import argparse
import os
import subprocess
import hashlib

parser = argparse.ArgumentParser(
                    prog='507 Labs EX Packer',
                    description='Packs a source directory into a .507ex executable.',
                    epilog='[/|\]')
parser.add_argument('source')
parser.add_argument('packname')
parser.add_argument('-r', '--run',
                    action='store_true')
parser.add_argument('-t', '--temp', action='store_true')
args = parser.parse_args()
if os.path.exists(f"{args.source}/runfile"):
    os.chdir(f"{args.source}")
    sources = os.listdir(f"./")
    sources.sort()
    os.mkdir(".hash")
    for file in sources:
        hash_func = hashlib.new('sha256')
        with open(file, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)
        with open(f"./.hash/{str(file.name)}.hash", 'x') as f:
            f.write(hash_func.hexdigest())
    os.chdir("../")
    shutil.make_archive(f"{args.packname}", "zip", f"{args.source}")
    os.rename(f"{args.packname}.zip", f"{args.packname}.507ex")
    os.chdir(f"{args.source}")
    shutil.rmtree(".hash")
    os.chdir("../")
    print(f"Packed {args.packname}.507ex!")
else:
    print("Runfile not found or source directory doesn't exist.")
for file in os.listdir(f"{args.source}"):
    if file.endswith("hash"):
        os.remove(f"{args.source}/{file}")
if args.run:
    try:
        if args.temp:
            subprocess.run(f"python3 {os.getcwd()}/exec.py -d {args.packname}.507ex", shell=True)
        else:
            subprocess.run(f"python3 {os.getcwd()}/exec.py {args.packname}.507ex", shell=True)
    except KeyboardInterrupt:
        print("")
