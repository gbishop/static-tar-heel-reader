var path = require("path");

module.exports = {
  resolve: {
    extensions: ['.ts', '.js']
  },
  mode: "development",
  entry: {
    "find": "./find.ts",
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, '.'),
  },
  module: {
    rules: [
      { test: /\.ts$/, loader: "ts-loader" }
    ]
  },
  devServer: {
    stats: {
      assets: false,
      hash: false,
      chunks: false,
      errors: true,
      errorDetails: true,
    },
    overlay: true,
    /*
    proxy: {
      '/[0123]|index': {
        target: 'https://gb.cs.unc.edu/static/',
        secure: false,
        changeOrigin: true
      }
    }
  */
  }
};
