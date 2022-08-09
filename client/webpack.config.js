const webpack = require('webpack');
const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');
const outputPath = path.resolve(__dirname, 'assets');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const appDirectory = fs.realpathSync(process.cwd());
const resolveAppPath = (relativePath) => path.resolve(appDirectory, relativePath);
const host = process.env.HOST || 'localhost';

process.env.NODE_ENV = 'development';

module.exports = {
    plugins: ['@babel/plugin-proposal-class-properties', '@babel/proposal-object-rest-spread'],
    mode: 'development',
    entry: resolveAppPath('src/index.tsx'),

    output: {
        filename: 'idesa-web.js',
        path: outputPath,
        libraryTarget: 'umd',
        library: 'IDESAWeb',
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.css'],
    },
    devServer: {
        contentBase: resolveAppPath('src'),
        //'assets/templates'
        compress: true,

        hot: true,

        host,

        port: 3003,
        historyApiFallback: true,
        publicPath: '/',
    },
    plugins: [
        new webpack.EnvironmentPlugin(Object.keys(dotenv.config().parsed || {})),
        // new HtmlWebpackPlugin({
        //     inject: true,
        //     template: resolveAppPath('assets/templates/index.html'),
        // }),
    ],

    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg|png)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'fonts/',
                        },
                    },
                ],
            },
            {
                test: /\.tsx|\.js|\.ts$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env', '@babel/preset-react', '@babel/preset-typescript'],
                        },
                    },

                    {
                        loader: 'ts-loader',
                        options: {
                            configFile: path.resolve('./tsconfig.json'),
                        },
                    },
                ],
            },
        ],
    },
};
