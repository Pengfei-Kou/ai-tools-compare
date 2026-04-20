import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

export default defineConfig({
  integrations: [react()],
  server: {
    host: '0.0.0.0',
    port: 4321,
  },
  vite: {
    server: {
      allowedHosts: ['ai-compare.duckdns.org'],
      hmr: {
        clientPort: 443,
        protocol: 'wss',
      },
    },
  },
});
