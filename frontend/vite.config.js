import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Specify the port you want to use
    strictPort: true, // Set to true to exit if port is already in use
    host: true, // Allow access from network
    // Optional: HMR configuration if needed within Docker
    hmr: {
      clientPort: 5173, // Ensure HMR client connects to the correct port
    },
    watch: {
      usePolling: true, // Necessary for file watching in some Docker setups
    },
    // Add proxy configuration here
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Assuming your Flask backend runs on port 5000
        changeOrigin: true,
        secure: false
      }
    }
  },
})