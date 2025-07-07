import { createApp } from 'vue'
import App from './App.vue'
import './assets/reset.css'
import router from './router'
import 'uno.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
// createApp(App).mount('#app')
const app = createApp(App)
app.use(router)
app.use(Toast)
app.mount('#app')
