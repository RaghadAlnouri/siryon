#!/usr/bin/env bash
set -uo pipefail
ZIP=MASC_v1.0.zip
URL="https://zenodo.org/api/records/6496714/files/MASC_v1.0.zip/content"
[ -f "$ZIP" ] || { echo "downloading ~830MB..."; curl -L --progress-bar -o "$ZIP" "$URL"; }
find . -maxdepth 2 -type d -name "MASC*" | grep -q . || { echo "unzipping..."; unzip -q -o "$ZIP"; }
R=$(find . -maxdepth 2 -type d -name "MASC*" | head -1); R=${R:-.}
echo "root: $R"

echo; echo "=== STRUCTURE ==="
find "$R" -maxdepth 2 | head -50

echo; echo "=== FILE TYPES ==="
find "$R" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -15

echo; echo "=== TRANSLATION LAYER?  (the question that decides Phase 1) ==="
find "$R" -type f \( -iname "*trans*" -o -iname "*gloss*" -o -iname "*engl*" \
  -o -iname "*german*" -o -iname "*deutsch*" -o -iname "*.tsv" -o -iname "*.csv" \
  -o -iname "*.db" -o -iname "*.sqlite*" \) | head -25

echo; echo "=== DOCS / LICENCE ==="
for f in $(find "$R" -maxdepth 3 -type f \( -iname "*licen*" -o -iname "*readme*" \) | head -3); do
  echo "--- $f ---"; head -30 "$f"
done

echo; echo "=== SAMPLE DATA FILE ==="
F=$(find "$R" -type f \( -iname "*.txt" -o -iname "*.tsv" -o -iname "*.csv" \) \
     ! -iname "*licen*" ! -iname "*readme*" | head -1)
[ -n "$F" ] && { echo "$F:"; head -15 "$F"; }

echo; echo "=== AUDIO ==="
echo "files: $(find "$R" -type f \( -iname '*.wav' -o -iname '*.mp3' \) | wc -l | tr -d ' ')"
find "$R" -type f \( -iname '*.wav' -o -iname '*.mp3' \) -exec du -ch {} + 2>/dev/null | tail -1

echo; echo "=== SQLITE SCHEMA ==="
D=$(find "$R" -type f \( -iname "*.db" -o -iname "*.sqlite*" \) | head -1)
[ -n "$D" ] && command -v sqlite3 >/dev/null && { echo "$D"; sqlite3 "$D" ".tables"; sqlite3 "$D" ".schema" | head -40; }
