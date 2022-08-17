const target = process.env.ML_URL ?? 'https://pcare.dev-ml-service.ostis.ai/';

const proxy = {
    '/api': {
        target,
        logLevel: 'debug',
        changeOrigin: true,
        secure: false,
    },
};

module.exports = {
    compress: true,
    hot: true,
    open: true,
    https: true,
    historyApiFallback: true,
    port: 3080,
    proxy,
};
