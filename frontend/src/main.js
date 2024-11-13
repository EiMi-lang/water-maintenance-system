import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

Vue.use(ElementUI)

Vue.config.productionTip = false


// 全局配置 axios
// app.config.globalProperties.$axios = axios
// 配置 axios 默认值
axios.defaults.baseURL = 'http://localhost:8088'  // 设置基础URL
axios.defaults.timeout = 10000  // 设置超时时间

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
