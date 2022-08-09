#!/bin/bash

echo "$1"

APP_ROOT_PATH=$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd)

if [ "$1" == "-ci" ];
    then
      {
        echo PLATFORM_VERSION="prerelease/0.7.0"
        echo PLATFORM_PATH="${APP_ROOT_PATH}/ostis-web-platform"
        echo SC_MACHINE_PATH="${PLATFORM_PATH}/sc-machine"
        echo WORKING_PATH="$(pwd)"
        echo PLATFORM_REPO="https://github.com/ostis-ai/ostis-web-platform.git"
        echo REPO_PATH_FILE="repo.path"
        echo SCRIPTS_PATH="${APP_ROOT_PATH}"/scripts
        echo KB_PATH="${APP_ROOT_PATH}"/kb
      } >> "$GITHUB_ENV"
        echo APP_ROOT_PATH="$(pwd)" >> "$GITHUB_ENV"
    else
        export PLATFORM_VERSION="prerelease/0.7.0"
        export PLATFORM_PATH="${APP_ROOT_PATH}/ostis-web-platform"
        export SC_MACHINE_PATH="${PLATFORM_PATH}/sc-machine"
        WORKING_PATH="$(pwd)"
        export WORKING_PATH
        export PLATFORM_REPO="https://github.com/ostis-ai/ostis-web-platform.git"
        export APP_ROOT_PATH
        export REPO_PATH_FILE="repo.path"
        export SCRIPTS_PATH="${APP_ROOT_PATH}"/scripts
        export KB_PATH="${APP_ROOT_PATH}"/kb
    fi
