// User Types
export interface User {
  id: string
  name: string
  email: string
  role: UserRole
  department_id: string
  department_name?: string
  avatar?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface UserProfile {
  id: string
  user_id: string
  bio?: string
  phone?: string
  address?: string
  avatar_url?: string
  social_links?: Record<string, string>
  created_at: string
  updated_at: string
}

export type UserRole = 'student' | 'staff' | 'supervisor' | 'admin'

// Document Types
export interface Document {
  id: string
  title: string
  description: string
  file_path: string
  file_name: string
  file_size: number
  file_type: string
  status: DocumentStatus
  upload_date: string
  author_id: string
  author: User
  department: string
  tags: string[]
  version: number
  is_public: boolean
  download_count: number
  reviews: Review[]
  created_at: string
  updated_at: string
}

export type DocumentStatus = 'pending' | 'under_review' | 'approved' | 'rejected'

export interface DocumentUpload {
  title: string
  description: string
  file: File
  department: string
  tags: string[]
  is_public: boolean
}

export interface DocumentFilter {
  search?: string
  status?: DocumentStatus
  department?: string
  author_id?: string
  tags?: string[]
  date_from?: string
  date_to?: string
  page?: number
  limit?: number
}

// Review Types
export interface Review {
  id: string
  document_id: string
  reviewer_id: string
  reviewer: User
  status: ReviewStatus
  comments: string
  rating?: number
  reviewed_at: string
  created_at: string
  updated_at: string
}

export type ReviewStatus = 'pending' | 'approved' | 'rejected' | 'needs_revision'

export interface ReviewSubmission {
  document_id: string
  status: ReviewStatus
  comments: string
  rating?: number
}

// Auth Types
export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  name: string
  email: string
  password: string
  confirm_password: string
  role: UserRole
  department_id: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface TokenPayload {
  sub: string
  email: string
  role: UserRole
  exp: number
  iat: number
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
  errors?: Record<string, string[]>
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  pages: number
}

export interface ApiError {
  message: string
  status: number
  errors?: Record<string, string[]>
}

// UI Types
export interface SelectOption {
  value: string
  label: string
}

export interface TableColumn<T = any> {
  key: keyof T
  label: string
  sortable?: boolean
  render?: (value: any, item: T) => React.ReactNode
}

export interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
}

export interface ToastOptions {
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
}

// Theme Types
export type Theme = 'light' | 'dark' | 'system'

export interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
}

// Dashboard Types
export interface DashboardStats {
  total_documents: number
  pending_reviews: number
  approved_documents: number
  rejected_documents: number
  total_downloads: number
  recent_uploads: number
}

export interface ActivityItem {
  id: string
  type: 'upload' | 'review' | 'approval' | 'rejection' | 'download'
  message: string
  user: User
  document?: Document
  timestamp: string
}

// Search Types
export interface SearchResult {
  documents: Document[]
  users: User[]
  total_results: number
  query: string
  filters_applied: DocumentFilter
}

export interface SearchSuggestion {
  type: 'document' | 'user' | 'tag' | 'department'
  value: string
  label: string
}

// Notification Types
export interface Notification {
  id: string
  user_id: string
  type: NotificationType
  title: string
  message: string
  data?: Record<string, any>
  is_read: boolean
  created_at: string
}

export type NotificationType = 
  | 'document_uploaded'
  | 'review_requested'
  | 'review_completed'
  | 'document_approved'
  | 'document_rejected'
  | 'system_announcement'

// Audit Types
export interface AuditLog {
  id: string
  user_id: string
  user: User
  action: string
  resource_type: string
  resource_id: string
  details: Record<string, any>
  ip_address: string
  user_agent: string
  timestamp: string
}

// File Upload Types
export interface FileUploadProps {
  accept?: string
  multiple?: boolean
  maxSize?: number
  onUpload: (files: File[]) => void
  onError?: (error: string) => void
}

export interface UploadProgress {
  file: File
  progress: number
  status: 'pending' | 'uploading' | 'completed' | 'error'
  error?: string
}

// Form Types
export interface FormFieldProps {
  name: string
  label?: string
  type?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  error?: string
  help?: string
}

export interface FormSelectProps extends FormFieldProps {
  options: SelectOption[]
  multiple?: boolean
}

export interface FormTextareaProps extends FormFieldProps {
  rows?: number
  maxLength?: number
}

// Statistics Types
export interface DocumentStats {
  total: number
  by_status: Record<DocumentStatus, number>
  by_department: Record<string, number>
  by_month: Record<string, number>
  top_tags: Array<{ tag: string; count: number }>
}

export interface UserStats {
  total: number
  by_role: Record<UserRole, number>
  by_department: Record<string, number>
  active_users: number
  new_registrations: Record<string, number>
}

// Export all types
export type {
  // Add any additional exports here
}
