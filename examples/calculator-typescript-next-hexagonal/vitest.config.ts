import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: {
    alias: {
      // The real package throws outside a React Server environment.
      'server-only': fileURLToPath(new URL('./tests/support/serverOnly.ts', import.meta.url)),
    },
  },
  test: {
    environment: 'node',
  },
});
