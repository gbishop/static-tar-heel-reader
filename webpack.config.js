var path = require('path');

module.exports = {
  resolve: {
    extensions: ['.ts', '.js'],
  },
  mode: 'development',
  entry: {
    find: './find.ts',
    book: './book.ts',
	index: './index.ts',
	worker: './service-worker.ts',
    settings: './settings.ts',
    favorites: './favorites.ts',
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '.'),
  },
  module: {
    rules: [{test: /\.ts$/, loader: 'ts-loader'}],
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
    proxy: [
      {
        context: ['/content', 'config.json'],
        target: 'https://gb.cs.unc.edu/static/tiny',
        secure: false,
        changeOrigin: true,
      },
    ],
  },
  devtool: 'eval-source-map',
};
