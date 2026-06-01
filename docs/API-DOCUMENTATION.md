# 菜谱分享系统 API 接口文档

## 项目简介

菜谱分享系统是一个基于前后端分离架构的Web应用，支持用户注册登录、菜谱管理、评论互动等功能。

**技术栈：**
- 后端：Flask + SQLAlchemy + JWT
- 前端：Vue 3 + TypeScript + Element Plus
- 数据库：SQLite（开发）/ MySQL（生产）

## 基础信息

- **API基础URL**: `http://localhost:5000`
- **内容类型**: `application/json`
- **认证方式**: JWT Bearer Token
- **API版本**: v1

## 认证说明

除了登录和注册接口外，所有API都需要在请求头中包含JWT Token：

```
Authorization: Bearer <access_token>
```

## 接口列表

### 1. 用户认证 (/api/auth)

#### 1.1 用户注册

**接口**: `POST /api/auth/register`

**描述**: 创建新用户账号

**请求参数**:
```json
{
  "username": "string",    // 用户名（唯一）
  "email": "string",       // 邮箱（唯一）
  "password": "string"     // 密码
}
```

**成功响应** (201):
```json
{
  "message": "注册成功"
}
```

**错误响应** (400):
```json
{
  "message": "邮箱已存在"
}
```

#### 1.2 用户登录

**接口**: `POST /api/auth/login`

**描述**: 用户登录获取访问令牌

**请求参数** (支持用户名或邮箱登录):
```json
{
  "username": "string",    // 用户名（与email二选一）
  "email": "string",       // 邮箱（与username二选一）
  "password": "string"     // 密码
}
```

**成功响应** (200):
```json
{
  "access_token": "jwt_token_string",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "bio": "个人简介",
    "avatar": null,
    "created_at": "2025-12-11T08:44:48.181946"
  }
}
```

**错误响应** (401):
```json
{
  "message": "用户名/邮箱或密码错误"
}
```

### 2. 用户管理 (/api/users)

#### 2.1 获取用户资料

**接口**: `GET /api/users/profile`

**描述**: 获取当前用户的个人资料（需要认证）

**请求头**:
```
Authorization: Bearer <access_token>
```

