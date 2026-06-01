<template>
  <div class="edit-recipe" v-loading="loading">
    <el-card class="edit-card" v-if="recipeForm">
      <template #header>
        <div class="card-header">
          <h2>编辑菜谱</h2>
          <p>修改和完善你的菜谱内容</p>
        </div>
      </template>

      <!-- 粘贴区域 -->
      <el-card class="paste-section" shadow="never">
        <div class="paste-header">
          <span class="paste-title">📝 智能识别粘贴</span>
          <span class="paste-hint">粘贴菜谱内容，系统将自动识别并填充</span>
        </div>
        <el-input
          v-model="pasteText"
          type="textarea"
          :rows="6"
          placeholder="在此粘贴您的菜谱内容，例如：&#10;菜名：红烧肉&#10;食材：五花肉 500g，冰糖 30g...&#10;做法：1. 五花肉切块..."
          @paste="handlePaste"
          @input="handlePasteInput"
        />
        <el-button 
          type="primary" 
          class="parse-btn" 
          :disabled="!pasteText.trim()"
          @click="parseAndFill"
        >
          智能识别并填充
        </el-button>
        <div class="paste-tips">
          <el-text size="small" type="info">
            提示：粘贴后点击按钮，系统将自动识别菜名、食材、做法等信息
          </el-text>
        </div>
      </el-card>

      <el-divider />

      <el-form
        ref="recipeFormRef"
        :model="recipeForm"
        :rules="recipeRules"
        label-width="100px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="菜谱标题" prop="title">
          <el-input
            v-model="recipeForm.title"
            placeholder="请输入菜谱标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="菜谱描述" prop="description">
          <el-input
            v-model="recipeForm.description"
            type="textarea"
            :rows="3"
            placeholder="请简单描述这道菜的特色和口感"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="准备时间" prop="prep_time">
              <el-input-number
                v-model="recipeForm.prep_time"
                :min="0"
                :max="999"
                placeholder="分钟"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="烹饪时间" prop="cook_time">
              <el-input-number
                v-model="recipeForm.cook_time"
                :min="0"
                :max="999"
                placeholder="分钟"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="份量" prop="servings">
              <el-input-number
                v-model="recipeForm.servings"
                :min="1"
                :max="50"
                placeholder="人份"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="难度等级" prop="difficulty">
              <el-select
                v-model="recipeForm.difficulty"
                placeholder="请选择难度"
                style="width: 100%"
              >
                <el-option
                  v-for="difficulty in difficultyOptions"
                  :key="difficulty.value"
                  :label="difficulty.label"
                  :value="difficulty.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜谱图片">
              <el-upload
                class="image-uploader"
                :show-file-list="false"
                :before-upload="beforeImageUpload"
                :on-success="handleImageSuccess"
                :on-error="handleImageError"
                action=""
                :http-request="customUpload"
              >
                <img v-if="imageUrl" :src="imageUrl" class="uploaded-image" />
                <el-icon v-else class="image-uploader-icon"><Plus /></el-icon>
              </el-upload>
              <div v-if="uploading" class="uploading-text">上传中...</div>
              <el-button
                v-if="recipeForm.image"
                type="danger"
                size="small"
                text
                @click="removeImage"
                style="margin-top: 8px;"
              >
                移除图片
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="食材清单" prop="ingredients">
          <el-input
            v-model="recipeForm.ingredients"
            type="textarea"
            :rows="6"
            placeholder="请输入所需食材和用量"
          />
          <div class="form-help">
            请每行填写一种食材，包含用量
          </div>
        </el-form-item>

        <el-form-item label="制作步骤" prop="instructions">
          <el-input
            v-model="recipeForm.instructions"
            type="textarea"
            :rows="10"
            placeholder="请详细描述制作步骤"
          />
          <div class="form-help">
            请按顺序描述制作步骤，步骤要清晰明了
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="submitting"
            @click="handleSubmit"
          >
            保存修改
          </el-button>
          <el-button
            size="large"
            @click="handleCancel"
          >
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, FormInstance } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { recipeApi, type RecipeRequest, DIFFICULTY_OPTIONS } from '@/api/recipes'
import { uploadApi } from '@/api/uploads'
import { parseRecipeText } from '@/utils/recipeParser'

const router = useRouter()
const route = useRoute()
const recipeFormRef = ref<FormInstance>()
const loading = ref(false)
const submitting = ref(false)
const uploading = ref(false)
const imageUrl = ref('')
const pasteText = ref('')

// 表单数据
const recipeForm = ref<RecipeRequest | null>(null)

const difficultyOptions = DIFFICULTY_OPTIONS

// 表单验证规则
const recipeRules = {
  title: [
    { required: true, message: '请输入菜谱标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度在2到100个字符之间', trigger: 'blur' }
  ],
  description: [
    { max: 500, message: '描述不能超过500个字符', trigger: 'blur' }
  ],
  ingredients: [
    { required: true, message: '请输入食材清单', trigger: 'blur' },
    { min: 10, message: '食材信息不能太少', trigger: 'blur' }
  ],
  instructions: [
    { required: true, message: '请输入制作步骤', trigger: 'blur' },
    { min: 20, message: '制作步骤不能太少', trigger: 'blur' }
  ],
  difficulty: [
    { required: true, message: '请选择难度等级', trigger: 'change' }
  ]
}

