# 菜谱分享系统 - 开发环境搭建指南

## 团队组建方案

### 核心团队配置（3人精简团队）

#### 1. 全栈技术负责人 (1人)
**技能要求**：
- 3年以上全栈开发经验
- 精通Python/Vue技术栈
- 有项目管理和技术决策能力
- 具备基础的产品思维

**主要职责**：
- 技术架构设计和选型
- 后端核心功能开发
- 前端架构搭建和关键组件开发
- 团队技术指导和代码审核
- 项目进度把控和风险识别
- 与产品需求的对接和转化

**工作占比**：后端40% + 前端30% + 管理30%

#### 2. 前端开发工程师 (1人)
**技能要求**：
- Vue 3 + TypeScript
- Element Plus等UI组件库
- 响应式设计和移动端适配
- 基础的后端API对接能力

**主要职责**：
- 用户界面和组件开发
- 前端路由和状态管理
- API接口对接和数据交互
- 前端性能优化
- 用户体验实现和bug修复
- 协助产品界面设计和调整

**工作占比**：前端开发70% + UI设计20% + 测试10%

#### 3. 后端开发工程师 (1人)
**技能要求**：
- Python 3.9+ + Flask
- MySQL数据库设计和优化
- Redis缓存和任务队列
- RESTful API开发
- 基础的运维部署能力

**主要职责**：
- API接口开发和文档编写
- 数据库设计和维护
- 业务逻辑实现
- 用户认证和权限管理
- 服务端部署和运维
- 协助前端接口调试

**工作占比**：后端开发80% + 运维部署15% + 数据管理5%

### 团队协作特点

**1. 一人多能，职责交叉**
- 全栈负责人：技术决策 + 核心开发 + 项目管理
- 前端工程师：界面开发 + UI设计 + 基础测试
- 后端工程师：API开发 + 数据库 + 运维部署

**2. 敏捷开发模式**
- 2周一个冲刺周期
- 每日站会同步进度
- 代码交叉审核机制
- 快速迭代和反馈

**3. 外部协作支持**
- **UI设计外包**：关键页面设计阶段可外包
- **测试用户群体**：邀请10-20名种子用户参与测试
- **技术顾问**：复杂技术问题可寻求外部专家咨询
- **内容运营**：后期可考虑兼职或外包

### 3人团队工作流程

#### 每日工作安排
- **9:30-10:00**：每日站会（进度同步 + 问题讨论）
- **10:00-12:00**：专注开发时间
- **14:00-15:30**：代码审核 + 问题解决
- **15:30-17:00**：功能开发 + 测试
- **17:00-17:30**：当日总结 + 明日计划

#### 每周工作节奏
- **周一**：周会 + 本周目标制定
- **周二-周三**：核心功能开发
- **周四**：代码审核 + 功能测试
- **周五**：部署演示 + 周总结

#### 分工协作模式
- **并行开发**：前后端可同时进行，API先行设计
- **交叉支持**：人员互补，前后端互相协助调试
- **轮岗机制**：定期轮换负责模块，提升团队整体技能

## 开发环境搭建

### 系统要求
- **操作系统**：Windows 10/11、macOS 10.14+、Ubuntu 18.04+
- **内存**：8GB以上推荐
- **存储**：50GB可用空间
- **网络**：稳定的互联网连接

### 核心工具安装

#### 1. 前端开发环境
```bash
# Node.js 16+ 版本
node --version  # v16.0.0+
npm --version   # 8.0.0+

# 推荐使用 yarn 包管理器
npm install -g yarn

# Vue CLI 工具
npm install -g @vue/cli
```

#### 2. 后端开发环境
```bash
# Python 3.9+
python --version  # 3.9.0+

# 虚拟环境工具
python -m pip install --upgrade pip
pip install virtualenv

# 数据库客户端
# MySQL Workbench 或 DBeaver
# Redis Desktop Manager
```

#### 3. 开发工具推荐
- **IDE**：VS Code / WebStorm / PyCharm
- **Git客户端**：SourceTree / GitKraken / 命令行
- **API测试**：Postman / Insomnia
- **数据库管理**：DBeaver / MySQL Workbench

### 项目环境配置

#### 1. 创建项目目录结构
```bash
# 主项目目录
recipe-sharing-platform/
├── frontend/          # Vue前端项目
├── backend/           # Flask后端项目
├── docs/             # 项目文档
├── docker/           # Docker配置文件
├── scripts/          # 部署和工具脚本
└── README.md         # 项目说明
```

#### 2. 前端环境配置
```bash
# 进入前端目录
cd frontend

# 创建Vue 3项目
vue create recipe-app

# 选择配置
- Choose Vue version: 3.x
- TypeScript: Yes
- Router: Yes
- Vuex: Yes
- CSS Pre-processors: Yes (Sass/SCSS)
- Linter / Formatter: Yes (ESLint + Prettier)
- Unit Testing: Yes (Jest)

# 安装UI组件库
npm install element-plus
npm install @element-plus/icons-vue

# 安装其他依赖
npm install axios
npm install vue-router@4
npm install vuex@4
npm install sass
```

#### 3. 后端环境配置
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-jwt-extended
pip install flask-cors
pip install flask-limiter
pip install redis
pip install celery
pip install pymysql
pip install python-dotenv
pip install marshmallow
pip install pillow
pip install pytest
```

### 数据库配置

#### 1. MySQL 5.7.44 配置
```sql
-- 创建数据库
CREATE DATABASE recipe_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'recipe_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON recipe_platform.* TO 'recipe_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 2. Redis 配置
```bash
# Windows: 下载Redis for Windows
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server

# 启动Redis服务
redis-server
```

### 开发工具配置

#### 1. VS Code 扩展推荐
```json
{
  "recommendations": [
    "vue.volar",
    "bradlc.vscode-tailwindcss",
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode-remote.remote-containers"
  ]
}
```

#### 2. Git 配置
```bash
# 全局配置
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 项目初始化
git init
git add .
git commit -m "Initial commit: Project setup"

# 创建分支策略
git checkout -b develop
git checkout -b feature/user-auth
git checkout -b feature/recipe-management
```

### Docker 配置（可选）

#### 1. 前端 Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

#### 2. 后端 Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### 3. docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - mysql
      - redis
    environment:
      - DATABASE_URL=mysql+pymysql://recipe_user:password@mysql:3306/recipe_platform
      - REDIS_URL=redis://redis:6379

  mysql:
    image: mysql:5.7
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=recipe_platform
      - MYSQL_USER=recipe_user
      - MYSQL_PASSWORD=password
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  mysql_data:
```

### 开发流程规范

#### 1. Git 工作流
```
main (生产环境)
├── develop (开发环境)
    ├── feature/user-auth
    ├── feature/recipe-crud
    ├── feature/search-filter
    └── hotfix/critical-bug
```

#### 2. 代码提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

#### 3. 开发环境启动步骤
```bash
# 1. 克隆项目
git clone <repository-url>
cd recipe-sharing-platform

# 2. 启动后端
cd backend
source venv/bin/activate
flask run  # 或 python app.py

# 3. 启动前端
cd frontend
npm run serve

# 4. 启动数据库服务
# MySQL 和 Redis 服务需要单独启动

# 5. 使用 Docker（推荐）
docker-compose up -d
```

### 下一步行动

1. **团队成员招募**：按配置要求招聘合适人员
2. **环境统一**：确保所有开发人员环境一致
3. **工具培训**：对团队进行工具使用培训
4. **规范制定**：制定详细的开发规范和流程
5. **项目初始化**：创建Git仓库，设置CI/CD流程

---

**更新时间**：2025年12月11日
**文档版本**：v1.0