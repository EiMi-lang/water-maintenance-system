import Vue from 'vue'
import VueRouter from 'vue-router'
import DeviceList from '../views/DeviceList.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'DeviceList',
    component: DeviceList
  }
]

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
