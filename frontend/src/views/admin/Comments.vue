<template>
  <div class="admin-comments">
    <div class="page-header">
      <h2>评论管理</h2>
      <p>管理用户评论</p>
    </div>

    <el-card v-loading="loading">
      <el-table :data="comments" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="content" label="评论内容" show-overflow-tooltip />
        <el-table-column prop="user.username" label="评论者" width="120" />
        <el-table-column prop="rating" label="评分" width="100">
          <template #default="scope">
            <el-rate v-model="scope.row.rating" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewComment(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteComment(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="pagination.total > 0"
        @current-change="handlePageChange"
        :current-page="pagination.currentPage"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, prev, pager, next"
        style="margin-top: 20px; justify-content: center"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api/index'

const loading = ref(false)
const comments = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 获取评论列表
const fetchComments = async (page = 1) => {
  loading.value = true
  try {
    const data = await api.get('/admin/comments', {
      params: {
        page: page,
        per_page: pagination.value.pageSize
      }
    })

    if (data) {
      comments.value = data.comments
      pagination.value.total = data.total
      pagination.value.currentPage = data.current_page
    }
  } catch (error: any) {
    console.error('获取评论列表失败:', error)
    ElMessage.error('获取评论列表失败')
  } finally {
    loading.value = false
  }
}

// 处理分页
const handlePageChange = (page: number) => {
  fetchComments(page)
}

// 查看评论
const viewComment = (comment: any) => {
  ElMessageBox.alert(
    `
    <div style="text-align: left;">
      <p><strong>评论者:</strong> ${comment.user?.username || '未知'}</p>
      <p><strong>评分:</strong> ${comment.rating || 5}分</p>
      <p><strong>内容:</strong></p>
      <p>${comment.content}</p>
      <p><strong>时间:</strong> ${formatDate(comment.created_at)}</p>
    </div>
    `,
    '评论详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭'
    }
  )
}

// 删除评论
const deleteComment = async (comment: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
  } catch (error: any) {
    // 用户取消操作，静默返回
    return
  }

  try {
    await api.delete(`/comments/${comment.id}`)
    ElMessage.success('删除成功')
    fetchComments(pagination.value.currentPage)
  } catch (error: any) {
    console.error('删除评论失败:', error)
    ElMessage.error('删除评论失败')
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.admin-comments {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
}
</style>
