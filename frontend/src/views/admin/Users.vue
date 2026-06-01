<template>
  <div class="admin-users">
    <div class="page-header">
      <h2>用户管理</h2>
      <p>管理系统用户</p>
    </div>

    <el-card v-loading="loading">
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="created_at" label="创建时间">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="is_admin" label="管理员" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_admin ? 'danger' : 'primary'" size="small">
              {{ scope.row.is_admin ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="scope">
            <el-button
              :type="scope.row.is_admin ? 'warning' : 'success'"
              size="small"
              @click="handleToggleAdmin(scope.row)"
              :loading="scope.row._loading"
            >
              {{ scope.row.is_admin ? '取消管理员' : '设为管理员' }}
            </el-button>
            <el-popconfirm
              title="确定要注销该用户吗？注销后用户将无法登录"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="handleDeactivateUser(scope.row)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  size="small"
                  :loading="scope.row._loading"
                >
                  注销用户
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="pagination.total > 0"
        @current-change="handlePageChange"
        :current-page="pagination.currentPage"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, prev, pager, next"
        style="margin-top: 20px; justify-content: center"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api/index'

const loading = ref(false)
const users = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 获取用户列表
const fetchUsers = async (page = 1) => {
  loading.value = true
  try {
    const data = await api.get('/admin/users', {
      params: {
        page: page,
        per_page: pagination.value.pageSize
      }
    })

    if (data) {
      users.value = data.users
      pagination.value.total = data.total
      pagination.value.currentPage = data.current_page
    }
  } catch (error: any) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 处理分页
const handlePageChange = (page: number) => {
  fetchUsers(page)
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 设置/取消管理员
const handleToggleAdmin = async (user: any) => {
  // 为该用户设置loading状态
  user._loading = true

  try {
    const data = await api.put(`/admin/users/${user.id}/toggle-admin`)

    if (data) {
      ElMessage.success(data.message || '操作成功')
      // 刷新用户列表
      await fetchUsers(pagination.value.currentPage)
    }
  } catch (error: any) {
    console.error('操作失败:', error)
    const errorMessage = error?.response?.data?.message || error?.message || '操作失败'
    ElMessage.error(errorMessage)
  } finally {
    user._loading = false
  }
}

// 注销用户
const handleDeactivateUser = async (user: any) => {
  // 为该用户设置loading状态
  user._loading = true

  try {
    const data = await api.put(`/admin/users/${user.id}/deactivate`)

    if (data) {
      ElMessage.success(data.message || '注销成功')
      // 刷新用户列表
      await fetchUsers(pagination.value.currentPage)
    }
  } catch (error: any) {
    console.error('注销失败:', error)
    const errorMessage = error?.response?.data?.message || error?.message || '注销失败'
    ElMessage.error(errorMessage)
  } finally {
    user._loading = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.admin-users {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
}
</style>