// 获取菜谱详情
const fetchRecipe = async () => {
  try {
    loading.value = true
    const recipeId = Number(route.params.id)
    const recipe = await recipeApi.getRecipe(recipeId)

    recipeForm.value = {
      title: recipe.title,
      description: recipe.description || '',
      ingredients: recipe.ingredients,
      instructions: recipe.instructions,
      prep_time: recipe.prep_time,
      cook_time: recipe.cook_time,
      difficulty: recipe.difficulty || '',
      servings: recipe.servings || 1,
      image: recipe.image || ''
    }

    // 设置当前图片URL
    if (recipeForm.value.image) {
      imageUrl.value = recipeForm.value.image
    }

  } catch (error: any) {
    console.error('获取菜谱详情失败:', error)
    ElMessage.error('获取菜谱详情失败')
    router.push('/recipes')
  } finally {
    loading.value = false
  }
}

// 图片上传前检查
const beforeImageUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt16M = file.size / 1024 / 1024 < 16

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt16M) {
    ElMessage.error('图片大小不能超过16MB!')
    return false
  }
  return true
}

// 自定义上传
const customUpload = async (options: any) => {
  const { file, onSuccess, onError } = options

  try {
    uploading.value = true
    const response = await uploadApi.uploadImage(file)

    // 设置图片URL
    if (recipeForm.value) {
      // 直接使用后端返回的url（相对路径）
      recipeForm.value.image = response.url
      // 用于预显示，拼接完整URL
      imageUrl.value = uploadApi.getImageUrl(response.filename)

      console.log('图片上传成功，保存路径:', recipeForm.value.image)
      console.log('预览URL:', imageUrl.value)
    }

    ElMessage.success('图片上传成功!')
    onSuccess(response)
  } catch (error: any) {
    ElMessage.error('图片上传失败: ' + (error.response?.data?.error || '网络错误'))
    onError(error)
  } finally {
    uploading.value = false
  }
}

// 图片上传成功
const handleImageSuccess = (response: any) => {
  console.log('图片上传成功:', response)
}

// 图片上传失败
const handleImageError = (error: any) => {
  console.error('图片上传失败:', error)
}

// 移除图片
const removeImage = () => {
  if (recipeForm.value) {
    recipeForm.value.image = ''
    imageUrl.value = ''
    ElMessage.success('图片已移除')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!recipeFormRef.value || !recipeForm.value) return

  try {
    const valid = await recipeFormRef.value.validate()
    if (!valid) return

    submitting.value = true

    const recipeId = Number(route.params.id)
    await recipeApi.updateRecipe(recipeId, recipeForm.value)

    ElMessage.success('菜谱更新成功!')
    router.push(`/recipes/${recipeId}`)

  } catch (error: any) {
    console.error('更新菜谱失败:', error)
    ElMessage.error('更新菜谱失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

// 处理粘贴事件
const handlePaste = (event: ClipboardEvent) => {
  // 可以在这里添加额外的处理，比如清理粘贴的格式
}

// 处理粘贴输入
const handlePasteInput = () => {
  // 实时输入时不做处理，等用户点击按钮再识别
}

// 智能解析并填充
const parseAndFill = () => {
  if (!pasteText.value.trim()) {
    ElMessage.warning('请先粘贴菜谱内容')
    return
  }

  if (!recipeForm.value) {
    ElMessage.error('表单加载中，请稍后')
    return
  }

  try {
    const parsed = parseRecipeText(pasteText.value)
    
    // 填充表单
    if (parsed.title) {
      recipeForm.value.title = parsed.title
    }
    if (parsed.description) {
      recipeForm.value.description = parsed.description
    }
    if (parsed.ingredients) {
      recipeForm.value.ingredients = parsed.ingredients
    }
    if (parsed.instructions) {
      recipeForm.value.instructions = parsed.instructions
    }
    if (parsed.prep_time !== undefined) {
      recipeForm.value.prep_time = parsed.prep_time
    }
    if (parsed.cook_time !== undefined) {
      recipeForm.value.cook_time = parsed.cook_time
    }
    if (parsed.servings !== undefined) {
      recipeForm.value.servings = parsed.servings
    }
    if (parsed.difficulty) {
      recipeForm.value.difficulty = parsed.difficulty
    }

    ElMessage.success('智能识别成功！请检查和完善内容')
  } catch (error) {
    console.error('解析失败:', error)
    ElMessage.error('解析失败，请手动填写')
  }
}

// 取消编辑
const handleCancel = () => {
  router.back()
}

// 页面加载时获取数据
onMounted(() => {
  fetchRecipe()
})
</script>

<style scoped>
.edit-recipe {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.paste-section {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  border: 2px dashed #d1d5db;
}

.paste-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.paste-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.paste-hint {
  font-size: 13px;
  color: #6b7280;
}

.parse-btn {
  margin-top: 12px;
  width: 100%;
}

.paste-tips {
  margin-top: 12px;
}


.edit-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
  font-weight: 600;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.image-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

.image-uploader:hover {
  border-color: #409eff;
}

.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.uploaded-image {
  width: 178px;
  height: 178px;
  object-fit: cover;
  display: block;
}

.uploading-text {
  text-align: center;
  color: #409eff;
  font-size: 14px;
  margin-top: 8px;
}

.form-help {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .edit-recipe {
    padding: 16px 10px;
  }

  .edit-card {
    margin: 0;
  }
}
</style>