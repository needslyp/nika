#!/bin/bash
if [[ -e  ${ERRORS_FILE} ]]; then
    rm "$ERRORS_FILE"
fi
touch "$ERRORS_FILE"

if [ "$1" == "prepare_platform" ];
    then
        python3 "${PLATFORM_PATH}"/scripts/kb_scripts/prepare_kb.py "$PLATFORM_PATH" $PREPARED_KB $REPO_PATH_FILE "$ERRORS_FILE"
    else
        python3 "${PLATFORM_PATH}"/scripts/kb_scripts/prepare_kb.py "$APP_ROOT_PATH" $PREPARED_KB $REPO_PATH_FILE "$ERRORS_FILE"
    fi
