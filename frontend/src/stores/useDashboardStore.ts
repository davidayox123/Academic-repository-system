import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'
import api from '../services/api'
import toast from 'react-hot-toast'

interface DashboardStats {
  total_documents: {
    value: number
    change: string
    change_type: 'positive' | 'negative' | 'neutral'
  }
  pending_reviews: {
    value: number
    change: string
    change_type: 'positive' | 'negative' | 'neutral'
  }
  approved_documents: {
    value: number
    change: string
    change_type: 'positive' | 'negative' | 'neutral'
  }
  total_downloads: {
    value: number
    change: string
    change_type: 'positive' | 'negative' | 'neutral'
  }
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
    ...initialState,

    fetchStats: async () => {
      try {
        set({ isLoading: true, error: null })
        const response = await api.get('/dashboard/stats')
        set({ 
          stats: response.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = error.response?.data?.detail || 'Failed to fetch dashboard stats'
        set({ error: message, isLoading: false })
        toast.error(message)
      }
    },

    fetchRecentDocuments: async () => {
      try {
        set({ isLoading: true, error: null })
        const response = await api.get('/dashboard/recent-documents')
        set({ 
          recentDocuments: response.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = error.response?.data?.detail || 'Failed to fetch recent documents'
        set({ error: message, isLoading: false })
        toast.error(message)
      }
    },

    fetchRecentActivity: async () => {
      try {
        set({ isLoading: true, error: null })
        const response = await api.get('/dashboard/recent-activity')
        set({ 
          recentActivity: response.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = error.response?.data?.detail || 'Failed to fetch recent activity'
        set({ error: message, isLoading: false })
        toast.error(message)
      }
    },

    fetchAllDashboardData: async () => {
      try {
        set({ isLoading: true, error: null })
        
        const [statsResponse, documentsResponse, activityResponse] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/recent-documents'),
          api.get('/dashboard/recent-activity')
        ])

        set({
          stats: statsResponse.data,
          recentDocuments: documentsResponse.data,
          recentActivity: activityResponse.data,
          isLoading: false,
          lastUpdated: new Date()
        })
      } catch (error: any) {
        const message = error.response?.data?.detail || 'Failed to fetch dashboard data'
        set({ error: message, isLoading: false })
        toast.error(message)
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
