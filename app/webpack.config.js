/*
 * Copyright 2019-2020 Simon Zigelli
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const path = require('path');
const autoprefixer = require('autoprefixer');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    // mode: 'development',
    mode: 'production',
    entry: {
        main: ['./index.js', './style.scss']
    },
    output: {
        filename: 'js/[name].bundle.js',
        chunkFilename: 'js/[name].bundle.js',
        libraryTarget: 'var',
        library: ['StagyBee', '[name]'],
        path: path.resolve(__dirname, 'StagyBee/static')
    },
    optimization: {
        splitChunks: {
            cacheGroups: {
                external: {
                    test: /node_modules/,
                    chunks: 'initial',
                    name: 'external',
                    enforce: true
                },
            }
        }
    },
    devtool: 'source-map',
    module: {
        rules: [{
            test: /\.scss$/,
            use: [
                {
                    loader: 'file-loader',
                    options: {
                        name: 'css/bundle.css',
                    },
                },
                {loader: 'extract-loader'},
                {loader: 'css-loader'},
                {
                    loader: 'postcss-loader',
                    options: {
                        plugins: () => [autoprefixer()]
                    }
                },
                {
                    loader: 'sass-loader',
                    options: {
                        // Prefer Dart Sass
                        implementation: require('sass'),
                        sassOptions: {
                            includePaths: ['./node_modules'],
                        },
                    },
                }
            ],
        },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'fonts',
                            publicPath: '../fonts',
                        }
                    }
                ]
            }
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/[name].bundle.css',
        }),
    ],
};