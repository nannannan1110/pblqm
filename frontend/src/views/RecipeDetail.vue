<template>
  <div class="recipe-detail">
    <div v-loading="loading" class="detail-content">
      <!-- 菜谱信息 -->
      <div v-if="recipe" class="recipe-header">
        <el-row :gutter="30">
          <el-col :span="12">
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
          </el-col>

          <el-col :span="12">
            <div class="recipe-info">
              <h1 class="recipe-title">{{ recipe.title }}</h1>
              <p class="recipe-description">{{ recipe.description || '暂无描述' }}</p>

              <div class="recipe-meta">
                <div class="meta-item">
                  <el-icon><Clock /></el-icon>
                  <span>准备时间: {{ formatTime(recipe.prep_time) }}</span>
                </div>
                <div class="meta-item">
                  <el-icon><Clock /></el-icon>
                  <span>烹饪时间: {{ formatTime(recipe.cook_time) }}</span>
                </div>
                <div class="meta-item">
                  <el-icon><User /></el-icon>
                  <span>份量: {{ recipe.servings || 1 }}人份</span>
                </div>
                <div class="meta-item">
                  <el-icon><Star /></el-icon>
                  <span>难度: {{ recipe.difficulty || '未知' }}</span>
                </div>
              </div>

              <div class="recipe-actions">
                <el-button 
                  :type="isFavorite ? 'warning' : 'primary'" 
                  @click="toggleFavorite"
                  class="animate-btn"
                >
                  <el-icon><HeartFilled v-if="isFavorite" /><Heart v-else /></el-icon>
                  {{ isFavorite ? '已收藏' : '收藏菜谱' }}
                </el-button>
                <el-button v-if="canEdit" type="primary" @click="editRecipe">
                  <el-icon><Edit /></el-icon>
                  编辑菜谱
                </el-button>
                <el-button v-if="canEdit" type="danger" @click="deleteRecipe">
                  <el-icon><Delete /></el-icon>
                  删除菜谱
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 制作步骤 -->
      <div v-if="recipe" class="recipe-sections">
        <el-row :gutter="30">
          <el-col :span="12">
            <el-card class="section-card">
              <template #header>
                <div class="section-header-content">
                  <h3><el-icon><ShoppingBag /></el-icon> 食材清单</h3>
                  <el-button type="primary" size="small" @click="exportShoppingList">
                    <el-icon><Document /></el-icon>
                    生成购物清单
                  </el-button>
                </div>
              </template>
              <div class="ingredients-list">
                <div v-if="parsedIngredients.length > 0" class="ingredients-checkbox-list">
                  <div 
                    v-for="(ingredient, index) in parsedIngredients" 
                    :key="index"
                    class="ingredient-item"
                    @click="toggleIngredient(index)"
                  >
                    <el-checkbox 
                      v-model="checkedIngredients[index]" 
                      @click.stop
                    />
                    <span 
                      :class="{ 'ingredient-checked': checkedIngredients[index] }"
                      class="ingredient-text"
                    >
                      {{ ingredient }}
                    </span>
                  </div>
                </div>
                <pre v-else>{{ recipe.ingredients || '暂无食材信息' }}</pre>
              </div>
            </el-card>
          </el-col>

          <el-col :span="12">
            <el-card class="section-card">
              <template #header>
                <h3><el-icon><Document /></el-icon> 制作步骤</h3>
              </template>
              <div class="instructions-list">
                <pre>{{ recipe.instructions || '暂无制作步骤' }}</pre>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 评论区 -->
      <div v-if="recipe" class="comments-section">
        <el-card>
          <template #header>
            <div class="comments-header">
              <h3><el-icon><ChatLineSquare /></el-icon> 用户评价</h3>
              <div class="comments-stats">
                <span class="rating-display">
                  <el-rate
                    v-model="commentStats.average_rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                  />
                  <span class="comment-count">({{ commentStats.total_comments }}条评价)</span>
                </span>
              </div>
            </div>
          </template>

          <!-- 评分分布 -->
          <div class="rating-distribution">
            <div v-for="(count, rating) in commentStats.rating_distribution" :key="rating" class="rating-item">
              <span class="rating-label">{{ rating }}星</span>
              <el-progress
                :percentage="commentStats.total_comments ? (count / commentStats.total_comments * 100) : 0"
                :show-text="false"
                :stroke-width="8"
              />
              <span class="rating-count">{{ count }}</span>
            </div>
          </div>

          <!-- 写评论 -->
          <div v-if="authApi.isLoggedIn()" class="write-comment">
            <h4>发表评价</h4>
            <el-rate
              v-model="newComment.rating"
              show-text
              :texts="['很差', '较差', '一般', '推荐', '强烈推荐']"
            />
            <el-form class="comment-form">
              <el-form-item>
                <el-input
                  v-model="newComment.content"
                  type="textarea"
                  :rows="4"
                  placeholder="分享你的制作体验..."
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="submittingComment" @click="submitComment">
                  发表评价
                </el-button>
              </el-form-item>
            </el-form>
          </div>

          <!-- 评论列表 -->
          <div class="comments-list">
            <div v-if="comments.length === 0" class="no-comments">
              <el-empty description="暂无评价，快来发表第一条评价吧！" />
            </div>

            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <el-avatar :size="40" :src="comment.user?.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="comment-info">
                  <div class="comment-author">{{ comment.user?.username || '匿名用户' }}</div>
                  <div class="comment-meta">
                    <el-rate
                      v-model="comment.rating"
                      disabled
                      size="small"
                    />
                    <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
                  </div>
                </div>
                <div v-if="canEditComment(comment)" class="comment-actions">
                  <el-button type="text" size="small" @click="editComment(comment)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button type="text" size="small" @click="deleteComment(comment.id)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>

            <!-- 分页 -->
            <div v-if="pagination.total > 0" class="comments-pagination">
              <el-pagination
                v-model:current-page="pagination.currentPage"
                v-model:page-size="pagination.pageSize"
                :page-sizes="[5, 10, 20]"
                :total="pagination.total"
                layout="total, sizes, prev, pager, next"
                @size-change="handlePageChange"
                @current-change="handlePageChange"
              />
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Clock,
  User,
  Star,
  ShoppingBag,
  Document,
  ChatLineSquare,
  Edit,
  Delete,
  Heart,
  HeartFilled
} from '@element-plus/icons-vue'
import { recipeApi, type Recipe } from '@/api/recipes'
import { commentApi, type Comment, type CommentStats } from '@/api/comments'
import { authApi, type User as UserType } from '@/api/auth'
import { formatTime } from '@/api/recipes'
import { formatRelativeTime } from '@/api/comments'

