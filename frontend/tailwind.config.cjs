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
          DEFAULT: '#00A45F', // Logo Green
          'hover': '#00894F', // Slightly darker for hover
          'dark': '#006B38', // Even darker for dark variant
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
          DEFAULT: '#00A45F', // Logo Green
          'hover': '#00894F', // Slightly darker for hover
        },
        'neutral': {
          'light': '#F9FAFB', // Gray-50
          'DEFAULT': '#E5E7EB', // Gray-200
          'medium': '#9CA3AF', // Gray-400
          'dark': '#374151', // Gray-700
        },
        // Dark Theme Palette (Inspired by Remix)
        background: '#131217', // Updated to new primary background
        foreground: '#E0E0E0', // Light gray for text
        'foreground-dark': '#A0A0A0', // Medium gray for secondary text
        card: '#1E1E1E', // Slightly lighter dark for card backgrounds
        border: '#333333', // Dark border color
        // Green Accents
        'accent-cyan': '#00A45F', // Logo Green
        'accent-green': '#00A45F', // Logo Green
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
