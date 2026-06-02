import { createStore, Store } from 'vuex'
import { authApi } from '@/api/auth'

export interface State {
  theme: 'light' | 'dark'
  searchHistory: string[]
  viewHistory: any[]
  favorites: any[]
  user: any
}

const store = createStore<State>({
  state: {
    theme: 'light',
    searchHistory: JSON.parse(localStorage.getItem('searchHistory') || '[]'),
    viewHistory: JSON.parse(localStorage.getItem('viewHistory') || '[]'),
    favorites: JSON.parse(localStorage.getItem('favorites') || '[]'),
    user: null
  },
  getters: {
    isDarkMode: (state) => state.theme === 'dark'
  },
  mutations: {
    SET_THEME(state, theme: 'light' | 'dark') {
      state.theme = theme
      localStorage.setItem('theme', theme)
      if (theme === 'dark') {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
    TOGGLE_THEME(state) {
      const newTheme = state.theme === 'light' ? 'dark' : 'light'
      this.commit('SET_THEME', newTheme)
    },
    ADD_SEARCH_HISTORY(state, keyword: string) {
      if (!state.searchHistory.includes(keyword)) {
        state.searchHistory.unshift(keyword)
        state.searchHistory = state.searchHistory.slice(0, 10)
        localStorage.setItem('searchHistory', JSON.stringify(state.searchHistory))
      }
    },
    ADD_VIEW_HISTORY(state, recipe: any) {
      const index = state.viewHistory.findIndex(item => item.id === recipe.id)
      if (index !== -1) {
        state.viewHistory.splice(index, 1)
      }
      state.viewHistory.unshift({
        ...recipe,
        viewDate: new Date().toISOString()
      })
      state.viewHistory = state.viewHistory.slice(0, 20)
      localStorage.setItem('viewHistory', JSON.stringify(state.viewHistory))
    },
    TOGGLE_FAVORITE(state, recipe: any) {
      const index = state.favorites.findIndex(item => item.id === recipe.id)
      if (index !== -1) {
        state.favorites.splice(index, 1)
      } else {
        state.favorites.unshift({
          ...recipe,
          favoriteDate: new Date().toISOString()
        })
      }
      localStorage.setItem('favorites', JSON.stringify(state.favorites))
    },
    SET_USER(state, user) {
      state.user = user
    }
  },
  actions: {
    initTheme({ commit }) {
      const savedTheme = localStorage.getItem('theme') as 'light' | 'dark'
      const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      const initialTheme = savedTheme || (systemDark ? 'dark' : 'light')
      commit('SET_THEME', initialTheme)
    }
  }
})

export default store
