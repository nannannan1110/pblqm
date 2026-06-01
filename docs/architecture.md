# 菜谱分享系统全栈架构文档

**文档版本**: v1.0
**创建时间**: 2025年12月24日
**架构师**: Winston (AI Architect)
**项目状态**: 棕地项目（现有系统架构文档化）

---

## 1. 引言

### 1.1 文档概述

本文档是**菜谱分享系统**的完整全栈架构文档，整合了前端、后端、数据库、部署和开发工作流的统一架构规范。该文档作为 AI 驱动开发的单一真实来源（Single Source of Truth），确保整个技术栈的一致性和可维护性。

### 1.2 项目背景

**菜谱分享系统**是一个基于 Web 的智能美食平台，为用户提供个性化的菜谱发现、学习和分享体验。系统采用前后端分离架构，结合现代化技术栈，实现高性能、可扩展的美食社区平台。

**核心功能**：
- 用户注册登录与个人资料管理
- 菜谱创建、浏览、搜索和管理
- 图片上传和管理
- 评论评分和互动
- 个人收藏和历史记录

**目标用户**：
- 主要：25-45 岁都市健康生活家
- 次要：专业厨师和美食博主

### 1.3 启动模板或现有项目

**状态**: 现有项目（棕地开发）

**项目基础**:
- 本项目是基于团队自主开发的现有系统
- 前端：Vue 3 + TypeScript + Vite + Element Plus
- 后端：Flask + SQLAlchemy + JWT
- 数据库：MySQL 5.7.44（生产）/ SQLite（开发）
- 已实现核心功能：用户认证、菜谱 CRUD、图片上传、搜索

**架构约束**：
- 必须保持 MySQL 5.7.44 兼容性
- 前后端已分离部署，需保持独立仓库结构
- 现有 API 接口需保持向后兼容

### 1.4 变更日志

| 日期 | 版本 | 描述 | 作者 |
|------|------|------|------|
| 2025-12-24 | v1.0 | 初始全栈架构文档创建 | Winston (AI) |

---

## 2. 高层架构

### 2.1 技术总结

菜谱分享系统采用**前后端分离的 RESTful 架构**，前端使用 Vue 3 组合式 API 和 TypeScript 构建响应式 SPA，后端基于 Flask 微服务框架提供 RESTful API，数据持久化使用 MySQL 5.7.44 关系型数据库，Redis 作为缓存层提升性能。系统通过 JWT 实现无状态认证，采用 Nginx 反向代理部署，支持高并发访问和水平扩展。

### 2.2 平台和基础设施选择

**部署平台**: 本地 Linux 服务器（Ubuntu 20.04 LTS）

**核心服务**:
- **Web 服务器**: Nginx 1.18+ (反向代理 + 静态文件服务)
- **应用服务器**: Gunicorn (WSGI 服务器)
- **数据库**: MySQL 5.7.44
- **缓存**: Redis 6.0+
- **容器化**: Docker & Docker Compose (可选)

**部署主机和区域**:
- **开发环境**: 本地 Windows (D:\pbl5\myproject)
- **生产环境**: 单机部署（Ubuntu 20.04 LTS）
- **区域**: 本地部署，暂无多区域需求

**决策理由**:
- **本地部署**：确保数据安全和完全控制
- **MySQL 5.7.44**：成熟稳定，团队经验丰富
- **Nginx + Gunicorn**：行业标准，性能优秀
- **Redis 缓存**：提升搜索性能，减轻数据库压力

### 2.3 仓库结构

**结构**: 前后端分离（独立 Git 仓库）

**Monorepo 工具**: N/A（采用分离仓库）

**包组织**:
```
myproject/
├── frontend/          # 前端仓库（可独立 Git）
├── backend/           # 后端仓库（可独立 Git）
├── docs/              # 共享文档（PRD、API、架构）
├── scripts/           # 共享脚本（部署、初始化）
└── infrastructure/    # 基础设施代码（Docker、Nginx 配置）
```

**共享代码策略**:
- TypeScript 类型定义：`frontend/src/types/` 维护，前后端通过 API 契约同步
- 常量配置：各自维护，通过环境变量统一
- 工具函数：前后端独立实现，避免语言耦合

### 2.4 高层架构图

```mermaid
graph TB
    User[用户浏览器] -->|HTTPS| Nginx[Nginx 反向代理]

    Nginx -->|静态资源| Frontend[Vue 3 前端应用]
    Nginx -->|/api/*| Backend[Flask 后端 API]

    Backend -->|SQL| MySQL[(MySQL 5.7.44)]
    Backend -->|缓存| Redis[(Redis 缓存)]
    Backend -->|文件存储| FileSystem[本地文件系统]

    Frontend -->|RESTful API| Backend

    style Frontend fill:#42b983
    style Backend fill:#4CAF50
    style MySQL fill:#FF6B6B
    style Redis fill:#DC382D
    style Nginx fill:#009688
```

### 2.5 架构模式

**整体架构模式**：
- **前后端分离 (SPA + RESTful API)**: 前端负责 UI 渲染和用户交互，后端提供数据和业务逻辑，通过 RESTful API 通信
  - **理由**: 解耦前后端开发，提升可维护性，支持多端扩展（未来移动端）

**前端架构模式**：
- **组件化架构 (Component-Based UI)**: Vue 3 组合式 API，组件复用
  - **理由**: 提升代码复用性，降低维护成本
- **状态管理 (Centralized State)**: Pinia 集中式状态管理
  - **理由**: 简化跨组件状态共享，提升开发效率
- **路由守卫 (Route Guards)**: Vue Router 路由级别权限控制
  - **理由**: 统一认证和权限管理

**后端架构模式**：
- **MVC 架构 (Model-View-Controller)**: Flask 蓝图组织路由
  - **理由**: 清晰的职责分离，便于测试和维护
- **Repository 模式**: SQLAlchemy ORM 抽象数据访问
  - **理由**: 解耦业务逻辑和数据访问，提升可测试性
- **JWT 无状态认证**: Token-based 认证
  - **理由**: 支持水平扩展，无会话状态

**集成模式**：
- **RESTful API 规范**: 资源导向的 API 设计
  - **理由**: 标准化接口，易于理解和集成
- **API 版本控制**: URL 路径版本 (/api/v1/)
  - **理由**: 支持平滑升级和向后兼容

---

## 3. 技术栈

### 3.1 技术栈表

**⚠️ 重要**: 这是项目的技术栈单一真实来源（Single Source of Truth），所有开发必须严格使用以下技术及版本。

