import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'
import api from '../services/api'
import toast from 'react-hot-toast'
import { useAuthStore } from './useAuthStore'

interface DashboardStats {
  // Admin stats
  total_users?: number
  total_documents?: number
  total_departments?: number
  pending_reviews?: number
  approved_documents?: number
  rejected_documents?: number
  under_review?: number
  total_downloads?: number
  storage_used_mb?: number
  recent_uploads?: number
  active_users?: number
  category_stats?: Array<{ name: string; count: number }>
  department_stats?: Array<{ name: string; count: number }>
  
  // Supervisor stats
  assigned_reviews?: number
  completed_reviews?: number
  department_documents?: number
  recent_submissions?: number
  avg_review_time?: number
  review_workload?: string
  
  // Staff stats
  my_uploads?: number
  
  // Student stats
  my_documents?: number
  total_uploads?: number
  approved_uploads?: number
  rejected_uploads?: number
  average_rating?: number
}

interface RecentDocument {
  id: string
  title: string
  status: string
  uploaded_at: string
  downloads: number
  uploader: {
    name: string
    email: string
  }
}

interface RecentActivity {
  id: string
  type: string
  message: string
  timestamp: string
  document_id?: string
}

interface DashboardState {
  // State
  stats: DashboardStats | null
  recentDocuments: RecentDocument[]
  recentActivity: RecentActivity[]
  isLoading: boolean
  error: string | null
  lastUpdated: Date | null

  // Actions
  fetchStats: () => Promise<void>
  fetchRecentDocuments: () => Promise<void>
  fetchRecentActivity: () => Promise<void>
  fetchAllDashboardData: () => Promise<void>
  clearError: () => void
  reset: () => void
}

const initialState = {
  stats: null,
  recentDocuments: [],
  recentActivity: [],
  isLoading: false,
  error: null,
  lastUpdated: null,
}

export const useDashboardStore = create<DashboardState>()(
  subscribeWithSelector((set) => ({
    ...initialState,    fetchStats: async () => {
      try {
        set({ isLoading: true, error: null })
        
        // Get current role and user from auth store
        const authStore = useAuthStore.getState()
        const currentRole = authStore.user?.role?.toUpperCase() || undefined;
        const userId = authStore.user?.id
        
        const params: any = {}
        if (currentRole) params.role = currentRole
        if (userId) params.user_id = userId
        if (authStore.user?.department_id) params.department_id = authStore.user.department_id
        
        const response = await api.get('/dashboard/stats', { params })
        set({ 
          stats: response.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = 'Failed to fetch dashboard stats'
        set({ error: message, isLoading: false })
        // Only show error toast for network/server errors, not auth errors
        if (error.response?.status !== 401) {
          toast.error(message)
        }
      }
    },    fetchRecentDocuments: async () => {
      try {
        set({ isLoading: true, error: null })
        
        // Get current role and user from auth store
        const authStore = useAuthStore.getState()
        const currentRole = authStore.user?.role?.toUpperCase() || undefined;
        const userId = authStore.user?.id
        
        const params: any = {}
        if (currentRole) params.role = currentRole
        if (userId) params.user_id = userId
        if (authStore.user?.department_id) params.department_id = authStore.user.department_id
        
        const response = await api.get('/dashboard/recent-documents', { params })
        set({ 
          recentDocuments: response.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = 'Failed to fetch recent documents'
        set({ error: message, isLoading: false })
        // Only show error toast for network/server errors, not auth errors
        if (error.response?.status !== 401) {
          toast.error(message)
        }
      }
    },    fetchRecentActivity: async () => {
      try {
        set({ isLoading: true, error: null })
        
        // Get current role and user from auth store
        const authStore = useAuthStore.getState()
        const currentRole = authStore.user?.role?.toUpperCase() || undefined;
        const userId = authStore.user?.id
        
        const params: any = {}
        if (currentRole) params.role = currentRole
        if (userId) params.user_id = userId
        if (authStore.user?.department_id) params.department_id = authStore.user.department_id
        
        const response = await api.get('/dashboard/activity', { params })
        set({ 
          recentActivity: response.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = 'Failed to fetch recent activity'
        set({ error: message, isLoading: false })
        // Only show error toast for network/server errors, not auth errors
        if (error.response?.status !== 401) {
          toast.error(message)
        }
      }
    },    fetchAllDashboardData: async () => {
      try {
        set({ isLoading: true, error: null })
        
        // Get current role and user from auth store
        const authStore = useAuthStore.getState()
        const currentRole = authStore.user?.role?.toUpperCase() || undefined;
        const userId = authStore.user?.id
        
        const params: any = {}
        if (currentRole) params.role = currentRole
        if (userId) params.user_id = userId
        if (authStore.user?.department_id) params.department_id = authStore.user.department_id
        
        const [statsResponse, documentsResponse, activityResponse] = await Promise.all([
          api.get('/dashboard/stats', { params }),
          api.get('/dashboard/recent-documents', { params }),
          api.get('/dashboard/recent-activity', { params })
        ])

        set({
          stats: statsResponse.data,
          recentDocuments: documentsResponse.data,
          recentActivity: activityResponse.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = 'Failed to fetch dashboard data'
        set({ error: message, isLoading: false })
        // Only show error toast for network/server errors, not auth errors
        if (error.response?.status !== 401) {
          toast.error(message)
        }
      }
    },

    clearError: () => set({ error: null }),

    reset: () => set(initialState),
  }))
)

// Auto-refresh dashboard data every 5 minutes
let refreshInterval: number | null = null

export const startDashboardAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  refreshInterval = setInterval(() => {
    const { fetchAllDashboardData } = useDashboardStore.getState()
    fetchAllDashboardData()
  }, 5 * 60 * 1000) // 5 minutes
}

export const stopDashboardAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}
