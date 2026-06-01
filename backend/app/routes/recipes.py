from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Recipe, User, Like, Favorite
from sqlalchemy import or_, and_

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '').strip()
    difficulty = request.args.get('difficulty', '').strip()
    max_prep_time = request.args.get('max_prep_time', type=int)
    max_cook_time = request.args.get('max_cook_time', type=int)
    sort_by = request.args.get('sort_by', 'created_at')  # created_at, title, prep_time, difficulty
    sort_order = request.args.get('sort_order', 'desc')  # asc, desc

    # 构建查询
    query = Recipe.query

    # 搜索功能
    if search:
        search_filter = or_(
            Recipe.title.contains(search),
            Recipe.description.contains(search),
            Recipe.ingredients.contains(search)
        )
        query = query.filter(search_filter)

    # 难度筛选
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)

    # 准备时间筛选
    if max_prep_time:
        query = query.filter(Recipe.prep_time <= max_prep_time)

    # 烹饪时间筛选
    if max_cook_time:
        query = query.filter(Recipe.cook_time <= max_cook_time)

    # 排序
    if sort_by == 'created_at':
        order_field = Recipe.created_at.desc() if sort_order == 'desc' else Recipe.created_at.asc()
    elif sort_by == 'title':
        order_field = Recipe.title.desc() if sort_order == 'desc' else Recipe.title.asc()
    elif sort_by == 'prep_time':
        order_field = Recipe.prep_time.desc() if sort_order == 'desc' else Recipe.prep_time.asc()
    elif sort_by == 'cook_time':
        order_field = Recipe.cook_time.desc() if sort_order == 'desc' else Recipe.cook_time.asc()
    else:
        order_field = Recipe.created_at.desc()

    query = query.order_by(order_field)

    recipes = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'recipes': [recipe.to_dict() for recipe in recipes.items],
        'total': recipes.total,
        'pages': recipes.pages,
        'current_page': page,
        'search_params': {
            'search': search,
            'difficulty': difficulty,
            'max_prep_time': max_prep_time,
            'max_cook_time': max_cook_time,
            'sort_by': sort_by,
            'sort_order': sort_order
        }
    })

@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    """专门的搜索接口"""
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not q:
        return jsonify({
            'message': '搜索关键词不能为空'
        }), 400

    # 构建搜索查询
    search_filter = or_(
        Recipe.title.contains(q),
        Recipe.description.contains(q),
        Recipe.ingredients.contains(q)
    )

    recipes = Recipe.query.filter(search_filter)\
        .order_by(Recipe.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'recipes': [recipe.to_dict() for recipe in recipes.items],
        'total': recipes.total,
        'pages': recipes.pages,
        'current_page': page,
        'search_query': q
    })

@recipes_bp.route('/difficulties', methods=['GET'])
def get_difficulties():
    """获取所有难度级别，按指定顺序排序"""
    difficulties = db.session.query(Recipe.difficulty).distinct().all()
    difficulty_list = [d[0] for d in difficulties if d[0]]

    # 按指定顺序排序：简单、中等、困难
    difficulty_order = {'简单': 1, '中等': 2, '困难': 3}
    difficulty_list.sort(key=lambda x: difficulty_order.get(x, 999))

    return jsonify({'difficulties': difficulty_list})

@recipes_bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    print("=== CREATE RECIPT START ===")  # 调试日志

    try:
        print(f"DEBUG: Request method: {request.method}")  # 调试日志
        print(f"DEBUG: Request content-type: {request.content_type}")  # 调试日志
        print(f"DEBUG: Request data: {request.data}")  # 调试日志

        data = request.get_json()
        print(f"DEBUG: Parsed JSON data: {data}")  # 调试日志

        # 验证请求数据
        if not data:
            print("DEBUG: No data received")  # 调试日志
            return jsonify({'message': '请求数据不能为空'}), 400

        # 验证必填字段
        required_fields = ['title', 'ingredients', 'instructions']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            print(f"DEBUG: Missing fields: {missing_fields}")  # 调试日志
            return jsonify({
                'message': f'缺少必填字段: {", ".join(missing_fields)}'
            }), 400

        user_id = get_jwt_identity()
        print(f"DEBUG: User ID: {user_id}")  # 调试日志

        recipe = Recipe(
            title=data['title'],
            description=data.get('description'),
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            prep_time=data.get('prep_time'),
            cook_time=data.get('cook_time'),
            difficulty=data.get('difficulty'),
            servings=data.get('servings'),
            image=data.get('image'),  # 添加image字段
            user_id=user_id
        )

        # 打印图片字段用于调试
        print(f"DEBUG: Image field value: {data.get('image')}")  # 调试日志

        db.session.add(recipe)
        db.session.commit()

        print(f"DEBUG: Recipe created with ID: {recipe.id}")  # 调试日志
        return jsonify(recipe.to_dict()), 201

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")  # 错误日志
        import traceback
        traceback.print_exc()  # 打印完整的堆栈跟踪
        return jsonify({'message': f'服务器错误: {str(e)}'}), 500

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())

