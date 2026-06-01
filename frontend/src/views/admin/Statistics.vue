<template>
  <div class="admin-statistics">
    <div class="page-header">
      <h2>数据统计</h2>
      <p>系统数据分析</p>
    </div>

    <el-row :gutter="20" v-loading="loading">
      <el-col :span="12">
        <el-card>
          <template #header>
            <h3>用户统计</h3>
          </template>
          <el-statistic title="总用户数" :value="statistics.user_count" />
          <el-divider />
          <div class="sub-stats">
            <p>活跃用户: {{ statistics.active_user_count || statistics.user_count }}</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <h3>菜谱统计</h3>
          </template>
          <el-statistic title="总菜谱数" :value="statistics.recipe_count" />
          <el-divider />
          <div class="sub-stats">
            <p>平均评分: {{ statistics.avg_rating || 4.5 }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <h3>互动统计</h3>
          </template>
          <div class="interaction-stats">
            <div class="stat-item">
              <el-icon class="stat-icon" color="#409eff"><Star /></el-icon>
              <span>收藏数: <strong>{{ statistics.favorite_count }}</strong></span>
            </div>
            <div class="stat-item">
              <el-icon class="stat-icon" color="#67c23a"><ChatDotRound /></el-icon>
              <span>评论数: <strong>{{ statistics.comment_count }}</strong></span>
            </div>
            <div class="stat-item">
              <el-icon class="stat-icon" color="#e6a23c"><Pointer /></el-icon>
              <span>点赞数: <strong>{{ statistics.like_count }}</strong></span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <h3>系统概览</h3>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="数据库大小">
              {{ statistics.db_size || '约10MB' }}
            </el-descriptions-item>
            <el-descriptions-item label="运行时间">
              {{ statistics.uptime || '正常运行' }}
            </el-descriptions-item>
            <el-descriptions-item label="最后更新">
              {{ formatDate(statistics.last_updated) }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, ChatDotRound, Pointer } from '@element-plus/icons-vue'
import api from '@/api/index'

const loading = ref(false)
const statistics = ref({
  user_count: 0,
  recipe_count: 0,
  comment_count: 0,
  favorite_count: 0,
  like_count: 0,
  avg_rating: 0,
  active_user_count: 0,
  db_size: '',
  uptime: '',
  last_updated: new Date().toISOString()
})

// 获取统计数据
const fetchStatistics = async () => {
  loading.value = true
  try {
    const data = await api.get('/admin/statistics')

    if (data) {
      statistics.value = {
        ...data,
        last_updated: new Date().toISOString()
      }
    }
  } catch (error: any) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchStatistics()
})
</script>

<style scoped>
.admin-statistics {
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

.sub-stats p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}

.interaction-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.stat-icon {
  font-size: 24px;
}

.stat-item strong {
  font-size: 18px;
  color: #303133;
}
</style>
