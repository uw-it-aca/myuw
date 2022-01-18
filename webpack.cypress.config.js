'use strict'
const path = require('path');
const webpack = require('webpack');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

if (!('VUE_DEVTOOLS' in process.env) || process.env.VUE_DEVTOOLS.length === 0) {
  process.env.VUE_DEVTOOLS = process.env.ENV === 'localdev';
}

module.exports = {
  context: __dirname,
  entry: {
    home: [
      "./myuw_vue/home.js",
    ],
    academics: [
      "./myuw_vue/academics.js",
    ],
    teaching: [
      "./myuw_vue/teaching.js",
    ],
    accounts: [
      "./myuw_vue/accounts.js"
    ],
    future_quarters: [
      "./myuw_vue/future_quarters.js"
    ],
    profile: [
      "./myuw_vue/profile.js"
    ],
    textbooks: [
      "./myuw_vue/textbooks.js"
    ],
    husky_experience: [
      "./myuw_vue/husky_experience.js"
    ],
    notices: [
      "./myuw_vue/notices.js"
    ],
    teaching_classlist: [
      "./myuw_vue/teaching_classlist.js"
    ],
    resources: [
      "./myuw_vue/resources.js"
    ],
    calendar: [
      "./myuw_vue/calendar.js"
    ],
  },

  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        options: {
          plugins: [
            ["istanbul", {extension: ['.js', '.vue']}],
          ],
        },
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ],
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'sass-loader',
            options: {
              sassOptions: { quietDeps: true },
            },
          }
        ],
      },
      {
        test: /\.less$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'less-loader'
        ]
      },
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, use: "url-loader?limit=10000&mimetype=application/font-woff" },
      { test: /\.(png|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, use: "file-loader" },
    ]
  },

  plugins: [
    new webpack.EnvironmentPlugin(['VUE_DEVTOOLS']),
    new CleanWebpackPlugin(),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name]-[contenthash].css',
      chunkFilename: '[id]-[contenthash].css',
    }),
    new HtmlWebpackPlugin(),
  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
    extensions: ['*', '.js', '.vue', '.json'],
  },

  stats: {
    colors: true,
  },
  devtool: 'eval-source-map',
}