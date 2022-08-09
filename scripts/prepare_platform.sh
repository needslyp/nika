#!/bin/bash

echo -en "Install OSTIS platform\n"
git clone "${PLATFORM_REPO}" --single-branch --branch "${PLATFORM_VERSION}" || { echo "OSTIS web platform wasn't installed"; exit 1; }

cd "${APP_ROOT_PATH}"
git submodule update --init --recursive || { echo "Submodules weren't installed"; exit 1; }

cd "${PLATFORM_PATH}"/scripts || { echo "OSTIS web platform was installed incorrectly. Scripts not found"; exit 1; }
./prepare.sh no_build_kb no_build_sc_machine
