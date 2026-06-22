<template>
  <div class="home">
    <div class="hero-section">
      <h1 class="animate-fade-in-up">菜谱分享系统</h1>
      <p class="animate-fade-in-up animate-delay-1">发现美味，分享快乐</p>
      <div class="action-buttons animate-fade-in-up animate-delay-2">
        <el-button type="primary" size="large" class="hero-btn animate-btn" @click="$router.push('/recipes')">
          <el-icon><Search /></el-icon>
          浏览菜谱
        </el-button>
        <el-button size="large" class="hero-btn animate-btn" v-if="authApi.isLoggedIn()" @click="$router.push('/create-recipe')">
          <el-icon><Plus /></el-icon>
          创建菜谱
        </el-button>
      </div>
      <div class="decoration">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { authApi } from '@/api/auth'
import { Search, Plus } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Home',
  components: { Search, Plus },
  setup() {
    return {
      authApi
    }
  }
})
</script>

<style scoped>
.home {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.hero-section {
  text-align: center;
  z-index: 10;
  position: relative;
}

/* 动画关键帧 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) both;
}

.animate-delay-1 {
  animation-delay: 0.15s;
}

.animate-delay-2 {
  animation-delay: 0.3s;
}

.hero-section h1 {
  font-size: 64px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 24px 0;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.hero-section p {
  font-size: 24px;
  color: var(--text-secondary);
  margin: 0 0 48px 0;
  line-height: 1.6;
  font-weight: 400;
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 16px 40px;
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  letter-spacing: 0.3px;
}

.hero-btn:first-child {
  background: var(--accent-gradient);
  border: none;
  color: white;
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
}

.hero-btn:first-child:hover {
  background: var(--accent-gradient-hover);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
}

/* 装饰性背景 */
.decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: -1;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  animation: float 10s ease-in-out infinite;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -150px;
  right: -150px;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  bottom: -120px;
  left: -120px;
  animation-delay: -3s;
}

.blob-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: 30%;
  right: 10%;
  animation-delay: -5s;
}

/* 按钮动画类（与App.vue一致） */
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
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(64, 158, 255, 0.4);
}

.animate-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(64, 158, 255, 0.3);
}

@media (max-width: 768px) {
  .home {
    padding: 40px 16px;
  }

  .hero-section h1 {
    font-size: 38px;
  }

  .hero-section p {
    font-size: 18px;
    margin-bottom: 28px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .action-buttons .el-button {
    width: 100%;
    max-width: 280px;
  }

  .blob-1 {
    width: 250px;
    height: 250px;
  }

  .blob-2 {
    width: 200px;
    height: 200px;
  }

  .blob-3 {
    width: 160px;
    height: 160px;
  }
}
</style>
