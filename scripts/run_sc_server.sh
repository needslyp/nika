set -eo pipefail

source set_vars.sh

python3 "${PLATFORM_PATH}"/sc-machine/scripts/run_sc_server.py -c "${APP_ROOT_PATH}"/idesa.ini
