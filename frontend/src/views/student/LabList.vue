<template>
  <el-card>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="搜索名称/编号" clearable style="width: 220px" @keyup.enter="load" />
      <el-button type="primary" @click="load">查询</el-button>
    </div>

    <el-table :data="list" v-loading="loading" border>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="code" label="编号" width="120" />
      <el-table-column prop="location" label="位置" />
      <el-table-column prop="capacity" label="容纳人数" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'available' ? 'success' : 'warning'">{{ row.status === 'available' ? '可用' : '维护中' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="primary" size="small" :disabled="row.status !== 'available'" @click="openReserve(row)">预约</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="pagination"
      layout="total, prev, pager, next"
      :total="total"
      :page-size="query.page_size"
      :current-page="query.page"
      @current-change="handlePage"
    />

    <el-dialog v-model="reserveVisible" title="预约实验室" width="480px">
      <el-form :model="reserveForm" label-width="90px">
        <el-form-item label="实验室">
          <el-input :model-value="currentLab?.name" disabled />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="reserveForm.date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="开始时间">
          <el-time-select v-model="reserveForm.start_time" start="08:00" step="00:30" end="22:00" placeholder="开始时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-time-select v-model="reserveForm.end_time" start="08:00" step="00:30" end="22:00" placeholder="结束时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="用途说明">
          <el-input v-model="reserveForm.purpose" type="textarea" :rows="3" placeholder="请说明实验内容/用途" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reserveVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleReserve">提交预约</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listLabs } from '../../api/lab'
import { createReservation } from '../../api/reservation'

const loading = ref(false)
const submitting = ref(false)
const reserveVisible = ref(false)
const currentLab = ref(null)
const list = ref([])
const total = ref(0)
const query = reactive({ page: 1, page_size: 10, keyword: '' })

const reserveForm = reactive({ lab_id: null, date: '', start_time: '', end_time: '', purpose: '' })

async function load() {
  loading.value = true
  try {
    const res = await listLabs({ page: query.page, page_size: query.page_size, keyword: query.keyword || undefined })
    list.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function handlePage(p) {
  query.page = p
  load()
}

function openReserve(row) {
  currentLab.value = row
  Object.assign(reserveForm, { lab_id: row.id, date: '', start_time: '', end_time: '', purpose: '' })
  reserveVisible.value = true
}

async function handleReserve() {
  if (!reserveForm.date || !reserveForm.start_time || !reserveForm.end_time || !reserveForm.purpose) {
    ElMessage.warning('请完整填写预约信息')
    return
  }
  submitting.value = true
  try {
    await createReservation(reserveForm)
    ElMessage.success('预约提交成功，等待审核')
    reserveVisible.value = false
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.pagination {
  margin-top: 16px;
  justify-content: flex-end;
}
</style>
