const path = require('path');

module.exports = {
  entry: {
    'shared': './shared.ts',
    'scrub': './scrub.ts',
    'appeal': './appeal.ts',
    'appeal_fetcher': './appeal_fetcher.ts',
    'entity_fetcher': './entity_fetcher.ts',
  },
  resolve: {
    extensions: ['.ts', '.js'], // Automatically resolve these extensions
  },
  module: {
    rules: [
      {
        test: /\.ts$/, // Apply this rule to .ts files
        use: 'ts-loader', // Use ts-loader to process TypeScript files
        exclude: /node_modules/, // Exclude node_modules from processing
      },
    ],
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
    publicPath: '',
  },
  experiments: {
    topLevelAwait: true
  },
};
