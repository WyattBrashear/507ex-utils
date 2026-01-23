#!/usr/bin/env python3
"""
507 Labs .507ex Unpacker.
"""
import shutil
import zipfile
import argparse
import os

def main():
    """Main function for unpacking .507ex files."""
    parser = argparse.ArgumentParser(
                        prog='507 Labs EX Unpacker',
                        description='Unpacks a .507ex executable.',
                        epilog=r'[/|\]]')

    parser.add_argument('source')
    parser.add_argument('output')
    args = parser.parse_args()
    shutil.copy(f"{args.source}", f"{args.output}.zip")
    with zipfile.ZipFile(f'{args.output}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'./{args.output}')
    shutil.rmtree(f'./{args.output}/.hash')
    os.remove(f'{args.output}.zip')

if __name__ == "__main__":
    main()
