#!/bin/bash
# Segmented hard-class (p ≡ 1 mod 24) Erdős–Straus f(p) sweep: 10^6 → 10^7.
# Combined with hard_1e6.csv (already computed, 5..10^6) this gives the full
# dataset to 10^7. Segments are exactly equivalent to one run (verified).
cd "$(dirname "$0")"
for spec in "1000001 2000000 2" "2000001 4000000 3" "4000001 6000000 4" "6000001 8000000 5" "8000001 10000000 6"; do
  set -- $spec
  echo "[$(date +%T)] segment $3 ($1..$2) starting"
  ./fpr "$1" "$2" 1 "hard_seg$3.csv" 16 2>&1 || { echo "SEGMENT_$3_FAILED"; exit 1; }
done
echo ALL_SEGMENTS_DONE
