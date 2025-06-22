import axios from 'axios'
import type { AxiosInstance, AxiosResponse } from 'axios'
import type {
  User,
  Document,
  Review,
  LoginCredentials,
  RegisterData,
  ApiResponse,
  PaginatedResponse,
  DashboardStats,
  DocumentStats,
  UserStats,
  AuditLog,
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

// Request interceptor (simplified - no auth needed)
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor (simplified - no auth error handling)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error)
  }
)

// Authentication API
export const authApi = {
  login: (credentials: LoginCredentials): Promise<AxiosResponse<{
    access_token: string
    refresh_token: string
    token_type: string
    user: User
  }>> => {
    return api.post('/auth/login', credentials)
  },

  register: (data: RegisterData): Promise<AxiosResponse<{
    access_token: string
    refresh_token: string
    token_type: string
    user: User
  }>> => {
    return api.post('/auth/register', data)
  },refreshToken: (refreshToken: string): Promise<AxiosResponse<{
    access_token: string
    token_type: string
  }>> => {
    return api.post('/auth/refresh', {}, {
      headers: {
        Authorization: `Bearer ${refreshToken}`
      }
    })
  },  getCurrentUser: (): Promise<AxiosResponse<User>> => {
    return api.get('/auth/profile')
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
  getDocuments: (filters?: Record<string, any>): Promise<AxiosResponse<PaginatedResponse<Document>>> => {
    return api.get('/documents', { params: filters })
  },
  getDocument: (id: string): Promise<AxiosResponse<ApiResponse<Document>>> => {
    return api.get(`/documents/${id}`)
  },
  uploadDocument: (data: FormData, onUploadProgress?: (progressEvent: any) => void): Promise<AxiosResponse<Document>> => {
    return api.post('/documents/upload', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
      onUploadProgress,
    })
  },
  updateDocument: (id: string, data: FormData): Promise<AxiosResponse<Document>> => {
    return api.put(`/documents/${id}`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  deleteDocument: (id: string): Promise<AxiosResponse<ApiResponse<void>>> => {
    return api.delete(`/documents/${id}`)
  },
  downloadDocument: (id: string, userId?: string): Promise<AxiosResponse<Blob>> => {
    const params = userId ? { user_id: userId } : {}
    return api.get(`/documents/${id}/download`, { responseType: 'blob', params })
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
  submitReview: (data: Record<string, any>): Promise<AxiosResponse<ApiResponse<Review>>> => {
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
  getStats: (role?: string): Promise<AxiosResponse<DashboardStats>> => {
    const params = role ? { role } : {}
    return api.get('/dashboard/stats', { params })
  },

  getRecentDocuments: (limit: number = 10, role?: string): Promise<AxiosResponse<Document[]>> => {
    const params = { limit, ...(role && { role }) }
    return api.get('/dashboard/recent-documents', { params })
  },
}

// Audit API
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
    return api.get('/audit', { params: filters })  },
}

// Admin API
export const adminApi = {
  // User Management
  getUsers: (filters?: {
    skip?: number
    limit?: number
    role?: string
    department?: string
    search?: string
  }): Promise<AxiosResponse<{
    items: Array<{
      id: string
      name: string
      email: string
      role: string
      department_name: string
      is_active: boolean
      created_at: string
    }>
    total: number
    skip: number
    limit: number
  }>> => {
    return api.get('/users', { params: filters })
  },

  getUser: (id: string): Promise<AxiosResponse<{
    id: string
    name: string
    email: string
    role: string
    department_name: string
    is_active: boolean
    created_at: string
    updated_at?: string
  }>> => {
    return api.get(`/users/${id}`)
  },
  getUserStats: (): Promise<AxiosResponse<{
    total_users: number
    active_users: number
    by_role: {
      students: number
      staff: number
      supervisors: number
      admins: number
    }
    departments_count: number
  }>> => {
    return api.get('/users/stats/overview')
  },

  createUser: (userData: {
    name: string
    email: string
    role: string
    department_id?: string
    is_active?: boolean
  }): Promise<AxiosResponse<{
    id: string
    name: string
    email: string
    role: string
    department_name: string
    is_active: boolean
    created_at: string
  }>> => {
    return api.post('/users', userData)
  },

  updateUser: (id: string, userData: {
    name?: string
    email?: string
    role?: string
    department_id?: string
    is_active?: boolean
  }): Promise<AxiosResponse<{
    id: string
    name: string
    email: string
    role: string
    department_name: string
    is_active: boolean
    created_at: string
    updated_at?: string
  }>> => {
    return api.put(`/users/${id}`, userData)
  },

  deleteUser: (id: string): Promise<AxiosResponse<{ message: string }>> => {
    return api.delete(`/users/${id}`)
  },

  getDepartments: (): Promise<AxiosResponse<Array<{
    id: string
    name: string
    description?: string
  }>>> => {
    return api.get('/users/departments/list')
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
