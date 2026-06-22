<template>
  <div class="discover-container">
    <!-- 顶部搜索栏 -->
    <div class="search-section animate-fade-in-up">
      <div class="search-wrapper">
        <div class="search-input-wrapper">
          <el-icon class="search-icon"><Search /></el-icon>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索菜名、食材、口味..."
            class="search-input"
            @keyup.enter="handleSearch"
            @focus="showSearchHistory = true"
          />
          <div v-if="showSearchHistory && searchHistory.length > 0" class="search-history">
            <div class="history-title">
              <span>搜索历史</span>
              <el-button type="text" size="small" @click="clearSearchHistory">清空</el-button>
            </div>
            <div class="history-tags">
              <el-tag
                v-for="item in searchHistory"
                :key="item"
                class="history-tag"
                @click="useHistorySearch(item)"
              >
                {{ item }}
              </el-tag>
            </div>
          </div>
        </div>
        <el-button type="primary" class="search-btn btn-animate" @click="handleSearch">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button class="theme-btn" @click="toggleTheme">
          <el-icon><Sunny v-if="!isDarkMode" /><Moon v-else /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 筛选器区域 -->
    <div class="filters-section animate-fade-in-up animate-delay-1">
      <div class="filter-card">
        <!-- 第一行：主要筛选 -->
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><TrendCharts /></el-icon>
              排序方式
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="sort in sortOptions"
                :key="sort.value"
                :class="{ active: selectedSort === sort.value }"
                class="sort-tag"
                :type="selectedSort === sort.value ? 'primary' : ''"
                @click="handleSortChange(sort.value)"
              >
                {{ sort.label }}
              </el-tag>
            </div>
          </div>
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Star /></el-icon>
              难度筛选
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="diff in difficulties"
                :key="diff"
                :class="{ active: selectedDifficulty === diff }"
                class="difficulty-tag"
                :type="getDifficultyType(diff)"
                @click="selectedDifficulty = selectedDifficulty === diff ? '' : diff"
              >
                {{ diff }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 第二行：时间和评分 -->
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Timer /></el-icon>
              总时长
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="time in timeOptions"
                :key="time.value"
                :class="{ active: selectedTime === time.value }"
                class="time-tag"
                @click="selectedTime = selectedTime === time.value ? '' : time.value"
              >
                {{ time.label }}
              </el-tag>
            </div>
          </div>
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Star /></el-icon>
              最低评分
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="rating in ratingOptions"
                :key="rating.value"
                :class="{ active: selectedMinRating === rating.value }"
                class="rating-tag"
                :type="selectedMinRating === rating.value ? 'warning' : ''"
                @click="selectedMinRating = selectedMinRating === rating.value ? 0 : rating.value"
              >
                {{ rating.label }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 第三行：食材筛选（可多选） -->
        <div class="filter-row">
          <div class="filter-group full-width">
            <span class="filter-label">
              <el-icon><Food /></el-icon>
              食材筛选
              <el-tag size="small" type="info" v-if="selectedIngredients.length > 0">
                已选 {{ selectedIngredients.length }} 个
              </el-tag>
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="ingredient in ingredientOptions"
                :key="ingredient.label"
                :class="{ active: selectedIngredients.includes(ingredient.label) }"
                class="ingredient-tag"
                @click="toggleIngredient(ingredient.label)"
              >
                {{ ingredient.label }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 第四行：操作按钮 -->
        <div class="filter-actions">
          <el-button @click="resetFilters" size="small" type="info">
            <el-icon><RefreshRight /></el-icon>
            重置筛选
          </el-button>
          <el-button @click="applyFilters" type="primary" size="small">
            <el-icon><Filter /></el-icon>
            应用筛选
          </el-button>
        </div>
      </div>
    </div>

    <!-- 筛选结果统计 -->
    <div v-if="hasActiveFilters || hasSearchQuery" class="results-header animate-fade-in-up">
      <div class="results-info">
        <h3>
          <el-icon><List /></el-icon>
          搜索结果
          <span class="results-count">共 {{ filteredRecipes.length }} 道菜谱</span>
        </h3>
        <div class="active-filters">
          <el-tag
            v-if="searchQuery"
            closable
            size="small"
            @close="clearSearch"
            class="filter-chip"
          >
            关键词: {{ searchQuery }}
          </el-tag>
          <el-tag
            v-if="selectedDifficulty"
            closable
            size="small"
            type="success"
            @close="selectedDifficulty = ''"
            class="filter-chip"
          >
            难度: {{ selectedDifficulty }}
          </el-tag>
          <el-tag
            v-if="selectedTime"
            closable
            size="small"
            type="warning"
            @close="selectedTime = ''"
            class="filter-chip"
          >
            时长: {{ getTimeLabel(selectedTime) }}
          </el-tag>
          <el-tag
            v-if="selectedMinRating > 0"
            closable
            size="small"
            type="danger"
            @close="selectedMinRating = 0"
            class="filter-chip"
          >
            评分: ≥{{ selectedMinRating }}
          </el-tag>
          <el-tag
            v-if="selectedSort !== 'created_at'"
            closable
            size="small"
            type="info"
            @close="selectedSort = 'created_at'"
            class="filter-chip"
          >
            排序: {{ getSortLabel(selectedSort) }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 筛选/搜索结果 -->
      <div v-if="hasActiveFilters || hasSearchQuery" class="section results-section animate-fade-in-up">
        <div v-if="resultsLoading" class="loading-wrapper">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        <div v-else-if="filteredRecipes.length === 0" class="empty-state">
          <el-empty description="暂无匹配的菜谱">
            <el-button type="primary" @click="resetFilters">重置筛选</el-button>
          </el-empty>
        </div>
        <div v-else class="recipe-grid">
          <div
            v-for="(recipe, index) in filteredRecipes"
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
      </div>

      <!-- 每日推荐 -->
      <div v-if="!hasActiveFilters && !hasSearchQuery && dailyRecommendations.length > 0" class="section daily-section animate-fade-in-up">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Star /></el-icon>
            每日推荐
            <span class="section-desc">为您精选的菜谱</span>
          </h2>
        </div>
        <div v-if="dailyLoading" class="loading-wrapper">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        <div v-else class="recipe-grid">
          <div
            v-for="(recipe, index) in dailyRecommendations"
            :key="recipe.id"
            class="recipe-card-wrapper"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <RecipeCard
              :recipe="recipe"
              :is-favorite="isFavorite(recipe)"
              @click="viewRecipeDetail(recipe)"
              @toggle-favorite="toggleFavorite(recipe)"
            />
          </div>
        </div>
      </div>

      <!-- 历史记录 -->
      <div v-if="!hasActiveFilters && !hasSearchQuery && viewHistory.length > 0" class="section history-section animate-fade-in-up">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Clock /></el-icon>
            浏览历史
            <span class="section-desc">最近看过的菜谱</span>
          </h2>
          <el-button type="text" size="small" @click="clearViewHistory">清除</el-button>
        </div>
        <div class="recipe-scroll">
          <div
            v-for="recipe in viewHistory"
            :key="recipe.id"
            class="mini-recipe-card"
            @click="viewRecipeDetail(recipe)"
          >
            <img :src="getImageUrl(recipe.image)" :alt="recipe.title" class="mini-img" />
            <div class="mini-info">
              <h4 class="mini-title">{{ recipe.title }}</h4>
              <span class="mini-time">{{ formatTimeDisplay(recipe.prep_time, recipe.cook_time) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 我的收藏 -->
      <div v-if="!hasActiveFilters && !hasSearchQuery && favorites.length > 0" class="section favorite-section animate-fade-in-up">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><StarFilled /></el-icon>
            我的收藏
            <span class="section-desc">收藏的菜谱</span>
          </h2>
        </div>
        <div class="recipe-grid">
          <div
            v-for="recipe in favorites"
            :key="recipe.id"
            class="recipe-card-wrapper"
          >
            <RecipeCard
              :recipe="recipe"
              :is-favorite="true"
              @click="viewRecipeDetail(recipe)"
              @toggle-favorite="toggleFavorite(recipe)"
            />
          </div>
        </div>
      </div>

      <!-- 热门推荐 -->
      <div v-if="!hasActiveFilters && !hasSearchQuery" class="section hot-section animate-fade-in-up">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><TrendCharts /></el-icon>
            热门菜谱
            <span class="section-desc">大家都在看</span>
          </h2>
          <el-button type="primary" size="small" @click="loadMoreHot">
            查看更多
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
        <div v-if="hotLoading" class="loading-wrapper">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        <div v-else class="recipe-grid">
          <div
            v-for="(recipe, index) in hotRecipes"
            :key="recipe.id"
            class="recipe-card-wrapper"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <RecipeCard
              :recipe="recipe"
              :is-favorite="isFavorite(recipe)"
              @click="viewRecipeDetail(recipe)"
              @toggle-favorite="toggleFavorite(recipe)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Search, Sunny, Moon, Food, TrendCharts, Timer, Star, Clock, StarFilled,
  List, RefreshRight, Filter, Loading, ArrowRight
} from '@element-plus/icons-vue'
import { recipeApi, type Recipe } from '@/api/recipes'
import { authApi } from '@/api/auth'
import RecipeCard from '@/components/RecipeCard.vue'

const store = useStore()
const router = useRouter()

// 状态
const searchQuery = ref('')
const showSearchHistory = ref(false)
const selectedIngredients = ref<string[]>([])
const selectedDifficulty = ref('')
const selectedTime = ref('')
const selectedMinRating = ref(0)
const selectedSort = ref('created_at')

// 排序选项
const sortOptions = [
  { label: '最新发布', value: 'created_at' },
  { label: '最多点赞', value: 'likes_count' },
  { label: '最高评分', value: 'ratings_count' },
  { label: '最短时间', value: 'prep_time' }
]

// 时间选项
const timeOptions = [
  { label: '15分钟内', value: '15' },
  { label: '30分钟内', value: '30' },
  { label: '1小时内', value: '60' },
  { label: '1-2小时', value: '120' }
]

// 评分选项
const ratingOptions = [
  { label: '4分以上', value: 4 },
  { label: '4.5分以上', value: 4.5 },
  { label: '满分', value: 5 }
]

// 食材选项（包含同义词映射）
const ingredientOptions = [
  { label: '鸡肉', keywords: ['鸡肉', '鸡腿肉', '鸡胸肉', '鸡翅', '鸡丁'] },
  { label: '牛肉', keywords: ['牛肉', '牛腩', '牛排', '牛肉末'] },
  { label: '猪肉', keywords: ['猪肉', '五花肉', '排骨', '瘦肉', '里脊'] },
  { label: '鱼', keywords: ['鱼', '鲈鱼', '鲫鱼', '鲤鱼', '草鱼'] },
  { label: '虾', keywords: ['虾', '虾仁', '大虾', '基围虾'] },
  { label: '鸡蛋', keywords: ['鸡蛋', '蛋'] },
  { label: '豆腐', keywords: ['豆腐', '嫩豆腐', '老豆腐'] },
  { label: '青菜', keywords: ['青菜', '西兰花', '菠菜', '白菜', '油菜'] },
  { label: '土豆', keywords: ['土豆', '马铃薯'] },
  { label: '番茄', keywords: ['番茄', '西红柿'] }
]

// 难度选项
const difficulties = ['简单', '中等', '困难']

// 数据
const dailyLoading = ref(false)
const hotLoading = ref(false)
const resultsLoading = ref(false)
const allRecipes = ref<Recipe[]>([])
const dailyRecommendations = ref<Recipe[]>([])
const hotRecipes = ref<Recipe[]>([])
const filteredRecipes = ref<Recipe[]>([])

// 计算属性
const isDarkMode = computed(() => store.getters.isDarkMode)
const searchHistory = computed(() => store.state.searchHistory)
const viewHistory = computed(() => store.state.viewHistory)
const favorites = computed(() => store.state.favorites)

const hasSearchQuery = computed(() => searchQuery.value.trim().length > 0)
const hasActiveFilters = computed(() => 
  selectedIngredients.value.length > 0 || 
  selectedDifficulty.value.length > 0 || 
  selectedTime.value !== '' ||
  selectedMinRating.value > 0
)

// 方法
const toggleTheme = () => {
  store.commit('TOGGLE_THEME')
}

const handleSortChange = async (sortValue: string) => {
  selectedSort.value = sortValue
  // 如果有活动筛选条件或搜索查询，应用筛选
  if (hasActiveFilters.value || hasSearchQuery.value) {
    await applyFilters()
  }
}

const handleSearch = () => {
  const query = searchQuery.value.trim()
  if (query) {
    store.commit('ADD_SEARCH_HISTORY', query)
  }
  showSearchHistory.value = false
  applyFilters()
}

const useHistorySearch = (keyword: string) => {
  searchQuery.value = keyword
  handleSearch()
}

const clearSearchHistory = () => {
  localStorage.removeItem('searchHistory')
  window.location.reload()
}

const clearSearch = () => {
  searchQuery.value = ''
  applyFilters()
}

const toggleIngredient = (ingredient: string) => {
  const index = selectedIngredients.value.indexOf(ingredient)
  if (index !== -1) {
    selectedIngredients.value.splice(index, 1)
  } else {
    selectedIngredients.value.push(ingredient)
  }
}

const getTimeLabel = (value: string) => {
  const time = timeOptions.find(t => t.value === value)
  return time ? time.label : value
}

const getSortLabel = (value: string) => {
  const sort = sortOptions.find(s => s.value === value)
  return sort ? sort.label : value
}

const applyFilters = async () => {
  resultsLoading.value = true
  try {
    const query = {
      page: 1,
      per_page: 50,
      search: searchQuery.value.trim() || undefined,
      difficulty: selectedDifficulty.value || undefined,
      sort_by: selectedSort.value || 'created_at',
      sort_order: selectedSort.value === 'prep_time' ? 'asc' : 'desc'
    }

    // 处理时间筛选（前端过滤）
    const response = await recipeApi.getRecipes(query)
    let recipes = response.recipes || []

    // 时间筛选（前端处理，因为后端只支持max时间）
    if (selectedTime.value) {
      const maxTime = parseInt(selectedTime.value as string)
      recipes = recipes.filter(r => {
        const total = (r.prep_time || 0) + (r.cook_time || 0)
        return total <= maxTime
      })
    }

    // 食材筛选（前端处理，使用关键词匹配）
    if (selectedIngredients.value.length > 0) {
      recipes = recipes.filter(r => {
        const ingredientsText = r.ingredients || ''
        return selectedIngredients.value.some(selectedIng => {
          // 查找选中食材的关键词列表
          const ingOption = ingredientOptions.find(opt => opt.label === selectedIng)
          if (!ingOption) return false
          // 检查任一关键词是否在食材文本中
          return ingOption.keywords.some(keyword => ingredientsText.includes(keyword))
        })
      })
    }

    // 评分筛选（前端处理，因为后端没有这个字段）
    if (selectedMinRating.value > 0) {
      recipes = recipes.filter(r =>
        (r as any).stats?.avg_rating >= selectedMinRating.value
      )
    }

    filteredRecipes.value = recipes
    console.log('筛选结果:', recipes.length, '条')
    console.log('筛选后菜谱数据:', recipes)
  } catch (error: any) {
    console.error('筛选失败:', error)
    ElMessage.error('筛选失败')
  } finally {
    resultsLoading.value = false
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedIngredients.value = []
  selectedDifficulty.value = ''
  selectedTime.value = ''
  selectedMinRating.value = 0
  selectedSort.value = 'created_at'
  filteredRecipes.value = []
}

const isFavorite = (recipe: Recipe) => {
  return store.state.favorites.some(f => f.id === recipe.id)
}

const toggleFavorite = async (recipe: Recipe) => {
  try {
    if (isFavorite(recipe)) {
      await recipeApi.removeFavorite(recipe.id)
      store.commit('TOGGLE_FAVORITE', recipe)
      ElMessage.success('已取消收藏')
    } else {
      await recipeApi.toggleFavorite(recipe.id)
      store.commit('TOGGLE_FAVORITE', recipe)
      ElMessage.success('收藏成功')
    }
  } catch (error: any) {
    console.error('收藏操作失败:', error)
    // 如果未登录，仍然允许本地收藏
    if (!authApi.isLoggedIn()) {
      store.commit('TOGGLE_FAVORITE', recipe)
      ElMessage.success(isFavorite(recipe) ? '已收藏（本地）' : '已取消收藏（本地）')
    } else {
      ElMessage.error('收藏操作失败')
    }
  }
}

const viewRecipeDetail = (recipe: Recipe) => {
  store.commit('ADD_VIEW_HISTORY', recipe)
  router.push(`/recipes/${recipe.id}`)
}

const clearViewHistory = () => {
  localStorage.removeItem('viewHistory')
  window.location.reload()
}

const getDifficultyType = (diff: string) => {
  switch (diff) {
    case '简单': return 'success'
    case '中等': return 'warning'
    case '困难': return 'danger'
    default: return 'info'
  }
}

const getImageUrl = (image?: string) => {
  if (!image) return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTUwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48L3N2Zz4='
  if (image.startsWith('http')) return image
  return `http://localhost:5000/static/uploads/images/${image}`
}

const formatTimeDisplay = (prepTime?: number, cookTime?: number) => {
  const total = (prepTime || 0) + (cookTime || 0)
  if (total < 60) return `${total}分钟`
  const hours = Math.floor(total / 60)
  const mins = total % 60
  return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
}

const fetchAllRecipes = async () => {
  try {
    const response = await recipeApi.getRecipes({ page: 1, per_page: 100 })
    allRecipes.value = response.recipes || []
    dailyRecommendations.value = allRecipes.value.slice(0, 4)
  } catch (error: any) {
    console.error('获取菜谱失败:', error)
  }
}

const fetchHotRecipes = async () => {
  hotLoading.value = true
  try {
    // 使用后端API获取热门菜谱
    const response = await recipeApi.getHotRecipes(1, 8)
    hotRecipes.value = response.recipes || []
  } catch (error: any) {
    console.error('获取热门菜谱失败:', error)
    // 如果API失败，使用本地数据
    hotRecipes.value = allRecipes.value.slice(0, 8)
  } finally {
    hotLoading.value = false
  }
}

const loadMoreHot = () => {
  // 可以导航到专门的热门菜谱页面
  selectedSort.value = 'likes_count'
  applyFilters()
}

onMounted(() => {
  fetchAllRecipes()
  fetchHotRecipes()

  // 点击外部关闭搜索历史
  document.addEventListener('click', (e) => {
    const target = e.target as HTMLElement
    if (!target.closest('.search-wrapper')) {
      showSearchHistory.value = false
    }
  })
})
</script>

<style scoped>
.discover-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 搜索区 */
.search-section {
  margin-bottom: 24px;
}

.search-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.search-input-wrapper {
  flex: 1;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 14px 48px;
  font-size: 16px;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-lg);
  background: var(--bg-card);
  color: var(--text-primary);
  transition: all var(--transition-base);
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
  color: var(--text-secondary);
}

.search-history {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  padding: 12px;
  z-index: 10;
  margin-top: 8px;
}

.history-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.history-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.history-tag {
  cursor: pointer;
}

.search-btn {
  padding: 14px 24px;
  font-size: 16px;
}

.theme-btn {
  padding: 14px 16px;
}

/* 筛选区域 */
.filters-section {
  margin-bottom: 24px;
}

.filter-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
}

.filter-row {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group.full-width {
  flex-basis: 100%;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 标签样式 */
.filter-tags :deep(.el-tag) {
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-secondary);
}

.filter-tags :deep(.el-tag.active) {
  border-color: var(--accent-primary);
  background: var(--accent-primary);
  color: white;
}

.filter-tags :deep(.el-tag:hover) {
  transform: translateY(-1px);
}

.sort-tag.active {
  font-weight: 500;
}

.difficulty-tag.active {
  font-weight: 500;
}

.ingredient-tag.active {
  background: var(--accent-primary);
  border-color: var(--accent-primary);
  color: white;
}

.time-tag.active {
  background: #e6a23c;
  border-color: #e6a23c;
  color: white;
}

.rating-tag.active {
  background: #f56c6c;
  border-color: #f56c6c;
  color: white;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
  margin-top: 16px;
}

/* 筛选结果统计 */
.results-header {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
}

.results-info h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px 0;
  font-size: 18px;
  color: var(--text-primary);
}

.results-count {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: normal;
  margin-left: 8px;
}

.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip {
  margin: 0;
}

/* 内容区域 */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section {
  margin-bottom: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 20px;
  color: var(--text-primary);
}

.section-desc {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: normal;
  margin-left: 8px;
}

/* 加载状态 */
.loading-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 12px;
  color: var(--text-secondary);
}

.loading-wrapper .el-icon {
  font-size: 32px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

/* 菜谱网格 */
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

/* 历史记录滚动 */
.recipe-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 8px 0;
  scroll-snap-type: x mandatory;
}

.mini-recipe-card {
  flex: 0 0 160px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
  scroll-snap-align: start;
}

.mini-recipe-card:hover {
  transform: scale(1.05);
}

.mini-img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

.mini-info {
  padding: 8px 12px;
}

.mini-title {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mini-time {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .discover-container {
    padding: 12px;
  }

  .filter-row {
    flex-direction: column;
    gap: 16px;
  }

  .filter-group {
    min-width: 100%;
  }

  .recipe-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
