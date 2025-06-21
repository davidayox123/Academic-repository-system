import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, LoginCredentials, RegisterData } from '../types'
import { authApi } from '../services/api'
import toast from 'react-hot-toast'

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  isInitialized: boolean
}

interface AuthActions {
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  refreshAuth: () => Promise<void>
  updateUser: (user: Partial<User>) => void
  initialize: () => Promise<void>
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      // State
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      isInitialized: false,

      // Actions
      login: async (credentials: LoginCredentials) => {        try {
          set({ isLoading: true })
          
          const response = await authApi.login(credentials)
          const { access_token, refresh_token, user } = response.data

          // Store tokens in localStorage for API interceptor
          localStorage.setItem('auth-token', access_token)
          localStorage.setItem('refresh-token', refresh_token)

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          toast.success(`Welcome back, ${user.name}!`)
        } catch (error: any) {
          set({ isLoading: false })
          const message = error.response?.data?.detail || 'Login failed'
          toast.error(message)
          throw error
        }
      },      register: async (data: RegisterData) => {
        try {
          set({ isLoading: true })
            const response = await authApi.register(data)
          const { access_token, refresh_token, user } = response.data

          // Store tokens in localStorage for API interceptor
          localStorage.setItem('auth-token', access_token)
          localStorage.setItem('refresh-token', refresh_token)

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          toast.success('Registration successful! Welcome to Academic Repository.')
        } catch (error: any) {
          set({ isLoading: false })
          const message = error.response?.data?.detail || 'Registration failed'
          toast.error(message)
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
          isLoading: false,
        })
        
        // Clear any cached data
        localStorage.removeItem('auth-storage')
        
        toast.success('Logged out successfully')
      },

      refreshAuth: async () => {
        try {
          const { refreshToken } = get()
          
          if (!refreshToken) {
            throw new Error('No refresh token available')
          }          const response = await authApi.refreshToken(refreshToken)
          const { access_token } = response.data

          // Update localStorage
          localStorage.setItem('auth-token', access_token)

          set({
            token: access_token,
            isAuthenticated: true,
          })
        } catch (error) {
          // If refresh fails, log out the user
          get().logout()
          throw error
        }
      },

      updateUser: (updatedUser: Partial<User>) => {
        const { user } = get()
        if (user) {
          set({
            user: { ...user, ...updatedUser }
          })
        }
      },      initialize: async () => {
        try {
          const { token, refreshToken } = get()
          
          if (token) {
            try {
              // Verify token is still valid
              const response = await authApi.getCurrentUser()
              set({
                user: response.data,
                isAuthenticated: true,
                isInitialized: true,
              })
            } catch (error) {
              // Token might be expired, try to refresh
              if (refreshToken) {
                try {
                  await get().refreshAuth()
                } catch (refreshError) {
                  // Refresh failed, clear auth state
                  get().logout()
                }
              } else {
                // No refresh token, clear auth state
                get().logout()
              }
            }
          }
        } catch (error) {
          console.error('Auth initialization failed:', error)
        } finally {
          set({ isInitialized: true })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Initialize auth on app start
useAuthStore.getState().initialize()
