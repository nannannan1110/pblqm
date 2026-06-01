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
