#!/bin/bash
if [[ -z ${PLATFORM_PATH+1} ]];
then
  source set_vars.sh
fi

./prepare_kb.sh
cd ..


if [[ -f ${ERRORS_FILE} && ! ( -s ${ERRORS_FILE} )]]; then
  set -e -o pipefail
  "${PLATFORM_PATH}"/sc-machine/bin/sc-builder -f -c -i $PREPARED_KB/$REPO_PATH_FILE -o "${PLATFORM_PATH}"/kb.bin -s "${PLATFORM_PATH}"/config/sc-web.ini -e "${PLATFORM_PATH}"/sc-machine/bin/extensions
  rm "$ERRORS_FILE"
fi