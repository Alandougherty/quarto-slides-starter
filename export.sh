#!/bin/bash
# Export the deck to a slide-faithful PDF. Decktape is the recommended
# route: exact page geometry, scriptable, repeatable.
#   quarto preview deck.qmd --port 4200 --no-browser &
#   ./export.sh http://localhost:4200/ deck.pdf
#
# Manual fallback (documented Quarto flow): open the deck in Chrome,
# press `e`, then Cmd+P -> Save as PDF, margins: none, background
# graphics: on.
set -euo pipefail
# --size must match the deck's authored aspect ratio (1920x1080 = 16:9,
# the starter's 1244x700 canvas). Change it if you change the canvas ratio.
npx -y decktape reveal "${1:?usage: export.sh <url> <out.pdf>}" "${2:?usage: export.sh <url> <out.pdf>}" --size 1920x1080
