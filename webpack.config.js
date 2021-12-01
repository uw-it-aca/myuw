'use strict'
const path = require('path');
const webpack = require('webpack');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

if (!('VUE_DEVTOOLS' in process.env) || process.env.VUE_DEVTOOLS.length === 0) {
  process.env.VUE_DEVTOOLS = process.env.ENV === 'localdev';
}

module.exports = {
  mode: (process.env.ENV === 'localdev' ? 'development' : 'production'),
  context: __dirname,
  optimization: {
    minimizer: [
      new CssMinimizerPlugin(),
      new TerserJSPlugin(),
    ],
    splitChunks: {
      chunks: 'all',
    },
  },

  // MARK: Specify the 'entry point' js for the vue application. Multiple entry points can be
  // declared using an object
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

  // MARK: Put the 'bundles' in a name-spaced directory in the django app statics
  // where it be collected when using 'collectstatic'
  output: {
    path: path.resolve('./myuw/static/myuw/bundles/'),
    filename: "[name]-[contenthash].js",
    chunkFilename: '[id]-[contenthash].js',
    publicPath: '/static/myuw/bundles/',
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
        loader: 'babel-loader'
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

    // MARK: Put the 'webpack-stats.json' file in the static location directory so that it 
    // can be accessed during development and production static collection
    new BundleTracker({
      //path: path.resolve('../static/myuw/'),
      filename: './myuw/static/webpack-stats.json',
    }),
  ],

  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
  }
}

if (process.env.ENV == 'localdev') {
  module.exports.devtool = 'source-map';
}

if (process.env.BUNDLE_ANALYZER === "True") {
  module.exports.plugins.push(
    new BundleAnalyzerPlugin({
      analyzerHost: '0.0.0.0',
    })
  );
}