| 类别 | 技术 | 版本 | 用途 | 选择理由 |
|------|------|------|------|----------|
| **前端语言** | TypeScript | 4.9+ | 类型安全的 JavaScript | 提升代码质量，减少运行时错误 |
| **前端框架** | Vue.js | 3.3+ | 渐进式前端框架 | 组合式 API，性能优秀，学习曲线平缓 |
| **UI 组件库** | Element Plus | 2.4+ | Vue 3 UI 组件库 | 丰富的企业级组件，中文文档完善 |
| **状态管理** | Pinia | 2.1+ | Vue 官方状态管理 | TypeScript 原生支持，API 简洁 |
| **路由管理** | Vue Router | 4.2+ | Vue 官方路由 | 与 Vue 3 深度集成，支持导航守卫 |
| **HTTP 客户端** | Axios | 1.6+ | HTTP 请求库 | 拦截器支持，Promise API |
| **构建工具** | Vite | 5.0+ | 前端构建工具 | 快速热更新，原生 ESM 支持 |
| **CSS 框架** | SCSS | - | CSS 预处理器 | 变量、嵌套、混入等特性 |
| **后端语言** | Python | 3.8+ | 后端开发语言 | 生态丰富，开发效率高 |
| **后端框架** | Flask | 2.3+ | 微服务框架 | 轻量级，灵活性强 |
| **API 框架** | Flask-RESTful | 0.3.8+ | RESTful API 扩展 | 快速构建 REST API |
| **数据库 ORM** | SQLAlchemy | 2.0+ | Python ORM | 强大的数据映射和查询功能 |
| **数据库迁移** | Flask-Migrate | 4.0+ | 数据库版本管理 | Alembic 集成，支持迁移回滚 |
| **认证** | Flask-JWT-Extended | 4.5+ | JWT 认证 | 无状态认证，支持 Token 刷新 |
| **数据库** | MySQL | 5.7.44 | 关系型数据库 | 成熟稳定，团队经验丰富 |
| **缓存** | Redis | 6.0+ | 内存数据库缓存 | 高性能缓存，支持多种数据结构 |
| **文件上传** | Flask-Uploads | - | 文件上传处理 | 简化文件上传逻辑 |
| **任务队列** | Celery | 5.3+ | 异步任务处理 | (可选) 异步任务，定时任务 |
| **前端测试** | Vitest | 1.0+ | 单元测试框架 | Vite 原生集成，快速执行 |
| **后端测试** | pytest | 7.4+ | Python 测试框架 | 插件丰富，断言清晰 |
| **E2E 测试** | Cypress | 13.0+ | 端到端测试 | (可选) 真实浏览器测试 |
| **代码规范** | ESLint + Prettier | - | 前端代码规范 | 统一代码风格 |
| **代码规范** | Black + Flake8 | - | Python 代码规范 | Python 官方推荐风格 |
| **Web 服务器** | Nginx | 1.18+ | 反向代理/静态文件 | 高性能，负载均衡 |
| **应用服务器** | Gunicorn | 21.2+ | WSGI 服务器 | 生产级 Python 服务器 |
| **容器化** | Docker | 24.0+ | 容器化部署 | (可选) 环境一致性 |
| **CI/CD** | GitHub Actions | - | 持续集成/部署 | (可选) 自动化构建测试 |
| **监控** | - | - | (待规划) | 未来集成 Sentry/DataDog |
| **日志** | Python logging | - | 后端日志 | Python 标准库 |

---

## 4. 数据模型

### 4.1 用户 (User)

**用途**: 表示系统用户，存储用户认证和个人信息

**关键属性**:
- `id: Integer` - 用户唯一标识（主键，自增）
- `username: String(50)` - 用户名（唯一，非空）
- `email: String(100)` - 邮箱（唯一，非空）
- `password_hash: String(255)` - 密码哈希（bcrypt，非空）
- `avatar: String(255)` - 头像 URL（可选）
- `bio: Text` - 个人简介（可选）
- `location: String(100)` - 地区（可选）
- `created_at: DateTime` - 创建时间（自动时间戳）
- `updated_at: DateTime` - 更新时间（自动时间戳）
- `is_active: Boolean` - 账户状态（默认：true）
- `email_verified: Boolean` - 邮箱验证状态（默认：false）

**TypeScript 接口**:
```typescript
// frontend/src/types/user.ts
export interface User {
  id: number;
  username: string;
  email: string;
  avatar?: string;
  bio?: string;
  location?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  email_verified: boolean;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
}

export interface UserUpdate {
  username?: string;
  avatar?: string;
  bio?: string;
  location?: string;
}
```

**关系**:
- 一对多：一个用户可以创建多个菜谱 (Recipe.user_id)
- 一对多：一个用户可以发表多个评论 (Comment.user_id)
- 一对多：一个用户可以有多个收藏 (Favorite.user_id)

---

### 4.2 菜谱 (Recipe)

**用途**: 表示用户创建的菜谱，包含完整的菜品信息

**关键属性**:
- `id: Integer` - 菜谱唯一标识（主键，自增）
- `title: String(100)` - 菜谱标题（非空）
- `description: Text` - 菜谱描述/简介
- `difficulty: Enum('easy', 'medium', 'hard')` - 难度等级（非空）
- `prep_time: Integer` - 准备时间（分钟，非空）
- `cook_time: Integer` - 烹饪时间（分钟）
- `servings: Integer` - 份量（人份）
- `ingredients: Text` - 食材清单（文本格式）
- `instructions: Text` - 制作步骤（文本格式）
- `image: String(255)` - 菜谱图片 URL
- `author_id: Integer` - 作者 ID（外键 → users.id）
- `is_published: Boolean` - 是否发布（默认：false）
- `is_deleted: Boolean` - 是否删除（软删除，默认：false）
- `created_at: DateTime` - 创建时间
- `updated_at: DateTime` - 更新时间

**TypeScript 接口**:
```typescript
// frontend/src/types/recipe.ts
export interface Recipe {
  id: number;
  title: string;
  description?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  prep_time: number;
  cook_time?: number;
  servings?: number;
  ingredients: string;
  instructions: string;
  image?: string;
  author_id: number;
  author?: User;  // 关联加载
  is_published: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface RecipeCreate {
  title: string;
  description?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  prep_time: number;
  cook_time?: number;
  servings?: number;
  ingredients: string;
  instructions: string;
  image?: string;
}

export interface RecipeUpdate {
  title?: string;
  description?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  prep_time?: number;
  cook_time?: number;
  servings?: number;
  ingredients?: string;
  instructions?: string;
  image?: string;
  is_published?: boolean;
}
```

**关系**:
- 多对一：属于一个用户 (User.id)
- 一对多：一个菜谱可以有多个评论 (Comment.recipe_id)
- 一对多：一个菜谱可以被多个用户收藏 (Favorite.recipe_id)

---

### 4.3 评论 (Comment)

**用途**: 用户对菜谱的评论和评分

