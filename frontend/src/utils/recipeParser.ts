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
  const fullText = normalizedText

  // 常见关键词
  const titleKeywords = ['菜名', '菜名', '菜谱名', '名称', '题目', '标题']
  const ingredientKeywords = ['食材', '材料', '原料', '配料', '主料', '辅料', '调料', '所需食材', '食材及用量']
  const instructionKeywords = ['做法', '步骤', '制作', '方法', '烹饪', '流程', '制作步骤', '烹饪步骤']
  const descriptionKeywords = ['简介', '介绍', '特色', '描述', '说明', '这道菜', '是一道']
  const timeKeywords = ['时间', '准备', '烹饪', '分钟', 'min']
  const servingsKeywords = ['份量', '人数', '份', '人', '人份', '可制作']
  const difficultyKeywords = ['难度', '难易', '程度', '等级']

  // ==========================================
  // 模式 1：从整段文本中提取标题
  // ==========================================
  
  // 先尝试从【】或""中提取标题
  const bracketTitleMatch = fullText.match(/【([^】]+)】|「([^」]+)」|"([^"]+)"|'([^']+)'/)
  if (bracketTitleMatch) {
    result.title = (bracketTitleMatch[1] || bracketTitleMatch[2] || bracketTitleMatch[3] || bracketTitleMatch[4]).trim()
  }

  // 如果从括号中没找到，尝试找"这道XX"或"XX是一道"
  if (!result.title) {
    const titlePattern1 = fullText.match(/这道[是为]*[一道]*[的]*([^\s，。、；：]+)/)
    const titlePattern2 = fullText.match(/([^\s，。、；：]+)[是一]*道[经典的]*[菜色的]*/)
    if (titlePattern1 && titlePattern1[1].length > 1) {
      result.title = titlePattern1[1].trim()
    } else if (titlePattern2 && titlePattern2[1].length > 1) {
      result.title = titlePattern2[1].trim()
    }
  }

  // ==========================================
  // 模式 2：提取描述信息
  // ==========================================
  let descriptionText = ''
  const descEndMarkers = ingredientKeywords.concat(['制作', '需要', '所需', '准备', '食材', '材料'])
  
  // 从开头到第一个食材/做法标记
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    let foundMarker = false
    for (const marker of descEndMarkers) {
      if (line.includes(marker)) {
        foundMarker = true
        break
      }
    }
    if (foundMarker) break
    descriptionText += (descriptionText ? '\n' : '') + line.trim()
  }
  
  result.description = descriptionText.trim()

  // ==========================================
  // 模式 3：提取食材信息
  // ==========================================
  let ingredientsText = ''
  let ingredientsStartIdx = -1
  let ingredientsEndIdx = -1

  // 找食材关键词
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    for (const keyword of ingredientKeywords) {
      if (line.includes(keyword)) {
        ingredientsStartIdx = i
        break
      }
    }
    if (ingredientsStartIdx !== -1) break
  }

  // 从食材关键词开始，直到做法关键词
  if (ingredientsStartIdx !== -1) {
    for (let i = ingredientsStartIdx; i < lines.length; i++) {
      const line = lines[i]
      let foundEnd = false
      for (const keyword of instructionKeywords) {
        if (line.includes(keyword)) {
          foundEnd = true
          ingredientsEndIdx = i
          break
        }
      }
      if (foundEnd) break
      
      // 清理冒号前的标签
      let cleanLine = line.trim()
      const colonMatch = cleanLine.match(/^[^:：]+[:：]\s*(.+)$/)
      if (colonMatch) {
        cleanLine = colonMatch[1]
      }
      
      // 尝试把顿号和逗号分隔的食材拆分成多行
      if (cleanLine.includes('、') || cleanLine.includes('，') || cleanLine.includes(',')) {
        const items = cleanLine.split(/[、，,]/).map(item => item.trim()).filter(item => item)
        ingredientsText += (ingredientsText ? '\n' : '') + items.join('\n')
      } else if (cleanLine) {
        ingredientsText += (ingredientsText ? '\n' : '') + cleanLine
      }
    }
  } else {
    // 如果没找到明确的食材标签，尝试用规则从文本中提取
    // 查找有数字+单位的行，这些很可能是食材
    const possibleIngredients: string[] = []
    for (const line of lines) {
      if (line.match(/\d+\s*(g|克|kg|公斤|ml|毫升|个|片|块|勺|碗|杯|根|条|粒|颗)/i)) {
        possibleIngredients.push(line.trim())
      }
    }
    
    if (possibleIngredients.length > 0) {
      ingredientsText = possibleIngredients.join('\n')
    }
  }

  result.ingredients = ingredientsText.trim()

  // ==========================================
  // 模式 4：提取做法信息
  // ==========================================
  let instructionsText = ''
  let instructionsStartIdx = -1

  // 找做法关键词
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    for (const keyword of instructionKeywords) {
      if (line.includes(keyword)) {
        instructionsStartIdx = i
        break
      }
    }
    if (instructionsStartIdx !== -1) break
  }

  if (instructionsStartIdx !== -1) {
    for (let i = instructionsStartIdx; i < lines.length; i++) {
      let line = lines[i].trim()
      
      // 清理冒号前的标签
      const colonMatch = line.match(/^[^:：]+[:：]\s*(.+)$/)
      if (colonMatch) {
        line = colonMatch[1]
      }
      
      // 自动给步骤添加编号（如果没有的话）
      if (line && !/^\s*\d+[.、]/.test(line) && !/^\s*[一二三四五六七八九十]+[.、]/.test(line)) {
        // 看看句子里有没有"首先"、"接着"、"然后"、"随后"、"最后"等词
        if (/^(首先|第一|第一步|1[.、]|一[.、])/.test(line)) {
          line = '1. ' + line.replace(/^(首先|第一|第一步|1[.、]|一[.、])\s*/, '')
        } else if (/^(接着|其次|第二|第二步|2[.、]|二[.、])/.test(line)) {
          line = '2. ' + line.replace(/^(接着|其次|第二|第二步|2[.、]|二[.、])\s*/, '')
        } else if (/^(然后|随后|第三|第三步|3[.、]|三[.、])/.test(line)) {
          line = '3. ' + line.replace(/^(然后|随后|第三|第三步|3[.、]|三[.、])\s*/, '')
        } else if (/^(最后|第四|第四步|4[.、]|四[.、])/.test(line)) {
          line = '4. ' + line.replace(/^(最后|第四|第四步|4[.、]|四[.、])\s*/, '')
        } else if (instructionsText) {
          // 如果前面已经有内容了，自动编号
          const count = instructionsText.split('\n').filter(l => l.trim()).length + 1
          line = count + '. ' + line
        }
      }
      
      if (line) {
        instructionsText += (instructionsText ? '\n' : '') + line
      }
    }
  }

  result.instructions = instructionsText.trim()

  // ==========================================
  // 模式 5：提取时间信息
  // ==========================================
  
  // 准备时间
  const prepTimeMatch = fullText.match(/准备时间[^\d]*(\d+)|准备[^\d]*(\d+)\s*分[钟]*/i)
  if (prepTimeMatch) {
    result.prep_time = parseInt(prepTimeMatch[1] || prepTimeMatch[2])
  }
  
  // 烹饪时间
  const cookTimeMatch = fullText.match(/烹饪时间[^\d]*(\d+)|煮[^\d]*(\d+)\s*分[钟]*|炒[^\d]*(\d+)\s*分[钟]*|烹饪[^\d]*(\d+)\s*分[钟]*/i)
  if (cookTimeMatch) {
    result.cook_time = parseInt(cookTimeMatch[1] || cookTimeMatch[2] || cookTimeMatch[3] || cookTimeMatch[4])
  }
  
  // 份量
  const servingsMatch = fullText.match(/(\d+)\s*人份|(\d+)\s*份|可制作[^\d]*(\d+)|(\d+)\s*人/i)
  if (servingsMatch) {
    result.servings = parseInt(servingsMatch[1] || servingsMatch[2] || servingsMatch[3] || servingsMatch[4])
  }
  
  // 难度
  const lowerText = fullText.toLowerCase()
  if (lowerText.includes('简单') || lowerText.includes('容易') || lowerText.includes('入门')) {
    result.difficulty = 'easy'
  } else if (lowerText.includes('中等') || lowerText.includes('一般') || lowerText.includes('普通')) {
    result.difficulty = 'medium'
  } else if (lowerText.includes('困难') || lowerText.includes('难') || lowerText.includes('复杂')) {
    result.difficulty = 'hard'
  }

  // ==========================================
  // 补充处理：如果上面没找到，尝试用传统方式
  // ==========================================
  if (!result.ingredients && !result.instructions) {
    // 模式1：按标签分区（传统方式）
    let currentSection = 'title'
    let titleFound = !!result.title
    let ingredientsContent: string[] = []
    let instructionsContent: string[] = []
    let descriptionContent: string[] = []
    let otherContent: string[] = []

    for (let line of lines) {
      const trimmedLine = line.trim()
      const lowerLine = trimmedLine.toLowerCase()
      let isNewSection = false

      // 食材检测
      if (!isNewSection) {
        for (const keyword of ingredientKeywords) {
          if (lowerLine.includes(keyword) && lowerLine.length < 30) {
            currentSection = 'ingredients'
            isNewSection = true
            break
          }
        }
      }

      // 做法检测
      if (!isNewSection) {
        for (const keyword of instructionKeywords) {
          if (lowerLine.includes(keyword) && lowerLine.length < 30) {
            currentSection = 'instructions'
            isNewSection = true
            break
          }
        }
      }

      // 简介检测
      if (!isNewSection) {
        for (const keyword of descriptionKeywords) {
          if (lowerLine.includes(keyword) && lowerLine.length < 30) {
            currentSection = 'description'
            isNewSection = true
            break
          }
        }
      }

      // 处理当前行内容
      if (!isNewSection) {
        if (currentSection === 'ingredients') {
          ingredientsContent.push(trimmedLine)
        } else if (currentSection === 'instructions') {
          instructionsContent.push(trimmedLine)
        } else if (currentSection === 'description') {
          descriptionContent.push(trimmedLine)
        } else if (!titleFound && trimmedLine.length > 0 && trimmedLine.length < 50) {
          if (!result.title) result.title = trimmedLine
          titleFound = true
        } else {
          otherContent.push(trimmedLine)
        }
      }
    }

    // 模式2：如果还是没有找到，尝试自动识别
    if (ingredientsContent.length === 0 && instructionsContent.length === 0 && otherContent.length > 0) {
      let stepLineStart = -1
      
      // 查找带有序号的行
      for (let i = 0; i < otherContent.length; i++) {
        const line = otherContent[i]
        if (/^\s*(\d+[.、]|[一二三四五六七八九十]+[.、])/.test(line)) {
          stepLineStart = i
          break
        }
      }

      if (stepLineStart !== -1) {
        ingredientsContent = otherContent.slice(0, stepLineStart)
        instructionsContent = otherContent.slice(stepLineStart)
      }
    }

    // 整理结果
    if (!result.ingredients) result.ingredients = ingredientsContent.join('\n')
    if (!result.instructions) result.instructions = instructionsContent.join('\n')
    if (!result.description) result.description = descriptionContent.join('\n')
  }

  // 如果还是没有标题，使用第一行非空文本
  if (!result.title && lines.length > 0) {
    for (const line of lines) {
      if (line.trim()) {
        // 如果第一行太长，截取前30个字符
        result.title = line.trim().substring(0, 30)
        break
      }
    }
  }

  return result
}
