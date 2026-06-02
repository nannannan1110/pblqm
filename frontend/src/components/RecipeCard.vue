<template>
  <div class="recipe-card" @click="handleClick">
    <div class="card-image-wrapper">
      <img :src="imageUrl" :alt="recipe.title" class="card-image" />
      <div class="card-overlay">
        <el-button type="primary" size="small" class="view-btn">
          <el-icon><View /></el-icon>
          查看详情
        </el-button>
      </div>
      <div class="difficulty-badge" :class="difficultyClass">
        {{ recipe.difficulty || '未知' }}
      </div>
      <button
        class="favorite-btn"
        :class="{ active: isFavorite }"
        @click.stop="handleToggleFavorite"
      >
        <el-icon><HeartFilled v-if="isFavorite" /><Heart v-else /></el-icon>
      </button>
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ recipe.title }}</h3>
      <p class="card-desc">{{ recipe.description || '暂无描述' }}</p>
      <div class="card-meta">
        <div class="meta-item">
          <el-icon><Timer /></el-icon>
          <span>{{ totalTime }}</span>
        </div>
        <div class="meta-item">
          <el-icon><User /></el-icon>
          <span>{{ recipe.servings || 1 }}人份</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { View, HeartFilled, Heart, Timer, User } from '@element-plus/icons-vue'

interface Props {
  recipe: any
  isFavorite?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isFavorite: false
})

const emit = defineEmits(['click', 'toggle-favorite'])

const imageUrl = computed(() => {
  if (!props.recipe.image) {
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2Y1ZjVmNSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTUwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48L3N2Zz4='
  }
  if (props.recipe.image.startsWith('http')) return props.recipe.image
  return `http://localhost:5000/static/uploads/images/${props.recipe.image}`
})

const totalTime = computed(() => {
  const total = (props.recipe.prep_time || 0) + (props.recipe.cook_time || 0)
  if (total < 60) return `${total}分钟`
  const hours = Math.floor(total / 60)
  const mins = total % 60
  return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
})

const difficultyClass = computed(() => {
  switch (props.recipe.difficulty) {
    case '简单': return 'easy'
    case '中等': return 'medium'
    case '困难': return 'hard'
    default: return 'unknown'
  }
})

const handleClick = () => {
  emit('click', props.recipe)
}

const handleToggleFavorite = () => {
  emit('toggle-favorite', props.recipe)
}
</script>

<style scoped>
.recipe-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.recipe-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
}

.card-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.recipe-card:hover .card-image {
  transform: scale(1.1);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.7) 100%);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 20px;
  opacity: 0;
  transition: opacity var(--transition-base);
}

.recipe-card:hover .card-overlay {
  opacity: 1;
}

.view-btn {
  border: none;
}

.difficulty-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  backdrop-filter: blur(8px);
  box-shadow: var(--shadow-sm);
}

.difficulty-badge.easy {
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.95), rgba(76, 175, 80, 0.95));
}

.difficulty-badge.medium {
  background: linear-gradient(135deg, rgba(230, 162, 60, 0.95), rgba(255, 152, 0, 0.95));
}

.difficulty-badge.hard {
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.95), rgba(244, 67, 54, 0.95));
}

.difficulty-badge.unknown {
  background: linear-gradient(135deg, rgba(144, 147, 153, 0.95), rgba(158, 158, 158, 0.95));
}

.favorite-btn {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.favorite-btn:hover {
  transform: scale(1.1);
}

.favorite-btn.active {
  background: linear-gradient(135deg, #f56c6c, #f093fb);
  color: white;
}

.favorite-btn .el-icon {
  font-size: 18px;
}

.card-content {
  padding: 18px;
}

.card-title {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-base);
}

.recipe-card:hover .card-title {
  color: var(--accent-primary);
}

.card-desc {
  margin: 0 0 14px 0;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.card-meta {
  display: flex;
  gap: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--border-light);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-tertiary);
}

.meta-item .el-icon {
  font-size: 15px;
}

@media (max-width: 768px) {
  .card-image-wrapper {
    height: 160px;
  }
  
  .card-content {
    padding: 14px;
  }
  
  .card-title {
    font-size: 15px;
  }
}
</style>
