import api from './index'

export interface PostComment {
  id: number
  user_id: number
  post_id: number
  content: string
  created_at: string
  author: {
    id: number
    username: string
    avatar?: string
  }
}

export interface Post {
  id: number
  user_id: number
  title: string
  content: string
  image?: string
  created_at: string
  updated_at: string
  likes_count: number
  comments_count: number
  author: {
    id: number
    username: string
    avatar?: string
  }
}

// 获取帖子列表
export const getPosts = (page = 1, perPage = 10) => {
  return api.get('/posts', { params: { page, per_page: perPage } })
}

// 获取我的帖子
export const getMyPosts = (page = 1, perPage = 10) => {
  return api.get('/posts/my', { params: { page, per_page: perPage } })
}

// 获取单个帖子
export const getPost = (postId: number) => {
  return api.get(`/posts/${postId}`)
}

// 创建帖子
export const createPost = (data: { title: string; content: string; image?: File }) => {
  const formData = new FormData()
  formData.append('title', data.title)
  formData.append('content', data.content)
  if (data.image) {
    formData.append('image', data.image)
  }
  return api.post('/posts', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// 更新帖子
export const updatePost = (postId: number, data: { title?: string; content?: string }) => {
  return api.put(`/posts/${postId}`, data)
}

// 删除帖子
export const deletePost = (postId: number) => {
  return api.delete(`/posts/${postId}`)
}

// 点赞/取消点赞帖子
export const togglePostLike = (postId: number) => {
  return api.post(`/posts/${postId}/like`)
}

// 获取帖子评论
export const getPostComments = (postId: number) => {
  return api.get(`/posts/${postId}/comments`)
}

// 添加评论
export const addPostComment = (postId: number, content: string) => {
  return api.post(`/posts/${postId}/comments`, { content })
}

// 删除评论
export const deletePostComment = (postId: number, commentId: number) => {
  return api.delete(`/posts/${postId}/comments/${commentId}`)
}
