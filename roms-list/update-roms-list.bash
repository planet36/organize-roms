# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

# Run this script from the target directory.
# Examples:
# bash update-roms-list.bash <base-path-to-roms>/'Nintendo - Game Boy Color/Nintendo - Game Boy Color '*
# bash update-roms-list.bash <base-path-to-roms>/'Nintendo - Game Boy/Nintendo - Game Boy '*
# bash update-roms-list.bash <base-path-to-roms>/'Nintendo - NES/Nintendo - Nintendo Entertainment System '*
# bash update-roms-list.bash <base-path-to-roms>/'Nintendo - SNES/Nintendo - Super Nintendo Entertainment System '*
# bash update-roms-list.bash <base-path-to-roms>/'Sega - 32X/Sega - 32X '*
# bash update-roms-list.bash <base-path-to-roms>/'Sega - Game Gear/Sega - Game Gear '*
# bash update-roms-list.bash <base-path-to-roms>/'Sega - Master System - Mark III/Sega - Master System - Mark III '*
# bash update-roms-list.bash <base-path-to-roms>/'Sega - Mega Drive - Genesis/Sega - Mega Drive - Genesis '*

# shellcheck disable=SC2034

SCRIPT_PATH="$(realpath -- "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname -- "$SCRIPT_PATH")"
SCRIPT_NAME=$(basename -- "$SCRIPT_PATH")

ROMS_DIR="$1"

if [[ -z "$ROMS_DIR" ]]
then
	printf 'Error: Must give path to ROMs directory\n' 1>&2
	printf 'Usage: bash %q ROMS_DIR\n' "$SCRIPT_NAME" 1>&2
	exit 1
fi

if [[ ! -d "$ROMS_DIR" ]]
then
	printf 'Error: ROMs directory not found: %q\n' "$ROMS_DIR" 1>&2
	printf 'Usage: bash %q ROMS_DIR\n' "$SCRIPT_NAME" 1>&2
	exit 1
fi

ROMS_LIST_FILE="$(basename -- "$ROMS_DIR" | tr -d '()[]' | tr ' ' '-' | sed -E -e 's/-+/-/g' -e 's/-[0-9]{8}-[0-9]{6}//g')"
ROMS_LIST_VERSION="$(basename -- "$ROMS_DIR" | sed -E -e 's/.+\(([0-9]{8}-[0-9]{6})\).*/\1/')"

if [[ -f "$ROMS_LIST_FILE" ]]
then
	# Backup existing file.
	mv --verbose --backup=numbered -- "$ROMS_LIST_FILE" "$ROMS_LIST_FILE~" || exit
fi

# Create file with list of ROMs.
find "$ROMS_DIR" -maxdepth 1 -type f -printf '%f\n' | LC_ALL=C sort --dictionary-order --ignore-case > "$ROMS_LIST_FILE" || exit

if git rev-parse --is-inside-work-tree &> /dev/null
then
	printf 'git diff %q\n' "$ROMS_LIST_FILE"
	printf 'git commit -m "Update %s" %q\n' "$ROMS_LIST_VERSION" "$ROMS_LIST_FILE"
fi
