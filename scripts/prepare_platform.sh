#!/bin/bash

echo -en "Install OSTIS platform\n"
git clone "${PLATFORM_REPO}"
cd "${PLATFORM_PATH}" || { echo "OSTIS web platform wasn't installed"; exit 1; }
git checkout main
cd "${APP_ROOT_PATH}" || { echo "Submodules wasn't installed"; exit 1; }
git submodule update --init --recursive

cd "${PLATFORM_PATH}"/scripts || { echo "OSTIS web platform was incorrectly installed. Scripts not found"; exit 1; }
./prepare.sh no_build_kb no_build_sc_machine

if ! grep -q "${INTERFACE_PATH}" "${PLATFORM_PATH}/sc-machine/config/config.ini.in";
        then
            INTERFACE_PATH_ESCAPED="$(echo "${INTERFACE_PATH}" | sed -e 's/[/]/\\&/g')"
            sed -i "s/^path.*=.*/path = ${INTERFACE_PATH_ESCAPED}/" "${PLATFORM_PATH}/sc-machine/config/config.ini.in"
fi

if ! grep -q "${PYTHON_PATH}" "${PLATFORM_PATH}/sc-machine/config/config.ini.in";
        then
            PYTHON_PATH_ESCAPED="$(echo "${PYTHON_PATH}" | sed -e 's/[/]/\\&/g')"
            sed -i "/modules_path/ s/$/;${PYTHON_PATH_ESCAPED}/" "${PLATFORM_PATH}/sc-machine/config/config.ini.in"
fi
if ! grep -q "${CONNECTED_TOOLS_PATH}" "${PLATFORM_PATH}/sc-machine/config/config.ini.in";
        then
            CONNECTED_TOOLS_PATH_ESCAPED="$(echo "${CONNECTED_TOOLS_PATH}" | sed -e 's/[/]/\\&/g')"
            sed -i "/modules_path/ s/$/;${CONNECTED_TOOLS_PATH_ESCAPED}/" "${PLATFORM_PATH}/sc-machine/config/config.ini.in"
fi

cd "${PLATFORM_PATH}" || { echo "OSTIS web platform was removed"; exit 1; }
rm ./ims.ostis.kb/ui/ui_start_sc_element.scs
rm ./ims.ostis.kb/ims/knowledge_base_IMS.scs
rm -rf ./kb/menu                                                                                                                                                                                   

cd "${APP_ROOT_PATH}"/scripts || { echo "Scripts was removed"; exit 1; }
./prepare_kb.sh prepare_platform
