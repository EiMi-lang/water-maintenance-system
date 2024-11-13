import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/fault-warning'
  },
  {
    path: '/fault-warning',
    name: 'FaultWarning',
    component: () => import('@/views/FaultWarning.vue')
  },
  {
    path: '/diagnosis',
    name: 'Diagnosis',
    component: () => import('@/views/FaultDiagnosis.vue')
  },
  {
    path: '/device-details',
    name: 'DeviceDetail',
    component: () => import('@/views/DeviceDetails.vue')
  },
  {
    path: '/simulation',
    name: 'Simulation',
    component: () => import('@/views/SimulationInput.vue')
  },
  {
    path: '/device-details/:deviceId',
    name: 'DeviceDetails',
    component: () => import('@/views/DeviceDetails.vue'),
    meta: { title: '设备详情' }
  }
]

const router = new VueRouter({
  routes
})

export default router
