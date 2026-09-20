<template>
  <el-card>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="搜索名称/编号" clearable style="width: 220px" @keyup.enter="load" />
      <el-select v-model="query.lab_id" placeholder="所属实验室" clearable style="width: 180px" @change="load">
        <el-option v-for="l in labs" :key="l.id" :label="l.name" :value="l.id" />
      </el-select>
      <el-button type="primary" @click="load">查询</el-button>
    </div>

    <el-table :data="list" v-loading="loading" border>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="code" label="编号" width="120" />
      <el-table-column prop="model" label="型号" width="120" />
      <el-table-column prop="lab_name" label="所属实验室" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusTag(row.status)">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
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
import { listEquipments } from '../../api/equipment'
import { listLabs } from '../../api/lab'

const loading = ref(false)
const list = ref([])
const labs = ref([])
const total = ref(0)
const query = reactive({ page: 1, page_size: 10, keyword: '', lab_id: '' })

const statusMap = { available: '可用', in_use: '使用中', maintenance: '维护中' }
const statusTagMap = { available: 'success', in_use: 'primary', maintenance: 'warning' }
const statusText = (s) => statusMap[s] || s
const statusTag = (s) => statusTagMap[s] || 'info'

async function loadLabs() {
  const res = await listLabs({ page: 1, page_size: 100 })
  labs.value = res.data.items
}

async function load() {
  loading.value = true
  try {
    const params = { page: query.page, page_size: query.page_size, keyword: query.keyword || undefined }
    if (query.lab_id) params.lab_id = query.lab_id
    const res = await listEquipments(params)
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

onMounted(() => {
  loadLabs()
  load()
})
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
