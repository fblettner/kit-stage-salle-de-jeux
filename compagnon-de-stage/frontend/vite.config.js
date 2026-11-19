import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    // Pendant le développement, les appels à /api sont redirigés vers le serveur Python (port 8000)
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
  build: {
    // "npm run build" range le site prêt à publier dans backend/dist,
    // pour que le serveur Python le serve avec l'API (un seul programme à déployer)
    outDir: '../backend/dist',
    emptyOutDir: true,
  },
})
