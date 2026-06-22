<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>欢迎登录</h2>
          <p class="subtitle">菜谱分享系统</p>
        </div>
      </template>

      <!-- 登录类型选择 -->
      <div class="login-type-selector">
        <el-radio-group v-model="loginType" class="type-group">
          <el-radio-button
            :class="['type-btn', loginType === 'user' ? 'active' : '']"
            label="user"
          >
            <el-icon><User /></el-icon>
            <span>用户登录</span>
          </el-radio-button>
          <el-radio-button
            :class="['type-btn', loginType === 'admin' ? 'active' : '']"
            label="admin"
          >
            <el-icon><Setting /></el-icon>
            <span>管理员登录</span>
          </el-radio-button>
        </el-radio-group>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="80px"
        @submit.prevent="handleLogin"
        class="login-form"
      >
        <el-form-item :label="loginType === 'admin' ? '管理员账号' : '用户名'" prop="username">
          <el-input
            v-model="loginForm.username"
            :placeholder="loginType === 'admin' ? '请输入管理员账号' : '请输入用户名或邮箱'"
            :prefix-icon="User"
            clearable
            size="large"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            clearable
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item v-if="loginType === 'admin'" class="admin-notice">
          <el-alert
            title="管理员登录"
            type="warning"
            :closable="false"
            show-icon
          >
            请使用管理员账号登录以访问管理后台
          </el-alert>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            size="large"
            style="width: 100%"
            @click="handleLogin"
          >
            {{ loginType === 'admin' ? '管理员登录' : '用户登录' }}
          </el-button>
        </el-form-item>

        <div class="login-footer">
          <router-link to="/register" class="register-link">
            还没有账号？立即注册
          </router-link>
          <span class="separator">|</span>
          <a href="#" class="forgot-link" @click.prevent="handleForgotPassword">
            忘记密码？
          </a>
        </div>
      </el-form>
    </el-card>

    <!-- 登录提示信息 -->
    <div class="login-tips" v-if="showTips">
      <el-alert
        title="登录提示"
        type="info"
        :closable="true"
        @close="showTips = false"
      >
        <template #default>
          <p v-if="loginType === 'admin'">
            管理员账号请联系系统管理员获取<br>
            如有登录问题，请联系技术支持
          </p>
          <p v-else>
            普通用户可以直接注册使用<br>
            注册后即可浏览和创建菜谱
          </p>
        </template>
      </el-alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus'
import { User, Lock, Setting } from '@element-plus/icons-vue'
import { authApi, type LoginRequest } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const loginType = ref<'user' | 'admin'>('user')
const showTips = ref(false)

// 表单数据
const loginForm = reactive<LoginRequest>({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

// 处理登录类型切换
const handleLoginTypeChange = (type: 'user' | 'admin') => {
  loginType.value = type
  // 清空表单
  loginForm.username = ''
  loginForm.password = ''
  // 清除验证状态
  if (loginFormRef.value) {
    loginFormRef.value.clearValidate()
  }

  // 显示相应的提示
  if (type === 'admin') {
    showTips.value = true
  }
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    // 根据登录类型设置不同的登录参数
    const loginData: LoginRequest = {
      username: loginForm.username,
      password: loginForm.password
    }

    console.log('=== Login Request ===')
    console.log('Login data:', loginData)
    
    const response = await authApi.login(loginData)
    
    console.log('=== Login Response ===')
    console.log('Response:', response)
    console.log('Access token:', response?.access_token)
    console.log('User:', response?.user)

    // 验证登录类型是否匹配
    if (loginType.value === 'admin' && !response.user.is_admin) {
      ElMessage.error({
        message: '该账号不是管理员账号，请使用管理员账号登录',
        duration: 2000
      })
      return
    }

    if (loginType.value === 'user' && response.user.is_admin) {
      // 管理员在用户登录界面登录，给予友好提示
      try {
        await ElMessageBox.confirm(
          '检测到您是管理员账号，是否跳转到管理后台？',
          '登录确认',
          {
            confirmButtonText: '跳转管理后台',
            cancelButtonText: '继续使用用户端',
            type: 'info'
          }
        )
        // 用户选择跳转管理后台
        authApi.saveUserInfo(response.access_token, response.user)
        ElMessage.success({
          message: '登录成功！欢迎管理员',
          duration: 1500
        })
        router.push('/admin/dashboard')
        return
      } catch {
        // 用户选择继续使用用户端，正常跳转到首页
        authApi.saveUserInfo(response.access_token, response.user)
        ElMessage.success({
          message: '登录成功！欢迎回来',
          duration: 1500
        })
        const redirect = route.query.redirect as string
        router.push(redirect || '/home')
        return
      }
    }

    // 保存用户信息和token
    authApi.saveUserInfo(response.access_token, response.user)

    // 根据用户类型显示不同的成功消息
    if (response.user.is_admin) {
      ElMessage.success({
        message: '管理员登录成功！',
        duration: 1500
      })
      // 管理员直接跳转到管理后台
      const redirect = route.query.redirect as string
      router.push(redirect || '/admin/dashboard')
    } else {
      ElMessage.success({
        message: '登录成功！欢迎回来',
        duration: 1500
      })
      // 普通用户跳转到首页
      const redirect = route.query.redirect as string
      router.push(redirect || '/home')
    }

  } catch (error: any) {
    console.error('登录失败:', error)
    // 错误信息已由axios拦截器处理
  } finally {
    loading.value = false
  }
}

// 处理忘记密码
const handleForgotPassword = async () => {
  if (loginType.value === 'admin') {
    ElMessageBox.alert(
      '管理员账号忘记密码，请联系系统管理员重置',
      '忘记密码',
      {
        confirmButtonText: '知道了',
        type: 'warning'
      }
    )
  } else {
    // 这里可以实现用户忘记密码的功能，比如发送重置邮件
    ElMessageBox.alert(
      '忘记密码功能开发中，请联系客服协助',
      '忘记密码',
      {
        confirmButtonText: '知道了',
        type: 'info'
      }
    )
  }
}

// 页面加载时根据URL参数设置登录类型
onMounted(() => {
  const type = route.query.type as string
  if (type === 'admin') {
    loginType.value = 'admin'
    showTips.value = true
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%),
              url('http://localhost:5000/static/images/login-bg.jpg') center center / cover no-repeat;
  background-attachment: fixed;
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.5) 100%);
  pointer-events: none;
}

