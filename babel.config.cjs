console.log('*** IS babel.config.cjs BEING READ AT ALL? ***'); // Added distinct log
// frontend/babel.config.cjs
console.log('--- Loading babel.config.cjs ---'); // Updated comment
// ... rest of the console logs ...
console.log('--- Exporting Babel config as function ---');

// Export a function instead of an object
module.exports = function (api) {
  // ... existing function code ...
  console.log('--- Babel config function called ---'); // Added log
  api.cache.using(() => process.env.NODE_ENV);
  console.log('--- Babel API cache enabled ---');
  console.log(`--- Babel NODE_ENV: ${process.env.NODE_ENV} ---`); // Added log

  const presets = [
      // ... existing presets ...
      ['@babel/preset-env', { targets: { node: 'current' } }],
      ['@babel/preset-react', { runtime: 'automatic' }],
  ];
  console.log('--- Babel presets configured:', JSON.stringify(presets)); // Added log

  return {
    presets, // Use the defined presets
  };
};
