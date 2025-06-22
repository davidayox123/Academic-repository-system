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

// Real users from database
const realUsers: Record<UserRole, User> = {
  student: {
    id: '7e3cf886-559d-43de-b69c-f3772398f03a',
    name: 'Alex Thompson',
    email: 'student1@university.edu',
    role: 'student',
    department_id: '7e3cf886-559d-43de-b69c-f3772398f03a', // Will be updated with real dept ID
    department_name: 'Computer Science',
    avatar: undefined,
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  staff: {
    id: '264f717b-55ae-4982-9973-a89cd50c41f9',
    name: 'Jane Smith',
    email: 'staff1@university.edu',
    role: 'staff',
    department_id: '264f717b-55ae-4982-9973-a89cd50c41f9',
    department_name: 'Computer Science',
    avatar: undefined,
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  supervisor: {
    id: '5091d4ee-02cb-4e99-a34b-d98f1bc72811',
    name: 'Dr. Alice Johnson',
    email: 'supervisor1@university.edu',
    role: 'supervisor',
    department_id: '5091d4ee-02cb-4e99-a34b-d98f1bc72811',
    department_name: 'Computer Science',
    avatar: undefined,
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  admin: {
    id: '6c513b2d-0188-4133-8796-aa6c7753d2de',
    name: 'System Administrator',
    email: 'admin@university.edu',
    role: 'admin',
    department_id: '6c513b2d-0188-4133-8796-aa6c7753d2de',
    department_name: 'Computer Science',
    avatar: undefined,
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
}

const createMockUser = (role: UserRole): User => realUsers[role]

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