**关键属性**:
- `id: Integer` - 评论唯一标识（主键，自增）
- `content: Text` - 评论内容（非空，10-500 字符）
- `rating: Integer` - 评分（1-5 星，非空）
- `user_id: Integer` - 评论者 ID（外键 → users.id）
- `recipe_id: Integer` - 关联菜谱 ID（外键 → recipes.id）
- `parent_id: Integer` - 父评论 ID（自关联外键，支持回复）
- `is_deleted: Boolean` - 是否删除（软删除）
- `created_at: DateTime` - 创建时间
- `updated_at: DateTime` - 更新时间

**TypeScript 接口**:
```typescript
// frontend/src/types/comment.ts
export interface Comment {
  id: number;
  content: string;
  rating: number;  // 1-5
  user_id: number;
  user?: User;  // 关联加载
  recipe_id: number;
  parent_id?: number;
  parent?: Comment;  // 父评论
  replies?: Comment[];  // 子评论
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface CommentCreate {
  content: string;
  rating: number;
  recipe_id: number;
  parent_id?: number;
}

export interface CommentUpdate {
  content?: string;
  rating?: number;
}
```

**关系**:
- 多对一：属于一个用户 (User.id)
- 多对一：属于一个菜谱 (Recipe.id)
- 自关联：可以有父评论（支持嵌套回复）

---

### 4.4 收藏 (Favorite)

**用途**: 用户收藏的菜谱

**关键属性**:
- `id: Integer` - 收藏记录 ID（主键，自增）
- `user_id: Integer` - 用户 ID（外键 → users.id）
- `recipe_id: Integer` - 菜谱 ID（外键 → recipes.id）
- `created_at: DateTime` - 收藏时间

**唯一约束**: `(user_id, recipe_id)` - 一个用户对同一菜谱只能收藏一次

**TypeScript 接口**:
```typescript
// frontend/src/types/favorite.ts
export interface Favorite {
  id: number;
  user_id: number;
  recipe_id: number;
  recipe?: Recipe;  // 关联加载
  created_at: string;
}
```

**关系**:
- 多对一：属于一个用户 (User.id)
- 多对一：关联一个菜谱 (Recipe.id)

---

## 5. API 规范

### 5.1 REST API 规范 (OpenAPI 3.0)

```yaml
openapi: 3.0.0
info:
  title: 菜谱分享系统 API
  version: 1.0.0
  description: 菜谱分享系统的 RESTful API 接口文档
servers:
  - url: http://localhost:5000
    description: 开发环境
  - url: https://api.example.com
    description: 生产环境

paths:
  /api/auth/register:
    post:
      summary: 用户注册
      tags: [认证]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [username, email, password]
              properties:
                username:
                  type: string
                  minLength: 3
                  maxLength: 50
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        '201':
          description: 注册成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        '400':
          description: 请求参数错误或邮箱已存在

  /api/auth/login:
    post:
      summary: 用户登录
      tags: [认证]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [password]
              properties:
                username:
                  type: string
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: 登录成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  user:
                    $ref: '#/components/schemas/User'
        '401':
          description: 用户名或密码错误

  /api/users/profile:
    get:
      summary: 获取当前用户资料
      tags: [用户]
      security:
        - BearerAuth: []
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: 未授权

  /api/recipes/:
    get:
      summary: 获取菜谱列表（分页）
      tags: [菜谱]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 10
        - name: search
          in: query
          description: 搜索关键词
          schema:
            type: string
        - name: difficulty
          in: query
          description: 难度筛选
          schema:
            type: string
            enum: [easy, medium, hard]
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  recipes:
                    type: array
                    items:
                      $ref: '#/components/schemas/Recipe'
                  total:
                    type: integer
                  pages:
                    type: integer
                  current_page:
                    type: integer

    post:
      summary: 创建菜谱
      tags: [菜谱]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RecipeCreate'
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'

  /api/recipes/{recipe_id}:
    get:
      summary: 获取单个菜谱详情
      tags: [菜谱]
      parameters:
        - name: recipe_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Recipe'
        '404':
          description: 菜谱不存在

    put:
      summary: 更新菜谱
      tags: [菜谱]
      security:
        - BearerAuth: []
      parameters:
        - name: recipe_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RecipeUpdate'
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限
        '404':
          description: 菜谱不存在

    delete:
      summary: 删除菜谱
      tags: [菜谱]
      security:
        - BearerAuth: []
      parameters:
        - name: recipe_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 删除成功
        '403':
          description: 无权限
        '404':
          description: 菜谱不存在

  /api/recipes/{recipe_id}/comments:
    get:
      summary: 获取菜谱评论列表
      tags: [评论]
      parameters:
        - name: recipe_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Comment'

    post:
      summary: 发表评论
      tags: [评论]
      security:
        - BearerAuth: []
      parameters:
        - name: recipe_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentCreate'
      responses:
        '201':
          description: 评论成功
        '400':
          description: 参数错误

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
          format: email
        avatar:
          type: string
          nullable: true
        bio:
          type: string
          nullable: true
        location:
          type: string
          nullable: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Recipe:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        description:
          type: string
          nullable: true
        difficulty:
          type: string
          enum: [easy, medium, hard]
        prep_time:
          type: integer
        cook_time:
          type: integer
          nullable: true
        servings:
          type: integer
          nullable: true
        ingredients:
          type: string
        instructions:
          type: string
        image:
          type: string
          nullable: true
        author_id:
          type: integer
        is_published:
          type: boolean
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    RecipeCreate:
      type: object
      required: [title, difficulty, prep_time, ingredients, instructions]
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
        difficulty:
          type: string
          enum: [easy, medium, hard]
        prep_time:
          type: integer
          minimum: 1
        cook_time:
          type: integer
        servings:
          type: integer
        ingredients:
          type: string
        instructions:
          type: string
        image:
          type: string

    Comment:
      type: object
      properties:
        id:
          type: integer
        content:
          type: string
        rating:
          type: integer
          minimum: 1
          maximum: 5
        user_id:
          type: integer
        recipe_id:
          type: integer
        parent_id:
          type: integer
          nullable: true
        created_at:
          type: string
          format: date-time

    CommentCreate:
      type: object
      required: [content, rating]
      properties:
        content:
          type: string
          minLength: 10
          maxLength: 500
        rating:
          type: integer
          minimum: 1
          maximum: 5
        parent_id:
          type: integer
```

---

## 6. 组件

### 6.1 前端组件

#### 6.1.1 认证组件 (AuthComponents)

**职责**: 用户注册、登录、密码重置

**关键接口**:
- `<RegisterForm>`: 注册表单组件
- `<LoginForm>`: 登录表单组件
- `<PasswordReset>`: 密码重置组件

**依赖**: Pinia Auth Store, API Client

**技术栈**: Vue 3 Composition API, Element Plus Form

---

#### 6.1.2 菜谱组件 (RecipeComponents)

**职责**: 菜谱列表展示、详情页、创建/编辑表单

**关键接口**:
- `<RecipeList>`: 菜谱列表（分页）
- `<RecipeCard>`: 单个菜谱卡片
- `<RecipeDetail>`: 菜谱详情页
- `<RecipeForm>`: 菜谱创建/编辑表单
- `<RecipeSearch>`: 搜索栏组件