const route = useRoute()
const router = useRouter()
const store = useStore()

const recipe = ref<Recipe | null>(null)
const comments = ref<Comment[]>([])
const commentStats = ref<CommentStats>({
  total_comments: 0,
  average_rating: 0,
  rating_distribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
})

const loading = ref(false)
const submittingComment = ref(false)
const checkedIngredients = ref<boolean[]>([])

// 解析食材文本为列表
const parsedIngredients = computed(() => {
  if (!recipe.value?.ingredients) return []
  
  // 按换行符分割
  let ingredients = recipe.value.ingredients
    .split(/\n+/)
    .map((line: string) => line.trim())
    .filter((line: string) => line.length > 0)
  
  // 如果没有换行符，尝试按常见分隔符分割
  if (ingredients.length === 1) {
    const text = ingredients[0]
    if (text.includes('，')) {
      ingredients = text.split('，').map((s: string) => s.trim())
    } else if (text.includes(',')) {
      ingredients = text.split(',').map((s: string) => s.trim())
    }
  }
  
  // 初始化勾选状态
  checkedIngredients.value = new Array(ingredients.length).fill(false)
  
  return ingredients
})

// 切换食材勾选
const toggleIngredient = (index: number) => {
  checkedIngredients.value[index] = !checkedIngredients.value[index]
}

// 生成购物清单
const exportShoppingList = () => {
  if (!recipe.value?.ingredients) {
    ElMessage.warning('没有食材信息')
    return
  }
  
  let shoppingText = `🛒 ${recipe.value.title} - 购物清单\n`
  shoppingText += '='.repeat(30) + '\n\n'
  
  if (parsedIngredients.value.length > 0) {
    const uncheckedIngredients = parsedIngredients.value.filter(
      (_, index) => !checkedIngredients.value[index]
    )
    
    if (uncheckedIngredients.length > 0) {
      shoppingText += '需要购买的食材：\n'
      uncheckedIngredients.forEach((ingredient, i) => {
        shoppingText += `${i + 1}. ${ingredient}\n`
      })
    } else {
      shoppingText += '所有食材已准备完成！'
    }
  } else {
    shoppingText += recipe.value.ingredients
  }
  
  // 复制到剪贴板
  navigator.clipboard.writeText(shoppingText)
    .then(() => ElMessage.success('购物清单已复制到剪贴板！'))
    .catch(() => ElMessage.error('复制失败，请手动复制'))
}

