import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 30000, // 增加到30秒
  withCredentials: false, // CORS credentials
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加JWT token和用户ID
api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加 X-User-ID 头（后端需要这个来验证用户身份）
    const userStr = sessionStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        config.headers['X-User-ID'] = user.id.toString()
      } catch {
        // 忽略
      }
    }

    // 添加请求日志
    console.log('=== API Request ===')
    console.log('URL:', config.baseURL + config.url)
    console.log('Method:', config.method?.toUpperCase())
    console.log('Headers:', config.headers)
    console.log('Data:', config.data)

    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 详细日志
    console.error('=== API Error ===')
    console.error('Error config:', error.config?.url)
    console.error('Error response:', error.response)
    console.error('Error message:', error.message)
    console.error('Error request:', error.request ? 'exists' : 'none')

    // 处理不同的HTTP错误状态
    if (error.response) {
      const status = error.response.status
      const data = error.response.data

      switch (status) {
        case 401:
          // 未授权，清除token并跳转登录
          sessionStorage.removeItem('access_token')
          sessionStorage.removeItem('user')
          ElMessage.error('登录已过期，请重新登录')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          // 安全地获取错误消息
          const errorMsg = (data && data.message) || `请求失败 (${status})`
          ElMessage.error(errorMsg)
      }
    } else if (error.request) {
      console.error('Network error - no response received')
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      console.error('Request config error')
      ElMessage.error('请求配置错误')
    }

    return Promise.reject(error)
  }
)

export default api