# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

# Run this script from the target directory.

# shellcheck disable=SC2034

SCRIPT_PATH="$(realpath -- "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname -- "$SCRIPT_PATH")"
SCRIPT_NAME=$(basename -- "$SCRIPT_PATH")

ROMS_LIST_FILE="$1"

if [[ -z "$ROMS_LIST_FILE" ]]
then
	printf 'Error: Must give file with names of ROMs\n' 1>&2
	printf 'Usage: bash %q ROMS_LIST_FILE\n' "$SCRIPT_NAME" 1>&2
	exit 1
fi

if [[ ! -f "$ROMS_LIST_FILE" ]]
then
	printf 'Error: ROMs file not found: %q\n' "$ROMS_LIST_FILE" 1>&2
	printf 'Usage: bash %q ROMS_LIST_FILE\n' "$SCRIPT_NAME" 1>&2
	exit 1
fi

ROMS_DIR_TEMPLATE="ROMs.$(basename -- "$ROMS_LIST_FILE").XXXXXXXXXXX"

cd -- "$(mktemp --directory --tmpdir=. -t "$ROMS_DIR_TEMPLATE")" || exit

xargs --arg-file="$ROMS_LIST_FILE" --delimiter='\n' --max-lines=1 -- touch
