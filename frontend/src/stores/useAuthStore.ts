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
  selectRole: (role: UserRole, userId: string) => void
  switchRole: (role: UserRole) => void
  logout: () => void
}

// Real users from the database with static UUIDs
const realUsers: Record<UserRole, User> = {
  student: {
    id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    first_name: 'John',
    last_name: 'Doe',
    email: 'john.doe@student.edu',
    role: 'student',
    department_id: '8f9b5b3a-3d1b-4c6a-8a0a-8d7e6f5c4b3a',
    matric_no: 'CS/19/001',
    level: '400',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  staff: {
    id: 'b2c3d4e5-f6a7-8901-2345-67890abcdef0',
    first_name: 'Jennifer',
    last_name: 'Anderson',
    email: 'jennifer.anderson@staff.edu',
    role: 'staff',
    department_id: '8f9b5b3a-3d1b-4c6a-8a0a-8d7e6f5c4b3a',
    staff_id: 'ST001',
    position: 'Research Assistant',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  supervisor: {
    id: 'c3d4e5f6-a7b8-9012-3456-7890abcdef01',
    first_name: 'Dr. Rachel',
    last_name: 'White',
    email: 'rachel.white@supervisor.edu',
    role: 'supervisor',
    department_id: '8f9b5b3a-3d1b-4c6a-8a0a-8d7e6f5c4b3a',
    specialization_area: 'Artificial Intelligence, Machine Learning',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  admin: {
    id: 'd4e5f6a7-b8c9-0123-4567-890abcdef012',
    first_name: 'Super',
    last_name: 'Administrator',
    email: 'super.admin@admin.edu',
    role: 'admin',
    department_id: '8f9b5b3a-3d1b-4c6a-8a0a-8d7e6f5c4b3a',
    admin_level: 'super',
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
}

const createMockUser = (role: UserRole, userId: string): User => {
  const user = realUsers[role];
  return { ...user, id: userId };
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set) => ({
      // State - Start with no role selected
      user: null,
      isAuthenticated: false,
      currentRole: null,
      hasSelectedRole: false,

      // Actions
      selectRole: (role: UserRole, userId: string) => {
        const user = createMockUser(role, userId)
        set({
          user,
          currentRole: role,
          isAuthenticated: true,
          hasSelectedRole: true
        })
      },

      switchRole: (role: UserRole) => {
        // Find the user ID based on the role from the realUsers object
        const userId = realUsers[role].id;
        const user = createMockUser(role, userId)
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
