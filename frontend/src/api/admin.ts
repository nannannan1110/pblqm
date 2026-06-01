import axios from 'axios'
import { authApi } from './auth'

const API_BASE_URL = 'http://localhost:5000/api'

// 创建axios实例
const adminAxios = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

// 请求拦截器 - 添加管理员权限头
adminAxios.interceptors.request.use(
  (config) => {
    const currentUser = authApi.getCurrentUser()
    if (currentUser && currentUser.id) {
      config.headers['X-User-ID'] = currentUser.id.toString()
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
adminAxios.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 403) {
      // 权限不足，跳转到首页
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export const adminApi = {
  // ============= 用户管理 API =============
  // 获取用户列表
  getUsers: (params?: any) => {
    return adminAxios.get('/admin/users', { params })
  },

  // 获取用户详情
  getUser: (userId: number) => {
    return adminAxios.get(`/admin/users/${userId}`)
  },

  // 更新用户信息
  updateUser: (userId: number, data: any) => {
    return adminAxios.put(`/admin/users/${userId}`, data)
  },

  // 删除用户
  deleteUser: (userId: number) => {
    return adminAxios.delete(`/admin/users/${userId}`)
  },

  // 更新用户角色
  updateUserRoles: (userId: number, roleIds: number[]) => {
    return adminAxios.put(`/admin/users/${userId}/roles`, { role_ids: roleIds })
  },

  // ============= 角色管理 API =============
  // 获取角色列表
  getRoles: () => {
    return adminAxios.get('/roles')
  },

  // ============= 业务数据管理 API =============
  // 批量删除菜谱
  deleteRecipes: (recipeIds: number[]) => {
    return adminAxios.delete('/admin/recipes', {
      data: { recipe_ids: recipeIds }
    })
  },

  // 批量删除评论
  deleteComments: (commentIds: number[]) => {
    return adminAxios.delete('/admin/comments', {
      data: { comment_ids: commentIds }
    })
  },

  // ============= 数据统计 API =============
  // 获取统计数据
  getStatistics: () => {
    return adminAxios.get('/admin/statistics')
  },

  // 获取仪表板数据
  getDashboard: () => {
    return adminAxios.get('/admin/dashboard')
  }
}

export default adminApi