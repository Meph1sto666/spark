import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    watch: {
      ignored: ['**/data/**/*', '**/dep/**/*', '**/build/**/*', '**/lib/**/*', '**/ref/**/*', '**/node_modules/**/*', '**/.github/**/*'],
    },
  },
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}'],
  },
});
