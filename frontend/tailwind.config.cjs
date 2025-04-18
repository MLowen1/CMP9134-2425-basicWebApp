/** @type {import('tailwindcss').Config} */
module.exports = { // Ensure this uses module.exports if you had issues with postcss.config.js syntax
  content: [
    "./index.html", // Include your main HTML file
    "./src/**/*.{js,ts,jsx,tsx}", // Include all JS/TS/JSX/TSX files in the src directory
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          DEFAULT: '#3B82F6', // Blue-500
          'hover': '#2563EB', // Blue-600
          'dark': '#1D4ED8', // Blue-700
        },
        'secondary': {
          DEFAULT: '#6B7280', // Gray-500
          'hover': '#4B5563', // Gray-600
        },
        'danger': {
          DEFAULT: '#EF4444', // Red-500
          'hover': '#DC2626', // Red-600
        },
        'success': {
          DEFAULT: '#10B981', // Green-500
          'hover': '#059669', // Green-600
        },
        'neutral': {
          'light': '#F9FAFB', // Gray-50
          'DEFAULT': '#E5E7EB', // Gray-200
          'medium': '#9CA3AF', // Gray-400
          'dark': '#374151', // Gray-700
        },
        // Dark Theme Palette (Inspired by Remix)
        background: '#121212', // Very dark gray / near black
        foreground: '#E0E0E0', // Light gray for text
        'foreground-dark': '#A0A0A0', // Medium gray for secondary text
        card: '#1E1E1E', // Slightly lighter dark for card backgrounds
        border: '#333333', // Dark border color
        // Remix-style Accents
        'accent-cyan': '#22D3EE',
        'accent-green': '#4ADE80',
        'accent-yellow': '#FACC15',
        'accent-orange': '#F97316', // Added orange as another option
      }
      // Optional: Add font family if desired
      // fontFamily: {
      //   sans: ['Inter', 'sans-serif'], // Example using Inter
      // },
    },
  },
  plugins: [],
}
