#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser(description='Print a Histogram of how much space is wasted in total per Btrfs chunk utilization')
parser.add_argument('path', metavar='path', type=str, default="/", nargs='?', help='Pth to the filesystem (defaults to /)')
path = parser.parse_args().path

# ensure root
import os
if os.getuid() != 0:
    from elevate import elevate
    elevate(graphical=False)

import btrfs

fs = btrfs.FileSystem(path)

bg = lambda chunk: fs.block_group(chunk.vaddr, chunk.length)

ratios = [ block_group.used / block_group.length for block_group in map(bg,fs.chunks()) if block_group.flags & btrfs.BLOCK_GROUP_TYPE_MASK == btrfs.BLOCK_GROUP_DATA ]

import numpy as np
import shutil

resolution = 20
maxwidth = shutil.get_terminal_size((80, 20)).columns

counts, bin_edges = np.histogram(ratios, bins=[0,0.00001]+list(np.linspace(0,1,resolution+1))[1:-1]+[0.99999,1])
sizes = counts.astype(float)

sizes *= 1024**3 * ( 1 - bin_edges[:-1] )

bars = sizes.copy()
bars /= bars.max()
bars *= maxwidth - 40
bars *= 2
bars = bars.round().astype(int)

bins = zip( bin_edges[:-1], bin_edges[1:] )

print(" Usage  | estimated savable space (number of chunks)")
started = 0
for bin, size, bar, count in zip( bins, sizes, bars, counts ):
    if not size and not started:
        continue
    started = 1
    
    print(f"{bin[0]*100:6.3f}% | {'█'*(bar//2)}{'▌'*(bar%2)}\t {btrfs.utils.pretty_size(size)} ({count})")

print(f"Total savable {btrfs.utils.pretty_size((len(ratios)-sum(ratios))*1024**3)}")
