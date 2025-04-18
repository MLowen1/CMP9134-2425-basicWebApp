/** @type {import('tailwindcss').Config} */
module.exports = { // Ensure this uses module.exports if you had issues with postcss.config.js syntax
  content: [
    "./index.html", // Include your main HTML file
    "./src/**/*.{js,ts,jsx,tsx}", // Include all JS/TS/JSX/TSX files in the src directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}