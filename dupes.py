#!/usr/bin/env python3

import argparse
import hashlib
import os
import stat
import pathlib


# Compute SHA256 hash for a file
def sha256_file(ff):
   h256 = hashlib.sha256()
   with open(ff,'rb') as file:
     chunk = 0
     while chunk != b'':
       chunk = file.read(1024)
       h256.update(chunk)
   return h256.hexdigest()

# Pretty print a list of filenames
def ppr(ll):
  s = ''
  for ff in ll:
    s += ff + ' '
  print(s.strip())

ap = argparse.ArgumentParser(description='Find dupes')
ap.add_argument('-r', '--recursive', action='store_true', help='Recursively search directories')
ap.add_argument('-u', '--unique', action='store_true', help='Print uniques instead of dupes')
ap.add_argument('path', nargs='+', type=pathlib.Path, help='Files or directories')
args = ap.parse_args()

ffs = []
for apath in args.path:
  if apath.is_file():
    if os.access(apath, os.R_OK):
      ffs.append(apath.name)

  elif apath.is_dir():
    sdirs = [apath]
    while sdirs:
      for line in os.scandir(sdirs.pop(0)):
        if line.is_symlink():
          continue
        if line.is_dir():
          if args.recursive:
            sdirs.append(line)
        elif line.is_file():
          if os.access(line, os.R_OK):
            ffs.append(line.path)

  else:
    print(str(apath) + " No such file or directory")
    exit(1)

hashes = {}
for ff in ffs:
  hexd = sha256_file(ff)
  if hexd not in hashes:
    hashes[hexd] = []
  hashes[hexd].append(ff)

if args.unique:
  for k,v in hashes.items():
    if len(v) == 1:
      ppr(v)
else:
  if len(ffs) == len(hashes):
    exit(0)
  for k,v in hashes.items():
    if len(v) != 1:
      ppr(v)
