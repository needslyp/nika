const target = process.env.ML_URL ?? 'http://localhost:3003';

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
    https: false,
    historyApiFallback: true,
    port: 3033,
    proxy,
};
