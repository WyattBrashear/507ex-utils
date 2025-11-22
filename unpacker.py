#!/usr/bin/env python3
import shutil
import zipfile
import argparse
import os
parser = argparse.ArgumentParser(
                    prog='507 Labs EX Unpacker',
                    description='Unpacks a .507ex executable.',
                    epilog='[/|\]]')

parser.add_argument('source')
parser.add_argument('output')
args = parser.parse_args()
shutil.copy(f"{args.source}", f"{args.output}.zip")
with zipfile.ZipFile(f'{args.output}.zip', 'r') as zip_ref:
    zip_ref.extractall(f'./{args.output}')
shutil.rmtree(f'./{args.output}/.hash')
os.remove(f'{args.output}.zip')
