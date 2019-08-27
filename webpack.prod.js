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
      favorites: "./src/favorites.ts",
      worker: "./src/worker.ts"
    },
    output: {
      filename: "[name].js",
      path: path.resolve(__dirname, "dist")
    },
    module: {
      rules: [{ test: /\.ts$/, loader: "ts-loader" }]
    },
    optimization: {
      minimize: false
    }
  }
];
