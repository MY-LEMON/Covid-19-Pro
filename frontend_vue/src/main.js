import Vue from 'vue'
import App from './App.vue'
import router from './router'
import qs from 'qs'
import axios from "axios"

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false

Vue.use(ElementUI)


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

Vue.prototype.$axios = axios
Vue.prototype.$qs = qs
