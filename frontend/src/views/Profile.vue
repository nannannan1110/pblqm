<template>
  <div class="profile">
    <!-- 个人信息卡片 -->
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

    <!-- 数据统计卡片 -->
    <el-card class="stats-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <h3>我的数据统计</h3>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item recipes">
            <div class="stat-icon-wrapper">
              <el-icon><BookOpen /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.total_recipes }}</div>
              <div class="stat-label">创建菜谱</div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item likes">
            <div class="stat-icon-wrapper">
              <el-icon><ThumbsUp /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.total_likes }}</div>
              <div class="stat-label">获得点赞</div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item favorites">
            <div class="stat-icon-wrapper">
              <el-icon><HeartFilled /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.total_favorites }}</div>
              <div class="stat-label">收藏次数</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 标签页 -->
    <el-card class="content-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <el-tabs v-model="activeTab" class="profile-tabs">
            <el-tab-pane label="我的收藏" name="favorites">
              <span class="tab-badge">{{ favoritesTotal }}</span>
            </el-tab-pane>
            <el-tab-pane label="热门菜谱" name="hot">
              <span class="tab-badge">🔥</span>
            </el-tab-pane>
          </el-tabs>
        </div>
      </template>

      <!-- 我的收藏 -->
      <div v-if="activeTab === 'favorites'" class="tab-content">
        <div v-if="favoritesLoading" class="loading-container">
          <el-loading-spinner />
          <span>加载中...</span>
        </div>
        
        <div v-else-if="favorites.length === 0" class="empty-state">
          <el-empty description="还没有收藏任何菜谱" />
          <el-button type="primary" @click="goToExplore">去探索</el-button>
        </div>

        <div v-else class="recipe-grid">
          <div 
            v-for="recipe in favorites" 
            :key="recipe.id" 
            class="recipe-card"
            @click="goToRecipe(recipe.id)"
          >
            <div class="recipe-image-wrapper">
              <img :src="getImageUrl(recipe.image)" :alt="recipe.title" class="recipe-image" />
              <div class="recipe-badge" :class="difficultyClass(recipe.difficulty)">
                {{ recipe.difficulty || '未知' }}
              </div>
            </div>
            <div class="recipe-info">
              <h3 class="recipe-title">{{ recipe.title }}</h3>
              <p class="recipe-description">{{ recipe.description || '暂无描述' }}</p>
              <div class="recipe-meta">
                <span class="meta-item">
                  <el-icon><Clock /></el-icon>
                  {{ formatTime(recipe.cook_time) }}
                </span>
                <span class="meta-item">
                  <el-icon><Star /></el-icon>
                  {{ recipe.stats?.avg_rating || 0 }}
                </span>
              </div>
              <div class="recipe-actions">
                <span class="action-btn" @click.stop="removeFavorite(recipe.id)">
                  <el-icon><HeartFilled /></el-icon>
                  取消收藏
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 收藏分页 -->
        <div v-if="favoritesTotal > 0" class="pagination-container">
          <el-pagination
            v-model:current-page="favoritesPage"
            v-model:page-size="pageSize"
            :total="favoritesTotal"
            layout="total, prev, pager, next"
            @current-change="loadFavorites"
          />
        </div>
      </div>

      <!-- 热门菜谱 -->
      <div v-if="activeTab === 'hot'" class="tab-content">
        <div v-if="hotLoading" class="loading-container">
          <el-loading-spinner />
          <span>加载中...</span>
        </div>
        
        <div v-else-if="hotRecipes.length === 0" class="empty-state">
          <el-empty description="暂无热门菜谱" />
        </div>

        <div v-else class="recipe-grid">
          <div 
            v-for="(recipe, index) in hotRecipes" 
            :key="recipe.id" 
            class="recipe-card"
            @click="goToRecipe(recipe.id)"
          >
            <div class="recipe-image-wrapper">
              <img :src="getImageUrl(recipe.image)" :alt="recipe.title" class="recipe-image" />
              <div v-if="index < 3" class="hot-rank" :class="'rank-' + (index + 1)">
                {{ index + 1 }}
              </div>
              <div class="recipe-badge" :class="difficultyClass(recipe.difficulty)">
                {{ recipe.difficulty || '未知' }}
              </div>
            </div>
            <div class="recipe-info">
              <h3 class="recipe-title">{{ recipe.title }}</h3>
              <p class="recipe-description">{{ recipe.description || '暂无描述' }}</p>
              <div class="recipe-meta">
                <span class="meta-item">
                  <el-icon><Clock /></el-icon>
                  {{ formatTime(recipe.cook_time) }}
                </span>
                <span class="meta-item">
                  <el-icon><Star /></el-icon>
                  {{ recipe.stats?.avg_rating || 0 }}
                </span>
                <span class="meta-item">
                  <el-icon><ThumbsUp /></el-icon>
                  {{ recipe.stats?.likes_count || 0 }}
                </span>
              </div>
              <div class="recipe-actions">
                <span 
                  class="action-btn" 
                  :class="{ 'favorited': isFavorite(recipe.id) }"
                  @click.stop="toggleFavorite(recipe)"
                >
                  <el-icon><HeartFilled v-if="isFavorite(recipe.id)" /><Heart v-else /></el-icon>
                  {{ isFavorite(recipe.id) ? '已收藏' : '收藏' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 热门菜谱分页 -->
        <div v-if="hotTotal > 0" class="pagination-container">
          <el-pagination
            v-model:current-page="hotPage"
            v-model:page-size="pageSize"
            :total="hotTotal"
            layout="total, prev, pager, next"
            @current-change="loadHotRecipes"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import {
  BookOpen,
  ThumbsUp,
  HeartFilled,
  Heart,
  Clock,
  Star
} from '@element-plus/icons-vue'
import { authApi, type User } from '@/api/auth'
import { recipeApi, type Recipe, formatTime } from '@/api/recipes'

const router = useRouter()
const store = useStore()

const user = ref<User | null>(null)
const stats = ref({
  total_recipes: 0,
  total_likes: 0,
  total_favorites: 0
})

// 标签页状态
const activeTab = ref('favorites')
const pageSize = ref(6)

// 收藏数据
const favorites = ref<Recipe[]>([])
const favoritesTotal = ref(0)
const favoritesPage = ref(1)
const favoritesLoading = ref(false)

// 热门菜谱数据
const hotRecipes = ref<Recipe[]>([])
const hotTotal = ref(0)
const hotPage = ref(1)
const hotLoading = ref(false)

// 使用data URL作为默认图片
const defaultImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTMwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48dGV4dCB4PSIyMDAiIHk9IjE3MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjQwIiBmaWxsPSIjY2NjIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5KePC90ZXh0Pjwvc3ZnPg=='

// 获取完整的图片URL
const getImageUrl = (image?: string) => {
  if (!image) return defaultImage
  if (image.startsWith('http')) return image
  if (image.startsWith('/static')) return `http://localhost:5000${image}`
  return `http://localhost:5000/static/uploads/images/${image}`
}

// 检查是否已收藏
const isFavorite = (recipeId: number) => {
  return store.state.favorites.some(fav => fav.id === recipeId)
}

// 切换收藏状态
const toggleFavorite = (recipe: Recipe) => {
  store.commit('TOGGLE_FAVORITE', recipe)
  if (isFavorite(recipe.id)) {
    ElMessage.success('已收藏')
  } else {
    ElMessage.success('已取消收藏')
  }
}

// 取消收藏
const removeFavorite = (recipeId: number) => {
  const recipe = favorites.value.find(r => r.id === recipeId)
  if (recipe) {
    store.commit('TOGGLE_FAVORITE', recipe)
    favorites.value = favorites.value.filter(r => r.id !== recipeId)
    favoritesTotal.value--
    ElMessage.success('已取消收藏')
  }
}

// 获取难度样式类
const difficultyClass = (difficulty?: string) => {
  switch (difficulty) {
    case '简单': return 'difficulty-easy'
    case '中等': return 'difficulty-medium'
    case '困难': return 'difficulty-hard'
    default: return 'difficulty-unknown'
  }
}

// 获取用户信息
const loadUserProfile = async () => {
  try {
    user.value = authApi.getCurrentUser()
    if (!user.value) {
      ElMessage.error('未登录')
      return
    }
    await loadUserStats()
    await loadFavorites()
  } catch (error: any) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  }
}

// 获取用户统计数据
const loadUserStats = async () => {
  try {
    const response = await recipeApi.getRecipes({ page: 1, per_page: 1000 })
    const allRecipes = response.recipes || []
    const userRecipes = allRecipes.filter((recipe: any) => recipe.user_id === user.value?.id)

    stats.value = {
      total_recipes: userRecipes.length,
      total_likes: userRecipes.reduce((sum: number, r: any) => sum + (r.stats?.likes_count || r.likes_count || 0), 0),
      total_favorites: userRecipes.reduce((sum: number, r: any) => sum + (r.stats?.favorites_count || r.favorites_count || 0), 0)
    }
  } catch (error: any) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载我的收藏
const loadFavorites = async (page: number = favoritesPage.value) => {
  favoritesPage.value = page
  favoritesLoading.value = true
  try {
    const response = await recipeApi.getMyFavorites(page, pageSize.value)
    favorites.value = response.recipes || []
    favoritesTotal.value = response.total || 0
  } catch (error: any) {
    console.error('加载收藏失败:', error)
    ElMessage.error('加载收藏失败')
  } finally {
    favoritesLoading.value = false
  }
}

// 加载热门菜谱
const loadHotRecipes = async (page: number = hotPage.value) => {
  hotPage.value = page
  hotLoading.value = true
  try {
    const response = await recipeApi.getHotRecipes(page, pageSize.value)
    hotRecipes.value = response.recipes || []
    hotTotal.value = response.total || 0
  } catch (error: any) {
    console.error('加载热门菜谱失败:', error)
    ElMessage.error('加载热门菜谱失败')
  } finally {
    hotLoading.value = false
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

// 跳转到菜谱详情
const goToRecipe = (recipeId: number) => {
  router.push(`/recipe/${recipeId}`)
}

// 跳转到探索页面
const goToExplore = () => {
  router.push('/recipes')
}

// 标签页切换时加载数据
const handleTabChange = () => {
  if (activeTab.value === 'hot' && hotRecipes.value.length === 0) {
    loadHotRecipes()
  }
}

onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped>
.profile {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-card, .stats-card, .content-card {
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

/* 统计卡片样式 */
.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  color: white;
}

.stat-item.recipes {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-item.likes {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-item.favorites {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 24px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

/* 标签页样式 */
.profile-tabs {
  width: 100%;
}

.tab-badge {
  margin-left: 8px;
  background: #f56c6c;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
}

/* 标签内容区域 */
.tab-content {
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #909399;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 16px;
}

/* 菜谱网格 */
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  padding: 16px 0;
}

/* 菜谱卡片 */
.recipe-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}

.recipe-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.recipe-image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.recipe-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hot-rank {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  font-size: 14px;
}

.rank-1 {
  background: linear-gradient(135deg, #ffd700 0%, #ffb700 100%);
}

.rank-2 {
  background: linear-gradient(135deg, #c0c0c0 0%, #a0a0a0 100%);
}

.rank-3 {
  background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
}

.recipe-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  color: white;
  backdrop-filter: blur(4px);
}

.difficulty-easy { background-color: rgba(103, 194, 58, 0.8); }
.difficulty-medium { background-color: rgba(230, 162, 60, 0.8); }
.difficulty-hard { background-color: rgba(245, 108, 108, 0.8); }
.difficulty-unknown { background-color: rgba(144, 147, 153, 0.8); }

.recipe-info {
  padding: 16px;
}

.recipe-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recipe-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.recipe-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.recipe-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 13px;
  color: #606266;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #ecf5ff;
  color: #409eff;
}

.action-btn.favorited {
  background: #fef0f0;
  color: #f56c6c;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile {
    padding: 16px;
  }

  .stat-item {
    flex-direction: column;
    text-align: center;
  }

  .recipe-grid {
    grid-template-columns: 1fr;
  }

  .recipe-meta {
    flex-wrap: wrap;
  }
}
</style>