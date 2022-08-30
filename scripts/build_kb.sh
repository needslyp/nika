#!/bin/bash
if [[ -z ${PLATFORM_PATH+1} ]];
then
  source set_vars.sh
fi

set -e -o pipefail
python3 "${PLATFORM_PATH}"/sc-machine/scripts/build_kb.py "${APP_ROOT_PATH}/repo$1.path" -c "${APP_ROOT_PATH}/nika.ini" -b "${APP_ROOT_PATH}"/bin
