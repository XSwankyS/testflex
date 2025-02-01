// main.js или main.ts
import { createApp } from 'vue';
import App from './App.vue';
import Toast from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const app = createApp(App);

app.use(Toast, {
  position: 'top-right'
});

app.mount('#app');