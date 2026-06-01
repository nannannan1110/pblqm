# MySQL数据库配置指南

## 数据库连接配置

### 1. MySQL 5.7.44 连接信息
- **服务端口**: 3306
- **默认用户**: root
- **数据库**: recipe_platform

### 2. 创建数据库和用户

请使用以下SQL命令创建数据库和用户：

```sql
-- 创建数据库
CREATE DATABASE recipe_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建专用用户
CREATE USER 'recipe_user'@'localhost' IDENTIFIED BY 'recipe_password_2024';

-- 授权
GRANT ALL PRIVILEGES ON recipe_platform.* TO 'recipe_user'@'localhost';
FLUSH PRIVILEGES;

-- 验证创建
SHOW DATABASES;
SELECT User, Host FROM mysql.user;
```

### 3. 应用配置文件

后端配置文件位置：`backend/.env`

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production

# 数据库连接
DATABASE_URL=mysql+pymysql://recipe_user:recipe_password_2024@localhost:3306/recipe_platform

# Redis连接
REDIS_URL=redis://localhost:6379

# 其他配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### 4. 数据库初始化脚本

运行以下命令初始化数据库：

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
set FLASK_APP=app.py
set FLASK_ENV=development

# 初始化数据库
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 测试数据库连接
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Database connection:', db.engine.execute('SELECT 1').scalar())"
```

### 5. 表结构验证

数据库创建后将包含以下表：

- `users` - 用户信息表
- `recipes` - 菜谱表
- `comments` - 评论表
- `tags` - 标签表
- `recipe_tags` - 菜谱标签关联表

### 6. 常见问题解决

#### 问题1：MySQL连接失败
```
错误：Access denied for user 'root'@'localhost'
解决：检查MySQL服务状态，确认用户名密码
```

#### 问题2：字符编码问题
```
确保数据库使用utf8mb4字符集
CREATE DATABASE recipe_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 问题3：端口占用
```
检查3306端口是否被占用
netstat -an | findstr 3306
```

### 7. 开发环境测试

```python
# 测试脚本 test_db.py
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # 创建表
    db.create_all()

    # 测试用户创建
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()

    # 验证
    print(f"用户创建成功: {user.to_dict()}")
```

### 8. 备份和恢复

```bash
# 备份数据库
mysqldump -u recipe_user -p recipe_platform > backup.sql

# 恢复数据库
mysql -u recipe_user -p recipe_platform < backup.sql
```

---

**重要提示**：在生产环境中，请确保：
1. 使用强密码
2. 启用SSL连接
3. 定期备份数据
4. 限制数据库访问权限