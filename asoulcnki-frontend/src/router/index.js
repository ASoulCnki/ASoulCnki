import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/index.vue'
import MIndex from '../views/mIndex.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'index',
    component: navigator.userAgent.match(/(iPhone|iPod|Android|ios|iPad)/i) ? MIndex : Index
  },
  {
    path: '/m_index',
    name: 'm_index',
    component: () => import(/* webpackChunkName: "m_index" */ '../views/mIndex.vue')
  },
  {
    path: '/maintaining',
    name: 'maintaining',
    component: () => import(/* webpackChunkName: "maintaining" */ '../views/maintaining.vue')
  },
  {
    path: '/result',
    name: 'result',
    component: () => import(/* webpackChunkName: "result" */ '../views/result.vue')
  },
  {
    path: '/protocol',
    name: 'protocol',
    component: () => import(/* webpackChunkName: "result" */ '../views/protocol.vue')
  },
  // 兼容旧版本.html
  {
    path: '/m_index.html',
    name: 'm_index',
    component: () => import(/* webpackChunkName: "m_index" */ '../views/mIndex.vue')
  },
  {
    path: '/maintaining.html',
    name: 'maintaining',
    component: () => import(/* webpackChunkName: "maintaining" */ '../views/maintaining.vue')
  },
  {
    path: '/result.html',
    name: 'result',
    component: () => import(/* webpackChunkName: "result" */ '../views/result.vue')
  },
  {
    path: '/protocol.html',
    name: 'protocol',
    component: () => import(/* webpackChunkName: "result" */ '../views/protocol.vue')
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
