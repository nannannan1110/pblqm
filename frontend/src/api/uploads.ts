import api from './index'

// 文件上传响应类型
export interface UploadResponse {
  message: string
  filename: string
  url: string
  size: number
}

// 文件上传API
export const uploadApi = {
  // 上传图片
  uploadImage(file: File) {
    const formData = new FormData()
    formData.append('image', file)

    return api.post('/uploads/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }) as Promise<UploadResponse>
  },

  // 删除图片
  deleteImage(filename: string) {
    return api.delete(`/uploads/delete-image/${filename}`)
  },

  // 获取图片URL（拼接完整URL）
  getImageUrl(filename: string): string {
    return `${process.env.VUE_APP_API_URL || 'http://localhost:5000'}/static/uploads/images/${filename}`
  }
}
