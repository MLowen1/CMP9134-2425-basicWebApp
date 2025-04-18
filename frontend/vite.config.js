import { defineConfig } from 'vite'; // Changed to import
import react from '@vitejs/plugin-react'; // Changed to import

// https://vitejs.dev/config/
export default defineConfig({ // Changed to export default
  plugins: [react()],
  server: {
    host: true, // Allow access from network
    port: 5173, // Default Vite port
    // Optional: HMR configuration if needed within Docker
    hmr: {
      clientPort: 5173, // Ensure HMR client connects to the correct port
    },
    watch: {
      usePolling: true, // Necessary for file watching in some Docker setups
    },
  },
});