// 使用data URL作为默认图片（仅当真正没有图片时）
const defaultImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTMwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48dGV4dCB4PSIyMDAiIHk9IjE3MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjQwIiBmaWxsPSIjY2NjIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5KePC90ZXh0Pjwvc3ZnPg=='

// 获取完整的图片URL
const getImageUrl = (image?: string) => {
  // 如果没有图片，返回默认图片
  if (!image) return defaultImage

  // 如果已经是完整URL，直接返回
  if (image.startsWith('http')) return image

  // 如果是完整路径，添加后端域名
  if (image.startsWith('/static')) return `http://localhost:5000${image}`

  // 如果是相对路径（文件名），拼接完整URL
  return `http://localhost:5000/static/uploads/images/${image}`
}

// 新评论表单
const newComment = ref({
  content: '',
  rating: 5
})

// 分页数据
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 当前用户
const currentUser = computed(() => authApi.getCurrentUser() as UserType)

// 检查是否可以编辑菜谱
const canEdit = computed(() => {
  return currentUser.value && recipe.value && currentUser.value.id === recipe.value.user_id
})

// 检查是否可以编辑评论
const canEditComment = (comment: Comment) => {
  return currentUser.value && comment.user_id === currentUser.value.id
}

// 检查是否已收藏
const isFavorite = computed(() => {
  return store.state.favorites.some(fav => fav.id === recipe.value?.id)
})

// 切换收藏状态
const toggleFavorite = () => {
  if (!recipe.value) return
  
  store.commit('TOGGLE_FAVORITE', recipe.value)
  
  if (isFavorite.value) {
    ElMessage.success('已收藏')
  } else {
    ElMessage.success('已取消收藏')
  }
}

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

// 获取菜谱详情
const fetchRecipe = async () => {
  try {
    loading.value = true
    const recipeId = Number(route.params.id)
    recipe.value = await recipeApi.getRecipe(recipeId)
    
    // 添加到浏览历史
    if (recipe.value) {
      store.commit('ADD_VIEW_HISTORY', recipe.value)
    }

    // 获取评论统计
    await fetchCommentStats()
    // 获取评论列表
    await fetchComments()
  } catch (error) {
    console.error('获取菜谱详情失败:', error)
    ElMessage.error('获取菜谱详情失败')
  } finally {
    loading.value = false
  }
}

// 获取评论统计
const fetchCommentStats = async () => {
  if (!recipe.value) {
    console.warn('菜谱数据未加载，无法获取评论统计')
    return
  }

  try {
    console.log(`开始获取菜谱 ${recipe.value.id} 的评论统计...`)
    const stats = await commentApi.getRecipeCommentStats(recipe.value.id)
    console.log('评论统计返回:', stats)
    commentStats.value = stats
  } catch (error) {
    console.error('获取评论统计失败:', error)
  }
}

// 获取评论列表
const fetchComments = async () => {
  if (!recipe.value) {
    console.warn('菜谱数据未加载，无法获取评论')
    return
  }

  try {
    console.log(`开始获取菜谱 ${recipe.value.id} 的评论...`)
    const response = await commentApi.getRecipeComments(recipe.value.id, {
      page: pagination.value.currentPage,
      per_page: pagination.value.pageSize
    })

    console.log('评论API返回:', response)
    console.log('评论数量:', response.comments?.length || 0)
    console.log('评论总数:', response.total)

    comments.value = response.comments || []
    pagination.value.total = response.total || 0

    console.log('设置后的comments.value:', comments.value)
  } catch (error) {
    console.error('获取评论列表失败:', error)
  }
}

// 提交评论
const submitComment = async () => {
  if (!recipe.value || !newComment.value.content.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  try {
    submittingComment.value = true

    await commentApi.createComment({
      content: newComment.value.content,
      rating: newComment.value.rating,
      recipe_id: recipe.value.id
    })

    ElMessage.success('评价发表成功')

    // 重置表单
    newComment.value.content = ''
    newComment.value.rating = 5

    // 刷新评论
    await fetchCommentStats()
    await fetchComments()
  } catch (error) {
    console.error('发表评论失败:', error)
  } finally {
    submittingComment.value = false
  }
}

// 编辑评论
const editComment = async (comment: Comment) => {
  // TODO: 实现编辑评论弹窗
  ElMessage.info('编辑评论功能开发中...')
}

// 删除评论
const deleteComment = async (commentId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
  } catch (error: any) {
    // 用户取消操作，静默返回
    return
  }

  try {
    await commentApi.deleteComment(commentId)
    ElMessage.success('评论删除成功')

    // 刷新评论
    await fetchCommentStats()
    await fetchComments()
  } catch (error: any) {
    console.error('删除评论失败:', error)
    ElMessage.error('删除评论失败')
  }
}

