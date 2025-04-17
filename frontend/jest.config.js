module.exports = {
  transform: { "^.+\\.[jt]sx?$": "babel-jest" },
  testEnvironment: "jsdom",
  moduleFileExtensions: ["js", "jsx"],
  // Load custom matchers like toBeInTheDocument
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
};