@recipes_bp.route('/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    """更新菜谱 - 只有菜谱创建者可以编辑（管理员不能编辑）"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    # 检查是否是菜谱的作者（只有创建者可以编辑，管理员也不能编辑）
    if not user.can_edit_recipe(recipe):
        return jsonify({'message': '无权限编辑此菜谱，只有菜谱创建者可以编辑'}), 403

    data = request.get_json()

    # 更新字段
    if 'title' in data:
        recipe.title = data['title']
    if 'description' in data:
        recipe.description = data['description']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'instructions' in data:
        recipe.instructions = data['instructions']
    if 'prep_time' in data:
        recipe.prep_time = data['prep_time']
    if 'cook_time' in data:
        recipe.cook_time = data['cook_time']
    if 'difficulty' in data:
        recipe.difficulty = data['difficulty']
    if 'servings' in data:
        recipe.servings = data['servings']
    if 'image' in data:
        recipe.image = data['image']

    db.session.commit()
    return jsonify(recipe.to_dict(current_user_id=user_id))

@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    """删除菜谱 - 菜谱创建者或管理员可以删除"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    # 检查是否是菜谱的作者或管理员
    if not user.can_delete_recipe(recipe):
        return jsonify({'message': '无权限删除此菜谱，只有菜谱创建者或管理员可以删除'}), 403

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': '菜谱删除成功'})


# 点赞功能
@recipes_bp.route('/<int:recipe_id>/like', methods=['POST'])
@jwt_required()
def like_recipe(recipe_id):
    """点赞菜谱"""
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)
    user = User.query.get(user_id)

    # 检查是否已点赞
    if user.has_liked_recipe(recipe_id):
        return jsonify({'message': '已经点赞过该菜谱'}), 400

    # 创建点赞记录
    like = Like(user_id=user_id, recipe_id=recipe_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({
        'message': '点赞成功',
        'likes_count': len(recipe.likes)
    }), 201


@recipes_bp.route('/<int:recipe_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_recipe(recipe_id):
    """取消点赞"""
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)

    # 查找点赞记录
    like = Like.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not like:
        return jsonify({'message': '还未点赞该菜谱'}), 400

    db.session.delete(like)
    db.session.commit()

    return jsonify({
        'message': '取消点赞成功',
        'likes_count': len(recipe.likes)
    })


# 收藏功能
@recipes_bp.route('/<int:recipe_id>/favorite', methods=['POST'])
@jwt_required()
def favorite_recipe(recipe_id):
    """收藏菜谱"""
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)
    user = User.query.get(user_id)

    # 检查是否已收藏
    if user.has_favorited_recipe(recipe_id):
        return jsonify({'message': '已经收藏过该菜谱'}), 400

    # 创建收藏记录
    favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        'message': '收藏成功',
        'favorites_count': len(recipe.favorites)
    }), 201


@recipes_bp.route('/<int:recipe_id>/favorite', methods=['DELETE'])
@jwt_required()
def unfavorite_recipe(recipe_id):
    """取消收藏"""
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)

    # 查找收藏记录
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not favorite:
        return jsonify({'message': '还未收藏该菜谱'}), 400

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        'message': '取消收藏成功',
        'favorites_count': len(recipe.favorites)
    })


# 获取用户收藏的菜谱
@recipes_bp.route('/favorites/my', methods=['GET'])
@jwt_required()
def get_my_favorites():
    """获取当前用户收藏的菜谱列表"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 分页查询用户的收藏
    favorites = Favorite.query.filter_by(user_id=user_id)\
        .order_by(Favorite.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    recipes = [fav.recipe for fav in favorites.items]

    return jsonify({
        'recipes': [recipe.to_dict(current_user_id=user_id) for recipe in recipes],
        'total': favorites.total,
        'pages': favorites.pages,
        'current_page': page
    })
