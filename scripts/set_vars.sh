#!/bin/bash

echo "$1"

APP_ROOT_PATH=$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd)

if [ "$1" == "-ci" ];
    then
      {
        echo PLATFORM_PATH="${APP_ROOT_PATH}/ostis-web-platform"
        echo WORKING_PATH="$(pwd)"
        echo PYTHON_PATH="${APP_ROOT_PATH}"/problem-solver/py/services
        echo PLATFORM_REPO="https://github.com/ostis-ai/ostis-web-platform.git"
        echo REPO_PATH_FILE="repo.path"
        echo PREPARED_KB="prepared_kb"
        echo ERRORS_FILE="${APP_ROOT_PATH}"/ostis-web-platform/scripts/prepare.log
        echo INTERFACE_PATH="${APP_ROOT_PATH}"
      } >> "$GITHUB_ENV"
        echo APP_ROOT_PATH="$(pwd)" >> "$GITHUB_ENV"
    else 
        export PLATFORM_PATH="${APP_ROOT_PATH}/ostis-web-platform"
        WORKING_PATH="$(pwd)"
        export WORKING_PATH
        export PYTHON_PATH="${APP_ROOT_PATH}"/problem-solver/py/services
        export PLATFORM_REPO="https://github.com/ostis-ai/ostis-web-platform.git"
        export APP_ROOT_PATH
        export REPO_PATH_FILE="repo.path"
        export PREPARED_KB="prepared_kb"
        export ERRORS_FILE="${PLATFORM_PATH}"/scripts/prepare.log
        export INTERFACE_PATH="${APP_ROOT_PATH}"
    fi    
