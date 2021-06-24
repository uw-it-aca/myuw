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
      "./myuw/static/vue/home.js",
    ],
    academics: [
      "./myuw/static/vue/academics.js",
    ],
    teaching: [
      "./myuw/static/vue/teaching.js",
    ],
    accounts: [
      "./myuw/static/vue/accounts.js"
    ],
    future_quarters: [
      "./myuw/static/vue/future_quarters.js"
    ],
    profile: [
      "./myuw/static/vue/profile.js"
    ],
    textbooks: [
      "./myuw/static/vue/textbooks.js"
    ],
    husky_experience: [
      "./myuw/static/vue/husky_experience.js"
    ],
    notices: [
      "./myuw/static/vue/notices.js"
    ],
    teaching_classlist: [
      "./myuw/static/vue/teaching_classlist.js"
    ],
    resources: [
      "./myuw/static/vue/resources.js"
    ],
    calendar: [
      "./myuw/static/vue/calendar.js"
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