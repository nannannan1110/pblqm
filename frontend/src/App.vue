<template>
  <div id="app" :class="{ 'admin-page': isAdminPage, 'auth-page': isAuthPage }">
    <!-- 导航栏（管理员页面和认证页面隐藏） -->
    <el-header v-if="!isAdminPage && !isAuthPage" class="app-header">
      <div class="header-container">
        <div class="header-left">
          <router-link to="/home" class="logo">
            <el-icon><Food /></el-icon>
            <span>菜谱分享</span>
          </router-link>
        </div>

        <div class="header-center">
          <el-menu
            :default-active="activeRoute"
            mode="horizontal"
            :router="true"
            class="nav-menu"
          >
            <el-menu-item index="/home">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/recipes">
              <el-icon><Collection /></el-icon>
              <span>菜谱</span>
            </el-menu-item>
            <el-menu-item v-if="authApi.isLoggedIn()" index="/create-recipe">
              <el-icon><Plus /></el-icon>
              <span>创建菜谱</span>
            </el-menu-item>
            <el-menu-item index="/about">
              <el-icon><InfoFilled /></el-icon>
              <span>关于</span>
            </el-menu-item>
          </el-menu>
        </div>

        <div class="header-right">
          <template v-if="authApi.isLoggedIn()">
            <!-- 用户菜单 -->
            <el-dropdown @command="handleUserMenuCommand">
              <div class="user-info">
                <el-avatar :size="32" :src="currentUser?.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="username">{{ currentUser?.username }}</span>
                <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人资料
                  </el-dropdown-item>
                  <el-dropdown-item command="my-recipes">
                    <el-icon><Collection /></el-icon>
                    我的菜谱
                  </el-dropdown-item>
                  <el-dropdown-item v-if="currentUser?.is_admin" command="admin">
                    <el-icon><Setting /></el-icon>
                    管理后台
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <!-- 登录/注册按钮 -->
            <el-button @click="$router.push('/')">登录</el-button>
            <el-button type="primary" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="app-main">
      <router-view />
    </el-main>

    <!-- 页脚（管理员页面和认证页面隐藏） -->
    <el-footer v-if="!isAdminPage && !isAuthPage" class="app-footer">
      <div class="footer-content">
        <p>&copy; 2025 菜谱分享系统. 保留所有权利.</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Food,
  House,
  Collection,
  Plus,
  InfoFilled,
  User,
  ArrowDown,
  SwitchButton,
  Setting
} from '@element-plus/icons-vue'
import { authApi, type User as UserType } from '@/api/auth'

const route = useRoute()
const router = useRouter()
const currentUser = ref<UserType | null>(null)

// 当前激活的菜单项
const activeRoute = computed(() => {
  // 处理详情页的特殊情况
  if (route.path.startsWith('/recipes/') && route.path !== '/recipes') {
    return '/recipes'
  }
  return route.path
})

// 检查是否为管理员页面
const isAdminPage = computed(() => {
  return route.path.startsWith('/admin')
})

// 检查是否为认证页面（登录/注册）
const isAuthPage = computed(() => {
  return route.path === '/' || route.path === '/register'
})

// 获取当前用户信息
const getCurrentUser = () => {
  currentUser.value = authApi.getCurrentUser()
}

// 处理用户菜单命令
const handleUserMenuCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'my-recipes':
      router.push('/my-recipes')
      break
    case 'admin':
      router.push('/admin/dashboard')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        authApi.clearUserInfo()
        currentUser.value = null
        ElMessage.success({
          message: '已退出登录',
          duration: 1500
        })

        // 如果在需要认证的页面，跳转到首页
        if (route.meta.requiresAuth) {
          router.push('/')
        }
      } catch {
        // 用户取消操作
      }
      break
  }
}

// 监听路由变化，更新用户信息和背景色
watch(
  () => route.path,
  () => {
    getCurrentUser()

    // 动态控制背景色
    if (isAuthPage.value) {
      // 认证页面：透明背景（让页面自己的背景图片显示）
      document.body.style.background = 'transparent'
      document.body.style.backgroundColor = 'transparent'
    } else if (isAdminPage.value) {
      // 管理员页面：浅灰色背景
      document.body.style.background = '#f0f2f5'
      document.body.style.backgroundColor = '#f0f2f5'
    } else {
      // 普通页面：白色背景
      document.body.style.background = '#ffffff'
      document.body.style.backgroundColor = '#ffffff'
    }
  },
  { immediate: true }
)

// 页面加载时获取用户信息
onMounted(() => {
  getCurrentUser()
})
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

/* 确保 html 和 body 在认证页面也不会遮挡背景 */
:deep(html) {
  height: 100%;
}

:deep(body) {
  min-height: 100%;
  margin: 0;
  padding: 0;
}

.app-header {
  background: white;
  border-bottom: 1px solid #f0f0f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  padding: 0;
  height: 60px;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 20px;
}

.header-left {
  flex-shrink: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.logo:hover {
  color: #337ecc;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-menu {
  border-bottom: none;
  background: transparent;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  color: #909399;
  transition: transform 0.3s ease;
}

.app-main {
  flex: 1;
  padding: 0;
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px);
}

/* 认证页面全屏显示，背景透明让背景图片完全显示 */
.auth-page .app-main {
  min-height: 100vh;
  background: transparent !important;
  background-color: transparent !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 确保认证页面的 #app 也是透明的 */
.auth-page {
  background: transparent !important;
  background-color: transparent !important;
}

/* 管理员页面特殊样式 */
.admin-page .app-main {
  min-height: 100vh;
  background-color: #f0f2f5;
}

.app-footer {
  background: white;
  border-top: 1px solid #f0f0f0;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  text-align: center;
  color: #909399;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
  }

  .logo {
    font-size: 18px;
  }

  .logo span {
    display: none;
  }

  .header-center {
    flex: 1;
    overflow-x: auto;
  }

  .nav-menu {
    min-width: max-content;
  }

  .username {
    display: none;
  }

  .header-right {
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 0 12px;
  }

  .nav-menu :deep(.el-menu-item) {
    padding: 0 12px;
  }

  .nav-menu :deep(.el-menu-item span) {
    display: none;
  }
}

/* Element Plus 样式覆盖 */
:deep(.el-menu--horizontal > .el-menu-item) {
  border-bottom: none;
  height: 60px;
  line-height: 60px;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  border-bottom: 2px solid #409eff;
  color: #409eff;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
