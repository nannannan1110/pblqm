<template>
  <div class="admin-recipes">
    <div class="page-header">
      <h2>菜谱管理</h2>
      <p>管理菜谱内容</p>
    </div>

    <el-card v-loading="loading">
      <el-table :data="recipes" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="菜谱名称" />
        <el-table-column prop="author" label="作者" />
        <el-table-column prop="difficulty" label="难度" width="100" />
        <el-table-column prop="created_at" label="创建时间">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="统计" width="150">
          <template #default="scope">
            <el-tag size="small" style="margin-right: 5px">
              👍 {{ scope.row.stats?.likes_count || 0 }}
            </el-tag>
            <el-tag size="small" type="success" style="margin-right: 5px">
              ⭐ {{ scope.row.stats?.favorites_count || 0 }}
            </el-tag>
            <el-tag size="small" type="warning">
              💬 {{ scope.row.stats?.comments_count || 0 }}
            </el-tag>
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
const recipes = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 获取菜谱列表
const fetchRecipes = async (page = 1) => {
  loading.value = true
  try {
    const data = await api.get('/admin/recipes', {
      params: {
        page: page,
        per_page: pagination.value.pageSize
      }
    })

    if (data) {
      recipes.value = data.recipes
      pagination.value.total = data.total
      pagination.value.currentPage = data.current_page
    }
  } catch (error: any) {
    console.error('获取菜谱列表失败:', error)
    ElMessage.error('获取菜谱列表失败')
  } finally {
    loading.value = false
  }
}

// 处理分页
const handlePageChange = (page: number) => {
  fetchRecipes(page)
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchRecipes()
})
</script>

<style scoped>
.admin-recipes {
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
