<template>
  <el-card>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="搜索名称/编号" clearable style="width: 200px" @keyup.enter="load" />
      <el-select v-model="query.lab_id" placeholder="所属实验室" clearable style="width: 180px">
        <el-option v-for="l in labs" :key="l.id" :label="l.name" :value="l.id" />
      </el-select>
      <el-select v-model="query.status" placeholder="状态" clearable style="width: 140px">
        <el-option label="可用" value="available" />
        <el-option label="使用中" value="in_use" />
        <el-option label="维护中" value="maintenance" />
      </el-select>
      <el-button type="primary" @click="load">查询</el-button>
      <el-button type="success" @click="openDialog()">新增设备</el-button>
    </div>

    <el-table :data="list" v-loading="loading" border>
      <el-table-column prop="id" label="ID" width="70" />
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
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑设备' : '新增设备'" width="520px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="编号">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="型号">
          <el-input v-model="form.model" />
        </el-form-item>
        <el-form-item label="所属实验室">
          <el-select v-model="form.lab_id" style="width: 100%">
            <el-option v-for="l in labs" :key="l.id" :label="l.name" :value="l.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="可用" value="available" />
            <el-option label="使用中" value="in_use" />
            <el-option label="维护中" value="maintenance" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listEquipments, createEquipment, updateEquipment, deleteEquipment } from '../../api/equipment'
import { listLabs } from '../../api/lab'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const list = ref([])
const labs = ref([])
const total = ref(0)
const query = reactive({ page: 1, page_size: 10, keyword: '', lab_id: '', status: '' })

const emptyForm = { id: null, name: '', code: '', model: '', lab_id: null, status: 'available', description: '' }
const form = reactive({ ...emptyForm })

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
    if (query.status) params.status = query.status
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

function openDialog(row) {
  Object.assign(form, emptyForm, row ? { ...row } : {})
  dialogVisible.value = true
}

async function handleSave() {
  if (!form.name || !form.code || !form.lab_id) {
    ElMessage.warning('请填写名称、编号并选择所属实验室')
    return
  }
  submitting.value = true
  try {
    const data = {
      name: form.name,
      code: form.code,
      model: form.model || null,
      lab_id: form.lab_id,
      status: form.status,
      description: form.description || null
    }
    if (form.id) {
      await updateEquipment(form.id, data)
    } else {
      await createEquipment(data)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    load()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除设备「${row.name}」吗？`, '提示', { type: 'warning' })
  await deleteEquipment(row.id)
  ElMessage.success('删除成功')
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
