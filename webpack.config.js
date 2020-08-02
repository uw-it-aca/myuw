'use strict'
const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = {
  devtool: (process.env.ENV == 'localdev' ? 'source-map' : 'none'),
  mode: (process.env.ENV === 'localdev' ? 'development' : 'production'),
  context: __dirname,
  optimization: {
    minimizer: [
      new TerserJSPlugin({}),
      new OptimizeCSSAssetsPlugin({
        cssProcessorOptions: {
          safe: true,
          discardComments: {
            removeAll: true,
          },
        },
      })
    ],
  },
  entry: {
      base: [
        "./myuw/static/vendor/css/bootstrap-3.3.5.min.css",
        "./myuw/static/vendor/css/font-awesome-4.7.0.min.css",
        "./myuw/static/vendor/css/user-fonts.css",
        "./myuw/static/css/mobile.less",
        "./myuw/static/css/desktop.less",
        "./myuw/static/css/typography.less",
        "./myuw/static/css/buttons.less",
        "./myuw/static/css/course_card.less",
        "./myuw/static/css/boilerplate.less",
        "./myuw/static/css/tabs.less",
        "./myuw/static/css/dropmenus.less",
        "./myuw/static/css/ratings.less",
        "./myuw/static/css/cards.less",
        "./myuw/static/css/components.less",
        "./myuw/static/css/photo_list.less",
        "./myuw/static/css/textbooks.less",
        "./myuw/static/css/huskyx.less",
        "./myuw/static/css/resources.less",
        "./myuw/static/css/notices.less",
      ],
      base_hybrid: "./myuw/static/css/hybrid.less",
  },
  output: {
      path: path.resolve('/static/myuw/'),
      filename: "[name]-[hash].js",
      chunkFilename: '[id]-[chunkhash].js',
      publicPath: '/static/myuw/',
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.js$/,
        loader: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [
          process.env.ENV === 'localdev' ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader'
        ],
      },
      {
        test: /\.scss$/,
        use: [
          process.env.ENV === 'localdev' ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ],
      },
      {
        test: /\.less$/,
        use: [
          process.env.ENV === 'localdev' ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          'less-loader'
        ]
      },
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
      { test: /\.(png|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
    ]
  },

  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({filename: './../static/myuw-webpack-stats.json'}),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css',
      chunkFilename: '[id]-[chunkhash].css',
    })
  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
    modules: ['node_modules'],
  }
}