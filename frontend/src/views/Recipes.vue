<template>
  <div class="recipes">
    <div class="recipes-header">
      <h1>菜谱列表</h1>
      <el-button
        v-if="authApi.isLoggedIn()"
        type="primary"
        @click="createRecipe"
      >
        <el-icon><Plus /></el-icon>
        创建菜谱
      </el-button>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" :inline="true" class="search-form">
          <!-- 搜索框 -->
          <el-form-item label="搜索">
            <el-input
              v-model="searchForm.search"
              placeholder="搜索菜谱名称、描述或食材..."
              clearable
              style="width: 300px"
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </el-form-item>

          <!-- 难度筛选 -->
          <el-form-item label="难度">
            <el-select
              v-model="searchForm.difficulty"
              placeholder="选择难度"
              clearable
              style="width: 120px"
            >
              <el-option
                v-for="difficulty in difficulties"
                :key="difficulty"
                :label="difficulty"
                :value="difficulty"
              />
            </el-select>
          </el-form-item>

          <!-- 最大准备时间 -->
          <el-form-item label="准备时间">
            <el-input-number
              v-model="searchForm.max_prep_time"
              placeholder="最多"
              :min="0"
              :max="999"
              style="width: 120px"
            />
            <span style="margin-left: 4px;">分钟</span>
          </el-form-item>

          <!-- 最大烹饪时间 -->
          <el-form-item label="烹饪时间">
            <el-input-number
              v-model="searchForm.max_cook_time"
              placeholder="最多"
              :min="0"
              :max="999"
              style="width: 120px"
            />
            <span style="margin-left: 4px;">分钟</span>
          </el-form-item>

          <!-- 排序 -->
          <el-form-item label="排序">
            <el-select
              v-model="searchForm.sort_by"
              style="width: 120px"
              @change="handleSearch"
            >
              <el-option label="创建时间" value="created_at" />
              <el-option label="标题" value="title" />
              <el-option label="准备时间" value="prep_time" />
              <el-option label="烹饪时间" value="cook_time" />
            </el-select>
            <el-select
              v-model="searchForm.sort_order"
              style="width: 80px; margin-left: 8px"
              @change="handleSearch"
            >
              <el-option label="降序" value="desc" />
              <el-option label="升序" value="asc" />
            </el-select>
          </el-form-item>

          <!-- 操作按钮 -->
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="resetSearch">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 搜索结果统计 -->
    <div v-if="searchParams.search || searchParams.difficulty || searchParams.max_prep_time || searchParams.max_cook_time" class="search-stats">
      <el-alert
        :title="`找到 ${pagination.total} 个菜谱`"
        type="info"
        :closable="false"
        show-icon
      >
        <template #default>
          <span v-if="searchParams.search">关键词: "{{ searchParams.search }}"</span>
          <span v-if="searchParams.difficulty" style="margin-left: 8px;">难度: {{ searchParams.difficulty }}</span>
          <span v-if="searchParams.max_prep_time" style="margin-left: 8px;">准备时间 ≤ {{ searchParams.max_prep_time }}分钟</span>
          <span v-if="searchParams.max_cook_time" style="margin-left: 8px;">烹饪时间 ≤ {{ searchParams.max_cook_time }}分钟</span>
        </template>
      </el-alert>
    </div>

    <div v-loading="loading" class="recipes-content">
      <el-empty v-if="!loading && recipes.length === 0" description="暂无菜谱" />
      <el-empty v-else-if="!loading && hasSearchConditions && recipes.length === 0" description="没有找到符合条件的菜谱" />

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
              <div class="recipe-difficulty" :class="difficultyClass(recipe.difficulty)">
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

              <div class="recipe-footer">
                <span class="recipe-date">{{ formatDate(recipe.created_at) }}</span>
                <el-button type="primary" size="small" text>
                  查看详情
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 分页 -->
      <div v-if="pagination.total > 0" class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[12, 24, 48]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Clock, User, Search, Refresh } from '@element-plus/icons-vue'
import { recipeApi, type Recipe, formatTime, formatDate, type RecipeQuery, type SearchParams } from '@/api/recipes'
import { authApi } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const recipes = ref<Recipe[]>([])
const difficulties = ref<string[]>([])

// 分页数据
const pagination = ref({
  currentPage: 1,
  pageSize: 12,
  total: 0
})

// 搜索表单
const searchForm = ref({
  search: '',
  difficulty: '',
  max_prep_time: undefined as number | undefined,
  max_cook_time: undefined as number | undefined,
  sort_by: 'created_at' as const,
  sort_order: 'desc' as const
})

// 当前搜索参数
const searchParams = ref<SearchParams>({})

// 使用data URL作为默认图片，避免404错误
const defaultImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTMwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48dGV4dCB4PSIyMDAiIHk9IjE3MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjQwIiBmaWxsPSIjY2NjIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5KePC90ZXh0Pjwvc3ZnPg=='

