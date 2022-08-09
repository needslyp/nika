#!/bin/bash
set -eo pipefail

cd ../ostis-web-platform/sc-machine/build

../bin/sc-builder -i ../tools/builder/tests/kb -o ../bin/sc-builder-test-repo --clear -f

ctest -C Debug -V