**依赖**: Recipe Store, API Client, Router

**技术栈**: Vue 3, Element Plus, Vue Router

---

#### 6.1.3 评论组件 (CommentComponents)

**职责**: 评论列表、发表评论、评论回复

**关键接口**:
- `<CommentList>`: 评论列表
- `<CommentItem>`: 单个评论项
- `<CommentForm>`: 评论表单
- `<RatingStars>`: 评分星级组件

**依赖**: Comment Store, API Client

---

#### 6.1.4 用户中心组件 (UserComponents)

**职责**: 个人资料、收藏夹、历史记录

**关键接口**:
- `<UserProfile>`: 个人资料页
- `<UserFavorites>`: 收藏夹
- `<UserHistory>`: 浏览历史

**依赖**: User Store, API Client

---

### 6.2 后端组件

#### 6.2.1 认证服务 (AuthService)

**职责**: 用户注册、登录、Token 生成/验证

**关键接口**:
- `register(username, email, password)`: 注册用户
- `login(username/email, password)`: 用户登录，返回 JWT Token
- `verify_token(token)`: 验证 Token 有效性
- `refresh_token(refresh_token)`: 刷新访问令牌

**依赖**: User Model, JWT Extended

**技术栈**: Flask-JWT-Extended, bcrypt

---

#### 6.2.2 菜谱服务 (RecipeService)

**职责**: 菜谱 CRUD、搜索、筛选

**关键接口**:
- `create_recipe(data, user_id)`: 创建菜谱
- `get_recipe(recipe_id)`: 获取单个菜谱
- `list_recipes(page, per_page, filters)`: 获取菜谱列表（分页）
- `update_recipe(recipe_id, data, user_id)`: 更新菜谱
- `delete_recipe(recipe_id, user_id)`: 软删除菜谱
- `search_recipes(keyword, filters)`: 搜索菜谱

**依赖**: Recipe Model, Redis Cache

**技术栈**: SQLAlchemy, Flask-RESTful

---

#### 6.2.3 评论服务 (CommentService)

**职责**: 评论 CRUD、评分统计

**关键接口**:
- `create_comment(data, user_id)`: 发表评论
- `get_comments(recipe_id)`: 获取菜谱评论
- `update_comment(comment_id, data, user_id)`: 更新评论
- `delete_comment(comment_id, user_id)`: 删除评论
- `get_average_rating(recipe_id)`: 获取平均评分

**依赖**: Comment Model, Recipe Model

---

#### 6.2.4 文件服务 (FileService)

**职责**: 图片上传、压缩、存储

**关键接口**:
- `upload_image(file)`: 上传图片
- `validate_image(file)`: 验证图片格式和大小
- `compress_image(image)`: 压缩图片
- `delete_image(filename)`: 删除图片

**依赖**: Flask-Uploads, Pillow (Python Imaging Library)

**技术栈**: Pillow, os.path

---

## 7. 外部 API

**状态**: N/A - 当前版本不集成外部 API

**未来规划**:
- 营养数据 API (USDA 或 Edamam)
- 短信/邮件服务 API (SendGrid, Twilio)
- 支付网关 API (Stripe, 支付宝)
- 社交登录 API (微信, Google OAuth)

---

## 8. 核心工作流

### 8.1 用户注册和登录流程

```mermaid
sequenceDiagram
    actor U as 用户
    participant F as 前端应用
    participant A as 认证服务
    participant D as 数据库

    U->>F: 填写注册信息
    F->>A: POST /api/auth/register
    A->>D: 创建用户记录
    D-->>A: 返回用户 ID
    A-->>F: 注册成功

    Note over U,F: 用户登录流程
    U->>F: 输入用户名/密码
    F->>A: POST /api/auth/login
    A->>D: 验证用户信息
    D-->>A: 返回用户数据
    A->>A: 生成 JWT Token
    A-->>F: 返回 access_token
    F->>F: 存储 Token 到 localStorage
    F->>A: 后续请求携带 Token
```

---

### 8.2 菜谱创建流程

```mermaid
sequenceDiagram
    actor U as 用户
    participant F as 前端应用
    participant R as 菜谱服务
    participant FS as 文件服务
    participant D as 数据库
    participant S as 存储系统

    U->>F: 点击"创建菜谱"
    F->>F: 显示菜谱表单
    U->>F: 填写菜谱信息 + 上传图片
    F->>FS: 上传图片
    FS->>S: 保存图片到本地
    FS-->>F: 返回图片 URL
    F->>R: POST /api/recipes/ (带 Token)
    R->>D: 保存菜谱到数据库
    D-->>R: 返回菜谱 ID
    R-->>F: 创建成功
    F->>U: 跳转到菜谱详情页
```

---

### 8.3 菜谱搜索流程

```mermaid
sequenceDiagram
    actor U as 用户
    participant F as 前端应用
    participant R as 菜谱服务
    participant Cache as Redis 缓存
    participant D as 数据库

    U->>F: 输入搜索关键词
    F->>R: GET /api/recipes/?search=xxx
    R->>Cache: 检查缓存
    alt 缓存命中
        Cache-->>R: 返回缓存结果
    else 缓存未命中
        R->>D: 执行数据库查询
        D-->>R: 返回菜谱列表
        R->>Cache: 写入缓存
    end
    R-->>F: 返回菜谱列表
    F->>U: 显示搜索结果
```

---

## 9. 数据库架构

### 9.1 数据库架构设计

**数据库类型**: MySQL 5.7.44

**字符集**: utf8mb4 (支持 Emoji 和特殊字符)

**排序规则**: utf8mb4_unicode_ci

### 9.2 核心表结构