**成功响应** (200):
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "bio": "个人简介",
  "avatar": null,
  "created_at": "2025-12-11T08:44:48.181946"
}
```

### 3. 菜谱管理 (/api/recipes)

#### 3.1 获取菜谱列表

**接口**: `GET /api/recipes/`

**描述**: 分页获取菜谱列表

**查询参数**:
- `page`: 页码（默认: 1）
- `per_page`: 每页数量（默认: 10）

**请求示例**:
```
GET /api/recipes/?page=1&per_page=10
```

**成功响应** (200):
```json
{
  "recipes": [
    {
      "id": 1,
      "title": "经典番茄炒蛋",
      "description": "简单易学的家常菜，酸甜可口，营养搭配均衡",
      "ingredients": "鸡蛋 3个\n番茄 2个\n葱 1根\n...",
      "instructions": "1. 番茄洗净切块，鸡蛋打散\n...",
      "prep_time": 10,        // 准备时间（分钟）
      "cook_time": 15,         // 烹饪时间（分钟）
      "difficulty": "简单",    // 难度：简单/中等/困难
      "servings": 2,           // 份量
      "image": "tomato_egg.jpg",
      "user_id": 1,
      "created_at": "2025-12-11T08:44:48.192924"
    }
  ],
  "total": 3,               // 总数
  "pages": 1,               // 总页数
  "current_page": 1         // 当前页码
}
```

#### 3.2 获取单个菜谱

**接口**: `GET /api/recipes/<recipe_id>`

**描述**: 获取指定菜谱的详细信息

**成功响应** (200):
```json
{
  "id": 1,
  "title": "经典番茄炒蛋",
  "description": "简单易学的家常菜，酸甜可口，营养搭配均衡",
  "ingredients": "鸡蛋 3个\n番茄 2个\n葱 1根\n...",
  "instructions": "1. 番茄洗净切块，鸡蛋打散\n...",
  "prep_time": 10,
  "cook_time": 15,
  "difficulty": "简单",
  "servings": 2,
  "image": "tomato_egg.jpg",
  "user_id": 1,
  "created_at": "2025-12-11T08:44:48.192924"
}
```

**错误响应** (404):
```json
{
  "message": "菜谱不存在"
}
```

#### 3.3 创建菜谱

**接口**: `POST /api/recipes/`

**描述**: 创建新菜谱（需要认证）

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求参数**:
```json
{
  "title": "string",           // 菜谱标题（必需）
  "description": "string",     // 菜谱描述（可选）
  "ingredients": "string",     // 食材清单（必需）
  "instructions": "string",    // 制作步骤（必需）
  "prep_time": 15,             // 准备时间（分钟，可选）
  "cook_time": 30,             // 烹饪时间（分钟，可选）
  "difficulty": "简单",        // 难度等级（可选）
  "servings": 4,               // 份量（可选）
  "image": "recipe.jpg"        // 图片文件名（可选）
}
```

**成功响应** (201):
```json
{
  "id": 4,
  "title": "新菜谱",
  "description": "菜谱描述",
  "ingredients": "食材清单",
  "instructions": "制作步骤",
  "prep_time": 15,
  "cook_time": 30,
  "difficulty": "简单",
  "servings": 4,
  "image": "recipe.jpg",
  "user_id": 1,
  "created_at": "2025-12-11T08:47:19.285478"
}
```

#### 3.4 更新菜谱

**接口**: `PUT /api/recipes/<recipe_id>`

**描述**: 更新指定菜谱（需要认证，只有菜谱作者可以更新）

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求参数**:
```json
{
  "title": "string",           // 菜谱标题（可选）
  "description": "string",     // 菜谱描述（可选）
  "ingredients": "string",     // 食材清单（可选）
  "instructions": "string",    // 制作步骤（可选）
  "prep_time": 15,             // 准备时间（可选）
  "cook_time": 30,             // 烹饪时间（可选）
  "difficulty": "简单",        // 难度等级（可选）
  "servings": 4,               // 份量（可选）
  "image": "recipe.jpg"        // 图片文件名（可选）
}
```

**成功响应** (200):
```json
{
  "id": 1,
  "title": "更新后的菜谱标题",
  "description": "更新后的描述",
  // ... 其他字段
  "updated_at": "2025-12-11T08:50:00.000000"
}
```

**错误响应**:
- 403: 无权限编辑此菜谱
- 404: 菜谱不存在

#### 3.5 删除菜谱

**接口**: `DELETE /api/recipes/<recipe_id>`

**描述**: 删除指定菜谱（需要认证，只有菜谱作者可以删除）

**请求头**:
```
Authorization: Bearer <access_token>
```

**成功响应** (200):
```json
{
  "message": "菜谱删除成功"
}
```

**错误响应**:
- 403: 无权限删除此菜谱
- 404: 菜谱不存在

## 数据模型

### 用户模型 (User)
```json
{
  "id": "integer",           // 用户ID
  "username": "string",      // 用户名（唯一）
  "email": "string",         // 邮箱（唯一）
  "password_hash": "string", // 密码哈希（不返回）
  "avatar": "string",        // 头像URL（可选）
  "bio": "string",           // 个人简介（可选）
  "created_at": "datetime",  // 创建时间
  "updated_at": "datetime"   // 更新时间
}
```

### 菜谱模型 (Recipe)
```json
{
  "id": "integer",           // 菜谱ID
  "title": "string",         // 标题
  "description": "string",   // 描述
  "ingredients": "text",     // 食材清单
  "instructions": "text",    // 制作步骤
  "prep_time": "integer",    // 准备时间（分钟）
  "cook_time": "integer",    // 烹饪时间（分钟）
  "difficulty": "string",    // 难度等级
  "servings": "integer",     // 份量
  "image": "string",         // 图片URL（可选）
  "user_id": "integer",      // 作者ID
  "created_at": "datetime",  // 创建时间
  "updated_at": "datetime"   // 更新时间
}
```

### 评论模型 (Comment)
```json
{
  "id": "integer",           // 评论ID
  "content": "text",         // 评论内容
  "rating": "integer",       // 评分（1-5）
  "user_id": "integer",      // 评论者ID
  "recipe_id": "integer",    // 菜谱ID
  "created_at": "datetime",  // 创建时间
  "updated_at": "datetime"   // 更新时间
}
```

## 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "message": "错误描述信息"
}
```

### 常见HTTP状态码

- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权/认证失败
- `403` - 权限不足
- `404` - 资源不存在
- `500` - 服务器内部错误

## 测试数据

系统初始化时会创建以下测试账号：

1. **管理员账号**:
   - 用户名: `admin`
   - 密码: `admin123`

2. **厨师账号**:
   - 用户名: `chef1`
   - 密码: `chef123`

3. **美食爱好者**:
   - 用户名: `foodie`
   - 密码: `food123`

## 使用示例

### 完整的菜谱创建流程

1. **用户登录**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

2. **创建菜谱**:
```bash
curl -X POST http://localhost:5000/api/recipes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "红烧肉",
    "description": "传统名菜",
    "ingredients": "五花肉 500g\n冰糖 30g\n生抽 3勺",
    "instructions": "1. 五花肉切块\n2. 炒糖色\n3. 红烧",
    "prep_time": 20,
    "cook_time": 60,
    "difficulty": "中等",
    "servings": 4
  }'
```

3. **获取菜谱列表**:
```bash
curl -X GET http://localhost:5000/api/recipes/
```

## 前端集成

前端Vue应用应按以下方式调用API：

1. 使用axios进行HTTP请求
2. 在请求拦截器中自动添加JWT Token
3. 处理401响应时自动跳转登录页面
4. 统一错误处理和用户提示

## 开发环境配置

- 后端服务: `http://localhost:5000`
- 前端服务: `http://localhost:8081`
- 数据库: `sqlite:///recipe_platform.db`

## 部署说明

生产环境需要修改以下配置：
- 数据库URL改为MySQL
- JWT密钥使用强密钥
- 禁用调试模式
- 配置CORS允许的域名
- 设置文件上传大小限制