// 在浏览器控制台运行这个脚本来测试API

const testAPI = async () => {
  console.log('开始测试API连接...')

  try {
    // 测试评论统计API
    console.log('\n1. 测试评论统计API:')
    const statsRes = await fetch('http://localhost:5000/api/comments/recipe/1/stats')
    console.log('Status:', statsRes.status)
    const stats = await statsRes.json()
    console.log('Stats:', stats)

    // 测试评论列表API
    console.log('\n2. 测试评论列表API:')
    const commentsRes = await fetch('http://localhost:5000/api/comments/recipe/1')
    console.log('Status:', commentsRes.status)
    const comments = await commentsRes.json()
    console.log('Comments:', comments)

    console.log('\n✅ API测试成功!')
  } catch (error) {
    console.error('\n❌ API测试失败:', error)
  }
}

// 运行测试
testAPI()
