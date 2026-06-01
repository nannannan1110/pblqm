import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { authApi } from '@/api/auth'

// 路由守卫 - 检查登录状态
const requireAuth = (to: any, from: any, next: any) => {
  if (!authApi.isLoggedIn()) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

// 管理员权限守卫 - 检查管理员权限
const requireAdmin = (to: any, from: any, next: any) => {
  if (!authApi.isLoggedIn()) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    const currentUser = authApi.getCurrentUser()
    if (!currentUser || !currentUser.is_admin) {
      next('/') // 非管理员跳转到首页
    } else {
      next()
    }
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue') // 根路径直接显示登录页
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true } // 首页需要登录
  },
  {
    path: '/login',
    redirect: '/' // /login 重定向到根路径
  },
  {
    path: '/recipes',
    name: 'Recipes',
    component: () => import('@/views/Recipes.vue'),
    meta: { requiresAuth: true } // 菜谱列表需要登录
  },
  {
    path: '/recipes/:id',
    name: 'RecipeDetail',
    component: () => import('@/views/RecipeDetail.vue'),
    meta: { requiresAuth: true } // 菜谱详情需要登录
  },
  // 注册页面
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue')
  },

  // 创建菜谱页面
  {
    path: '/create-recipe',
    name: 'CreateRecipe',
    component: () => import('@/views/CreateRecipe.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/edit-recipe/:id',
    name: 'EditRecipe',
    component: () => import('@/views/EditRecipe.vue'),
    meta: { requiresAuth: true }
  },
  // 个人资料页面
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  // 我的菜谱页面
  {
    path: '/my-recipes',
    name: 'MyRecipes',
    component: () => import('@/views/MyRecipes.vue'),
    meta: { requiresAuth: true }
  },

  // 管理员页面
  {
    path: '/admin',
    name: 'Admin',
    redirect: '/admin/dashboard',
    component: () => import('@/views/admin/AdminLayout.vue'),
    beforeEnter: requireAdmin,
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '仪表板' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'recipes',
        name: 'AdminRecipes',
        component: () => import('@/views/admin/Recipes.vue'),
        meta: { title: '菜谱管理' }
      },
      {
        path: 'comments',
        name: 'AdminComments',
        component: () => import('@/views/admin/Comments.vue'),
        meta: { title: '评论管理' }
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/views/admin/Statistics.vue'),
        meta: { title: '数据统计' }
      }
    ]
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
    meta: { requiresAuth: true } // 关于页面需要登录
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = authApi.isLoggedIn()

  // 如果访问根路径且已登录，跳转到首页
  if (to.path === '/' && isLoggedIn) {
    next('/home')
    return
  }

  // 如果访问注册页面且已登录，则跳转到首页
  if (to.path === '/register' && isLoggedIn) {
    next('/home')
    return
  }

  // 如果页面需要认证且用户未登录，跳转到登录页面（根路径）
  if (to.meta.requiresAuth && !isLoggedIn) {
    next({
      path: '/',
      query: { redirect: to.fullPath }
    })
    return
  }

  next()
})

export default router
