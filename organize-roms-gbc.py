# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

# pylint: disable=missing-module-docstring

# Run this from within the ROMs directory.

import fnmatch
import os
import re
from shlex import quote

__author__ = 'Steven Ward'
__version__ = '2021-12-03'

# Hopefully no ROM begins with "EOT"
rm_cmd = "cat <<EOT | xargs --no-run-if-empty --delimiter='\\n' --verbose -- rm --verbose || exit"

shebang = '#!/usr/bin/sh'

rom_ext = 'gbc'

glob_patterns_dev_status = (
		# keep
		#'*(Aftermarket*',
		#'*(Alt*',
		#'*(Unl*',
		'*(Beta*',
		'*(Demo*',
		'*(Pirate*',
		'*(Prerelease*',
		'*(Preview*',
		'*(Proto*',
		'*(Putative Beta*',
		'*(Sample*',
		'*(Tech Demo*',
		'*(Test Program*',
		)

glob_patterns_territory = (
		# keep
		#'*(Europe*',
		#'*(Japan*',
		#'*(USA*',
		'*(Argentina*',
		'*(Asia*',
		'*(Australia*',
		'*(Brazil*',
		'*(Canada*',
		'*(China*',
		'*(France*',
		'*(Germany*',
		'*(Hong Kong*',
		'*(Italy*',
		'*(Korea*',
		'*(Mexico*',
		'*(Netherlands*',
		'*(Russia*',
		'*(Spain*',
		'*(Sweden*',
		'*(Taiwan*',
		'*(United Kingdom*',
		'*(Unknown*',
		)

roms = set()
roms_to_delete = set()

path = '.'

with os.scandir(path) as it:
	for entry in it:
		if entry.is_file(follow_symlinks=False):
			roms.add(entry.name)

print(shebang)

# Remove ROMs (phase 1)

for glob_pattern in glob_patterns_dev_status:
	roms_to_delete.update(fnmatch.filter(roms, glob_pattern))

roms.difference_update(roms_to_delete)

if roms_to_delete: # not empty
	comment = '# ROMs matching glob patterns of development status'
	print()
	print(comment)
	print(rm_cmd)
	print('\n'.join(sorted(roms_to_delete)))
	print('EOT')
	roms_to_delete = set()

# Keep all BIOS files after phase 1.
roms.difference_update(fnmatch.filter(roms, '*BIOS*'))

# Remove ROMs (phase 2)

for glob_pattern in glob_patterns_territory:
	roms_to_delete.update(fnmatch.filter(roms, glob_pattern))

roms.difference_update(roms_to_delete)

if roms_to_delete: # not empty
	comment = '# ROMs matching glob patterns of territory'
	print()
	print(comment)
	print(rm_cmd)
	print('\n'.join(sorted(roms_to_delete)))
	print('EOT')
	roms_to_delete = set()

# Remove ROMs (phase 3)

usa_roms = set(
		fnmatch.filter(roms, '*(USA*') +
		fnmatch.filter(roms, '*, USA*'))
non_usa_roms = roms.difference(usa_roms)

usa_rom_base_pattern = r'(.+)\([^)]*\bUSA\b[^(]*\)'

# Remove Europe, Japan ROMs when a USA version exists.
for usa_rom in usa_roms:
	match = re.match(usa_rom_base_pattern, usa_rom)
	rom_base = match.group(1)
	glob_pattern_europe = rom_base + '(Europe*'
	glob_pattern_japan = rom_base + '(Japan*'
	roms_to_delete.update(fnmatch.filter(non_usa_roms, glob_pattern_europe))
	roms_to_delete.update(fnmatch.filter(non_usa_roms, glob_pattern_japan))

roms.difference_update(roms_to_delete)

if roms_to_delete: # not empty
	comment = '# Europe, Japan ROMs with an equivalent USA version'
	print()
	print(comment)
	print(rm_cmd)
	print('\n'.join(sorted(roms_to_delete)))
	print('EOT')
	roms_to_delete = set()

# Remove ROMs (phase 4)

europe_roms = set(
		fnmatch.filter(roms, '*(Europe*') +
		fnmatch.filter(roms, '*, Europe*'))
non_europe_roms = roms.difference(europe_roms)

# Do not consider USA ROMs
europe_roms.difference_update(usa_roms)
non_europe_roms.difference_update(usa_roms)

europe_rom_base_pattern = r'(.+)\([^)]*\bEurope\b[^(]*\)'

# Remove Japan ROMs when a Europe version exists.
for europe_rom in europe_roms:
	match = re.match(europe_rom_base_pattern, europe_rom)
	rom_base = match.group(1)
	glob_pattern_japan = rom_base + '(Japan*'
	roms_to_delete.update(fnmatch.filter(non_europe_roms, glob_pattern_japan))

roms.difference_update(roms_to_delete)

if roms_to_delete: # not empty
	# We may want to keep the Japan ROMs because they're NTSC rather than PAL.
	'''
	comment = '# Japan ROMs with an equivalent Europe version'
	print()
	print(comment)
	print(rm_cmd)
	print('\n'.join(sorted(roms_to_delete)))
	print('EOT')
	'''
	roms_to_delete = set()

dir_name_to_glob_pattern = {
		quote('_BIOS') : quote(r'\[BIOS\]*.' + rom_ext),
		quote('0-9'  ) : quote(r'[0-9]*.'    + rom_ext),
		quote('A'    ) : quote(r'A*.'        + rom_ext),
		quote('B'    ) : quote(r'B*.'        + rom_ext),
		quote('C'    ) : quote(r'C*.'        + rom_ext),
		quote('D'    ) : quote(r'D*.'        + rom_ext),
		quote('E-F'  ) : quote(r'[E-F]*.'    + rom_ext),
		quote('G'    ) : quote(r'G*.'        + rom_ext),
		quote('H'    ) : quote(r'H*.'        + rom_ext),
		quote('I-J'  ) : quote(r'[I-J]*.'    + rom_ext),
		quote('K'    ) : quote(r'K*.'        + rom_ext),
		quote('L'    ) : quote(r'L*.'        + rom_ext),
		quote('M'    ) : quote(r'M*.'        + rom_ext),
		quote('N-O'  ) : quote(r'[N-O]*.'    + rom_ext),
		quote('P'    ) : quote(r'P*.'        + rom_ext),
		quote('Q-R'  ) : quote(r'[Q-R]*.'    + rom_ext),
		quote('Sa-So') : quote(r'S[a-o]*.'   + rom_ext),
		quote('Sp-Sz') : quote(r'S[p-z]*.'   + rom_ext),
		quote('T'    ) : quote(r'T*.'        + rom_ext),
		quote('U-Z'  ) : quote(r'[U-Z]*.'    + rom_ext),
		}

print()
print('mkdir --verbose --parents -- \\')
print(' \\\n'.join(dir_name_to_glob_pattern.keys()))

for (dir_name, glob_pattern) in dir_name_to_glob_pattern.items():
	print()
	print(f'find . -maxdepth 1 -type f -iname {glob_pattern} -print0 |')
	print('xargs --no-run-if-empty --null --verbose \\')
	print(f'mv --verbose --target-directory={dir_name} || exit')
