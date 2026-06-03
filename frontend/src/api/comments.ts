import api from './index'
import { type User } from './auth'

// 评论类型定义
export interface Comment {
  id: number
  content: string
  user_id: number
  recipe_id: number
  parent_id?: number
  created_at: string
  updated_at?: string
  user?: User
  replies?: Comment[]
}

// 评论列表响应类型
export interface CommentsResponse {
  comments: Comment[]
  total: number
  pages: number
  current_page: number
}

// 评论统计类型
export interface CommentStats {
  comment_count: number
  rating_count: number
  average_score: number
  rating_distribution: {
    1: number
    2: number
    3: number
    4: number
    5: number
  }
}

// 创建评论请求数据
export interface CreateCommentRequest {
  content: string
  rating?: number
}

// 更新评论请求数据
export interface UpdateCommentRequest {
  content?: string
}

// 评论相关API
export const commentApi = {
  // 获取菜谱评论列表
  getRecipeComments(recipeId: number, query?: { page?: number; per_page?: number }) {
    const params = new URLSearchParams()
    if (query?.page) params.append('page', query.page.toString())
    if (query?.per_page) params.append('per_page', query.per_page.toString())

    const queryString = params.toString()
    const url = queryString ? `/recipes/${recipeId}/comments?${queryString}` : `/recipes/${recipeId}/comments`

    return api.get<CommentsResponse>(url)
  },

  // 创建评论
  createComment(recipeId: number, data: CreateCommentRequest) {
    return api.post<Comment>(`/recipes/${recipeId}/comments`, data)
  },

  // 更新评论
  updateComment(commentId: number, data: UpdateCommentRequest) {
    return api.put<Comment>(`/comments/${commentId}`, data)
  },

  // 删除评论
  deleteComment(commentId: number) {
    return api.delete<{ message: string }>(`/comments/${commentId}`)
  },

  // 获取菜谱评论统计
  getRecipeCommentStats(recipeId: number) {
    return api.get<CommentStats>(`/recipes/${recipeId}/comments/stats`)
  }
}

// 评分相关工具函数
export const ratingUtils = {
  // 获取评分星星数组
  getRatingStars(rating: number): boolean[] {
    const stars = []
    for (let i = 1; i <= 5; i++) {
      stars.push(i <= rating)
    }
    return stars
  },

  // 获取评分文本
  getRatingText(rating: number): string {
    const texts = ['', '很差', '较差', '一般', '推荐', '强烈推荐']
    return texts[rating] || '未评分'
  },

  // 获取评分颜色
  getRatingColor(rating: number): string {
    if (rating >= 4.5) return '#67c23a'
    if (rating >= 3.5) return '#e6a23c'
    if (rating >= 2.5) return '#f56c6c'
    return '#909399'
  }
}

// 格式化相对时间
export const formatRelativeTime = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diffInSeconds < 60) return '刚刚'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}分钟前`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}小时前`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}天前`

  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}