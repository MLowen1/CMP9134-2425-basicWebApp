// frontend/babel.config.cjs
console.log('--- Loading babel.config.cjs ---'); // Updated comment
// ... rest of the console logs ...
console.log('--- Exporting Babel config as function ---');

// Export a function instead of an object
module.exports = function (api) {
  // ... existing function code ...
  api.cache.using(() => process.env.NODE_ENV);
  console.log('--- Babel API cache enabled ---');

  return {
    presets: [
      // ... existing presets ...
      ['@babel/preset-env', { targets: { node: 'current' } }],
      ['@babel/preset-react', { runtime: 'automatic' }],
    ],
  };
};
