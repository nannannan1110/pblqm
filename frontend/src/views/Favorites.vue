<template>
  <div class="favorites-container">
    <!-- 页面标题 -->
    <div class="page-header animate-fade-in-up">
      <div class="header-content">
        <div class="header-icon">
          <el-icon><HeartFilled /></el-icon>
        </div>
        <div class="header-text">
          <h1 class="page-title">我的收藏</h1>
          <p class="page-desc">收藏的菜谱列表</p>
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="main-content">
      <!-- 收藏列表 -->
      <div v-if="favorites.length > 0" class="recipe-grid">
        <div
          v-for="(recipe, index) in favorites"
          :key="recipe.id"
          class="recipe-card-wrapper"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <RecipeCard
            :recipe="recipe"
            :is-favorite="true"
            @click="viewRecipeDetail(recipe)"
            @toggle-favorite="toggleFavorite(recipe)"
          />
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <div class="empty-icon">
          <el-icon><HeartFilled /></el-icon>
        </div>
        <h3>还没有收藏任何菜谱</h3>
        <p>去浏览菜谱，收藏喜欢的美食吧</p>
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
import { ElMessage } from 'element-plus'
import { HeartFilled, Search } from '@element-plus/icons-vue'
import { recipeApi, type Recipe } from '@/api/recipes'
import RecipeCard from '@/components/RecipeCard.vue'

const router = useRouter()
const favorites = ref<Recipe[]>([])

const fetchFavorites = async () => {
  try {
    const response = await recipeApi.getMyFavorites(1, 50)
    favorites.value = response.recipes || []
  } catch (error: any) {
    console.error('获取收藏失败:', error)
    ElMessage.error('获取收藏失败')
  }
}

const toggleFavorite = async (recipe: Recipe) => {
  try {
    await recipeApi.toggleFavorite(recipe.id)
    favorites.value = favorites.value.filter(r => r.id !== recipe.id)
    ElMessage.success('已取消收藏')
  } catch (error: any) {
    console.error('取消收藏失败:', error)
    ElMessage.error('取消收藏失败')
  }
}

const viewRecipeDetail = (recipe: Recipe) => {
  router.push(`/recipes/${recipe.id}`)
}

const goExplore = () => {
  router.push('/home')
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.favorites-container {
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
  background: linear-gradient(135deg, #ef4444, #f97316);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
}

.header-icon .el-icon {
  font-size: 28px;
  color: white;
}

.header-text {
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
  color: #ef4444;
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
  .favorites-container {
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