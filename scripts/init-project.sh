#!/bin/bash
# 菜谱分享系统项目初始化脚本

echo "🚀 菜谱分享系统项目初始化开始..."

# 创建项目根目录结构
echo "📁 创建项目目录结构..."
mkdir -p frontend/{src/{components,views,router,store,api,utils,assets,styles},public,tests}
mkdir -p backend/{app/{models,routes,services,utils,migrations},config,tests}
mkdir -p docs/{api,architecture,user-guides}
mkdir -p docker/{frontend,backend}
mkdir -p scripts/{deployment,development,testing}
mkdir -p .github/workflows

# 创建前端基础文件
echo "📝 创建前端配置文件..."
cd frontend

# package.json
cat > package.json << 'EOF'
{
  "name": "recipe-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "test:unit": "vue-cli-service test:unit",
    "lint": "vue-cli-service lint"
  },
  "dependencies": {
    "vue": "^3.2.0",
    "vue-router": "^4.0.0",
    "vuex": "^4.0.0",
    "axios": "^0.27.0",
    "element-plus": "^2.2.0",
    "@element-plus/icons-vue": "^2.0.0"
  },
  "devDependencies": {
    "@vue/cli-plugin-typescript": "~5.0.0",
    "@vue/cli-plugin-router": "~5.0.0",
    "@vue/cli-plugin-vuex": "~5.0.0",
    "@vue/cli-plugin-eslint": "~5.0.0",
    "@vue/cli-plugin-unit-jest": "~5.0.0",
    "@vue/cli-service": "~5.0.0",
    "typescript": "~4.5.0",
    "sass": "^1.32.0",
    "sass-loader": "^12.0.0",
    "eslint": "^8.0.0",
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "@typescript-eslint/parser": "^5.0.0"
  }
}
EOF

# Vue配置文件
cat > vue.config.js << 'EOF'
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  }
})
EOF

# TypeScript配置
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "esnext",
    "lib": [
      "esnext",
      "dom",
      "dom.iterable"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.d.ts",
    "src/**/*.tsx",
    "src/**/*.vue"
  ],
  "exclude": [
    "node_modules"
  ]
}
EOF

# 主应用文件
cat > src/main.ts << 'EOF'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(store)
app.use(router)
app.use(ElementPlus)

app.mount('#app')
EOF

# App组件
cat > src/App.vue << 'EOF'
<template>
  <div id="app">
    <nav>
      <router-link to="/">首页</router-link> |
      <router-link to="/recipes">菜谱</router-link> |
      <router-link to="/about">关于</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
EOF

# 路由配置
cat > src/router/index.ts << 'EOF'
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/recipes',
    name: 'Recipes',
    component: () => import('@/views/Recipes.vue')
  },
  {
    path: '/recipes/:id',
    name: 'RecipeDetail',
    component: () => import('@/views/RecipeDetail.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
EOF

# Store配置
cat > src/store/index.ts << 'EOF'
import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    recipes: [],
    loading: false
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_RECIPES(state, recipes) {
      state.recipes = recipes
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    }
  },
  actions: {
    async fetchRecipes({ commit }) {
      commit('SET_LOADING', true)
      try {
        // TODO: 实现API调用
        const recipes = []
        commit('SET_RECIPES', recipes)
      } catch (error) {
        console.error('获取菜谱失败:', error)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.user
  }
})
EOF

# 创建示例页面组件
cat > src/views/Home.vue << 'EOF'
<template>
  <div class="home">
    <h1>菜谱分享系统</h1>
    <p>发现美味，分享快乐</p>
    <el-button type="primary" @click="$router.push('/recipes')">
      浏览菜谱
    </el-button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Home'
})
</script>

<style scoped>
.home {
  text-align: center;
  padding: 60px 20px;
}
</style>
EOF

