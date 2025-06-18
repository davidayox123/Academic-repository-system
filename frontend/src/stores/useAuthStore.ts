import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, LoginCredentials, RegisterData } from '../types'
import toast from 'react-hot-toast'

// Mock API functions for now - will be replaced with actual API calls
const mockAuthApi = {
  login: async (credentials: LoginCredentials) => {
    // Mock login response
    return {
      data: {
        access_token: 'mock-token',
        refresh_token: 'mock-refresh-token',
        user: {
          id: '1',
          email: credentials.email,
          first_name: 'John',
          last_name: 'Doe',
          role: 'student' as const,
          department: 'Computer Science',
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }
      }
    }
  },
  register: async (data: RegisterData) => {
    return {
      data: {
        access_token: 'mock-token',
        refresh_token: 'mock-refresh-token',
        user: {
          id: '2',
          email: data.email,
          first_name: data.first_name,
          last_name: data.last_name,
          role: data.role,
          department: data.department,
          student_id: data.student_id,
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }
      }
    }
  },
  refreshToken: async () => {
    return {
      data: {
        access_token: 'new-mock-token',
        refresh_token: 'new-mock-refresh-token',
        user: {
          id: '1',
          email: 'user@example.com',
          first_name: 'John',
          last_name: 'Doe',
          role: 'student' as const,
          department: 'Computer Science',
          is_active: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }
      }
    }
  },
  getCurrentUser: async () => {
    return {
      data: {
        id: '1',
        email: 'user@example.com',
        first_name: 'John',
        last_name: 'Doe',
        role: 'student' as const,
        department: 'Computer Science',
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }
    }
  }
}

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
      login: async (credentials: LoginCredentials) => {
        try {
          set({ isLoading: true })
          
          const response = await mockAuthApi.login(credentials)
          const { access_token, refresh_token, user } = response.data

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          toast.success(`Welcome back, ${user.first_name}!`)
        } catch (error: any) {
          set({ isLoading: false })
          const message = error.response?.data?.message || 'Login failed'
          toast.error(message)
          throw error
        }
      },

      register: async (data: RegisterData) => {
        try {
          set({ isLoading: true })
          
          const response = await mockAuthApi.register(data)
          const { access_token, refresh_token, user } = response.data

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
          const message = error.response?.data?.message || 'Registration failed'
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
          }

          const response = await mockAuthApi.refreshToken()
          const { access_token, refresh_token, user } = response.data

          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
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
      },

      initialize: async () => {
        try {
          const { token, refreshToken } = get()
          
          if (token) {
            try {
              // Verify token is still valid
              const response = await mockAuthApi.getCurrentUser()
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
