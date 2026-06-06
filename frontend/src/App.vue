<template>
  <div id="app" :class="{ 'admin-page': isAdminPage, 'auth-page': isAuthPage, 'dark-mode': isDarkMode }">
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
            :background-color="isDarkMode ? '#1a1a2e' : '#ffffff'"
            :text-color="isDarkMode ? '#e4e4e7' : '#303133'"
            :active-text-color="'#667eea'"
          >
            <el-menu-item index="/home">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/recipes">
              <el-icon><Collection /></el-icon>
              <span>菜谱</span>
            </el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="/favorites">
              <el-icon><HeartFilled /></el-icon>
              <span>我的收藏</span>
            </el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="/history">
              <el-icon><Clock /></el-icon>
              <span>浏览历史</span>
            </el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="/discovery">
              <el-icon><Compass /></el-icon>
              <span>发现</span>
            </el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="/create-recipe">
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
          <!-- 主题切换按钮 -->
          <el-button circle size="small" class="theme-toggle-btn" @click="toggleTheme">
            <el-icon><Sunny v-if="!isDarkMode" /><Moon v-else /></el-icon>
          </el-button>
          
          <template v-if="isLoggedIn">
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
            <el-button class="animate-btn" @click="$router.push('/')">登录</el-button>
            <el-button type="primary" class="animate-btn" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
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
import { useStore } from 'vuex'
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
  Setting,
  Sunny,
  Moon,
  HeartFilled,
  Clock,
  Compass
} from '@element-plus/icons-vue'
import { authApi, type User as UserType } from '@/api/auth'

const store = useStore()
const route = useRoute()
const router = useRouter()
const currentUser = ref<UserType | null>(null)

// 计算属性：实时检测登录状态
const isLoggedIn = computed(() => {
  return authApi.isLoggedIn()
})

const isDarkMode = computed(() => store.getters.isDarkMode)

const toggleTheme = () => {
  store.commit('TOGGLE_THEME')
}

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

// 监听路由变化，更新登录状态
watch(
  () => route.path,
  () => {
    getCurrentUser()
  }
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
  background: var(--bg-secondary);
  color: var(--text-primary);
  transition: background-color var(--transition-base), color var(--transition-base);
}

/* 页面过渡动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px) translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px) translateY(-10px);
}

/* 按钮动画类 */
.animate-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.animate-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.animate-btn:hover::before {
  left: 100%;
}

.animate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.35);
}

.animate-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.25);
}

/* 确保 html 和 body 在认证页面也不会遮挡背景 */
:deep(html) {
  height: 100%;
}

:deep(body) {
  min-height: 100%;
  margin: 0;
  padding: 0;
  background: var(--bg-secondary);
  color: var(--text-primary);
  transition: background var(--transition-base), color var(--transition-base);
}

.app-header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  padding: 0;
  height: 60px;
  transition: all 0.3s ease;
}

.app-header:hover {
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
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
  color: var(--accent-primary);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo:hover {
  color: var(--accent-secondary);
  transform: scale(1.03);
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

.theme-toggle-btn {
  border: none;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  transition: all 0.3s ease;
}

.theme-toggle-btn:hover {
  background: var(--accent-gradient);
  color: white;
  transform: rotate(30deg);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.user-info:hover {
  background-color: var(--bg-hover);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  color: var(--text-tertiary);
  transition: transform 0.3s ease;
}

.app-main {
  flex: 1;
  padding: 0;
  background: var(--bg-secondary);
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
  background-color: var(--bg-secondary);
}

.app-footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border-color);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 -2px 15px rgba(0, 0, 0, 0.03);
}

.footer-content {
  text-align: center;
  color: var(--text-tertiary);
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  border-bottom: 2px solid var(--accent-primary);
  color: var(--accent-primary);
}

:deep(.el-menu--horizontal > .el-menu-item:hover) {
  color: var(--accent-primary);
  background-color: var(--bg-hover);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.25s ease;
}

:deep(.el-dropdown-menu__item:hover) {
  background: var(--bg-hover);
  transform: translateX(4px);
}

:deep(.el-button) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
