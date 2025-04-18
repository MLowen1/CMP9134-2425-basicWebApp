// frontend/babel.config.js
console.log('--- Loading babel.config.js ---');
console.log('Node version:', process.version);
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('Jest worker ID:', process.env.JEST_WORKER_ID);
console.log('Current working directory:', process.cwd());
console.log('__filename:', __filename);
console.log('--- Exporting Babel config as function ---');

// Export a function instead of an object
module.exports = function (api) {
  // You can use api.cache(true) to cache the config based on NODE_ENV
  api.cache.using(() => process.env.NODE_ENV);
  console.log('--- Babel API cache enabled ---');

  return {
    presets: [
      // Use @babel/preset-env options if needed, e.g., targeting specific node version
      ['@babel/preset-env', { targets: { node: 'current' } }],
      ['@babel/preset-react', { runtime: 'automatic' }],
    ],
  };
};