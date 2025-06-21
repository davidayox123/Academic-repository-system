import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '../types'

type UserRole = 'student' | 'staff' | 'supervisor' | 'admin'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  currentRole: UserRole | null
  hasSelectedRole: boolean
}

interface AuthActions {
  selectRole: (role: UserRole) => void
  switchRole: (role: UserRole) => void
  logout: () => void
}

// Mock user data for different roles
const createMockUser = (role: UserRole): User => ({
  id: '1',
  name: `${role.charAt(0).toUpperCase() + role.slice(1)} User`,
  email: `${role}@academic.edu`,
  role: role,
  department_id: 'dept-001',
  department_name: 'Computer Science',
  avatar: undefined,
  is_active: true,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString()
})

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set) => ({
      // State - Start with no role selected
      user: null,
      isAuthenticated: false,
      currentRole: null,
      hasSelectedRole: false,

      // Actions
      selectRole: (role: UserRole) => {
        const user = createMockUser(role)
        set({
          user,
          currentRole: role,
          isAuthenticated: true,
          hasSelectedRole: true
        })
      },

      switchRole: (role: UserRole) => {
        const user = createMockUser(role)
        set({
          user,
          currentRole: role,
          isAuthenticated: true,
          hasSelectedRole: true
        })
      },

      logout: () => {
        set({
          user: null,
          currentRole: null,
          isAuthenticated: false,
          hasSelectedRole: false
        })
      }
    }),
    {
      name: 'auth-storage',
    }
  )
)