```sql
-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(255),
    bio TEXT,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 菜谱表
CREATE TABLE recipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    prep_time INT NOT NULL,
    cook_time INT,
    servings INT,
    ingredients TEXT,
    instructions TEXT,
    image VARCHAR(255),
    author_id INT NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_author (author_id),
    INDEX idx_difficulty (difficulty),
    INDEX idx_created (created_at),
    FULLTEXT INDEX idx_search (title, description, ingredients)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 评论表
CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    parent_id INT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
    INDEX idx_recipe (recipe_id),
    INDEX idx_user (user_id),
    INDEX idx_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 收藏表
CREATE TABLE favorites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, recipe_id),
    INDEX idx_user (user_id),
    INDEX idx_recipe (recipe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 9.3 索引策略

**用户表**:
- `idx_username`: 用户名唯一索引（登录查询）
- `idx_email`: 邮箱唯一索引（注册和登录）

**菜谱表**:
- `idx_author`: 作者索引（查询用户菜谱）
- `idx_difficulty`: 难度索引（筛选查询）
- `idx_created`: 创建时间索引（排序查询）
- `idx_search`: 全文索引（关键词搜索）

**评论表**:
- `idx_recipe`: 菜谱索引（查询菜谱评论）
- `idx_user`: 用户索引（查询用户评论）
- `idx_parent`: 父评论索引（查询回复）

**收藏表**:
- `unique_favorite`: 唯一约束（防止重复收藏）
- `idx_user`: 用户索引（查询用户收藏）
- `idx_recipe`: 菜谱索引（查询收藏数）

---

## 10. 前端架构

### 10.1 组件架构

**组件组织**:
```
frontend/src/
├── components/           # 可复用组件
│   ├── common/          # 通用组件
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   └── Modal.vue
│   ├── recipe/          # 菜谱相关组件
│   │   ├── RecipeCard.vue
│   │   ├── RecipeList.vue
│   │   ├── RecipeDetail.vue
│   │   └── RecipeForm.vue
│   ├── comment/         # 评论组件
│   │   ├── CommentList.vue
│   │   ├── CommentItem.vue
│   │   └── CommentForm.vue
│   └── auth/            # 认证组件
│       ├── LoginForm.vue
│       └── RegisterForm.vue
├── views/               # 页面组件
│   ├── Home.vue
│   ├── Login.vue
│   ├── Register.vue
│   ├── RecipeDetail.vue
│   ├── CreateRecipe.vue
│   └── Profile.vue
├── router/              # 路由配置
│   └── index.ts
├── stores/              # Pinia 状态管理
│   ├── auth.ts
│   ├── recipe.ts
│   ├── comment.ts
│   └── user.ts
├── services/            # API 服务
│   ├── api.ts           # Axios 实例配置
│   ├── auth.service.ts
│   ├── recipe.service.ts
│   └── comment.service.ts
├── types/               # TypeScript 类型定义
│   ├── user.ts
│   ├── recipe.ts
│   └── comment.ts
├── utils/               # 工具函数
│   ├── validators.ts
│   ├── formatters.ts
│   └── constants.ts
├── assets/              # 静态资源
│   ├── styles/
│   │   ├── main.scss
│   │   └── variables.scss
│   └── images/
├── App.vue
└── main.ts
```

**组件模板**:
```vue
<!-- frontend/src/components/recipe/RecipeCard.vue -->
<template>
  <el-card class="recipe-card" @click="goToDetail">
    <img :src="recipe.image" :alt="recipe.title" class="recipe-image" />
    <div class="recipe-info">
      <h3>{{ recipe.title }}</h3>
      <p>{{ recipe.description }}</p>
      <div class="recipe-meta">
        <el-tag :type="difficultyType">{{ difficultyText }}</el-tag>
        <span class="prep-time">{{ recipe.prep_time }} 分钟</span>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import type { Recipe } from '@/types/recipe';

interface Props {
  recipe: Recipe;
}

const props = defineProps<Props>();
const router = useRouter();

const difficultyType = computed(() => {
  const map = { easy: 'success', medium: 'warning', hard: 'danger' };
  return map[props.recipe.difficulty];
});

const difficultyText = computed(() => {
  const map = { easy: '简单', medium: '中等', hard: '困难' };
  return map[props.recipe.difficulty];
});

const goToDetail = () => {
  router.push(`/recipes/${props.recipe.id}`);
};
</script>

<style scoped lang="scss">
.recipe-card {
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-4px);
  }
}

.recipe-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.recipe-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}
</style>
```

---

### 10.2 状态管理架构

**Pinia Store 结构**:
```typescript
// frontend/src/stores/auth.ts
import { defineStore } from 'pinia';
import { login, register, logout } from '@/services/auth.service';
import type { User, UserCreate } from '@/types/user';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isAuthenticated: false,
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated && !!state.token,
  },

  actions: {
    async login(credentials: { username: string; password: string }) {
      const response = await login(credentials);
      this.user = response.user;
      this.token = response.access_token;
      this.isAuthenticated = true;
      localStorage.setItem('access_token', response.access_token);
    },

    async register(userData: UserCreate) {
      await register(userData);
    },

    async logout() {
      await logout();
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
    },

    async fetchProfile() {
      if (this.token) {
        const user = await fetchProfile();
        this.user = user;
        this.isAuthenticated = true;
      }
    },
  },
});
```

**状态管理模式**:
- **集中式状态**: 所有全局状态存储在 Pinia Store 中
- **模块化设计**: 按功能划分 Store（auth, recipe, comment, user）
- **持久化**: Token 存储在 localStorage，用户信息在页面刷新时重新获取
- **响应式**: 使用 Vue 3 Composition API 的 computed 和 watch

---

### 10.3 路由架构

**路由组织**:
```typescript
// frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/recipes/:id',
    name: 'RecipeDetail',
    component: () => import('@/views/RecipeDetail.vue'),
  },
  {
    path: '/recipes/create',
    name: 'CreateRecipe',
    component: () => import('@/views/CreateRecipe.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/recipes/:id/edit',
    name: 'EditRecipe',
    component: () => import('@/views/EditRecipe.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if (to.meta.requiresGuest && authStore.isLoggedIn) {
    next({ name: 'Home' });
  } else {
    next();
  }
});

export default router;
```

**路由模式**: HTML5 History Mode (`createWebHistory`)

---

### 10.4 前端服务层

**API 客户端设置**:
```typescript
// frontend/src/services/api.ts
import axios, { AxiosInstance, AxiosError } from 'axios';
import { useAuthStore } from '@/stores/auth';
import { ElMessage } from 'element-plus';