cat > src/views/Recipes.vue << 'EOF'
<template>
  <div class="recipes">
    <h1>菜谱列表</h1>
    <div v-if="loading" class="loading">
      <el-loading-spinner></el-loading-spinner>
    </div>
    <div v-else>
      <el-row :gutter="20">
        <el-col v-for="recipe in recipes" :key="recipe.id" :span="8">
          <el-card class="recipe-card">
            <img :src="recipe.image" class="recipe-image">
            <h3>{{ recipe.title }}</h3>
            <p>{{ recipe.description }}</p>
            <el-button type="text" @click="viewRecipe(recipe.id)">
              查看详情
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Recipes',
  setup() {
    const store = useStore()
    const router = useRouter()

    const recipes = computed(() => store.state.recipes)
    const loading = computed(() => store.state.loading)

    const viewRecipe = (id: number) => {
      router.push(`/recipes/${id}`)
    }

    onMounted(() => {
      store.dispatch('fetchRecipes')
    })

    return {
      recipes,
      loading,
      viewRecipe
    }
  }
})
</script>

<style scoped>
.recipes {
  padding: 20px;
}

.recipe-card {
  margin-bottom: 20px;
}

.recipe-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>
EOF

cat > src/views/RecipeDetail.vue << 'EOF'
<template>
  <div class="recipe-detail">
    <h1>菜谱详情</h1>
    <p>菜谱ID: {{ $route.params.id }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RecipeDetail'
})
</script>
EOF

cat > src/views/About.vue << 'EOF'
<template>
  <div class="about">
    <h1>关于我们</h1>
    <p>菜谱分享系统 - 连接美食爱好者的平台</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'About'
})
</script>
EOF

# 环境配置文件
cat > .env.development << 'EOF'
VUE_APP_API_BASE_URL=http://localhost:5000/api
VUE_APP_ENV=development
EOF

cat > .env.production << 'EOF'
VUE_APP_API_BASE_URL=/api
VUE_APP_ENV=production
EOF

cd ..

# 创建后端基础文件
echo "📝 创建后端配置文件..."
cd backend

# requirements.txt
cat > requirements.txt << 'EOF'
Flask==2.2.0
Flask-SQLAlchemy==3.0.0
Flask-Migrate==4.0.0
Flask-JWT-Extended==4.4.0
Flask-CORS==3.0.10
Flask-Limiter==3.2.0
SQLAlchemy==1.4.0
PyMySQL==1.0.0
redis==4.3.0
celery==5.2.0
python-dotenv==0.19.0
marshmallow==3.17.0
Pillow==9.0.0
pytest==7.0.0
coverage==6.0.0
gunicorn==20.1.0
EOF

# 主应用文件
cat > app.py << 'EOF'
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.recipes import recipes_bp
    from app.routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF

# 配置文件
cat > config.py << 'EOF'
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://recipe_user:password@localhost/recipe_platform'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
EOF

# 创建应用包结构
mkdir -p app/{models,routes,services,utils,migrations}

# models/__init__.py
cat > app/__init__.py << 'EOF'
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
EOF

# 用户模型
cat > app/models/user.py << 'EOF'
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(200))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'bio': self.bio,
            'created_at': self.created_at.isoformat()
        }
EOF

# 菜谱模型
cat > app/models/recipe.py << 'EOF'
from datetime import datetime
from app import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # 分钟
    cook_time = db.Column(db.Integer)  # 分钟
    difficulty = db.Column(db.String(20))  # 简单/中等/困难
    servings = db.Column(db.Integer)
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    comments = db.relationship('Comment', backref='recipe', lazy=True)
    tags = db.relationship('Tag', secondary='recipe_tags', backref='recipes')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'difficulty': self.difficulty,
            'servings': self.servings,
            'image': self.image,
            'user_id': self.user_id,
            'author': self.author.username,
            'created_at': self.created_at.isoformat()
        }
EOF

# 创建基础路由文件
mkdir -p app/routes

cat > app/routes/auth.py << 'EOF'
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': '邮箱已存在'}), 400

    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        })

    return jsonify({'message': '邮箱或密码错误'}), 401
EOF

cat > app/routes/recipes.py << 'EOF'
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.recipe import Recipe
from app import db

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    recipes = Recipe.query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'recipes': [recipe.to_dict() for recipe in recipes.items],
        'total': recipes.total,
        'pages': recipes.pages,
        'current_page': page
    })

