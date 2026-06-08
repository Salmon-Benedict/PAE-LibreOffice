#!/bin/bash
set -e
cd "$(dirname "$0")"

rm -f PAEBird.oxt

zip -r PAEBird.oxt \
  META-INF/manifest.xml \
  description.xml \
  description-en.txt \
  Addons.xcu \
  CalcAddins.xcu \
  python/pae_bird.py \
  PaeBird/PaeBird.xlb \
  PaeBird/Module1.xba

echo "Built PAEBird.oxt ($(du -h PAEBird.oxt | cut -f1))"
