<template>
  <div class="discovery-page">
    <div class="page-header">
      <h1>发现页</h1>
      <p class="subtitle">分享你的厨艺，展示你的美食作品</p>
    </div>

    <!-- 发帖区域 -->
    <div class="create-post-card">
      <div class="post-input-header">
        <el-avatar :size="40" :src="currentUser?.avatar">
          {{ currentUser?.username?.charAt(0).toUpperCase() }}
        </el-avatar>
        <el-button type="primary" @click="showPostDialog = true">
          <el-icon><Plus /></el-icon>
          发布帖子
        </el-button>
      </div>
    </div>

    <!-- 帖子列表 -->
    <div class="posts-list">
      <PostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        @update="loadPosts"
      />
      
      <div v-if="posts.length === 0" class="empty-state">
        <el-empty description="暂无帖子，快来分享你的厨艺吧！">
          <el-button type="primary" @click="showPostDialog = true">发布帖子</el-button>
        </el-empty>
      </div>

      <!-- 加载更多 -->
      <div v-if="posts.length > 0 && hasMore" class="load-more">
        <el-button @click="loadMore" :loading="loadingMore">加载更多</el-button>
      </div>
    </div>

    <!-- 发帖对话框 -->
    <el-dialog
      v-model="showPostDialog"
      title="发布帖子"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="postForm" :rules="postRules" ref="postFormRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input 
            v-model="postForm.title" 
            placeholder="给你的帖子起个标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="postForm.content"
            type="textarea"
            :rows="6"
            placeholder="分享你的烹饪心得和美食故事..."
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="图片">
          <el-upload
            action="#"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleImageChange"
            accept="image/*"
          >
            <el-button v-if="!postForm.image" type="primary" plain>
              <el-icon><Upload /></el-icon>
              选择图片
            </el-button>
            <div v-else class="image-preview">
              <el-image :src="previewImage" fit="cover" />
              <el-button type="danger" circle @click.stop="removeImage">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showPostDialog = false">取消</el-button>
        <el-button type="primary" @click="submitPost" :loading="submitting">
          发布
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Upload, Delete } from '@element-plus/icons-vue'
import PostCard from '@/components/PostCard.vue'
import { getPosts, createPost } from '@/api/posts'
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

const posts = ref<Post[]>([])
const currentPage = ref(1)
const totalPages = ref(1)
const loadingMore = ref(false)
const showPostDialog = ref(false)
const submitting = ref(false)
const postFormRef = ref()

const postForm = ref({
  title: '',
  content: '',
  image: null as File | null
})

const postRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const currentUser = computed(() => authApi.getCurrentUser())

const hasMore = computed(() => currentPage.value < totalPages.value)

const previewImage = computed(() => {
  if (postForm.value.image) {
    return URL.createObjectURL(postForm.value.image)
  }
  return ''
})

const handleImageChange = (file: any) => {
  postForm.value.image = file.raw
}

const removeImage = () => {
  postForm.value.image = null
}

const loadPosts = async () => {
  try {
    const response = await getPosts(currentPage.value, 10)
    posts.value = response.posts || []
    totalPages.value = Math.ceil((response.total || 0) / 10) || 1
  } catch (error) {
    console.error('Failed to load posts:', error)
    ElMessage.error('加载帖子失败')
  }
}

const loadMore = async () => {
  if (!hasMore.value || loadingMore.value) return
  
  loadingMore.value = true
  currentPage.value++
  
  try {
    const response = await getPosts(currentPage.value, 10)
    posts.value = [...posts.value, ...(response.posts || [])]
    totalPages.value = Math.ceil((response.total || 0) / 10) || 1
  } catch (error) {
    console.error('Failed to load more posts:', error)
    currentPage.value--
    ElMessage.error('加载更多失败')
  } finally {
    loadingMore.value = false
  }
}

const submitPost = async () => {
  if (!postFormRef.value) return
  
  await postFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    
    submitting.value = true
    try {
      await createPost({
        title: postForm.value.title,
        content: postForm.value.content,
        image: postForm.value.image || undefined
      })
      
      ElMessage.success('发布成功！')
      showPostDialog.value = false
      postForm.value = { title: '', content: '', image: null }
      currentPage.value = 1
      await loadPosts()
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || '发布失败')
    } finally {
      submitting.value = false
    }
  })
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.discovery-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  color: #333;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #999;
  font-size: 16px;
  margin: 0;
}

.create-post-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.post-input-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.posts-list {
  min-height: 400px;
}

.empty-state {
  padding: 60px 0;
}

.load-more {
  text-align: center;
  padding: 20px 0;
}

.image-preview {
  position: relative;
  width: 200px;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
}

.image-preview .el-image {
  width: 100%;
  height: 100%;
}

.image-preview .el-button {
  position: absolute;
  top: 8px;
  right: 8px;
}
</style>
