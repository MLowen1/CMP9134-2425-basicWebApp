export default {
  transform: {
    "^.+\.(js|jsx)$": ["babel-jest", { configFile: './babel.config.cjs' }]
  },
  testEnvironment: "jsdom",
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "<rootDir>/src/tests/__mocks__/styleMock.js"
  },
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  globalTeardown: "<rootDir>/jest.teardown.cjs", // Update extension to .cjs
  verbose: true, // Ensure verbose output is enabled
  collectCoverage: true, // Ensure coverage is enabled (matches script)
  coverageDirectory: "coverage", // Optional: specify coverage output dir
  // Add roots if tests are only in src
  // roots: ["<rootDir>/src"],
};
