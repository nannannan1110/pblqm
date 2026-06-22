<template>
  <div class="history-container">
    <!-- 页面标题 -->
    <div class="page-header animate-fade-in-up">
      <div class="header-content">
        <div class="header-icon">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="header-text">
          <h1 class="page-title">浏览历史</h1>
          <p class="page-desc">最近浏览的菜谱</p>
        </div>
        <div class="header-action">
          <el-button v-if="history.length > 0" type="text" @click="clearHistory">
            <el-icon><Delete /></el-icon>
            清空历史
          </el-button>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="main-content">
      <!-- 历史列表 -->
      <div v-if="history.length > 0" class="recipe-grid">
        <div
          v-for="(recipe, index) in history"
          :key="recipe.id"
          class="recipe-card-wrapper"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <RecipeCard
            :recipe="recipe"
            :is-favorite="isFavorite(recipe)"
            @click="viewRecipeDetail(recipe)"
            @toggle-favorite="toggleFavorite(recipe)"
          />
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <div class="empty-icon">
          <el-icon><Clock /></el-icon>
        </div>
        <h3>还没有浏览记录</h3>
        <p>去浏览菜谱，发现美味吧</p>
        <el-button type="primary" @click="goExplore">
          <el-icon><Search /></el-icon>
          去探索
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Delete, Search, StarFilled } from '@element-plus/icons-vue'
import { recipeApi, type Recipe } from '@/api/recipes'
import RecipeCard from '@/components/RecipeCard.vue'

const router = useRouter()
const history = ref<Recipe[]>([])
const favorites = ref<number[]>([])

const STORAGE_KEY = 'viewHistory'

const loadHistory = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      const historyItems = JSON.parse(stored)
      const historyIds = historyItems.map((item: any) => item.id)
      fetchRecipes(historyIds)
    }
  } catch (error) {
    console.error('加载浏览历史失败:', error)
  }
}

const fetchRecipes = async (ids: number[]) => {
  if (ids.length === 0) return
  
  try {
    // 获取所有菜谱
    const response = await recipeApi.getRecipes({ page: 1, per_page: 100 })
    const allRecipes = response.recipes || []
    
    // 根据历史ID筛选并排序
    history.value = ids
      .map(id => allRecipes.find(r => r.id === id))
      .filter(Boolean) as Recipe[]
  } catch (error) {
    console.error('获取菜谱失败:', error)
  }
}

const fetchFavorites = async () => {
  try {
    const response = await recipeApi.getFavorites()
    favorites.value = (response.recipes || []).map(r => r.id)
  } catch (error) {
    console.error('获取收藏失败:', error)
  }
}

const isFavorite = (recipe: Recipe) => {
  return favorites.value.includes(recipe.id)
}

const toggleFavorite = async (recipe: Recipe) => {
  try {
    const isFavorited = favorites.value.includes(recipe.id)
    if (isFavorited) {
      await recipeApi.removeFavorite(recipe.id)
      favorites.value = favorites.value.filter(id => id !== recipe.id)
      ElMessage.success('已取消收藏')
    } else {
      await recipeApi.toggleFavorite(recipe.id)
      favorites.value.push(recipe.id)
      ElMessage.success('收藏成功')
    }
  } catch (error: any) {
    console.error('收藏操作失败:', error)
    ElMessage.error('收藏操作失败')
  }
}

const viewRecipeDetail = (recipe: Recipe) => {
  router.push(`/recipes/${recipe.id}`)
}

const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空浏览历史吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    localStorage.removeItem(STORAGE_KEY)
    history.value = []
    ElMessage.success('已清空浏览历史')
  } catch {
    // 用户取消操作
  }
}

const goExplore = () => {
  router.push('/home')
}

onMounted(() => {
  loadHistory()
  fetchFavorites()
})
</script>

<style scoped>
.history-container {
  min-height: calc(100vh - 60px);
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 40px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.header-icon .el-icon {
  font-size: 28px;
  color: white;
}

.header-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.page-desc {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.header-action {
  flex-shrink: 0;
}

.main-content {
  min-height: 400px;
}

.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.recipe-card-wrapper {
  animation: fadeInUp 0.5s ease forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  width: 100px;
  height: 100px;
  background: var(--bg-tertiary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.empty-icon .el-icon {
  font-size: 48px;
  color: #667eea;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 14px;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .history-container {
    padding: 24px 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .recipe-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
  }
}
</style>