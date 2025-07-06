import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:4000', // Port auf 4000 geändert
        changeOrigin: true
      },
      '/socket.io': {
        target: 'http://localhost:4000', // Port auf 4000 geändert
        ws: true
      }
    }
  }
})