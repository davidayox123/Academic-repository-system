// User Types
export interface User {
  id: string // UUID, maps to user_id in backend
  first_name: string
  middle_name?: string
  last_name: string
  email: string
  role: UserRole
  department_id: string
  is_active: boolean
  avatar?: string

  // Student attributes
  matric_no?: string
  level?: '100' | '200' | '300' | '400' | '500'

  // Staff attributes
  staff_id?: string
  position?: string
  office_no?: string

  // Supervisor attributes
  title?: string
  assigned_department?: string
  specialization_area?: string
  max_documents?: number
  years_of_experience?: number

  // Admin attributes
  admin_id?: string
  admin_level?: 'super' | 'department' | 'limited'
  permissions_scope?: string

  created_at: string
  updated_at: string

  // Relational properties (optional)
  department?: Department
  uploaded_documents?: Document[]
  supervised_documents?: Document[]
  reviews?: Review[]
  audit_logs?: AuditLog[]
  downloads?: Download[]
}

export type UserRole = 'student' | 'staff' | 'supervisor' | 'admin'

export interface Department {
  id: string // department_id
  name: string // department_name
  code: string
  faculty: string
  description?: string
  head_of_department?: string
  contact_email?: string
  contact_phone?: string
  building?: string
  room_number?: string
  is_active: string
  created_at: string
  updated_at: string
  total_users: number
  total_documents: number
  users?: User[]
  documents?: Document[]
}

// Update Document type to match backend response
export interface Document {
  id: string;
  title: string;
  status: string;
  upload_date: string;
  uploader: User | UploaderInfo;
  department_id: string;
  file_path?: string;
  file_size?: number;
  rejection_reason?: string;
  download_url?: string;
}

export interface UploaderInfo {
  id: string;
  full_name: string;
  email: string;
}

export type DocumentStatus = 'pending' | 'under_review' | 'approved' | 'rejected' | 'archived'
export type DocumentCategory = 'research' | 'thesis' | 'assignment' | 'presentation' | 'paper' | 'report' | 'project' | 'other'
export type DocumentType = 'pdf' | 'doc' | 'docx' | 'ppt' | 'pptx' | 'txt' | 'image' | 'video' | 'audio' | 'archive'

export interface Review {
  id: string // review_id
  document_id: string
  reviewer_id: string
  status: ReviewStatus
  decision?: ReviewDecision
  comments?: string
  feedback?: string
  suggestions?: string
  rating_quality?: number
  rating_relevance?: number
  rating_originality?: number
  overall_rating?: number
  assigned_date: string
  started_date?: string
  completed_date?: string
  priority?: string
  estimated_hours?: number
  actual_hours?: number
  created_at: string
  updated_at: string
  document?: Document
  reviewer?: User
}

export type ReviewStatus = 'pending' | 'in_progress' | 'completed'
export type ReviewDecision = 'approved' | 'rejected' | 'needs_revision'

export interface Metadata {
  id: string // metadata_id
  document_id: string
  keywords: string
  publication_year: number
  authors: string
  abstract?: string
  subject_area?: string
  created_at: string
  updated_at: string
  document?: Document
}

export interface AuditLog {
  id: string // log_id
  user_id: string
  document_id?: string
  action: string
  details?: string
  ip_address?: string
  user_agent?: string
  timestamp: string
  created_at: string
  user?: User
  document?: Document
}

export interface Download {
  id: string // download_id
  document_id: string
  user_id: string
  download_date: string
  ip_address?: string
  user_agent?: string
  file_size_at_download?: number
  is_successful: string
  error_message?: string
  referrer?: string
  download_source?: string
  created_at: string
  document?: Document
  user?: User
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
  filters_applied: Record<string, any>
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
