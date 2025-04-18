module.exports = {
  transform: {
    "^.+\\.(js|jsx)$": ["babel-jest", { configFile: './babel.config.cjs' }]
  },
  transformIgnorePatterns: [
    "/node_modules/(?!.*\\.mjs$)"
  ],
  testEnvironment: "jsdom",
  moduleNameMapper: {
    "\\.(css|less|scss)$": "<rootDir>/src/tests/__mocks__/styleMock.js"
  },
  setupFilesAfterEnv: ["<rootDir>/src/tests/setupTests.js"]
};
