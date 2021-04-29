import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import QNA from '../views/QNA.vue'
import News from '../views/News.vue'
import SelfService from '../views/SelfService'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/news',
    name: 'News',
    component: News
  },
  {
    path: '/qna',
    name: 'QNA',
    component: QNA
  },
  {
    path: '/selfservice',
    name: 'SelfService',
    component: SelfService
  }
]

const router = new VueRouter({
  routes
})

export default router
