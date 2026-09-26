import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_');
  if (command === 'build') {
    const apiUrl = process.env.VITE_API_BASE_URL || env.VITE_API_BASE_URL;
    if (!apiUrl || !/^https?:\/\//.test(apiUrl)) {
      throw new Error('Set VITE_API_BASE_URL to the backend URL ending in /api/v1 before building.');
    }
  }
  return {
  plugins: [
    react(),
    tailwindcss(),
  ],
  };
})

