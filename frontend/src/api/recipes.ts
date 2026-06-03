import api from './index'

// 菜谱类型定义
export interface Recipe {
  id: number
  title: string
  description?: string
  ingredients: string
  instructions: string
  prep_time?: number
  cook_time?: number
  difficulty?: string
  servings?: number
  image?: string
  user_id: number
  created_at: string
  updated_at?: string
}

// 菜谱列表响应类型
export interface RecipesResponse {
  recipes: Recipe[]
  total: number
  pages: number
  current_page: number
  search_params?: SearchParams
}

// 搜索参数类型
export interface SearchParams {
  search?: string
  difficulty?: string
  max_prep_time?: number
  max_cook_time?: number
  sort_by?: 'created_at' | 'title' | 'prep_time' | 'cook_time' | 'likes_count' | 'ratings_count'
  sort_order?: 'asc' | 'desc'
}

// 扩展查询参数
export interface RecipeQuery extends SearchParams {
  page?: number
  per_page?: number
  // 排序选项
  sort_by?: 'created_at' | 'title' | 'prep_time' | 'cook_time' | 'likes_count' | 'ratings_count'
  sort_order?: 'asc' | 'desc'
}

// 创建/更新菜谱请求数据
export interface RecipeRequest {
  title: string
  description?: string
  ingredients: string
  instructions: string
  prep_time?: number
  cook_time?: number
  difficulty?: string
  servings?: number
  image?: string
}

// 扩展查询参数
export interface RecipeQuery extends SearchParams {
  page?: number
  per_page?: number
}

// 菜谱相关API
export const recipeApi = {
  // 获取菜谱列表（支持搜索和筛选）
  getRecipes(query?: RecipeQuery) {
    const params = new URLSearchParams()
    if (query?.page) params.append('page', query.page.toString())
    if (query?.per_page) params.append('per_page', query.per_page.toString())
    if (query?.search) params.append('search', query.search)
    if (query?.difficulty) params.append('difficulty', query.difficulty)
    if (query?.max_prep_time) params.append('max_prep_time', query.max_prep_time.toString())
    if (query?.max_cook_time) params.append('max_cook_time', query.max_cook_time.toString())
    if (query?.sort_by) params.append('sort_by', query.sort_by)
    if (query?.sort_order) params.append('sort_order', query.sort_order)

    const queryString = params.toString()
    const url = queryString ? `/recipes/?${queryString}` : '/recipes/'

    return api.get<RecipesResponse>(url)
  },

  // 搜索菜谱
  searchRecipes(q: string, page?: number, per_page?: number) {
    const params = new URLSearchParams()
    params.append('q', q)
    if (page) params.append('page', page.toString())
    if (per_page) params.append('per_page', per_page.toString())

    return api.get<RecipesResponse>(`/recipes/search?${params.toString()}`)
  },

  // 获取难度级别列表
  getDifficulties() {
    return api.get<{difficulties: string[]}>('/recipes/difficulties')
  },

  // 获取单个菜谱
  getRecipe(id: number) {
    return api.get<Recipe>(`/recipes/${id}`)
  },

  // 创建菜谱
  createRecipe(data: RecipeRequest) {
    return api.post<Recipe>('/recipes/', data)
  },

  // 更新菜谱
  updateRecipe(id: number, data: Partial<RecipeRequest>) {
    return api.put<Recipe>(`/recipes/${id}`, data)
  },

  // 删除菜谱
  deleteRecipe(id: number) {
    return api.delete<{ message: string }>(`/recipes/${id}`)
  },

  // 获取我收藏的菜谱
  getMyFavorites(page?: number, per_page?: number) {
    const params = new URLSearchParams()
    if (page) params.append('page', page.toString())
    if (per_page) params.append('per_page', per_page.toString())

    const queryString = params.toString()
    const url = queryString ? `/recipes/favorites/my?${queryString}` : '/recipes/favorites/my'

    return api.get<RecipesResponse>(url)
  },

  // 获取热门菜谱
  getHotRecipes(page?: number, per_page?: number) {
    const params = new URLSearchParams()
    if (page) params.append('page', page.toString())
    if (per_page) params.append('per_page', per_page.toString())

    const queryString = params.toString()
    const url = queryString ? `/recipes/hot?${queryString}` : '/recipes/hot'

    return api.get<RecipesResponse>(url)
  }
}

// 难度选项
export const DIFFICULTY_OPTIONS = [
  { label: '简单', value: '简单' },
  { label: '中等', value: '中等' },
  { label: '困难', value: '困难' }
]

// 格式化时间
export const formatTime = (minutes?: number): string => {
  if (!minutes) return '未知'
  if (minutes < 60) return `${minutes}分钟`
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
}

// 格式化创建时间
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}