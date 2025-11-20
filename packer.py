#!/usr/bin/env python3
#507 Labs .507ex Packer. Cross-Platform Executables.
import shutil
import argparse
import os
import subprocess

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
    shutil.make_archive(f"{args.packname}", "zip", f"{args.source}")
    os.rename(f"{args.packname}.zip", f"{args.packname}.507ex")
    print(f"Packed {args.packname}.507ex!")
else:
    print("Runfile not found or source directory doesn't exist.")
if args.run:
    try:
        subprocess.run(f"python3 ./runner.py {args.packname}.507ex", shell=True)
    except KeyboardInterrupt:
        print("")
