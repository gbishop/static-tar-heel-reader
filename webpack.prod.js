var path = require("path");

module.exports = [
  {
    resolve: {
      extensions: [".ts", ".js"]
    },
    mode: "production",
    entry: {
      find: "./src/find.ts",
      book: "./src/book.ts",
      index: "./src/index.ts",
      settings: "./src/settings.ts",
      favorites: "./src/favorites.ts"
    },
    output: {
      filename: "[name].[chunkhash:6].js",
      path: path.resolve(__dirname, "dist")
    },
    module: {
      rules: [{ test: /\.ts$/, loader: "ts-loader" }]
    }
  },
  {
    resolve: {
      extensions: [".ts", ".js"]
    },
    mode: "production",
    entry: {
      worker: "./src/service-worker.ts"
    },
    output: {
      filename: "[name].js",
      path: path.resolve(__dirname, "dist")
    },
    module: {
      rules: [{ test: /\.ts$/, loader: "ts-loader" }]
    }
  }
];
