if [[ -z ${PLATFORM_PATH+1} ]];
then
  source set_vars.sh
fi

cd ${APP_ROOT_PATH}/interface
yarn && yarn start