<template>
  <div class="admin-users">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div>
          <h2>用户管理</h2>
          <p>管理系统所有用户</p>
        </div>
        <div class="header-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户名或邮箱"
            class="search-input"
            prefix-icon="Search"
            @keyup.enter="handleSearch"
          />
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <el-row :gutter="16" class="stats-cards">
      <el-col :span="6">
        <div class="mini-stat-card">
          <el-icon class="mini-stat-icon"><Users /></el-icon>
          <div>
            <p class="mini-stat-value">{{ totalUsers }}</p>
            <p class="mini-stat-label">总用户</p>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="mini-stat-card admin-card">
          <el-icon class="mini-stat-icon"><UserFilled /></el-icon>
          <div>
            <p class="mini-stat-value">{{ adminCount }}</p>
            <p class="mini-stat-label">管理员</p>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="mini-stat-card active-card">
          <el-icon class="mini-stat-icon"><Activity /></el-icon>
          <div>
            <p class="mini-stat-value">{{ activeUsers }}</p>
            <p class="mini-stat-label">活跃用户</p>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="mini-stat-card new-card">
          <el-icon class="mini-stat-icon"><Clock /></el-icon>
          <div>
            <p class="mini-stat-value">{{ newUsersToday }}</p>
            <p class="mini-stat-label">今日新增</p>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 用户列表 -->
    <el-card v-loading="loading" class="main-card">
      <div class="table-header">
        <span class="table-title">用户列表</span>
        <el-button type="primary" icon="Plus" class="add-btn">
          导出用户
        </el-button>
      </div>

      <el-table :data="users" style="width: 100%" class="users-table">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" sortable />
        <el-table-column label="用户信息" min-width="200">
          <template #default="scope">
            <div class="user-info-cell">
              <el-avatar :size="40" :src="scope.row.avatar" class="user-avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="user-details">
                <p class="user-name">{{ scope.row.username }}</p>
                <p class="user-email">{{ scope.row.email }}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" sortable>
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="is_admin" label="角色" width="120">
          <template #default="scope">
            <el-tag 
              :type="scope.row.is_admin ? 'danger' : 'primary'" 
              size="small"
              class="role-tag"
            >
              {{ scope.row.is_admin ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag 
              :type="scope.row.status === 'active' ? 'success' : 'warning'" 
              size="small"
            >
              {{ scope.row.status === 'active' ? '正常' : '已注销' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="scope">
            <el-button
              :type="scope.row.is_admin ? 'warning' : 'success'"
              size="small"
              @click="handleToggleAdmin(scope.row)"
              :loading="scope.row._loading"
              class="action-btn"
            >
              {{ scope.row.is_admin ? '取消管理员' : '设为管理员' }}
            </el-button>
            <el-button
              v-if="scope.row.status === 'active'"
              type="danger"
              size="small"
              @click="handleDeactivateUser(scope.row)"
              :loading="scope.row._loading"
              class="action-btn"
            >
              注销用户
            </el-button>
            <el-button
              v-else
              type="primary"
              size="small"
              @click="handleActivateUser(scope.row)"
              :loading="scope.row._loading"
              class="action-btn"
            >
              恢复用户
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <span class="pagination-info">共 {{ pagination.total }} 条记录</span>
        <el-pagination
          v-if="pagination.total > 0"
          @current-change="handlePageChange"
          :current-page="pagination.currentPage"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="prev, pager, next, jumper"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Users, UserFilled, Activity, Clock, User, Search, Plus } from '@element-plus/icons-vue'
import api from '@/api/index'

const loading = ref(false)
const users = ref([])
const searchQuery = ref('')
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 统计数据
const totalUsers = computed(() => pagination.value.total)
const adminCount = computed(() => users.value.filter(u => u.is_admin).length)
const activeUsers = computed(() => users.value.filter(u => u.status === 'active').length)
const newUsersToday = ref(0)

// 获取用户列表
const fetchUsers = async (page = 1) => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: page,
      per_page: pagination.value.pageSize
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    const data = await api.get('/admin/users', { params })

    if (data) {
      users.value = data.users
      pagination.value.total = data.total
      pagination.value.currentPage = data.current_page
      // 模拟今日新增用户数
      newUsersToday.value = Math.floor(Math.random() * 5) + 1
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
  pagination.value.currentPage = page
  fetchUsers(page)
}

// 处理搜索
const handleSearch = () => {
  pagination.value.currentPage = 1
  fetchUsers(1)
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 设置/取消管理员
const handleToggleAdmin = async (user: any) => {
  user._loading = true

  try {
    const data = await api.put(`/admin/users/${user.id}/toggle-admin`)

    if (data) {
      ElMessage.success(data.message || '操作成功')
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
  try {
    await ElMessageBox.confirm(
      '确定要注销该用户吗？注销后用户将无法登录',
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch {
    return
  }

  user._loading = true

  try {
    const data = await api.put(`/admin/users/${user.id}/deactivate`)

    if (data) {
      ElMessage.success(data.message || '注销成功')
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

// 恢复用户
const handleActivateUser = async (user: any) => {
  user._loading = true

  try {
    const data = await api.put(`/admin/users/${user.id}/activate`)

    if (data) {
      ElMessage.success(data.message || '恢复成功')
      await fetchUsers(pagination.value.currentPage)
    }
  } catch (error: any) {
    console.error('恢复失败:', error)
    const errorMessage = error?.response?.data?.message || error?.message || '恢复失败'
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
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
  padding: 20px 0;
  border-bottom: 1px solid #e2e8f0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 24px;
  font-weight: 700;
}

.page-header p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.search-input {
  width: 280px;
  border-radius: 10px;
}

/* 统计卡片 */
.stats-cards {
  margin-bottom: 24px;
}

.mini-stat-card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.mini-stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.mini-stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.admin-card .mini-stat-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.active-card .mini-stat-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.new-card .mini-stat-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.mini-stat-value {
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.mini-stat-label {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

/* 主内容卡片 */
.main-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.add-btn {
  border-radius: 8px;
}

/* 用户列表表格 */
.users-table {
  --el-table-row-hover-bg-color: #f8fafc;
  --el-table-header-text-color: #64748b;
}

.users-table :deep(.el-table__header th) {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
  font-size: 14px;
}

.users-table :deep(.el-table__body tr) {
  transition: all 0.2s;
}

.users-table :deep(.el-table__body tr:hover) {
  transform: translateX(4px);
}

.user-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  margin: 0 0 4px 0;
  font-weight: 600;
  color: #1e293b;
}

.user-email {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

.role-tag {
  padding: 4px 12px;
  border-radius: 20px;
}

.action-btn {
  margin-right: 8px;
  border-radius: 6px;
}

.action-btn:last-child {
  margin-right: 0;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0 10px 0;
}

.pagination-info {
  font-size: 14px;
  color: #64748b;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .stats-cards .el-col {
    margin-bottom: 12px;
  }
  
  .search-input {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .search-input {
    width: 100%;
  }
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .pagination-wrapper {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
