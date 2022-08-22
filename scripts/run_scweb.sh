#!/bin/bash

set -eo pipefail

source set_vars.sh

cd "${PLATFORM_PATH}"/sc-web/scripts
./run_scweb.sh
