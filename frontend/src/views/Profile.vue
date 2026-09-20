<template>
  <el-card style="max-width: 560px">
    <template #header>个人信息修改</template>
    <el-form :model="form" label-width="90px">
      <el-form-item label="账号">
        <el-input v-model="form.username" disabled />
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="角色">
        <el-input :model-value="roleText" disabled />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item label="电话">
        <el-input v-model="form.phone" />
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="form.password" type="password" show-password placeholder="留空则不修改" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="loading" @click="handleSave">保存</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserInfo, updateUserInfo } from '../api/user'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const loading = ref(false)
const form = reactive({ username: '', name: '', email: '', phone: '', password: '' })

const roleMap = { admin: '管理员', teacher: '教师', student: '学生' }
const roleText = computed(() => roleMap[auth.role] || auth.role)

onMounted(async () => {
  const res = await getUserInfo()
  const u = res.data
  form.username = u.username
  form.name = u.name
  form.email = u.email || ''
  form.phone = u.phone || ''
})

async function handleSave() {
  loading.value = true
  try {
    const res = await updateUserInfo({
      name: form.name,
      email: form.email || null,
      phone: form.phone || null,
      password: form.password || null
    })
    auth.setUser(res.data)
    ElMessage.success('保存成功')
    form.password = ''
  } finally {
    loading.value = false
  }
}
</script>
