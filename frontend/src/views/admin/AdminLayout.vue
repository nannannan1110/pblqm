<template>
  <div class="admin-layout">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="250px" class="admin-sidebar">
        <div class="sidebar-header">
          <h2>管理后台</h2>
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
      </el-aside>

      <!-- 主内容区域 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header class="admin-header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">管理后台</el-breadcrumb-item>
              <el-breadcrumb-item>{{ getCurrentPageTitle() }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>

          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <div class="user-dropdown">
                <el-avatar :size="32" :src="currentUser?.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="username">{{ currentUser?.username }}</span>
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 主体内容 -->
        <el-main class="admin-main">
          <router-view />
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
  ArrowDown
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
}

.admin-sidebar {
  background: #304156;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.08);
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2674e6;
  color: white;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.admin-menu {
  border: none;
  background: #304156;
}

:deep(.admin-menu .el-menu-item) {
  color: #bfcbd9;
  border-left: 3px solid transparent;
}

:deep(.admin-menu .el-menu-item:hover) {
  background: #263445 !important;
  color: #409eff !important;
}

:deep(.admin-menu .el-menu-item.is-active) {
  background: #263445 !important;
  color: #409eff !important;
  border-left-color: #409eff;
}

:deep(.admin-menu .el-menu-item .el-icon) {
  margin-right: 8px;
}

.admin-header {
  background: white;
  border-bottom: 1px solid #d8dce5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background: #f5f7fa;
}

.username {
  margin: 0 8px;
  font-weight: 500;
  color: #303133;
}

.admin-main {
  background: #f0f2f5;
  padding: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    width: 200px !important;
  }

  .sidebar-header h2 {
    font-size: 16px;
  }

  .username {
    display: none;
  }
}

@media (max-width: 480px) {
  .admin-sidebar {
    width: 64px !important;
  }

  .sidebar-header h2 {
    display: none;
  }

  :deep(.admin-menu .el-menu-item span) {
    display: none;
  }

  :deep(.admin-menu .el-menu-item .el-icon) {
    margin-right: 0;
    font-size: 18px;
  }
}

/* Element Plus 样式优化 */
:deep(.el-breadcrumb__item) {
  font-size: 14px;
}

:deep(.el-dropdown-menu__item) {
  font-size: 14px;
}
</style>