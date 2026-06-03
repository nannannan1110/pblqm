<template>
  <div class="admin-layout">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="260px" class="admin-sidebar">
        <div class="sidebar-header">
          <div class="logo-wrapper">
            <el-icon class="logo-icon"><ChefHat /></el-icon>
            <h2>美食管理</h2>
          </div>
        </div>

        <el-menu
          :default-active="activeMenu"
          router
          unique-opened
          class="admin-menu"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><Odometer /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>

          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>

          <el-menu-item index="/admin/recipes">
            <el-icon><Food /></el-icon>
            <span>菜谱管理</span>
          </el-menu-item>

          <el-menu-item index="/admin/comments">
            <el-icon><ChatDotRound /></el-icon>
            <span>评论管理</span>
          </el-menu-item>

          <el-menu-item index="/admin/statistics">
            <el-icon><TrendCharts /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
        </el-menu>

        <!-- 侧边栏底部信息 -->
        <div class="sidebar-footer">
          <div class="version-info">
            <span>版本 1.0.0</span>
          </div>
        </div>
      </el-aside>

      <!-- 主内容区域 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header class="admin-header">
          <div class="header-left">
            <el-breadcrumb separator=">">
              <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">
                <el-icon><Home /></el-icon>
                <span>管理后台</span>
              </el-breadcrumb-item>
              <el-breadcrumb-item>{{ getCurrentPageTitle() }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>

          <div class="header-right">
            <!-- 通知按钮 -->
            <el-badge :value="0" class="notification-badge">
              <el-button icon="Bell" class="notification-btn" circle />
            </el-badge>
            
            <el-dropdown @command="handleCommand">
              <div class="user-dropdown">
                <el-avatar :size="36" :src="currentUser?.avatar" class="user-avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="user-info">
                  <span class="username">{{ currentUser?.username }}</span>
                  <span class="user-role">管理员</span>
                </div>
                <el-icon class="arrow-icon"><ChevronDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    <span>个人资料</span>
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    <span>系统设置</span>
                  </el-dropdown-item>
                  <el-dropdown-divider />
                  <el-dropdown-item command="logout">
                    <el-icon><LogOut /></el-icon>
                    <span>退出登录</span>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 主体内容 -->
        <el-main class="admin-main">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Odometer,
  User,
  Food,
  ChatDotRound,
  Collection,
  TrendCharts,
  ChefHat,
  Home,
  Bell,
  ChevronDown,
  Setting,
  LogOut
} from '@element-plus/icons-vue'
import { authApi, type User as UserType } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const currentUser = ref<UserType | null>(null)

const activeMenu = computed(() => route.path)

// 获取当前页面标题
const getCurrentPageTitle = () => {
  const titles: Record<string, string> = {
    '/admin/dashboard': '仪表盘',
    '/admin/users': '用户管理',
    '/admin/recipes': '菜谱管理',
    '/admin/comments': '评论管理',
    '/admin/statistics': '数据统计'
  }
  return titles[route.path] || '管理后台'
}

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      // 跳转到个人资料页面
      router.push('/profile')
      break
    case 'settings':
      // 系统设置（预留）
      ElMessage.info('系统设置功能开发中')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch (error: any) {
    // 用户取消操作，静默返回
    return
  }

  try {
    authApi.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error: any) {
    console.error('退出登录失败:', error)
    ElMessage.error('退出登录失败')
  }
}

// 页面加载时获取用户信息
onMounted(() => {
  currentUser.value = authApi.getCurrentUser()
})
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  display: flex;
  background: #f5f7fa;
}

.admin-sidebar {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  position: relative;
}

.admin-sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.sidebar-header {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 28px;
  color: white;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
}

.admin-menu {
  border: none;
  background: transparent;
  flex: 1;
  padding-top: 20px;
  position: relative;
  z-index: 1;
}

:deep(.admin-menu .el-menu-item) {
  color: #94a3b8;
  border-left: 3px solid transparent;
  margin: 4px 12px;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.admin-menu .el-menu-item:hover) {
  background: rgba(102, 126, 234, 0.15) !important;
  color: #e2e8f0 !important;
  border-left-color: rgba(102, 126, 234, 0.5);
  transform: translateX(4px);
}

:deep(.admin-menu .el-menu-item.is-active) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%) !important;
  color: #667eea !important;
  border-left-color: #667eea;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
}

:deep(.admin-menu .el-menu-item .el-icon) {
  margin-right: 12px;
  font-size: 18px;
}

:deep(.admin-menu .el-menu-item span) {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.version-info {
  text-align: center;
}

.version-info span {
  font-size: 12px;
  color: #64748b;
}

.admin-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  height: 70px;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #f8fafc;
  border: none;
  color: #64748b;
  transition: all 0.3s;
}

.notification-btn:hover {
  background: #e2e8f0;
  color: #667eea;
}

.notification-badge {
  --el-badge-bg-color: #ef4444;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 10px;
  transition: all 0.3s;
  gap: 12px;
}

.user-dropdown:hover {
  background: #f8fafc;
}

.user-avatar {
  border: 2px solid #e2e8f0;
  transition: all 0.3s;
}

.user-dropdown:hover .user-avatar {
  border-color: #667eea;
  box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  margin: 0;
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.user-role {
  margin: 0;
  font-size: 12px;
  color: #94a3b8;
}

.arrow-icon {
  font-size: 14px;
  color: #94a3b8;
  transition: transform 0.3s;
}

.user-dropdown:hover .arrow-icon {
  transform: rotate(180deg);
}

.admin-main {
  background: #f5f7fa;
  padding: 24px;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .admin-sidebar {
    width: 220px !important;
  }

  .sidebar-header h2 {
    font-size: 18px;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 72px !important;
  }

  .sidebar-header h2 {
    display: none;
  }

  .logo-wrapper {
    justify-content: center;
  }

  :deep(.admin-menu .el-menu-item span) {
    display: none;
  }

  :deep(.admin-menu .el-menu-item .el-icon) {
    margin-right: 0;
    font-size: 20px;
  }

  :deep(.admin-menu .el-menu-item) {
    text-align: center;
  }

  .sidebar-footer {
    display: none;
  }

  .user-info {
    display: none;
  }
}

@media (max-width: 480px) {
  .admin-header {
    padding: 0 12px;
  }

  .admin-main {
    padding: 16px;
  }
}

/* Element Plus 样式优化 */
:deep(.el-breadcrumb__item) {
  font-size: 14px;
}

:deep(.el-breadcrumb__item:last-child) {
  font-weight: 600;
  color: #1e293b;
}

:deep(.el-breadcrumb__separator) {
  color: #cbd5e1;
}

:deep(.el-dropdown-menu) {
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: none;
  padding: 8px;
}

:deep(.el-dropdown-menu__item) {
  font-size: 14px;
  padding: 10px 16px;
  border-radius: 8px;
  margin: 2px;
  transition: all 0.2s;
}

:deep(.el-dropdown-menu__item:hover) {
  background: #f1f5f9;
}

:deep(.el-dropdown-divider) {
  margin: 8px 0;
  background: #e2e8f0;
}
</style>