<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2 class="title">用户注册</h2>
      <el-form :model="form" label-width="70px">
        <el-form-item label="账号">
          <el-input v-model="form.username" placeholder="登录账号" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" placeholder="真实姓名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="密码" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="邮箱（可选）" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" placeholder="电话（可选）" />
        </el-form-item>
        <el-button type="primary" style="width: 100%" :loading="loading" @click="handleRegister">
          注 册
        </el-button>
        <div class="footer">
          <el-link type="primary" @click="$router.push('/login')">已有账号？去登录</el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '../api/auth'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', name: '', password: '', email: '', phone: '' })

async function handleRegister() {
  if (!form.username || !form.name || !form.password) {
    ElMessage.warning('请填写账号、姓名和密码')
    return
  }
  loading.value = true
  try {
    await register({ ...form, email: form.email || null, phone: form.phone || null })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1f6feb 0%, #6f42c1 100%);
}
.register-card {
  width: 400px;
  padding: 12px 8px;
}
.title {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}
.footer {
  margin-top: 16px;
  text-align: center;
}
</style>
