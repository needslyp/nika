if [[ -z ${PLATFORM_PATH+1} ]];
then
  source set_vars.sh
fi

cd ${APP_ROOT_PATH}/client
yarn && yarn webpack-dev