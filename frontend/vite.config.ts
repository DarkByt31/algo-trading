import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default (configEnv = {}) => {
  // ensure mode is defined (fallback to NODE_ENV or 'development')
  const mode = configEnv.mode || process.env.NODE_ENV || 'development'
  // load env variables for current mode (including VITE_ prefixed vars)
  const env = loadEnv(mode, process.cwd(), '') || {}
  const backendTarget = env.VITE_BACKEND_URL || 'http://backend:8000'

  return defineConfig({
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 3000,
      proxy: {
        '/api': {
          target: backendTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '/api/v1'),
        },
      },
    },
  })
}
