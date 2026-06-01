<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h2>仪表盘</h2>
      <p>欢迎来到管理后台</p>
    </div>

    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <el-icon class="stat-icon"><User /></el-icon>
            <div class="stat-content">
              <h3>{{ statistics.user_count }}</h3>
              <p>总用户数</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <el-icon class="stat-icon"><Food /></el-icon>
            <div class="stat-content">
              <h3>{{ statistics.recipe_count }}</h3>
              <p>菜谱数量</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <el-icon class="stat-icon"><ChatDotRound /></el-icon>
            <div class="stat-content">
              <h3>{{ statistics.comment_count }}</h3>
              <p>评论数量</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="stat-item">
            <el-icon class="stat-icon"><Star /></el-icon>
            <div class="stat-content">
              <h3>{{ statistics.favorite_count }}</h3>
              <p>收藏数量</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { User, Food, ChatDotRound, Star } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/api/index'

const loading = ref(false) //创建响应式变量loading，初始值为false
const statistics = ref({
  user_count: 0,
  recipe_count: 0,
  comment_count: 0,
  favorite_count: 0,
  like_count: 0
}) //创建了一个响应式对象，用于存储管理员仪表盘的统计数据。

// 获取统计数据
const fetchStatistics = async () => {
  loading.value = true
  try {
    // 从后端API获取统计数据
    const data = await api.get('/admin/statistics')
//异步数据获取的错误处理和数据更新的核心部分
    if (data) {
      statistics.value = data
    } //条件判断语句，检查 data 变量是否存在且不为null/undefined
  } catch (error: any) {
    console.error('获取统计数据失败:', error) //在浏览器控制台输出错误信息，便于开发者调试
    ElMessage.error('获取统计数据失败') //使用Element Plus的Message组件显示错误提示。
  } finally {
    loading.value = false
  } //将加载状态设置为 false，确保无论异步操作成功还是失败，都会执行特定的清理工作。
}
//Vue.js 3 的组合式 API 中的生命周期钩子，用于在组件挂载时自动执行数据获取操作。
onMounted(() => { //onMounted 是 Vue 的生命周期钩子，当组件被挂载到 DOM 上时触发
  fetchStatistics()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 24px;
  color: #409eff;
}

.stat-content h3 {
  margin: 0 0 4px 0;
  font-size: 24px;
  color: #303133;
}

.stat-content p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}
</style>
