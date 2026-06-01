<template>
  <div class="profile">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人资料</h2>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">
          {{ user?.username }}
        </el-descriptions-item>
        <el-descriptions-item label="邮箱">
          {{ user?.email || '未设置' }}
        </el-descriptions-item>
        <el-descriptions-item label="角色">
          <el-tag v-if="user?.is_admin" type="danger">管理员</el-tag>
          <el-tag v-else type="success">普通用户</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">
          {{ formatDate(user?.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="创建菜谱数" :span="2">
          {{ stats.total_recipes }} 个
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="stats-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <h3>我的数据统计</h3>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_recipes }}</div>
            <div class="stat-label">创建菜谱</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_likes }}</div>
            <div class="stat-label">获得点赞</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_favorites }}</div>
            <div class="stat-label">收藏次数</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { authApi, type User } from '@/api/auth'
import { recipeApi } from '@/api/recipes'

const user = ref<User | null>(null)
const stats = ref({
  total_recipes: 0,
  total_likes: 0,
  total_favorites: 0
})

const loading = ref(false)

// 获取用户信息
const loadUserProfile = async () => {
  try {
    user.value = authApi.getCurrentUser()
    if (!user.value) {
      ElMessage.error('未登录')
      return
    }
    await loadUserStats()
  } catch (error: any) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  }
}

// 获取用户统计数据
const loadUserStats = async () => {
  try {
    loading.value = true
    // 获取用户创建的所有菜谱
    const response = await recipeApi.getRecipes({ page: 1, per_page: 1000 })
    const allRecipes = response.recipes || []

    // 筛选出当前用户创建的菜谱
    const userRecipes = allRecipes.filter((recipe: any) => recipe.user_id === user.value?.id)

    stats.value = {
      total_recipes: userRecipes.length,
      total_likes: userRecipes.reduce((sum: number, r: any) => sum + (r.likes_count || 0), 0),
      total_favorites: userRecipes.reduce((sum: number, r: any) => sum + (r.favorites_count || 0), 0)
    }
  } catch (error: any) {
    console.error('加载统计数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped>
.profile {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.profile-card, .stats-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2, .card-header h3 {
  margin: 0;
  color: #303133;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}
</style>