@recipes_bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    data = request.get_json()
    user_id = get_jwt_identity()

    recipe = Recipe(
        title=data['title'],
        description=data.get('description'),
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        prep_time=data.get('prep_time'),
        cook_time=data.get('cook_time'),
        difficulty=data.get('difficulty'),
        servings=data.get('servings'),
        user_id=user_id
    )

    db.session.add(recipe)
    db.session.commit()

    return jsonify(recipe.to_dict()), 201

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())
EOF

cat > app/routes/users.py << 'EOF'
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
EOF

# 环境配置文件
cat > .env << 'EOF'
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=mysql+pymysql://recipe_user:password@localhost/recipe_platform
REDIS_URL=redis://localhost:6379
EOF

cd ..

# 创建Docker配置
echo "🐳 创建Docker配置..."
cd docker

# docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    volumes:
      - ../frontend:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true
    depends_on:
      - backend

  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ../backend:/app
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=mysql+pymysql://recipe_user:password@mysql:3306/recipe_platform
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mysql
      - redis

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
EOF

# 前端Dockerfile
cat > frontend/Dockerfile << 'EOF'
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
EOF

# 后端Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
EOF

cd ..

# 创建根目录配置文件
echo "📋 创建项目配置文件..."

# README.md
cat > README.md << 'EOF'
# 菜谱分享系统

一个基于Vue 3 + Flask的现代化菜谱分享平台。

## 技术栈

### 前端
- Vue 3 + TypeScript
- Element Plus UI组件库
- Vue Router 4
- Vuex 4
- Axios

### 后端
- Python 3.9+
- Flask
- SQLAlchemy ORM
- JWT认证
- MySQL 5.7
- Redis

### 开发工具
- Docker & Docker Compose
- Git
- VS Code

## 快速开始

### 使用Docker（推荐）

1. 克隆项目
```bash
git clone <repository-url>
cd recipe-sharing-platform
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问应用
- 前端: http://localhost:8080
- 后端API: http://localhost:5000

### 本地开发

1. 安装依赖
```bash
# 前端
cd frontend
npm install

# 后端
cd ../backend
pip install -r requirements.txt
```

2. 配置数据库
```sql
CREATE DATABASE recipe_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 启动服务
```bash
# 启动MySQL和Redis
# 启动后端
cd backend
python app.py

# 启动前端
cd ../frontend
npm run serve
```

## 项目结构

```
recipe-sharing-platform/
├── frontend/          # Vue前端项目
├── backend/           # Flask后端项目
├── docs/             # 项目文档
├── docker/           # Docker配置
├── scripts/          # 部署脚本
└── README.md         # 项目说明
```

## 开发规范

### Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactore: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

### 代码规范
- 前端使用ESLint + Prettier
- 后端使用Black + Flake8
- 所有代码需要通过测试

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

MIT License
EOF

# .gitignore
cat > .gitignore << 'EOF'
# 依赖
node_modules/
__pycache__/
*.pyc
venv/
env/

# 环境配置
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志
*.log
logs/

# 上传文件
uploads/

# 构建输出
dist/
build/

# 数据库
*.db
*.sqlite

# 系统文件
.DS_Store
Thumbs.db
EOF

# 创建开发脚本
cd scripts

# 开发环境启动脚本
cat > dev-start.sh << 'EOF'
#!/bin/bash
echo "🚀 启动开发环境..."

# 启动后端
echo "启动后端服务..."
cd ../backend
source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
python app.py &
BACKEND_PID=$!

# 启动前端
echo "启动前端服务..."
cd ../frontend
npm install
npm run serve &
FRONTEND_PID=$!

echo "✅ 开发环境启动完成！"
echo "前端: http://localhost:8080"
echo "后端: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

chmod +x dev-start.sh

cd ..

echo "✅ 项目初始化完成！"
echo ""
echo "📁 项目结构已创建"
echo "📝 配置文件已生成"
echo "🐳 Docker配置已就绪"
echo ""
echo "🎯 下一步："
echo "1. cd frontend && npm install"
echo "2. cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "3. 配置MySQL数据库连接"
echo "4. 运行数据库迁移"
echo "5. 启动开发服务器"
echo ""
echo "📖 详细文档请查看 docs/ 目录"