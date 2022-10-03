# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

'''
Usage: python3 roms-distribution.py ROMS_DIR...

For each ROMS_DIR, print the distribution of the first alpha-numeric character of the filenames.
The results are used to determine an optimal subdirectory structure into which ROMs could be split.

Examples:
python3 roms-distribution.py \
roms-list/ROMs.Nintendo-Game-Boy-Color.* \
roms-list/ROMs.Nintendo-Game-Boy.* \
roms-list/ROMs.Nintendo-Nintendo-Entertainment-System-unheadered.* \
roms-list/ROMs.Nintendo-Super-Nintendo-Entertainment-System.* \
roms-list/ROMs.Sega-32X.* \
roms-list/ROMs.Sega-Game-Gear.* \
roms-list/ROMs.Sega-Master-System-Mark-III.* \
roms-list/ROMs.Sega-Mega-Drive-Genesis.*

python3 roms-distribution.py \
<base-path-to-roms>/'Nintendo - Game Boy Color/Nintendo - Game Boy Color '* \
<base-path-to-roms>/'Nintendo - Game Boy/Nintendo - Game Boy '* \
<base-path-to-roms>/'Nintendo - NES/Nintendo - Nintendo Entertainment System '* \
<base-path-to-roms>/'Nintendo - SNES/Nintendo - Super Nintendo Entertainment System '* \
<base-path-to-roms>/'Sega - 32X/Sega - 32X '* \
<base-path-to-roms>/'Sega - Game Gear/Sega - Game Gear '* \
<base-path-to-roms>/'Sega - Master System - Mark III/Sega - Master System - Mark III '* \
<base-path-to-roms>/'Sega - Mega Drive - Genesis/Sega - Mega Drive - Genesis '*
'''

from shlex import quote
from collections import OrderedDict
from pathlib import Path
import sys

__author__ = 'Steven Ward'
__version__ = '2022-10-03'

def get_first_alnum(s: str):
	'''Find the first alpha-numeric character in the string.'''
	for c in s:
		if c.isalnum():
			return c
	return None

def roms_distribution(path: Path) -> OrderedDict:
	'''Get the distribution of the first alpha-numeric character of the filenames in the path.'''

	bios_pattern = '[BIOS]'
	num_pattern = '[0-9]'

	dist = OrderedDict()

	dist[bios_pattern] = 0
	dist[num_pattern] = 0
	dist['A'] = 0
	dist['B'] = 0
	dist['C'] = 0
	dist['D'] = 0
	dist['E'] = 0
	dist['F'] = 0
	dist['G'] = 0
	dist['H'] = 0
	dist['I'] = 0
	dist['J'] = 0
	dist['K'] = 0
	dist['L'] = 0
	dist['M'] = 0
	dist['N'] = 0
	dist['O'] = 0
	dist['P'] = 0
	dist['Q'] = 0
	dist['R'] = 0
	dist['S'] = 0
	dist['T'] = 0
	dist['U'] = 0
	dist['V'] = 0
	dist['W'] = 0
	dist['X'] = 0
	dist['Y'] = 0
	dist['Z'] = 0

	for child in path.iterdir():
		if child.is_file():
			s = child.stem
			key = None
			if s.startswith(bios_pattern):
				key = bios_pattern
			else:
				first_alnum = get_first_alnum(s.casefold())
				if first_alnum is None:
					print(f'# Warning: No alpha-numeric characters found in {quote(s)}', file=sys.stderr)
					continue
				if first_alnum.isalpha():
					key = first_alnum.upper()
				else: # isdecimal or isdigit or isnumeric
					key = num_pattern
			dist[key] += 1

	return dist

# pylint: disable=missing-function-docstring
def main(argv = None):

	if argv is None:
		argv = sys.argv[1:]

	for arg in argv:
		print(f'# {arg}')

		dist = roms_distribution(Path(arg))

		key_max_len = len(max(dist.keys(), key=len))

		for key, val in dist.items():
			print(f"{key:<{key_max_len}} {val}")
		print()

if __name__ == '__main__':
	sys.exit(main())
