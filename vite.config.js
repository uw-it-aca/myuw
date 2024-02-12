import { fileURLToPath, URL } from 'url';
import { defineConfig, splitVendorChunkPlugin } from 'vite';
import vue from '@vitejs/plugin-vue2';

// https://vitejs.dev/config/
export default defineConfig({
  // MARK: start vite build config

  // vite creates a manifest and assets during the build process (local and prod)
  // django collectstatics will put assets in '/static/app_name/assets'
  // django will put the manifest in '/static/manifest.json'
  // vite manifest prefaces all files with the path 'app_name/assets/xxxx'
  build: {
    manifest: true,
    rollupOptions: {
      input: [
        // list all entry points
        './myuw_vue/home.js',
        './myuw_vue/academics.js',
        './myuw_vue/teaching.js',
        './myuw_vue/accounts.js',
        './myuw_vue/future_quarters.js',
        './myuw_vue/profile.js',
        './myuw_vue/textbooks.js',
        './myuw_vue/husky_experience.js',
        './myuw_vue/notices.js',
        './myuw_vue/teaching_classlist.js',
        './myuw_vue/resources.js',
        './myuw_vue/calendar.js',
      ],
    },
    outDir: './myuw/static/', // relative path to django's static directory
    assetsDir: 'myuw/assets', // default ('assets')... this is the namespaced subdirectory of outDir that vite uses
    emptyOutDir: false, // set to false to ensure favicon is not overwritten
  },
  base: '/static/', // allows for proper css url path creation during the build process

  // MARK: standard vite/vue plugin and resolver config
  plugins: [vue(), splitVendorChunkPlugin()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./myuw_vue', import.meta.url)),
      vue: 'vue/dist/vue.esm.js',
    },
  },
});
