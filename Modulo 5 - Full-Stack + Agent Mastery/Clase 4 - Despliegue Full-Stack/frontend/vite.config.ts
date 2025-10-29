import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Tree-shaking: elimina código no usado
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,  // Elimina console.log en producción
        drop_debugger: true, // Elimina debugger statements
      },
    },
    // Code splitting: divide bundle en chunks para mejor caching
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor bundle: React y dependencias core (cacheable)
          vendor: ['react', 'react-dom', 'react-router-dom'],
          // Forms bundle: Solo se carga en páginas con formularios
          forms: ['react-hook-form', 'zod'],
        },
      },
    },
    // Compresión de assets
    reportCompressedSize: true,
    chunkSizeWarningLimit: 1000, // Warning si chunk > 1MB
    // Source maps solo para error reporting (no completos)
    sourcemap: 'hidden',
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  preview: {
    port: 4173,
  },
})
