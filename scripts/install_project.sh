#!/bin/bash
source set_vars.sh

prepare_platform()
{
	cd "${PLATFORM_PATH}"/scripts
	./prepare.sh no_build_kb
}


prepare_platform_without_build()
{
	./scripts/prepare_platform.sh
}


build_kb()
{
	cd "${APP_ROOT_PATH}"/scripts
	./build_kb.sh
}


build_problem_solver()
{
	cd "${APP_ROOT_PATH}"/scripts
	./build_problem_solver.sh
	cat "${PLATFORM_PATH}"/sc-machine/bin/config.ini >> "${PLATFORM_PATH}"/config/sc-web.ini
}

build_interface()
{
	cd "${APP_ROOT_PATH}"/scripts
	./build_interface.sh
}

set -eo pipefail

cd "${APP_ROOT_PATH}"
if [ -d "${PLATFORM_PATH}" ];
	then
		echo -en "Update OSTIS platform\n"
		cd "${PLATFORM_PATH}"
		git pull
		cd "${APP_ROOT_PATH}"
		git submodule update --init --recursive
		prepare_platform
		build_kb
		build_interface
	else
		prepare_platform_without_build
		build_problem_solver
		build_kb
		build_interface
fi

cd "${WORKING_PATH}"

