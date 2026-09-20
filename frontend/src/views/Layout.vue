<template>
  <el-container class="layout">
    <el-aside width="210px" class="aside">
      <div class="logo">实验室预约系统</div>
      <el-menu :default-active="$route.path" router background-color="#001529" text-color="#a6adb4" active-text-color="#ffffff">
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="page-title">{{ $route.meta.title }}</div>
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ auth.user?.name || auth.user?.username }}
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const auth = useAuthStore()

const allMenus = {
  dashboard: { path: '/dashboard', title: '数据看板', icon: 'DataAnalysis' },
  profile: { path: '/profile', title: '个人信息', icon: 'User' },
  user: { path: '/user', title: '用户管理', icon: 'UserFilled', roles: ['admin'] },
  lab: { path: '/lab', title: '实验室管理', icon: 'OfficeBuilding', roles: ['admin'] },
  equipment: { path: '/equipment', title: '设备管理', icon: 'Cpu', roles: ['admin'] },
  approval: { path: '/approval', title: '预约审核', icon: 'Checked', roles: ['admin', 'teacher'] },
  'lab-list': { path: '/lab-list', title: '实验室列表', icon: 'OfficeBuilding', roles: ['student'] },
  'equipment-list': { path: '/equipment-list', title: '设备列表', icon: 'Cpu', roles: ['student'] },
  'my-reservations': { path: '/my-reservations', title: '我的预约', icon: 'Calendar', roles: ['student'] }
}

const menus = computed(() => {
  return Object.values(allMenus).filter((m) => !m.roles || m.roles.includes(auth.role))
})

function handleCommand(command) {
  if (command === 'logout') {
    auth.logout()
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/profile')
  }
}
</script>

<style scoped>
.layout {
  height: 100%;
}
.aside {
  background-color: #001529;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
}
.aside :deep(.el-menu) {
  border-right: none;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e6e6e6;
  background: #fff;
}
.page-title {
  font-size: 16px;
  font-weight: 600;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: #303133;
}
.main {
  background: #f0f2f5;
}
</style>
