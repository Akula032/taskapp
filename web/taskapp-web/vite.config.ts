import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { presetAttributify } from 'unocss'
import presetWind3 from '@unocss/preset-wind3'
// import { presetUno } from 'unocss'
import extractorPug from '@unocss/extractor-pug'
import Unocss from 'unocss/vite'
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    Unocss({
      // presetUno()
      presets: [presetAttributify(), presetWind3()],
      include: [
        './index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
        './node_modules/unocss/**/*.{vue,js,ts,jsx,tsx}',
      ],
      extractors: [extractorPug()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
