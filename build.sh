#!/bin/bash
set -e
cd "$(dirname "$0")"

rm -f PAEBird.oxt

zip -r PAEBird.oxt \
  META-INF/manifest.xml \
  description.xml \
  description-en.txt \
  PaeBird/PaeBird.xlb \
  PaeBird/Module1.xba \
  CalcAddins.xcu \
  Addons.xcu \
  python/pae_bird.py

echo "Built PAEBird.oxt ($(du -h PAEBird.oxt | cut -f1))"
