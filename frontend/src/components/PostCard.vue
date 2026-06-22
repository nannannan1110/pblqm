<template>
  <div class="post-card">
    <div class="post-header">
      <div class="post-author">
        <el-avatar :size="40" :src="post.author?.avatar">
          {{ post.author?.username?.charAt(0).toUpperCase() }}
        </el-avatar>
        <div class="author-info">
          <span class="author-name">{{ post.author?.username }}</span>
          <span class="post-time">{{ formatTime(post.created_at) }}</span>
        </div>
      </div>
      <el-dropdown v-if="isOwner" trigger="click">
        <el-button text><el-icon><MoreFilled /></el-icon></el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleEdit">Edit</el-dropdown-item>
            <el-dropdown-item @click="handleDelete" divided>Delete</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <h3 class="post-title">{{ post.title }}</h3>
    <p class="post-content">{{ post.content }}</p>

    <div v-if="post.image" class="post-image">
      <el-image 
        :src="getImageUrl(post.image)" 
        fit="cover"
        :preview-src-list="[getImageUrl(post.image)]"
        :initial-index="0"
      />
    </div>

    <div class="post-actions">
      <div class="action-item" @click="handleLike">
        <el-icon :color="isLiked ? '#409EFF' : '#999'" :size="20">
          <StarFilled />
        </el-icon>
        <span>{{ post.likes_count }}</span>
      </div>
      <div class="action-item" @click="showComments = !showComments">
        <el-icon :size="20"><ChatLineSquare /></el-icon>
        <span>{{ post.comments_count }}</span>
      </div>
    </div>

    <!-- Comments Section -->
    <div v-if="showComments" class="comments-section">
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <el-avatar :size="32" :src="comment.author?.avatar">
            {{ comment.author?.username?.charAt(0).toUpperCase() }}
          </el-avatar>
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author?.username }}</span>
              <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
            </div>
            <p class="comment-text">{{ comment.content }}</p>
          </div>
          <el-button 
            v-if="comment.user_id === currentUserId" 
            text 
            type="danger"
            size="small"
            @click="handleDeleteComment(comment.id)"
          >
            Delete
          </el-button>
        </div>
        <div v-if="comments.length === 0" class="no-comments">
          No comments yet, be the first to comment!
        </div>
      </div>

      <div class="comment-input">
        <el-input
          v-model="newComment"
          placeholder="Write your comment..."
          size="small"
        />
        <el-button type="primary" size="small" @click="handleAddComment" :loading="submitting">
          Send
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { StarFilled, ChatLineSquare, MoreFilled } from '@element-plus/icons-vue'
import { getPostComments, addPostComment, deletePostComment, togglePostLike } from '@/api/posts'
import { authApi } from '@/api/auth'

interface Post {
  id: number
  user_id: number
  title: string
  content: string
  image?: string
  created_at: string
  updated_at: string
  likes_count: number
  comments_count: number
  author: {
    id: number
    username: string
    avatar?: string
  }
}

interface PostComment {
  id: number
  user_id: number
  post_id: number
  content: string
  created_at: string
  author: {
    id: number
    username: string
    avatar?: string
  }
}

const props = defineProps<{
  post: Post
}>()

const emit = defineEmits<{
  (e: 'update'): void
}>()

const comments = ref<PostComment[]>([])
const showComments = ref(false)
const newComment = ref('')
const submitting = ref(false)
const likedPosts = ref<Set<number>>(new Set())

const currentUserId = computed(() => {
  const user = authApi.getCurrentUser()
  return user?.id
})

const isOwner = computed(() => {
  return currentUserId.value === props.post.user_id
})

const isLiked = computed(() => {
  return likedPosts.value.has(props.post.id)
})

const getImageUrl = (image: string) => {
  if (!image) return ''
  if (image.startsWith('http')) return image
  return `http://localhost:5000/static/uploads/images/${image}`
}

const formatTime = (time: string) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes} min ago`
  if (hours < 24) return `${hours} hours ago`
  if (days < 7) return `${days} days ago`
  
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const loadComments = async () => {
  try {
    const response = await getPostComments(props.post.id)
    comments.value = response.comments || []
  } catch (error) {
    console.error('Failed to load comments:', error)
  }
}

const handleLike = async () => {
  try {
    const response = await togglePostLike(props.post.id)
    emit('update')
    
    // Update local like status
    if (isLiked.value) {
      likedPosts.value.delete(props.post.id)
    } else {
      likedPosts.value.add(props.post.id)
    }
  } catch (error) {
    ElMessage.error('Operation failed, please login first')
  }
}

const handleAddComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('Please enter comment content')
    return
  }

  submitting.value = true
  try {
    await addPostComment(props.post.id, newComment.value.trim())
    newComment.value = ''
    await loadComments()
    emit('update')
    ElMessage.success('Comment posted successfully')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.error || 'Failed to post comment')
  } finally {
    submitting.value = false
  }
}

const handleDeleteComment = async (commentId: number) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this comment?', 'Confirm', {
      confirmButtonText: 'Confirm',
      cancelButtonText: 'Cancel',
      type: 'warning'
    })
    
    await deletePostComment(props.post.id, commentId)
    await loadComments()
    emit('update')
    ElMessage.success('Comment deleted')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.error || 'Failed to delete comment')
    }
  }
}

const handleEdit = () => {
  emit('update')
}

const handleDelete = async () => {
  emit('update')
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.post-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.post-time {
  font-size: 12px;
  color: #999;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.post-content {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 12px 0;
}

.post-image {
  margin-bottom: 12px;
  border-radius: 8px;
  overflow: hidden;
}

.post-image .el-image {
  width: 100%;
  max-height: 400px;
}

.post-actions {
  display: flex;
  gap: 24px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #666;
  font-size: 14px;
}

.action-item:hover {
  color: #409EFF;
}

.comments-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.comments-list {
  margin-bottom: 12px;
}

.comment-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.comment-author {
  font-weight: 600;
  font-size: 13px;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-text {
  margin: 0;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

.no-comments {
  text-align: center;
  color: #999;
  padding: 20px 0;
  font-size: 14px;
}

.comment-input {
  display: flex;
  gap: 8px;
}

.comment-input .el-input {
  flex: 1;
}
</style>
