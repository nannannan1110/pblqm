<template>
  <div class="admin-dashboard">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div>
          <h2>仪表盘</h2>
          <p>欢迎回来，管理员</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" icon="Refresh" @click="refreshData">
            刷新数据
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="24" v-loading="loading" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card user-card">
          <div class="stat-item">
            <div class="stat-icon-wrapper user-icon">
              <el-icon class="stat-icon"><User /></el-icon>
            </div>
            <div class="stat-content">
              <p class="stat-label">总用户数</p>
              <h3 class="stat-value">{{ statistics.user_count }}</h3>
              <p class="stat-trend positive">
                <el-icon><TrendUp /></el-icon>
                <span>+12%</span>
                <span class="trend-label">较上月</span>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card recipe-card">
          <div class="stat-item">
            <div class="stat-icon-wrapper recipe-icon">
              <el-icon class="stat-icon"><Food /></el-icon>
            </div>
            <div class="stat-content">
              <p class="stat-label">菜谱数量</p>
              <h3 class="stat-value">{{ statistics.recipe_count }}</h3>
              <p class="stat-trend positive">
                <el-icon><TrendUp /></el-icon>
                <span>+8%</span>
                <span class="trend-label">较上月</span>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card comment-card">
          <div class="stat-item">
            <div class="stat-icon-wrapper comment-icon">
              <el-icon class="stat-icon"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-content">
              <p class="stat-label">评论数量</p>
              <h3 class="stat-value">{{ statistics.comment_count }}</h3>
              <p class="stat-trend positive">
                <el-icon><TrendUp /></el-icon>
                <span>+15%</span>
                <span class="trend-label">较上月</span>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card favorite-card">
          <div class="stat-item">
            <div class="stat-icon-wrapper favorite-icon">
              <el-icon class="stat-icon"><Star /></el-icon>
            </div>
            <div class="stat-content">
              <p class="stat-label">收藏数量</p>
              <h3 class="stat-value">{{ statistics.favorite_count }}</h3>
              <p class="stat-trend positive">
                <el-icon><TrendUp /></el-icon>
                <span>+22%</span>
                <span class="trend-label">较上月</span>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速操作区域 -->
    <el-row :gutter="24" class="quick-actions-row">
      <el-col :span="12">
        <el-card class="quick-action-card">
          <h3 class="section-title">
            <el-icon><BarChart /></el-icon>
            <span>最近活动</span>
          </h3>
          <div class="activity-list">
            <div class="activity-item">
              <el-avatar size="40" icon="User" class="activity-avatar" />
              <div class="activity-content">
                <p class="activity-title">新用户注册</p>
                <p class="activity-time">5分钟前</p>
              </div>
              <el-tag type="success" size="small">新用户</el-tag>
            </div>
            <div class="activity-item">
              <el-avatar size="40" icon="Food" class="activity-avatar" />
              <div class="activity-content">
                <p class="activity-title">新菜谱发布</p>
                <p class="activity-time">12分钟前</p>
              </div>
              <el-tag type="primary" size="small">菜谱</el-tag>
            </div>
            <div class="activity-item">
              <el-avatar size="40" icon="Message" class="activity-avatar" />
              <div class="activity-content">
                <p class="activity-title">新评论</p>
                <p class="activity-time">28分钟前</p>
              </div>
              <el-tag type="info" size="small">评论</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="quick-action-card">
          <h3 class="section-title">
            <el-icon><Zap /></el-icon>
            <span>快捷操作</span>
          </h3>
          <div class="quick-actions-grid">
            <el-button class="quick-action-btn add-user-btn" icon="UserPlus" @click="goTo('/admin/users')">
              <span>管理用户</span>
            </el-button>
            <el-button class="quick-action-btn add-recipe-btn" icon="Plus" @click="goTo('/admin/recipes')">
              <span>菜谱管理</span>
            </el-button>
            <el-button class="quick-action-btn comment-btn" icon="ChatDotRound" @click="goTo('/admin/comments')">
              <span>评论管理</span>
            </el-button>
            <el-button class="quick-action-btn stats-btn" icon="TrendCharts" @click="goTo('/admin/statistics')">
              <span>数据统计</span>
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, 
  Food, 
  ChatDotRound, 
  Star, 
  TrendUp,
  BarChart,
  Zap,
  UserPlus,
  Plus,
  Refresh
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/api/index'

const router = useRouter()
const loading = ref(false)
const statistics = ref({
  user_count: 0,
  recipe_count: 0,
  comment_count: 0,
  favorite_count: 0,
  like_count: 0
})

// 获取统计数据
const fetchStatistics = async () => {
  loading.value = true
  try {
    const data = await api.get('/admin/statistics')
    if (data) {
      statistics.value = data
    }
  } catch (error: any) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = () => {
  fetchStatistics()
  ElMessage.success('数据已刷新')
}

// 跳转到指定页面
const goTo = (path: string) => {
  router.push(path)
}

onMounted(() => {
  fetchStatistics()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
  padding: 20px 0;
  border-bottom: 1px solid #e2e8f0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 28px;
  font-weight: 700;
}

.page-header p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .el-button {
  border-radius: 8px;
  font-weight: 500;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.recipe-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.comment-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.favorite-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-icon {
  font-size: 26px;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-label {
  margin: 0 0 8px 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 500;
}

.stat-value {
  margin: 0 0 12px 0;
  color: #1e293b;
  font-size: 32px;
  font-weight: 700;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0;
  font-size: 13px;
}

.stat-trend.positive {
  color: #10b981;
}

.stat-trend.negative {
  color: #ef4444;
}

.trend-label {
  color: #94a3b8;
  margin-left: 4px;
}

.quick-actions-row {
  margin-bottom: 24px;
}

.quick-action-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px 0;
  color: #1e293b;
  font-size: 16px;
  font-weight: 600;
}

.section-title .el-icon {
  color: #667eea;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  transition: background-color 0.2s;
}

.activity-item:hover {
  background: #f8fafc;
}

.activity-avatar {
  background: #e2e8f0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  margin: 0 0 4px 0;
  color: #1e293b;
  font-size: 14px;
  font-weight: 500;
}

.activity-time {
  margin: 0;
  color: #94a3b8;
  font-size: 12px;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.quick-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border-radius: 12px;
  border: none;
  background: #f8fafc;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.quick-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.add-user-btn:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #667eea;
}

.add-recipe-btn:hover {
  background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);
  color: #f5576c;
}

.comment-btn:hover {
  background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
  color: #4facfe;
}

.stats-btn:hover {
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
  color: #43e97b;
}

.quick-action-btn .el-icon {
  margin-bottom: 8px;
  font-size: 24px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .stats-row .el-col {
    margin-bottom: 16px;
  }
  
  .quick-actions-row .el-col {
    margin-bottom: 16px;
  }
}

@media (max-width: 768px) {
  .page-header h2 {
    font-size: 22px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .quick-actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
