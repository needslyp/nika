const target = process.env.ML_URL ?? 'https://localhost:3003';

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
    port: 3030,
    proxy,
};
