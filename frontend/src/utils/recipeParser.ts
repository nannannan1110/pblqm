export interface ParsedRecipe {
  title: string
  description: string
  ingredients: string
  instructions: string
  prep_time?: number
  cook_time?: number
  servings?: number
  difficulty?: string
}

// 智能解析菜谱文本
export function parseRecipeText(text: string): ParsedRecipe {
  const result: ParsedRecipe = {
    title: '',
    description: '',
    ingredients: '',
    instructions: ''
  }

  // 规范化换行符
  const normalizedText = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n')
  const lines = normalizedText.split('\n').filter(line => line.trim())

  // 常见关键词
  const titleKeywords = ['菜名', '菜名', '菜谱名', '名称', '题目', '标题']
  const ingredientKeywords = ['食材', '材料', '原料', '配料', '主料', '辅料', '调料']
  const instructionKeywords = ['做法', '步骤', '制作', '方法', '烹饪', '流程']
  const descriptionKeywords = ['简介', '介绍', '特色', '描述', '说明']
  const timeKeywords = ['时间', '准备', '烹饪', '分钟', 'min']
  const servingsKeywords = ['份量', '人数', '份', '人', '人份']
  const difficultyKeywords = ['难度', '难易', '程度']

  // 模式1：按标签分区
  let currentSection = 'title'
  let titleFound = false
  let ingredientsContent: string[] = []
  let instructionsContent: string[] = []
  let descriptionContent: string[] = []
  let otherContent: string[] = []

  for (let line of lines) {
    const trimmedLine = line.trim()
    const lowerLine = trimmedLine.toLowerCase()

    // 检查是否是新的分区标签
    let isNewSection = false

    // 标题检测
    if (!titleFound && !isNewSection) {
      for (const keyword of titleKeywords) {
        if (lowerLine.includes(keyword) && lowerLine.length < 20) {
          // 提取标题：冒号后面的部分，或者整个行
          const titleMatch = trimmedLine.match(/[:：]\s*(.+)/)
          if (titleMatch) {
            result.title = titleMatch[1].trim()
          } else {
            // 下一行可能是标题
            titleFound = true
            currentSection = 'title-next'
          }
          isNewSection = true
          break
        }
      }
    }

    // 食材检测
    if (!isNewSection) {
      for (const keyword of ingredientKeywords) {
        if (lowerLine.includes(keyword) && lowerLine.length < 20) {
          currentSection = 'ingredients'
          isNewSection = true
          break
        }
      }
    }

    // 做法检测
    if (!isNewSection) {
      for (const keyword of instructionKeywords) {
        if (lowerLine.includes(keyword) && lowerLine.length < 20) {
          currentSection = 'instructions'
          isNewSection = true
          break
        }
      }
    }

    // 简介检测
    if (!isNewSection) {
      for (const keyword of descriptionKeywords) {
        if (lowerLine.includes(keyword) && lowerLine.length < 20) {
          currentSection = 'description'
          isNewSection = true
          break
        }
      }
    }

    // 处理当前行内容
    if (!isNewSection) {
      if (currentSection === 'title-next' && !result.title) {
        result.title = trimmedLine
        titleFound = true
        currentSection = 'other'
      } else if (currentSection === 'ingredients') {
        ingredientsContent.push(trimmedLine)
      } else if (currentSection === 'instructions') {
        instructionsContent.push(trimmedLine)
      } else if (currentSection === 'description') {
        descriptionContent.push(trimmedLine)
      } else if (!titleFound && trimmedLine.length > 0 && trimmedLine.length < 50) {
        // 如果没有找到明确标签，第一行非空短文本可能是标题
        result.title = trimmedLine
        titleFound = true
      } else {
        otherContent.push(trimmedLine)
      }
    }
  }

  // 模式2：如果没有找到明确分区，尝试自动识别
  if (ingredientsContent.length === 0 && instructionsContent.length === 0 && otherContent.length > 0) {
    let stepLineStart = -1
    
    // 查找带有序号的行（1. 2. 或 一、二、）
    for (let i = 0; i < otherContent.length; i++) {
      const line = otherContent[i]
      if (/^\s*(\d+[.、]|[一二三四五六七八九十]+[.、])/.test(line)) {
        stepLineStart = i
        break
      }
    }

    if (stepLineStart !== -1) {
      // 有序号的可能是步骤
      ingredientsContent = otherContent.slice(0, stepLineStart)
      instructionsContent = otherContent.slice(stepLineStart)
    } else {
      // 尝试按比例分配（前40%食材，后60%做法）
      const splitIndex = Math.floor(otherContent.length * 0.4)
      ingredientsContent = otherContent.slice(0, splitIndex)
      instructionsContent = otherContent.slice(splitIndex)
    }
  }

  // 提取时间和份量信息
  for (const line of [...lines, ...otherContent]) {
    const lowerLine = line.toLowerCase()
    
    // 准备时间
    for (const keyword of ['准备', 'prep']) {
      if (lowerLine.includes(keyword)) {
        const timeMatch = line.match(/(\d+)\s*(分|分钟|min)/i)
        if (timeMatch) {
          result.prep_time = parseInt(timeMatch[1])
        }
      }
    }
    
    // 烹饪时间
    for (const keyword of ['烹饪', '煮', '炒', 'cook']) {
      if (lowerLine.includes(keyword)) {
        const timeMatch = line.match(/(\d+)\s*(分|分钟|min)/i)
        if (timeMatch) {
          result.cook_time = parseInt(timeMatch[1])
        }
      }
    }
    
    // 份量
    for (const keyword of servingsKeywords) {
      if (lowerLine.includes(keyword)) {
        const servingsMatch = line.match(/(\d+)\s*(人|份)/i)
        if (servingsMatch) {
          result.servings = parseInt(servingsMatch[1])
        }
      }
    }
    
    // 难度
    for (const keyword of difficultyKeywords) {
      if (lowerLine.includes(keyword)) {
        if (lowerLine.includes('简') || lowerLine.includes('易')) {
          result.difficulty = 'easy'
        } else if (lowerLine.includes('中')) {
          result.difficulty = 'medium'
        } else if (lowerLine.includes('难')) {
          result.difficulty = 'hard'
        }
      }
    }
  }

  // 整理结果
  result.ingredients = ingredientsContent.join('\n')
  result.instructions = instructionsContent.join('\n')
  result.description = descriptionContent.join('\n')

  // 如果还是没有标题，使用第一行非空文本
  if (!result.title && lines.length > 0) {
    for (const line of lines) {
      if (line.trim()) {
        result.title = line.trim()
        break
      }
    }
  }

  return result
}