// 编辑菜谱
const editRecipe = () => {
  if (recipe.value) {
    router.push(`/edit-recipe/${recipe.value.id}`)
  }
}

// 删除菜谱
const deleteRecipe = async () => {
  if (!recipe.value) return

  try {
    await ElMessageBox.confirm(
      `确定要删除菜谱"${recipe.value.title}"吗？此操作不可恢复。`,
      '危险操作',
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
    await recipeApi.deleteRecipe(recipe.value.id)
    ElMessage.success('菜谱删除成功')
    router.push('/recipes')
  } catch (error: any) {
    console.error('删除菜谱失败:', error)
    ElMessage.error('删除菜谱失败')
  }
}

// 分页处理
const handlePageChange = (page: number, pageSize?: number) => {
  pagination.value.currentPage = page
  if (pageSize) {
    pagination.value.pageSize = pageSize
  }
  fetchComments()
}

// 页面加载时获取数据
onMounted(() => {
  fetchRecipe()
})
</script>

<style scoped>
.recipe-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.detail-content {
  min-height: 400px;
}

.recipe-header {
  margin-bottom: 30px;
}

.recipe-image-container {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.recipe-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recipe-image:hover {
  transform: scale(1.05);
}

.recipe-difficulty {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  backdrop-filter: blur(4px);
}

.difficulty-easy { background-color: rgba(103, 194, 58, 0.8); }
.difficulty-medium { background-color: rgba(230, 162, 60, 0.8); }
.difficulty-hard { background-color: rgba(245, 108, 108, 0.8); }
.difficulty-unknown { background-color: rgba(144, 147, 153, 0.8); }

.recipe-info {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.recipe-title {
  margin: 0 0 16px 0;
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.recipe-description {
  margin: 0 0 24px 0;
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
  flex: 1;
}

.recipe-meta {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.recipe-actions {
  display: flex;
  gap: 12px;
}

.recipe-sections {
  margin-bottom: 30px;
}

.section-card {
  margin-bottom: 0;
}

.section-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-card h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #303133;
}

.ingredients-list,
.instructions-list {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #606266;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.ingredients-checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ingredient-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.ingredient-item:hover {
  background: #f5f7fa;
}

.ingredient-text {
  flex: 1;
  color: #303133;
  transition: all 0.2s ease;
}

.ingredient-checked {
  text-decoration: line-through;
  color: #c0c4cc;
}

.comments-section {
  margin-top: 30px;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comments-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #303133;
}

.comments-stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.comment-count {
  font-size: 14px;
  color: #909399;
}

.rating-distribution {
  margin-bottom: 24px;
}

.rating-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.rating-label {
  width: 40px;
  font-size: 14px;
  color: #606266;
}

.rating-count {
  width: 40px;
  text-align: right;
  font-size: 14px;
  color: #606266;
}

.write-comment {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.write-comment h4 {
  margin: 0 0 16px 0;
  color: #303133;
}

.comment-form {
  margin-top: 16px;
}

.comments-list {
  min-height: 200px;
}

.no-comments {
  padding: 40px 0;
  text-align: center;
}

.comment-item {
  padding: 20px 0;
  border-bottom: 1px solid #f5f7fa;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.comment-info {
  flex: 1;
}

.comment-author {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.comment-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.comment-time {
  font-size: 12px;
  color: #c0c4cc;
}

.comment-actions {
  display: flex;
  gap: 4px;
}

.comment-content {
  margin-left: 52px;
  color: #606266;
  line-height: 1.6;
}

.comments-pagination {
  margin-top: 24px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recipe-detail {
    padding: 16px;
  }

  .recipe-header .el-col {
    margin-bottom: 20px;
  }

  .recipe-title {
    font-size: 24px;
  }

  .recipe-meta {
    grid-template-columns: 1fr;
  }

  .comments-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .comment-content {
    margin-left: 0;
  }
}
</style>