.login-card {
  width: 420px;
  box-shadow: var(--shadow-xl);
  border-radius: var(--radius-xl);
  overflow: hidden;
  backdrop-filter: blur(20px);
  background: var(--bg-glass);
  border: 1px solid var(--border-light);
  position: relative;
  z-index: 1;
}

.card-header {
  text-align: center;
  padding: 32px 24px 24px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
}

.card-header h2 {
  margin: 0 0 8px 0;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: var(--text-3xl);
  font-weight: 700;
  letter-spacing: -0.02em;
}

.card-header .subtitle {
  margin: 0;
  color: var(--text-tertiary);
  font-size: var(--text-base);
}

/* 登录类型选择器 */
.login-type-selector {
  margin: 24px 20px 0;
}

.type-group {
  display: flex;
  width: 100%;
  justify-content: center;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-secondary);
  padding: 4px;
  gap: 4px;
}

.type-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  cursor: pointer;
}

.type-btn:hover {
  background: var(--bg-hover);
  color: var(--accent-primary);
}

.type-btn.active {
  background: var(--accent-gradient);
  color: var(--text-inverse);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35);
}

.type-btn .el-icon {
  font-size: 18px;
}

/* 登录表单 */
.login-form {
  padding: 24px 24px 32px;
}

.login-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
}

.login-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  border: 1px solid var(--border-light);
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: var(--border-color);
  box-shadow: var(--shadow-md);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.login-form :deep(.el-input__inner) {
  font-size: var(--text-base);
  height: 44px;
  line-height: 44px;
}

.login-form :deep(.el-form-item__error) {
  font-size: var(--text-xs);
  padding-top: 4px;
}

.admin-notice {
  margin-bottom: 20px;
}

.admin-notice :deep(.el-alert__content) {
  font-size: var(--text-sm);
  line-height: 1.5;
}

/* 登录按钮 */
.login-form :deep(.el-button--primary) {
  background: var(--accent-gradient);
  border: none;
  height: 48px;
  font-size: var(--text-base);
  font-weight: 600;
  border-radius: var(--radius-md);
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35);
  transition: all var(--transition-base);
}

.login-form :deep(.el-button--primary:hover) {
  background: var(--accent-gradient-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.45);
}

/* 底部链接 */
.login-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
  padding: 0 24px;
}

.register-link,
.forgot-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--text-sm);
  transition: all var(--transition-base);
}

.register-link:hover {
  color: var(--accent-primary);
  text-decoration: none;
}

.forgot-link:hover {
  color: var(--accent-primary);
}

.separator {
  color: var(--border-color);
  font-size: var(--text-sm);
}

/* 登录提示 */
.login-tips {
  width: 100%;
  max-width: 420px;
  margin-top: 20px;
}

.login-tips :deep(.el-alert) {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.login-tips :deep(.el-alert__content p) {
  margin: 0;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card {
  animation: fadeIn 0.5s ease-out;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: 20px 16px;
  }

  .login-card {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
  }

  .card-header h2 {
    font-size: 24px;
  }

  .card-header .subtitle {
    font-size: 14px;
  }

  .type-btn {
    padding: 10px 16px;
    font-size: 14px;
  }

  .type-btn .el-icon {
    font-size: 16px;
  }

  .type-btn span {
    font-size: 14px;
  }

  .login-form {
    padding: 0 16px;
  }

  .login-footer {
    padding: 0 16px;
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 16px 12px;
    min-height: 100vh; /* 移动端也全屏显示 */
  }

  .login-card {
    width: 100%;
    max-width: 320px;
  }

  .card-header {
    padding-bottom: 16px;
  }

  .card-header h2 {
    font-size: 22px;
  }

  .card-header .subtitle {
    font-size: 13px;
  }

  .login-form :deep(.el-input__inner) {
    font-size: 15px;
    height: 44px;
    line-height: 44px;
  }

  .el-button {
    height: 44px;
    font-size: 15px;
  }
}

/* Element Plus 样式优化 */
:deep(.el-card__header) {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 2px solid #f0f2f5;
}

:deep(.el-radio-button__inner) {
  padding: 0;
}

:deep(.el-radio-button__original-radio) {
  display: none;
}

:deep(.el-radio-button) {
  margin-right: 0;
  border: 1px solid transparent;
  background: transparent;
  border-radius: 6px;
  transition: all 0.3s ease;
}

:deep(.el-radio-button:hover) {
  border-color: #c0c4cc;
}

:deep(.el-radio-button.is-active) {
  background: #409eff;
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}
</style>
