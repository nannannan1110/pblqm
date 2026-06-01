<template>
  <div class="my-recipes">
    <div class="page-header">
      <h2>我的菜谱</h2>
      <el-button type="primary" @click="createRecipe">
        <el-icon><Plus /></el-icon>
        创建新菜谱
      </el-button>
    </div>

    <div v-loading="loading" class="recipes-content">
      <el-empty v-if="!loading && recipes.length === 0" description="您还没有创建任何菜谱">
        <el-button type="primary" @click="createRecipe">创建第一个菜谱</el-button>
      </el-empty>

      <el-row v-else :gutter="20">
        <el-col v-for="recipe in recipes" :key="recipe.id" :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="recipe-card" shadow="hover" @click="viewRecipe(recipe.id)">
            <div class="recipe-image-container">
              <img
                :src="getImageUrl(recipe.image)"
                :alt="recipe.title"
                class="recipe-image"
                @error="handleImageError"
              />
              <div class="recipe-difficulty" :class="getDifficultyClass(recipe.difficulty)">
                {{ recipe.difficulty || '未知' }}
              </div>
            </div>
            <div class="recipe-content">
              <h3 class="recipe-title">{{ recipe.title }}</h3>
              <p class="recipe-description">{{ recipe.description || '暂无描述' }}</p>

              <div class="recipe-meta">
                <div class="recipe-time">
                  <el-icon><Clock /></el-icon>
                  <span>{{ formatTimeDisplay(recipe.prep_time, recipe.cook_time) }}</span>
                </div>
                <div class="recipe-servings">
                  <el-icon><User /></el-icon>
                  <span>{{ recipe.servings || 1 }}人份</span>
                </div>
              </div>

              <div class="recipe-stats">
                <span class="stat-item">
                  <el-icon><Star /></el-icon>
                  {{ recipe.likes_count || 0 }}
                </span>
                <span class="stat-item">
                  <el-icon><Collection /></el-icon>
                  {{ recipe.favorites_count || 0 }}
                </span>
              </div>

              <div class="recipe-footer">
                <span class="recipe-date">{{ formatDate(recipe.created_at) }}</span>
                <div class="recipe-actions">
                  <el-button
                    type="primary"
                    size="small"
                    text
                    @click.stop="editRecipe(recipe.id)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    text
                    @click.stop="deleteRecipe(recipe)"
                  >
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Clock, User, Star, Collection } from '@element-plus/icons-vue'
import { recipeApi, type Recipe } from '@/api/recipes'
import { authApi, type User as UserType } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const recipes = ref<Recipe[]>([])
const currentUser = ref<UserType | null>(null)

const loadMyRecipes = async () => {
  try {
    loading.value = true
    currentUser.value = authApi.getCurrentUser()

    if (!currentUser.value) {
      ElMessage.error('未登录')
      return
    }

    const response = await recipeApi.getRecipes({
      page: 1,
      per_page: 1000
    })

    const allRecipes = response.recipes || []
    recipes.value = allRecipes.filter(recipe => recipe.user_id === currentUser.value!.id)
  } catch (error: any) {
    console.error('加载我的菜谱失败:', error)
    ElMessage.error('加载我的菜谱失败')
  } finally {
    loading.value = false
  }
}

// 使用data URL作为默认图片，避免404错误
const defaultImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTMwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48dGV4dCB4PSIyMDAiIHk9IjE3MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjQwIiBmaWxsPSIjY2NjIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5KePC90ZXh0Pjwvc3ZnPg=='

const getImageUrl = (image?: string) => {
  if (!image) return defaultImage
  if (image.startsWith('http')) return image
  if (image.startsWith('/static')) return `http://localhost:5000${image}`
  return `http://localhost:5000/static/uploads/images/${image}`
}

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = defaultImage
}

const getDifficultyClass = (difficulty?: string) => {
  switch (difficulty) {
    case '简单':
      return 'difficulty-easy'
    case '中等':
      return 'difficulty-medium'
    case '困难':
      return 'difficulty-hard'
    default:
      return 'difficulty-unknown'
  }
}

const formatTimeDisplay = (prepTime?: number, cookTime?: number) => {
  const total = (prepTime || 0) + (cookTime || 0)
  if (total === 0) return '未知'
  if (total < 60) return `${total}分钟`
  const hours = Math.floor(total / 60)
  const mins = total % 60
  return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const viewRecipe = (id: number) => {
  router.push(`/recipes/${id}`)
}

const createRecipe = () => {
  router.push('/create-recipe')
}

const editRecipe = (id: number) => {
  router.push(`/edit-recipe/${id}`)
}

const deleteRecipe = async (recipe: Recipe) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除菜谱"${recipe.title}"吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch (error: any) {
    // 用户取消操作，静默返回
    return
  }

  try {
    loading.value = true
    await recipeApi.deleteRecipe(recipe.id)
    ElMessage.success('菜谱删除成功')
    await loadMyRecipes()
  } catch (error: any) {
    console.error('删除菜谱失败:', error)
    ElMessage.error('删除菜谱失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMyRecipes()
})
</script>

<style scoped>
.my-recipes {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.recipes-content {
  min-height: 400px;
}

.recipe-card {
  cursor: pointer;
  transition: transform 0.2s;
  margin-bottom: 20px;
}

.recipe-card:hover {
  transform: translateY(-4px);
}

.recipe-image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 12px;
}

.recipe-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recipe-difficulty {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
  font-weight: bold;
}

.difficulty-easy {
  background-color: rgba(103, 194, 58, 0.9);
}

.difficulty-medium {
  background-color: rgba(230, 162, 60, 0.9);
}

.difficulty-hard {
  background-color: rgba(245, 108, 108, 0.9);
}

.difficulty-unknown {
  background-color: rgba(144, 147, 153, 0.9);
}

.recipe-content {
  padding: 0 12px 12px;
}

.recipe-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 8px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recipe-description {
  font-size: 14px;
  color: #606266;
  margin: 0 0 12px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.recipe-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #909399;
}

.recipe-meta > div {
  display: flex;
  align-items: center;
  gap: 4px;
}

.recipe-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  padding: 8px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.recipe-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recipe-date {
  font-size: 12px;
  color: #909399;
}

.recipe-actions {
  display: flex;
  gap: 8px;
}
</style>
