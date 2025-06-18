import axios from 'axios'
import type { AxiosInstance, AxiosResponse } from 'axios'
import type {
  User,
  Document,
  Review,
  LoginCredentials,
  RegisterData,
  DocumentFilter,
  ReviewSubmission,
  ApiResponse,
  PaginatedResponse,
  DashboardStats,
  ActivityItem,
  SearchResult,
  Notification,
  AuditLog,
  DocumentStats,
  UserStats,
} from '../types'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh-token')
        if (refreshToken) {
          const response = await authApi.refreshToken(refreshToken)
          const { access_token } = response.data.data
          
          localStorage.setItem('auth-token', access_token)
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          
          return api.request(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('auth-token')
        localStorage.removeItem('refresh-token')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

// Authentication API
export const authApi = {
  login: (credentials: LoginCredentials): Promise<AxiosResponse<ApiResponse<{
    access_token: string
    refresh_token: string
    token_type: string
    expires_in: number
    user: User
  }>>> => {
    return api.post('/auth/login', credentials)
  },

  register: (data: RegisterData): Promise<AxiosResponse<ApiResponse<{
    access_token: string
    refresh_token: string
    token_type: string
    expires_in: number
    user: User
  }>>> => {
    return api.post('/auth/register', data)
  },

  refreshToken: (refreshToken: string): Promise<AxiosResponse<ApiResponse<{
    access_token: string
    refresh_token: string
    token_type: string
    expires_in: number
    user: User
  }>>> => {
    return api.post('/auth/refresh', { refresh_token: refreshToken })
  },

  getCurrentUser: (): Promise<AxiosResponse<ApiResponse<User>>> => {
    return api.get('/auth/me')
  },

  updateProfile: (data: Partial<User>): Promise<AxiosResponse<ApiResponse<User>>> => {
    return api.put('/auth/profile', data)
  },

  changePassword: (data: {
    current_password: string
    new_password: string
  }): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.put('/auth/password', data)
  },

  logout: (): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.post('/auth/logout')
  },
}

// Documents API
export const documentsApi = {
  getDocuments: (filters?: DocumentFilter): Promise<AxiosResponse<ApiResponse<PaginatedResponse<Document>>>> => {
    return api.get('/documents', { params: filters })
  },

  getDocument: (id: string): Promise<AxiosResponse<ApiResponse<Document>>> => {
    return api.get(`/documents/${id}`)
  },

  uploadDocument: (data: FormData): Promise<AxiosResponse<ApiResponse<Document>>> => {
    return api.post('/documents', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  updateDocument: (id: string, data: Partial<Document>): Promise<AxiosResponse<ApiResponse<Document>>> => {
    return api.put(`/documents/${id}`, data)
  },

  deleteDocument: (id: string): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.delete(`/documents/${id}`)
  },

  downloadDocument: (id: string): Promise<AxiosResponse<Blob>> => {
    return api.get(`/documents/${id}/download`, {
      responseType: 'blob',
    })
  },

  getDocumentStats: (): Promise<AxiosResponse<ApiResponse<DocumentStats>>> => {
    return api.get('/documents/stats')
  },
}

// Reviews API
export const reviewsApi = {
  getReviews: (documentId?: string): Promise<AxiosResponse<ApiResponse<Review[]>>> => {
    const params = documentId ? { document_id: documentId } : {}
    return api.get('/reviews', { params })
  },

  submitReview: (data: ReviewSubmission): Promise<AxiosResponse<ApiResponse<Review>>> => {
    return api.post('/reviews', data)
  },

  updateReview: (id: string, data: Partial<Review>): Promise<AxiosResponse<ApiResponse<Review>>> => {
    return api.put(`/reviews/${id}`, data)
  },

  deleteReview: (id: string): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.delete(`/reviews/${id}`)
  },
}

// Users API (Admin only)
export const usersApi = {
  getUsers: (filters?: {
    role?: string
    department?: string
    search?: string
    page?: number
    limit?: number
  }): Promise<AxiosResponse<ApiResponse<PaginatedResponse<User>>>> => {
    return api.get('/users', { params: filters })
  },

  getUser: (id: string): Promise<AxiosResponse<ApiResponse<User>>> => {
    return api.get(`/users/${id}`)
  },

  createUser: (data: RegisterData): Promise<AxiosResponse<ApiResponse<User>>> => {
    return api.post('/users', data)
  },

  updateUser: (id: string, data: Partial<User>): Promise<AxiosResponse<ApiResponse<User>>> => {
    return api.put(`/users/${id}`, data)
  },

  deleteUser: (id: string): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.delete(`/users/${id}`)
  },

  getUserStats: (): Promise<AxiosResponse<ApiResponse<UserStats>>> => {
    return api.get('/users/stats')
  },
}

// Dashboard API
export const dashboardApi = {
  getStats: (): Promise<AxiosResponse<ApiResponse<DashboardStats>>> => {
    return api.get('/dashboard/stats')
  },

  getActivity: (limit?: number): Promise<AxiosResponse<ApiResponse<ActivityItem[]>>> => {
    return api.get('/dashboard/activity', { params: { limit } })
  },
}

// Search API
export const searchApi = {
  search: (query: string, filters?: DocumentFilter): Promise<AxiosResponse<ApiResponse<SearchResult>>> => {
    return api.get('/search', { params: { q: query, ...filters } })
  },

  getSuggestions: (query: string): Promise<AxiosResponse<ApiResponse<string[]>>> => {
    return api.get('/search/suggestions', { params: { q: query } })
  },
}

// Notifications API
export const notificationsApi = {
  getNotifications: (unreadOnly?: boolean): Promise<AxiosResponse<ApiResponse<Notification[]>>> => {
    return api.get('/notifications', { params: { unread_only: unreadOnly } })
  },

  markAsRead: (id: string): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.put(`/notifications/${id}/read`)
  },

  markAllAsRead: (): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.put('/notifications/read-all')
  },

  deleteNotification: (id: string): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.delete(`/notifications/${id}`)
  },
}

// Audit API (Admin only)
export const auditApi = {
  getAuditLogs: (filters?: {
    user_id?: string
    action?: string
    resource_type?: string
    date_from?: string
    date_to?: string
    page?: number
    limit?: number
  }): Promise<AxiosResponse<ApiResponse<PaginatedResponse<AuditLog>>>> => {
    return api.get('/audit', { params: filters })
  },
}

// Utility functions
export const handleApiError = (error: any): string => {
  if (error.response?.data?.message) {
    return error.response.data.message
  }
  if (error.message) {
    return error.message
  }
  return 'An unexpected error occurred'
}

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export const getFileIcon = (fileType: string): string => {
  const type = fileType.toLowerCase()
  if (type.includes('pdf')) return '📄'
  if (type.includes('doc')) return '📝'
  if (type.includes('image')) return '🖼️'
  if (type.includes('video')) return '🎥'
  if (type.includes('audio')) return '🎵'
  if (type.includes('zip') || type.includes('rar')) return '📦'
  return '📄'
}

export default api