// 获取完整的图片URL
const getImageUrl = (image?: string) => {
  if (!image) return defaultImage
  // 如果已经是完整路径或完整URL，直接返回
  if (image.startsWith('http')) return image
  if (image.startsWith('/static')) return `http://localhost:5000${image}`
  // 否则拼接完整路径
  return `http://localhost:5000/static/uploads/images/${image}`
}

// 检查是否有搜索条件
const hasSearchConditions = computed(() => {
  return searchParams.value.search ||
         searchParams.value.difficulty ||
         searchParams.value.max_prep_time ||
         searchParams.value.max_cook_time
})

// 获取难度样式类
const difficultyClass = (difficulty?: string) => {
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

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = defaultImage
}

// 格式化时间显示
const formatTimeDisplay = (prepTime?: number, cookTime?: number) => {
  const total = (prepTime || 0) + (cookTime || 0)
  return formatTime(total)
}

// 查看菜谱详情
const viewRecipe = (id: number) => {
  router.push(`/recipes/${id}`)
}

// 创建菜谱
const createRecipe = () => {
  router.push('/create-recipe')
}

// 获取菜谱列表
const fetchRecipes = async () => {
  try {
    loading.value = true
    const queryParams: RecipeQuery = {
      page: pagination.value.currentPage,
      per_page: pagination.value.pageSize,
      ...searchParams.value
    }

    const response = await recipeApi.getRecipes(queryParams)

    recipes.value = response.recipes
    pagination.value.total = response.total
  } catch (error) {
    console.error('获取菜谱列表失败:', error)
    ElMessage.error('获取菜谱列表失败')
  } finally {
    loading.value = false
  }
}

// 获取难度列表
const fetchDifficulties = async () => {
  try {
    const response = await recipeApi.getDifficulties()
    difficulties.value = response.difficulties
  } catch (error) {
    console.error('获取难度列表失败:', error)
  }
}

// 处理搜索
const handleSearch = () => {
  // 保存当前搜索参数
  searchParams.value = { ...searchForm.value }

  // 重置页码到第一页
  pagination.value.currentPage = 1

  // 执行搜索
  fetchRecipes()
}

// 重置搜索
const resetSearch = () => {
  // 清空搜索表单
  searchForm.value = {
    search: '',
    difficulty: '',
    max_prep_time: undefined,
    max_cook_time: undefined,
    sort_by: 'created_at',
    sort_order: 'desc'
  }

  // 清空搜索参数
  searchParams.value = {}

  // 重置页码
  pagination.value.currentPage = 1

  // 重新获取数据
  fetchRecipes()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  pagination.value.currentPage = page
  fetchRecipes()
}

// 处理每页数量变化
const handleSizeChange = (size: number) => {
  pagination.value.pageSize = size
  pagination.value.currentPage = 1
  fetchRecipes()
}

// 页面加载时获取数据
onMounted(() => {
  fetchRecipes()
  fetchDifficulties()
})
</script>

<style scoped>
.recipes {
  padding: 20px;
  min-height: calc(100vh - 100px);
}

.recipes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.recipes-header h1 {
  margin: 0;
  color: #303133;
}

.search-section {
  margin-bottom: 24px;
}

.search-form {
  margin: 0;
}

.search-form :deep(.el-form-item) {
  margin-bottom: 0;
  margin-right: 16px;
}

.search-stats {
  margin-bottom: 16px;
}

.recipes-content {
  min-height: 400px;
}

.recipe-card {
  margin-bottom: 24px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
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
}

.recipe-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recipe-card:hover .recipe-image {
  transform: scale(1.05);
}

.recipe-difficulty {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: white;
  backdrop-filter: blur(4px);
}

.difficulty-easy {
  background-color: rgba(103, 194, 58, 0.8);
}

.difficulty-medium {
  background-color: rgba(230, 162, 60, 0.8);
}

.difficulty-hard {
  background-color: rgba(245, 108, 108, 0.8);
}

.difficulty-unknown {
  background-color: rgba(144, 147, 153, 0.8);
}

.recipe-content {
  padding: 16px;
}

.recipe-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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
  min-height: 42px;
}

.recipe-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 13px;
  color: #909399;
}

.recipe-time,
.recipe-servings {
  display: flex;
  align-items: center;
  gap: 4px;
}

.recipe-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.recipe-date {
  font-size: 12px;
  color: #c0c4cc;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recipes {
    padding: 16px;
  }

  .recipes-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .recipes-header h1 {
    text-align: center;
  }

  .search-form {
    display: block;
  }

  .search-form :deep(.el-form-item) {
    display: block;
    margin-right: 0;
    margin-bottom: 16px;
  }

  .recipe-image-container {
    height: 180px;
  }

  .recipe-title {
    font-size: 16px;
  }

  .recipe-description {
    font-size: 13px;
  }

  .recipe-meta {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .recipes {
    padding: 12px;
  }

  .recipe-image-container {
    height: 160px;
  }

  .recipe-content {
    padding: 12px;
  }

  .recipe-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .recipe-date {
    text-align: center;
  }
}

/* 加载动画 */
:deep(.el-loading-spinner) {
  margin-top: 100px;
}
</style>
