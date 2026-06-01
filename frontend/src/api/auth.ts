import api from './index'

// 用户类型定义
export interface User {
  id: number
  username: string
  email: string
  bio?: string
  avatar?: string
  created_at: string
  is_admin: boolean
}

// 登录响应类型定义
export interface LoginResponse {
  access_token: string
  user: User
}

// 注册请求数据
export interface RegisterRequest {
  username: string
  email: string
  password: string
}

// 登录请求数据
export interface LoginRequest {
  username?: string
  email?: string
  password: string
}

// 认证相关API
export const authApi = {
  // 用户注册
  register(data: RegisterRequest) {
    return api.post<{ message: string }>('/auth/register', data)
  },

  // 用户登录
  login(data: LoginRequest) {
    return api.post<LoginResponse>('/auth/login', data)
  },

  // 获取用户资料
  getProfile() {
    return api.get<User>('/users/profile')
  },

  // 保存用户信息到sessionStorage（仅在当前会话有效）
  saveUserInfo(token: string, user: User) {
    sessionStorage.setItem('access_token', token)
    sessionStorage.setItem('user', JSON.stringify(user))
  },

  // 清除用户信息
  clearUserInfo() {
    sessionStorage.removeItem('access_token')
    sessionStorage.removeItem('user')
  },

  // 获取当前用户信息
  getCurrentUser(): User | null {
    const userStr = sessionStorage.getItem('user')
    if (userStr) {
      try {
        return JSON.parse(userStr)
      } catch {
        return null
      }
    }
    return null
  },

  // 检查是否已登录
  isLoggedIn(): boolean {
    return !!sessionStorage.getItem('access_token')
  },

  // 退出登录
  logout() {
    this.clearUserInfo()
  }
}