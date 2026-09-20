<template>
  <el-card>
    <div class="toolbar">
      <el-radio-group v-model="query.status" @change="load">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="pending">待审核</el-radio-button>
        <el-radio-button value="approved">已通过</el-radio-button>
        <el-radio-button value="rejected">已驳回</el-radio-button>
        <el-radio-button value="cancelled">已取消</el-radio-button>
      </el-radio-group>
    </div>

    <el-table :data="list" v-loading="loading" border>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="lab_name" label="实验室" />
      <el-table-column prop="lab_location" label="位置" show-overflow-tooltip />
      <el-table-column prop="date" label="日期" width="110" />
      <el-table-column label="时段" width="130">
        <template #default="{ row }">{{ row.start_time }} ~ {{ row.end_time }}</template>
      </el-table-column>
      <el-table-column prop="purpose" label="用途" show-overflow-tooltip />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusTag(row.status)">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="review_comment" label="审核意见" show-overflow-tooltip />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending' || row.status === 'approved'"
            type="danger"
            size="small"
            @click="handleCancel(row)"
          >取消</el-button>
          <span v-else style="color: #909399">-</span>
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
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listReservations, cancelReservation } from '../../api/reservation'

const loading = ref(false)
const list = ref([])
const total = ref(0)
const query = reactive({ page: 1, page_size: 10, status: '' })

const statusMap = { pending: '待审核', approved: '已通过', rejected: '已驳回', cancelled: '已取消' }
const statusTagMap = { pending: 'warning', approved: 'success', rejected: 'danger', cancelled: 'info' }
const statusText = (s) => statusMap[s] || s
const statusTag = (s) => statusTagMap[s] || 'info'

async function load() {
  loading.value = true
  try {
    const params = { page: query.page, page_size: query.page_size }
    if (query.status) params.status = query.status
    const res = await listReservations(params)
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

async function handleCancel(row) {
  await ElMessageBox.confirm('确定取消该预约吗？', '提示', { type: 'warning' })
  await cancelReservation(row.id)
  ElMessage.success('已取消')
  load()
}

onMounted(load)
</script>

<style scoped>
.toolbar {
  margin-bottom: 16px;
}
.pagination {
  margin-top: 16px;
  justify-content: flex-end;
}
</style>
