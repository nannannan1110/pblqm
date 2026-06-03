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
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Globe /></el-icon>
              菜系分类
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="cuisine in cuisineOptions"
                :key="cuisine"
                :class="{ active: selectedCuisine === cuisine }"
                class="cuisine-tag"
                :type="selectedCuisine === cuisine ? 'primary' : ''"
                @click="selectedCuisine = selectedCuisine === cuisine ? '全部' : cuisine"
              >
                {{ cuisine }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Sunny /></el-icon>
              用餐场景
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="scene in sceneOptions"
                :key="scene"
                :class="{ active: selectedScene === scene }"
                class="scene-tag"
                :type="selectedScene === scene ? 'success' : ''"
                @click="selectedScene = selectedScene === scene ? '全部' : scene"
              >
                {{ scene }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Food /></el-icon>
              食材筛选
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="ingredient in ingredients"
                :key="ingredient"
                :class="{ active: selectedIngredients.includes(ingredient) }"
                class="ingredient-tag"
                @click="toggleIngredient(ingredient)"
              >
                {{ ingredient }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="filter-row">
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><TrendCharts /></el-icon>
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
          <div class="filter-group">
            <span class="filter-label">
              <el-icon><Timer /></el-icon>
              时长筛选
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
              口味偏好
            </span>
            <div class="filter-tags">
              <el-tag
                v-for="taste in tasteOptions"
                :key="taste"
                :class="{ active: selectedTaste === taste }"
                class="taste-tag"
                :type="selectedTaste === taste ? 'warning' : ''"
                @click="selectedTaste = selectedTaste === taste ? '全部' : taste"
              >
                {{ taste }}
              </el-tag>
            </div>
          </div>
        </div>
        <div class="filter-actions">
          <el-button @click="resetFilters" size="small">重置筛选</el-button>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 每日推荐 -->
      <div v-if="showDailyRecommend" class="section daily-section animate-fade-in-up animate-delay-2">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><Star /></el-icon>
            每日推荐
            <span class="section-desc">为您精选的菜谱</span>
          </h2>
        </div>
        <div v-if="dailyLoading" class="loading-wrapper">
          <div class="loading-spinner"></div>
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
      <div v-if="viewHistory.length > 0" class="section history-section animate-fade-in-up animate-delay-3">
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
      <div v-if="favorites.length > 0" class="section favorite-section animate-fade-in-up animate-delay-4">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><HeartFilled /></el-icon>
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

      <!-- 搜索/筛选结果 -->
      <div v-if="hasActiveFilters || hasSearchQuery" class="section results-section animate-fade-in-up animate-delay-2">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><List /></el-icon>
            搜索结果
            <span class="section-desc" v-if="filteredRecipes.length > 0">共 {{ filteredRecipes.length }} 道菜谱</span>
          </h2>
        </div>
        <div v-if="resultsLoading" class="loading-wrapper">
          <div class="loading-spinner"></div>
        </div>
        <div v-else-if="filteredRecipes.length === 0" class="empty-state">
          <el-empty description="暂无匹配的菜谱" />
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

      <!-- 热门推荐 -->
      <div v-if="!hasActiveFilters && !hasSearchQuery" class="section hot-section animate-fade-in-up animate-delay-5">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon><TrendCharts /></el-icon>
            热门菜谱
            <span class="section-desc">大家都在看</span>
          </h2>
        </div>
        <div v-if="hotLoading" class="loading-wrapper">
          <div class="loading-spinner"></div>
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
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Sunny, Moon, Food, TrendCharts, Timer, Star, Clock, HeartFilled, List, Heart, Globe } from '@element-plus/icons-vue'
import { recipeApi, type Recipe } from '@/api/recipes'

const store = useStore()
const router = useRouter()

// 状态
const searchQuery = ref('')
const showSearchHistory = ref(false)
const selectedIngredients = ref<string[]>([])
const selectedDifficulty = ref('')
const selectedTime = ref('')

// 数据
const dailyLoading = ref(false)
const hotLoading = ref(false)
const resultsLoading = ref(false)
const allRecipes = ref<Recipe[]>([])
const dailyRecommendations = ref<Recipe[]>([])
const hotRecipes = ref<Recipe[]>([])

// 选项
const ingredients = ['鸡肉', '牛肉', '猪肉', '鱼', '虾', '鸡蛋', '豆腐', '青菜', '土豆', '番茄']
const difficulties = ['简单', '中等', '困难']
const timeOptions = [
  { label: '15分钟内', value: '15' },
  { label: '30分钟内', value: '30' },
  { label: '1小时内', value: '60' },
  { label: '1小时以上', value: '60+' }
]
const cuisineOptions = ['全部', '中餐', '西餐', '日料', '韩餐', '东南亚', '其他']
const sceneOptions = ['全部', '早餐', '午餐', '晚餐', '下午茶', '宵夜', '便当']
const tasteOptions = ['全部', '清淡', '辣', '酸甜', '咸鲜', '酱香', '其他']

// 当前选择
const selectedCuisine = ref('全部')
const selectedScene = ref('全部')
const selectedTaste = ref('全部')

// 计算属性
const isDarkMode = computed(() => store.getters.isDarkMode)
const searchHistory = computed(() => store.state.searchHistory)
const viewHistory = computed(() => store.state.viewHistory)
const favorites = computed(() => store.state.favorites)

const hasSearchQuery = computed(() => searchQuery.value.trim().length > 0)
const hasActiveFilters = computed(() => 
  selectedIngredients.value.length > 0 || 
  selectedDifficulty.value.length > 0 || 
  selectedTime.value.length > 0
)

const showDailyRecommend = computed(() => !hasActiveFilters.value && !hasSearchQuery.value)

const filteredRecipes = computed(() => {
  let result = [...allRecipes.value]
  
  // 搜索过滤
  if (hasSearchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(r => 
      r.title.toLowerCase().includes(query) ||
      r.ingredients?.toLowerCase().includes(query) ||
      r.description?.toLowerCase().includes(query)
    )
  }
  
  // 菜系过滤 (模拟)
  if (selectedCuisine.value !== '全部') {
    result = result.filter(r => {
      // 简单的模拟分类逻辑
      const title = r.title.toLowerCase()
      if (selectedCuisine.value === '中餐') {
        return !['牛排', 'pizza', 'pasta', '寿司', '刺身'].some(key => title.includes(key))
      } else if (selectedCuisine.value === '西餐') {
        return ['牛排', 'pizza', '意大利', '意面', '意式'].some(key => title.includes(key))
      } else if (selectedCuisine.value === '日料') {
        return ['寿司', '刺身', '日式', '日本', '天妇罗'].some(key => title.includes(key))
      }
      return true
    })
  }
  
  // 场景过滤 (模拟)
  if (selectedScene.value !== '全部') {
    result = result.filter(r => {
      const title = r.title.toLowerCase()
      if (selectedScene.value === '早餐') {
        return ['蛋', '牛奶', '面包', '粥', '早餐'].some(key => title.includes(key))
      } else if (selectedScene.value === '晚餐' || selectedScene.value === '午餐') {
        return !['蛋', '牛奶', '面包', '粥', '早餐'].some(key => title.includes(key))
      }
      return true
    })
  }
  
  // 口味过滤 (模拟)
  if (selectedTaste.value !== '全部') {
    result = result.filter(r => {
      const desc = (r.description || '') + (r.ingredients || '')
      if (selectedTaste.value === '辣') {
        return desc.includes('辣') || desc.includes('辣椒')
      } else if (selectedTaste.value === '清淡') {
        return !desc.includes('辣') && !desc.includes('重口味')
      } else if (selectedTaste.value === '酸甜') {
        return desc.includes('酸') || desc.includes('甜')
      }
      return true
    })
  }
  
  // 难度过滤
  if (selectedDifficulty.value) {
    result = result.filter(r => r.difficulty === selectedDifficulty.value)
  }
  
  // 时长过滤
  if (selectedTime.value) {
    const maxTime = selectedTime.value === '60+' ? Infinity : parseInt(selectedTime.value)
    result = result.filter(r => {
      const total = (r.prep_time || 0) + (r.cook_time || 0)
      return selectedTime.value === '60+' ? total > 60 : total <= maxTime
    })
  }
  
  // 食材过滤 (简单模拟)
  if (selectedIngredients.value.length > 0) {
    result = result.filter(r => 
      selectedIngredients.value.some(ing => 
        r.ingredients?.includes(ing)
      )
    )
  }
  
  return result
})

// 方法
const toggleTheme = () => {
  store.commit('TOGGLE_THEME')
}

const handleSearch = () => {
  const query = searchQuery.value.trim()
  if (query) {
    store.commit('ADD_SEARCH_HISTORY', query)
  }
  showSearchHistory.value = false
}

const useHistorySearch = (keyword: string) => {
  searchQuery.value = keyword
  handleSearch()
}

const clearSearchHistory = () => {
  localStorage.removeItem('searchHistory')
  window.location.reload()
}

const toggleIngredient = (ingredient: string) => {
  const index = selectedIngredients.value.indexOf(ingredient)
  if (index !== -1) {
    selectedIngredients.value.splice(index, 1)
  } else {
    selectedIngredients.value.push(ingredient)
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedIngredients.value = []
  selectedDifficulty.value = ''
  selectedTime.value = ''
  selectedCuisine.value = '全部'
  selectedScene.value = '全部'
  selectedTaste.value = '全部'
}

const isFavorite = (recipe: Recipe) => {
  return store.state.favorites.some(f => f.id === recipe.id)
}

const toggleFavorite = (recipe: Recipe) => {
  store.commit('TOGGLE_FAVORITE', recipe)
  ElMessage.success(isFavorite(recipe) ? '已收藏' : '已取消收藏')
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
    console.log('=== Fetching recipes ===')
    console.log('Token exists:', !!sessionStorage.getItem('access_token'))
    console.log('User:', sessionStorage.getItem('user'))
    
    const response = await recipeApi.getRecipes({ page: 1, per_page: 100 })
    
    console.log('=== Recipes response ===')
    console.log('Response:', response)
    console.log('Recipes count:', response?.recipes?.length)
    
    allRecipes.value = response.recipes || []
    dailyRecommendations.value = allRecipes.value.slice(0, 4)
    hotRecipes.value = allRecipes.value.slice(0, 8).sort(() => Math.random() - 0.5)
  } catch (error: any) {
    console.error('=== 获取菜谱失败 ===')
    console.error('Error:', error)
    console.error('Error message:', error.message)
    console.error('Error response:', error.response)
    console.error('Error config:', error.config)
  }
}

onMounted(() => {
  fetchAllRecipes()
  
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
  color: var(--text-tertiary);
}

.search-history {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 8px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 16px;
  z-index: 100;
}

.history-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
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
  transition: all var(--transition-fast);
}

.history-tag:hover {
  background: var(--accent-primary) !important;
  color: white;
}

.search-btn {
  padding: 14px 32px;
  border-radius: var(--radius-lg);
  font-weight: 600;
}

.theme-btn {
  padding: 14px;
  border-radius: var(--radius-lg);
}

/* 筛选区 */
.filters-section {
  margin-bottom: 32px;
}

.filter-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-md);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 16px;
}

