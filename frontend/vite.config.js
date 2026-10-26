import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const proxy = {
  '^/(players|posts|settings)/': 'http://127.0.0.1:8000',
  '/media/': 'http://127.0.0.1:8000',
  '/admin/': 'http://127.0.0.1:8000',
  '/ckeditor5/': 'http://127.0.0.1:8000',
  '/static/': 'http://127.0.0.1:8000',
};

export default defineConfig({
  plugins: [react()],
  server: { proxy },
  preview: { proxy },
  test: {
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
    clearMocks: true,
  },
});
