<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.labTotal }}</div>
          <div class="stat-label">实验室总数</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.equipmentTotal }}</div>
          <div class="stat-label">设备总数</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.reservationTotal }}</div>
          <div class="stat-label">{{ isStudent ? '我的预约数' : '待审核预约数' }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="welcome" style="margin-top: 16px">
      <h3>欢迎使用智能实验室预约系统</h3>
      <p v-if="isStudent">你可以浏览实验室与设备，并在线发起预约，等待审核通过后即可使用实验室。</p>
      <p v-else>你可以管理用户、实验室、设备，并对学生提交的预约进行审核。</p>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted } from 'vue'
import { listLabs } from '../api/lab'
import { listEquipments } from '../api/equipment'
import { listReservations } from '../api/reservation'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const isStudent = computed(() => auth.role === 'student')

const stats = reactive({ labTotal: 0, equipmentTotal: 0, reservationTotal: 0 })

onMounted(async () => {
  const [labRes, equipRes, resvRes] = await Promise.all([
    listLabs({ page: 1, page_size: 1 }),
    listEquipments({ page: 1, page_size: 1 }),
    listReservations({ page: 1, page_size: 1, status: isStudent.value ? undefined : 'pending' })
  ])
  stats.labTotal = labRes.data.total
  stats.equipmentTotal = equipRes.data.total
  stats.reservationTotal = resvRes.data.total
})
</script>

<style scoped>
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #1f6feb;
}
.stat-label {
  margin-top: 8px;
  color: #909399;
}
.welcome p {
  color: #606266;
}
</style>
