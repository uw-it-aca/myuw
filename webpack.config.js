'use strict'
const path = require('path');
const ManifestPlugin = require('webpack-manifest-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

module.exports = {
  mode: (process.env.ENV === 'localdev' ? 'development' : 'production'),
  context: __dirname,
  optimization: {
    minimizer: [
      new TerserJSPlugin(),
      new OptimizeCSSAssetsPlugin({
        cssProcessorOptions: {
          safe: true,
          discardComments: {
            removeAll: true,
          },
        },
      })
    ],
    splitChunks: {
      chunks: 'all',
    },
  },
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
    textbooks: [
      "./myuw/static/vue/textbooks.js"
    ],
    teaching_classlist: [
      "./myuw/static/vue/teaching_classlist.js"
    ]
  },
  output: {
      path: path.resolve('../static/myuw/'),
      filename: "[name]-[hash].js",
      chunkFilename: '[id]-[chunkhash].js',
      publicPath: '/myuw/',
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
          'sass-loader'
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
    new ManifestPlugin(),
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: '[name]-[hash].css',
      chunkFilename: '[id]-[chunkhash].css',
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
