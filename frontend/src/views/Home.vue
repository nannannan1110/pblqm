<template>
  <div class="home">
    <div class="hero-section">
      <h1>菜谱分享系统</h1>
      <p>发现美味，分享快乐</p>
      <div class="action-buttons">
        <el-button type="primary" size="large" @click="$router.push('/recipes')">
          浏览菜谱
        </el-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { authApi } from '@/api/auth'

export default defineComponent({
  name: 'Home',
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
}

.hero-section {
  text-align: center;
}

.hero-section h1 {
  font-size: 48px;
  font-weight: 700;
  color: #303133;
  margin: 0 0 16px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-section p {
  font-size: 20px;
  color: #606266;
  margin: 0 0 32px 0;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .home {
    padding: 40px 16px;
  }

  .hero-section h1 {
    font-size: 36px;
  }

  .hero-section p {
    font-size: 18px;
    margin-bottom: 24px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .action-buttons .el-button {
    width: 200px;
  }
}
</style>