.filter-group {
  flex: 1;
  min-width: 300px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ingredient-tag,
.difficulty-tag,
.time-tag {
  cursor: pointer;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.ingredient-tag.active,
.difficulty-tag.active,
.time-tag.active {
  background: var(--accent-gradient) !important;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

/* 主内容区 */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-md);
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
  gap: 10px;
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

.section-desc {
  font-size: 14px;
  font-weight: 400;
  color: var(--text-tertiary);
  margin-left: 8px;
}

/* 网格 */
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.recipe-card-wrapper {
  animation: fadeInUp 0.5s ease-out both;
}

/* 滚动列表 */
.recipe-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.recipe-scroll::-webkit-scrollbar {
  height: 6px;
}

.mini-recipe-card {
  flex-shrink: 0;
  width: 180px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.mini-recipe-card:hover {
  transform: translateY(-4px);
}

.mini-img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: var(--radius-md);
}

.mini-info {
  padding: 0 4px;
}

.mini-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.mini-time {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* 加载 */
.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 0;
}

.empty-state {
  padding: 60px 0;
}

/* 动画 */
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out both;
}

.animate-delay-1 { animation-delay: 0.1s; }
.animate-delay-2 { animation-delay: 0.2s; }
.animate-delay-3 { animation-delay: 0.3s; }
.animate-delay-4 { animation-delay: 0.4s; }
.animate-delay-5 { animation-delay: 0.5s; }

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

/* 响应式 */
@media (max-width: 1024px) {
  .recipe-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
}

@media (max-width: 768px) {
  .discover-container {
    padding: 16px;
  }
  
  .search-wrapper {
    flex-direction: column;
  }
  
  .search-btn {
    width: 100%;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .recipe-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  
  .section {
    padding: 16px;
  }
}
</style>