const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：自动添加 Token
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：统一错误处理
apiClient.interceptors.response.use(
  (response) => response.data,
  (error: AxiosError<{ message: string }>) => {
    const authStore = useAuthStore();

    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          ElMessage.error('未授权，请重新登录');
          authStore.logout();
          window.location.href = '/login';
          break;
        case 403:
          ElMessage.error('无权限访问');
          break;
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
        case 500:
          ElMessage.error('服务器错误，请稍后重试');
          break;
        default:
          ElMessage.error(data?.message || '请求失败');
      }
    } else {
      ElMessage.error('网络连接失败');
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

**服务示例**:
```typescript
// frontend/src/services/recipe.service.ts
import apiClient from './api';
import type { Recipe, RecipeCreate, RecipeUpdate } from '@/types/recipe';

export const recipeService = {
  async list(params?: {
    page?: number;
    per_page?: number;
    search?: string;
    difficulty?: string;
  }) {
    return apiClient.get('/api/recipes/', { params });
  },

  async get(id: number) {
    return apiClient.get(`/api/recipes/${id}`);
  },

  async create(data: RecipeCreate) {
    return apiClient.post('/api/recipes/', data);
  },

  async update(id: number, data: RecipeUpdate) {
    return apiClient.put(`/api/recipes/${id}`, data);
  },

  async delete(id: number) {
    return apiClient.delete(`/api/recipes/${id}`);
  },

  async search(keyword: string) {
    return apiClient.get('/api/recipes/', { params: { search: keyword } });
  },
};
```

---

## 11. 后端架构

### 11.1 服务架构

**后端项目结构**:
```
backend/
├── app/
│   ├── __init__.py         # Flask 应用工厂
│   ├── config.py           # 配置管理
│   ├── models/             # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── recipe.py
│   │   └── comment.py
│   ├── routes/             # API 路由（蓝图）
│   │   ├── __init__.py
│   │   ├── auth.py         # 认证相关路由
│   │   ├── recipes.py      # 菜谱相关路由
│   │   ├── comments.py     # 评论相关路由
│   │   ├── users.py        # 用户相关路由
│   │   └── uploads.py      # 文件上传路由
│   ├── services/           # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── recipe_service.py
│   │   └── file_service.py
│   ├── utils/              # 工具函数
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── helpers.py
│   └── extensions.py       # Flask 扩展初始化
├── tests/                  # 测试
│   ├── test_auth.py
│   ├── test_recipes.py
│   └── test_comments.py
├── migrations/             # 数据库迁移（Alembic）
├── static/                 # 静态文件
│   └── uploads/            # 上传的图片
├── run.py                  # 应用入口
├── init_db.py              # 数据库初始化脚本
└── requirements.txt        # Python 依赖
```

---

### 11.2 数据库架构

**Schema 设计** (已在第 9 节详细描述)

**数据访问层 (Repository 模式)**:
```python
# backend/app/models/recipe.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.Enum('easy', 'medium', 'hard'), nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    author = db.relationship('User', backref=db.backref('recipes', lazy=True))
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'image': self.image,
            'author_id': self.author_id,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
```

---

### 11.3 认证和授权架构

**Auth Flow**:
```mermaid
sequenceDiagram
    participant C as 客户端
    participant M as JWT Middleware
    participant R as 受保护路由
    participant S as Auth Service

    C->>M: 请求 + Token (Authorization Header)
    M->>M: 验证 Token 签名和有效期
    alt Token 有效
        M->>M: 提取用户信息 (user_id)
        M->>R: 继续处理请求（附带 current_user）
        R->>S: 业务逻辑
        S-->>R: 返回数据
        R-->>C: 200 OK + 数据
    else Token 无效/过期
        M-->>C: 401 Unauthorized
    end
```

**Middleware/Guards**:
```python
# backend/app/utils/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def jwt_required_custom():
    """自定义 JWT 装饰器"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                current_user = User.query.get(current_user_id)

                if not current_user or not current_user.is_active:
                    return jsonify({'message': '用户不存在或已被禁用'}), 401

                return fn(current_user=current_user, *args, **kwargs)
            except Exception as e:
                return jsonify({'message': str(e)}), 401
        return wrapper
    return decorator
```

**使用示例**:
```python
# backend/app/routes/recipes.py
from flask import request, jsonify
from app.utils.decorators import jwt_required_custom
from app.services.recipe_service import RecipeService

@bp.route('/recipes/', methods=['POST'])
@jwt_required_custom()
def create_recipe(current_user):
    data = request.get_json()
    recipe = RecipeService.create_recipe(data, current_user.id)
    return jsonify(recipe.to_dict()), 201
```

---

## 12. 统一项目结构

**当前项目结构**:
```
myproject/
├── frontend/              # 前端应用 (Vue 3)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── assets/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── backend/               # 后端应用 (Flask)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── static/
│   │   └── uploads/
│   ├── tests/
│   ├── migrations/
│   ├── run.py
│   ├── init_db.py
│   └── requirements.txt
│
├── docs/                  # 共享文档
│   ├── prd.md
│   ├── architecture.md    # 本文档
│   ├── api-documentation.md
│   ├── brief.md
│   ├── database-setup.md
│   └── development-setup.md
│
├── scripts/               # 共享脚本
│   ├── init-project.sh
│   └── dev-start.sh
│
├── infrastructure/        # 基础设施代码
│   ├── nginx/
│   │   └── default.conf
│   └── docker/
│       ├── Dockerfile.frontend
│       ├── Dockerfile.backend
│       └── docker-compose.yml
│
└── README.md
```

---

## 13. 开发工作流

### 13.1 本地开发设置

**前置条件**:
```bash
# 前端
Node.js >= 16.x
npm >= 8.x

# 后端
Python >= 3.8
pip >= 20.x

# 数据库
MySQL 5.7.44 或 SQLite (开发环境)
Redis >= 6.0 (可选，用于缓存)
```

**初始化设置**:
```bash
# 1. 克隆项目
git clone <repository-url>
cd myproject

# 2. 后端设置
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
python init_db.py  # 初始化数据库

# 3. 前端设置
cd ../frontend
npm install
cp .env.example .env.local  # 配置环境变量

# 4. 启动服务（见下方）
```

---

### 13.2 开发命令

**启动所有服务**:
```bash
# 终端 1 - 启动后端
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python run.py

# 终端 2 - 启动前端
cd frontend
npm run dev
```

**仅启动前端**:
```bash
cd frontend
npm run dev
# 访问 http://localhost:8081
```

**仅启动后端**:
```bash
cd backend
venv\Scripts\activate
python run.py
# API 访问 http://localhost:5000
```

**运行测试**:
```bash
# 前端测试
cd frontend
npm run test           # 单元测试
npm run test:e2e      # E2E 测试

# 后端测试
cd backend
pytest tests/         # 运行所有测试
pytest tests/test_auth.py -v  # 运行特定测试
pytest --cov=app tests/  # 测试覆盖率
```

---

### 13.3 环境配置

**前端 (.env.local)**:
```bash
# API Base URL
VITE_API_BASE_URL=http://localhost:5000

# 应用配置
VITE_APP_TITLE=菜谱分享系统
VITE_UPLOAD_MAX_SIZE=5242880
```

**后端 (.env 或 config.py)**:
```bash
# Flask 配置
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=sqlite:///recipe_platform.db
# 生产环境:
# DATABASE_URL=mysql+pymysql://user:password@localhost/recipe_db

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# 文件上传配置
UPLOAD_FOLDER=static/uploads/images
MAX_CONTENT_LENGTH=5242880

# Redis 配置（可选）
REDIS_URL=redis://localhost:6379/0
```

---

## 14. 部署架构

### 14.1 部署策略

**前端部署**:
- **平台**: Nginx 静态文件服务
- **构建命令**: `npm run build`
- **输出目录**: `frontend/dist/`
- **CDN/边缘**: N/A（本地部署，暂无 CDN）

**后端部署**:
- **平台**: Gunicorn WSGI 服务器 + Nginx 反向代理
- **构建命令**: 无需构建，Python 解释执行
- **部署方法**:
  1. 使用 Gunicorn 启动 Flask 应用
  2. Nginx 反向代理 `/api/*` 到 Gunicorn
  3. Nginx 直接服务前端静态文件

---

### 14.2 CI/CD Pipeline

**GitHub Actions 示例** (可选):
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm run test
      - name: Build
        run: |
          cd frontend
          npm run build

  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/

  deploy:
    needs: [frontend-test, backend-test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to server
        run: |
          # 部署脚本
          ssh user@server 'cd /app && git pull && ./scripts/deploy.sh'
```

---

### 14.3 环境配置

| 环境 | 前端 URL | 后端 URL | 用途 |
|------|----------|----------|------|
| Development | http://localhost:8081 | http://localhost:5000 | 本地开发 |
| Staging | https://staging.example.com | https://api-staging.example.com | 预发布测试 |
| Production | https://example.com | https://api.example.com | 生产环境 |

---

## 15. 安全和性能

### 15.1 安全要求

**前端安全**:
- **CSP Headers**: 配置 Content-Security-Policy，限制资源来源
- **XSS 防护**: Vue 3 自动转义输出，避免 `v-html` 使用用户输入
- **安全存储**: 敏感信息（Token）存储在 localStorage（需配合 HTTPS）
- **HTTPS**: 生产环境强制使用 HTTPS

**后端安全**:
- **输入验证**: 所有用户输入验证（长度、格式、类型）
- **Rate Limiting**: 使用 Flask-Limit 限制 API 请求频率
- **CORS Policy**: 配置 Flask-CORS，仅允许可信域名
- **SQL 注入防护**: 使用 SQLAlchemy 参数化查询

**认证安全**:
- **Token 存储**: JWT 存储在 localStorage（Access Token）+ HttpOnly Cookie（Refresh Token）
- **会话管理**: JWT Access Token 有效期 1 小时，Refresh Token 7 天
- **密码策略**: bcrypt 加密，最小 8 位，包含字母和数字

---

### 15.2 性能优化

**前端性能**:
- **Bundle Size 目标**: 主包 < 500KB，gzip 压缩后 < 150KB
- **加载策略**: 路由级别代码分割（Lazy Loading）
- **缓存策略**:
  - 静态资源：浏览器缓存（1 年）
  - API 数据：内存缓存（5 分钟）

**后端性能**:
- **响应时间目标**: API < 500ms (P95)
- **数据库优化**:
  - 索引优化（详见第 9.3 节）
  - 查询优化（避免 N+1，使用 Eager Loading）
- **缓存策略**:
  - Redis 缓存热门菜谱（TTL: 1 小时）
  - 缓存搜索结果（TTL: 15 分钟）

---

## 16. 测试策略

### 16.1 测试金字塔

```
           E2E Tests
          /        \
    Integration Tests
    /              \
Frontend Unit  Backend Unit
```

**测试比例**: 70% 单元测试 + 20% 集成测试 + 10% E2E 测试

---

### 16.2 测试组织

**前端测试**:
```
frontend/src/
├── components/
│   ├── recipe/
│   │   ├── RecipeCard.vue
│   │   └── RecipeCard.spec.ts     # 组件单元测试
│   └── auth/
│       ├── LoginForm.vue
│       └── LoginForm.spec.ts
├── views/
│   └── RecipeDetail.spec.ts       # 视图测试
├── stores/
│   └── auth.spec.ts               # Store 测试
└── services/
    └── recipe.service.spec.ts     # 服务测试
```

**后端测试**:
```
backend/tests/
├── test_auth.py                   # 认证测试
├── test_recipes.py                # 菜谱测试
├── test_comments.py               # 评论测试
├── test_users.py                  # 用户测试
└── conftest.py                    # Pytest 配置
```

**E2E 测试**:
```
frontend/tests/e2e/
├── auth.spec.cy.ts                # 认证流程
├── recipe.spec.cy.ts              # 菜谱 CRUD
└── search.spec.cy.ts              # 搜索功能
```

---

### 16.3 测试示例

**前端组件测试**:
```typescript
// frontend/src/components/recipe/RecipeCard.spec.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import RecipeCard from './RecipeCard.vue';
import type { Recipe } from '@/types/recipe';

describe('RecipeCard', () => {
  const mockRecipe: Recipe = {
    id: 1,
    title: '番茄炒蛋',
    difficulty: 'easy',
    prep_time: 10,
    ingredients: '...',
    instructions: '...',
    author_id: 1,
    created_at: '2025-12-24T00:00:00Z',
    updated_at: '2025-12-24T00:00:00Z',
  };

  it('renders recipe title correctly', () => {
    const wrapper = mount(RecipeCard, {
      props: { recipe: mockRecipe },
    });
    expect(wrapper.text()).toContain('番茄炒蛋');
  });

  it('displays correct difficulty tag', () => {
    const wrapper = mount(RecipeCard, {
      props: { recipe: mockRecipe },
    });
    const tag = wrapper.find('.el-tag');
    expect(tag.text()).toBe('简单');
  });
});
```

**后端 API 测试**:
```python
# backend/tests/test_recipes.py
import pytest
from app import create_app, db
from app.models.recipe import Recipe

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_recipes(client):
    rv = client.get('/api/recipes/')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'recipes' in data
    assert isinstance(data['recipes'], list)

def test_create_recipe(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    data = {
        'title': '测试菜谱',
        'difficulty': 'easy',
        'prep_time': 10,
        'ingredients': '...',
        'instructions': '...'
    }
    rv = client.post('/api/recipes/', json=data, headers=headers)
    assert rv.status_code == 201
    response_data = rv.get_json()
    assert response_data['title'] == '测试菜谱'
```

**E2E 测试**:
```typescript
// frontend/tests/e2e/recipe.spec.cy.ts
describe('Recipe E2E', () => {
  beforeEach(() => {
    cy.login('testuser', 'password123');
  });

  it('creates a new recipe', () => {
    cy.visit('/recipes/create');
    cy.get('[data-testid="recipe-title"]').type('红烧肉');
    cy.get('[data-testid="recipe-difficulty"]').select('medium');
    cy.get('[data-testid="recipe-prep-time"]').type('30');
    cy.get('[data-testid="recipe-ingredients"]').type('五花肉...');
    cy.get('[data-testid="recipe-instructions"]').type('步骤...');
    cy.get('[data-testid="submit-btn"]').click();

    cy.url().should('include', '/recipes/');
    cy.contains('红烧肉').should('be.visible');
  });
});
```

---

## 17. 编码标准

### 17.1 关键全栈规则

**⚠️ 重要**: 这些是 AI 开发代理必须遵守的最小化但关键的标准。

1. **TypeScript 类型安全**: 前端所有组件和函数必须使用 TypeScript 类型定义，禁止使用 `any`
2. **API 调用统一**: 所有 API 调用必须通过 Service 层（`services/`），禁止组件直接使用 Axios
3. **环境变量抽象**: 后端禁止直接使用 `os.environ`，必须通过 `config.py` 统一管理
4. **错误处理统一**: 所有 API 路由必须使用统一错误处理器（`utils/error_handlers.py`）
5. **状态更新不可变**: Pinia Store 状态更新不可直接修改，必须通过 actions
6. **密码安全**: 密码字段禁止记录日志，传输必须使用 HTTPS
7. **SQL 注入防护**: 禁止字符串拼接 SQL，必须使用 SQLAlchemy 参数化查询
8. **认证检查**: 所有需要认证的路由必须使用 `@jwt_required_custom()` 装饰器

---

### 17.2 命名规范

| 元素 | 前端 (Vue/TS) | 后端 (Python) | 示例 |
|------|---------------|---------------|------|
| 组件 | PascalCase | - | `UserProfile.vue` |
| Hooks | camelCase with 'use' | - | `useAuth.ts` |
| API 路由 | - | kebab-case | `/api/user-profile` |
| 数据库表 | - | snake_case | `user_profiles` |
| 函数/方法 | camelCase | snake_case | `getUserData()` / `get_user_data()` |
常量 | UPPER_SNAKE_CASE | UPPER_SNAKE_CASE | `API_BASE_URL` / `MAX_UPLOAD_SIZE` |
TypeScript 接口 | PascalCase | - | `interface User {}` |
Python 类 | - | PascalCase | `class UserService:` |

---

## 18. 错误处理策略

### 18.1 错误响应格式

```typescript
// frontend/src/types/error.ts
interface ApiError {
  error: {
    code: string;           // 错误代码 (如: 'AUTH_INVALID_CREDENTIALS')
    message: string;        // 用户友好的错误信息
    details?: Record<string, any>;  // 额外错误详情
    timestamp: string;      // ISO 8601 时间戳
    requestId: string;      // 请求追踪 ID
  };
}
```

---

### 18.2 前端错误处理

```typescript
// frontend/src/utils/error-handler.ts
import { ElMessage } from 'element-plus';
import type { AxiosError } from 'axios';
import router from '@/router';

export function handleApiError(error: AxiosError<ApiError>) {
  if (error.response) {
    const { status, data } = error.response;

    switch (status) {
      case 401:
        ElMessage.error('登录已过期，请重新登录');
        // 清除本地存储并跳转到登录页
        localStorage.removeItem('access_token');
        router.push('/login');
        break;
      case 403:
        ElMessage.error('您没有权限执行此操作');
        break;
      case 404:
        ElMessage.error('请求的资源不存在');
        break;
      case 422:
        ElMessage.error(data.error.message || '请求参数验证失败');
        break;
      case 500:
        ElMessage.error('服务器内部错误，请稍后重试');
        break;
      default:
        ElMessage.error(data.error.message || '请求失败');
    }
  } else if (error.request) {
    ElMessage.error('网络连接失败，请检查您的网络');
  } else {
    ElMessage.error('请求配置错误');
  }

  // 记录错误到监控服务（如 Sentry）
  console.error('API Error:', error);
}
```

---

### 18.3 后端错误处理

```python
# backend/app/utils/error_handlers.py
from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging
from datetime import datetime

def setup_error_handlers(app):
    """统一错误处理器"""

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """处理 HTTP 异常"""
        response = {
            "error": {
                "code": e.name.upper().replace(' ', '_'),
                "message": e.description,
                "timestamp": datetime.utcnow().isoformat(),
                "requestId": str(g.request_id) if hasattr(g, 'request_id') else None
            }
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """处理未捕获的异常"""
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)

        response = {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "服务器内部错误",
                "timestamp": datetime.utcnow().isoformat(),
                "requestId": str(g.request_id) if hasattr(g, 'request_id') else None
            }
        }
        return jsonify(response), 500

    @app.errorhandler(404)
    def handle_not_found(e):
        """处理 404 错误"""
        response = {
            "error": {
                "code": "NOT_FOUND",
                "message": "请求的资源不存在",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        return jsonify(response), 404
```

---

## 19. 监控和可观测性

### 19.1 监控栈

**前端监控**:
- **错误追踪**: (待集成) Sentry 或 LogRocket
- **性能监控**: (待集成) Google Analytics 或 Web Vitals
- **用户行为**: (可选) Hotjar 或 Mixpanel

**后端监控**:
- **应用监控**: (待集成) Sentry 或 DataDog
- **错误追踪**: Python logging + 日志文件
- **性能监控**: (待集成) Prometheus + Grafana

**日志策略**:
- 前端：Console (开发) + Sentry (生产)
- 后端：文件日志（按日期轮转）
- 日志级别：DEBUG (开发) / INFO (生产)

---

### 19.2 关键指标

**前端指标**:
- **Core Web Vitals**:
  - LCP (Largest Contentful Paint) < 2.5s
  - FID (First Input Delay) < 100ms
  - CLS (Cumulative Layout Shift) < 0.1
- **JavaScript 错误率**: < 1%
- **API 响应时间 (P95)**: < 500ms
- **页面加载时间 (P95)**: < 3s

**后端指标**:
- **请求速率**: RPS (Requests Per Second)
- **错误率**: < 1%
- **响应时间 (P95)**: < 500ms
- **数据库查询性能**: < 100ms (P95)
- **缓存命中率**: > 80%

---

## 20. 检查清单结果报告

**状态**: ⚠️ 待执行

**说明**: 本架构文档已完成创建。接下来将执行 `architect-checklist` 进行架构质量检查和验证。

**下一步**:
1. 执行 `execute-checklist architect-checklist`
2. 根据检查清单结果完善架构文档
3. 生成拆分的架构子文档（如 `tech-stack.md`, `database-schema.md` 等）

---

## 附录

### A. 术语表

| 术语 | 定义 |
|------|------|
| **SPA** | Single Page Application，单页应用 |
| **RESTful API** | Representational State Transfer API，资源导向的 API 设计 |
| **JWT** | JSON Web Token，用于身份验证的令牌 |
| **ORM** | Object-Relational Mapping，对象关系映射 |
| **CRUD** | Create, Read, Update, Delete，增删改查操作 |
| **SSR** | Server-Side Rendering，服务端渲染 |
| **CSR** | Client-Side Rendering，客户端渲染 |
| **PWA** | Progressive Web App，渐进式 Web 应用 |
| **E2E** | End-to-End，端到端测试 |
| **TTL** | Time To Live，缓存过期时间 |

### B. 参考资源

- [Vue 3 官方文档](https://vuejs.org/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Element Plus 文档](https://element-plus.org/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [REST API 设计指南](https://restfulapi.net/)
- [MySQL 5.7 官方文档](https://dev.mysql.com/doc/refman/5.7/en/)

### C. 联系信息

**架构师**: Winston (AI Architect)
**项目维护**: 开发团队
**文档状态**: ✅ 已完成初版

---

**文档结束** - 下一步：执行架构检查清单 🏗️
