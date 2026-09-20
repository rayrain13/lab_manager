import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes = [
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register', component: () => import('../views/Register.vue') },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: '数据看板' } },
      { path: 'profile', component: () => import('../views/Profile.vue'), meta: { title: '个人信息' } },
      { path: 'user', component: () => import('../views/admin/UserManage.vue'), meta: { title: '用户管理', roles: ['admin'] } },
      { path: 'lab', component: () => import('../views/admin/LabManage.vue'), meta: { title: '实验室管理', roles: ['admin'] } },
      { path: 'equipment', component: () => import('../views/admin/EquipmentManage.vue'), meta: { title: '设备管理', roles: ['admin'] } },
      { path: 'approval', component: () => import('../views/admin/ReservationApproval.vue'), meta: { title: '预约审核', roles: ['admin', 'teacher'] } },
      { path: 'lab-list', component: () => import('../views/student/LabList.vue'), meta: { title: '实验室列表', roles: ['student'] } },
      { path: 'equipment-list', component: () => import('../views/student/EquipmentList.vue'), meta: { title: '设备列表', roles: ['student'] } },
      { path: 'my-reservations', component: () => import('../views/student/MyReservations.vue'), meta: { title: '我的预约', roles: ['student'] } }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.path === '/login' || to.path === '/register') {
    return true
  }

  if (!auth.isLogin) {
    return '/login'
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.role)) {
    return '/dashboard'
  }

  return true
})

export default router
