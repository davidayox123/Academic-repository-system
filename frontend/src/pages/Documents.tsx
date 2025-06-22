import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  FileText, 
  Search, 
  Filter, 
  Grid,
  List,
  SortAsc,
  SortDesc,
  Download,
  Eye,
  Clock,
  CheckCircle,
  AlertCircle,
  Users,
  X
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../stores/useAuthStore'
import { documentsApi, handleApiError } from '../services/api'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import toast from 'react-hot-toast'
import { formatDistanceToNow } from 'date-fns'

// Update DocumentItem to match backend Document type
interface DocumentItem {
  id: string
  title: string
  filename: string
  category: string
  status: string
  upload_date: string
  file_size: number
  uploader_id: string
  uploader?: string
  department_id: string
  department?: string
  download_count: number
  view_count: number
}

// Utility function for file size formatting
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const Documents: React.FC = () => {
  const { user } = useAuthStore()
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [filterOpen, setFilterOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [previewDocument, setPreviewDocument] = useState<DocumentItem | null>(null)

  // Filter options
  const statusOptions = ['pending', 'under_review', 'approved', 'rejected']
  const categoryOptions = ['research', 'thesis', 'assignment', 'presentation', 'paper', 'report', 'project', 'other']

  // Fetch documents from API
  const fetchDocuments = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const filters = {
        user_id: user?.id,
        search: searchQuery || undefined,
        status: statusFilter || undefined,
        category: categoryFilter || undefined
      }
      const response = await documentsApi.getDocuments(filters)
      const mappedDocs = (response.data.items || []).map((doc: any) => ({
        id: doc.id,
        title: doc.title,
        filename: doc.filename,
        category: doc.category,
        status: doc.status,
        upload_date: doc.upload_date,
        file_size: doc.file_size,
        uploader_id: doc.uploader_id,
        uploader: doc.uploader?.first_name + ' ' + doc.uploader?.last_name,
        department_id: doc.department_id,
        department: doc.department?.name,
        download_count: doc.download_count,
        view_count: doc.view_count
      }))
      setDocuments(mappedDocs)
    } catch (err: any) {
      const errorMessage = handleApiError(err)
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }  // Fetch documents on mount and when filters change
  useEffect(() => {
    fetchDocuments()
  }, [user?.role, user?.id, searchQuery, statusFilter, categoryFilter])
  // Handle download
  const handleDownload = async (documentId: string, title: string) => {
    try {
      const response = await documentsApi.downloadDocument(documentId, user?.id)
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = title
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      toast.success('Download started')
    } catch (err: any) {      const errorMessage = handleApiError(err)
      toast.error(`Failed to download: ${errorMessage}`)
    }
  }

  // TODO: Handle review (for supervisors and admins)
  const handleReview = async () => {
    toast('Review functionality is not yet implemented')
  }

  // Check if current user can review documents
  const canReview = user?.role === 'supervisor' || user?.role === 'admin'

  // Get status badge styling
  const getStatusBadge = (status: string) => {
    const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    switch (status) {
      case 'approved':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'rejected':
        return `${baseClasses} bg-red-100 text-red-800`
      case 'under_review':
        return `${baseClasses} bg-blue-100 text-blue-800`
      case 'pending':
        return `${baseClasses} bg-yellow-100 text-yellow-800`
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-500" />
      case 'under_review':
        return <AlertCircle className="w-4 h-4 text-blue-500" />
      default:
        return <FileText className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved':
        return 'status-approved'
      case 'pending':
        return 'status-pending'
      case 'under_review':
        return 'status-under-review'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="page-container">
      <div className="content-wrapper">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6"
            >
              <FileText className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="section-header">Document Library</h1>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Discover and explore academic research documents
            </p>
          </div>

          {/* Search and Filters */}
          <div className="glass p-6 rounded-2xl mb-8">
            <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
              {/* Search Bar */}
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search documents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-200 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-800/50 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-200"
                />
              </div>

              {/* Controls */}
              <div className="flex items-center space-x-4">
                {/* Filter Button */}
                <button
                  onClick={() => setFilterOpen(!filterOpen)}
                  className="btn-ghost flex items-center space-x-2"
                >
                  <Filter className="w-4 h-4" />
                  <span>Filters</span>
                </button>

                {/* Sort Button */}
                <button
                  onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                  className="btn-ghost flex items-center space-x-2"
                >
                  {sortOrder === 'asc' ? <SortAsc className="w-4 h-4" /> : <SortDesc className="w-4 h-4" />}
                  <span>Sort</span>
                </button>

                {/* View Mode Toggle */}
                <div className="flex items-center space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === 'grid'
                        ? 'bg-white dark:bg-gray-600 text-blue-600 shadow-sm'
                        : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                    }`}
                  >
                    <Grid className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === 'list'
                        ? 'bg-white dark:bg-gray-600 text-blue-600 shadow-sm'
                        : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                    }`}
                  >
                    <List className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>            {/* Filter Panel */}
            <AnimatePresence>
              {filterOpen && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-600"
                >
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Status Filter */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Status
                      </label>
                      <select 
                        value={statusFilter} 
                        onChange={(e) => setStatusFilter(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-200"
                      >
                        <option value="">All Statuses</option>
                        {statusOptions.map(status => (
                          <option key={status} value={status}>
                            {status.replace('_', ' ').toUpperCase()}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Category Filter */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Category
                      </label>
                      <select 
                        value={categoryFilter} 
                        onChange={(e) => setCategoryFilter(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-200"
                      >
                        <option value="">All Categories</option>
                        {categoryOptions.map(category => (
                          <option key={category} value={category}>
                            {category.charAt(0).toUpperCase() + category.slice(1)}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Clear Filters */}
                    <div className="flex items-end">
                      <button
                        onClick={() => {
                          setStatusFilter('')
                          setCategoryFilter('')
                          setSearchQuery('')
                        }}
                        className="w-full px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 border border-gray-200 dark:border-gray-600 rounded-lg hover:border-blue-500 transition-all duration-200"
                      >
                        Clear Filters
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>        {/* Documents Grid/List */}
        {isLoading ? (
          <div className="flex items-center justify-center min-h-[400px]">
            <LoadingSpinner size="lg" text="Loading documents..." />
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Failed to load documents</h3>
            <p className="text-gray-600 dark:text-gray-300 mb-4">{error}</p>            <button
              onClick={fetchDocuments}
              className="btn-primary inline-flex items-center space-x-2"
            >
              <span>Retry</span>
            </button>
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No documents found</h3>
            <p className="text-gray-600 dark:text-gray-300">Try adjusting your search or filters.</p>
          </div>
        ) : (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {documents.map((doc, index) => (
                <motion.div
                  key={doc.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass p-6 rounded-2xl card-hover group"
                >
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                        <FileText className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      </div>                      <div className="text-xs text-gray-500">
                        PDF • {formatFileSize(doc.file_size)}
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      {getStatusIcon(doc.status)}
                      <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(doc.status)}`}>
                        {doc.status.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                  </div>

                  {/* Content */}
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {doc.title}
                  </h3>                  <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
                    {doc.filename}
                  </p>

                  {/* Category */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="px-2 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs rounded-full">
                      {doc.category}
                    </span>
                  </div>                  {/* Meta Info */}
                  <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                    <div className="flex items-center space-x-2">
                      <Users className="w-4 h-4" />
                      <span>{doc.uploader}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <span>{doc.department}</span>
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <Eye className="w-4 h-4" />
                        <span>{doc.view_count}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Download className="w-4 h-4" />
                        <span>{doc.download_count}</span>
                      </div>
                    </div>
                    <span>{formatDistanceToNow(new Date(doc.upload_date), { addSuffix: true })}</span>
                  </div>                  {/* Actions */}
                  <div className="flex items-center space-x-2">                    <Link
                      to={`/documents/${doc.id}`}
                      className="btn-primary flex-1 py-2 text-sm flex items-center justify-center"
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      View
                    </Link>
                    <button
                      onClick={() => setPreviewDocument(doc)}
                      className="btn-ghost px-3 py-2"
                      title="Quick Preview"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDownload(doc.id, doc.filename)}
                      className="btn-secondary px-3 py-2"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {documents.map((doc, index) => (
                <motion.div
                  key={doc.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass p-6 rounded-2xl card-hover"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 flex-1">
                      <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                        <FileText className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                          {doc.title}
                        </h3>                        <p className="text-gray-600 dark:text-gray-300 text-sm mb-2">
                          {doc.filename}
                        </p>
                        <div className="flex items-center justify-between mb-2">
                          <span className={getStatusBadge(doc.status)}>
                            {doc.status.replace('_', ' ').toUpperCase()}
                          </span>
                          <span className="text-sm text-gray-500">{formatFileSize(doc.file_size)}</span>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                          <span>{doc.uploader}</span>
                          <span>•</span>
                          <span>{doc.department}</span>
                          <span>•</span>
                          <span>{formatDistanceToNow(new Date(doc.upload_date), { addSuffix: true })}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900 dark:text-white">{doc.view_count}</div>
                        <div className="text-xs text-gray-500">Views</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900 dark:text-white">{doc.download_count}</div>
                        <div className="text-xs text-gray-500">Downloads</div>
                      </div>                      <div className="flex items-center space-x-2">                        <Link
                          to={`/documents/${doc.id}`}
                          className="btn-primary py-2 px-4 flex items-center"
                        >
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </Link>
                        <button
                          onClick={() => setPreviewDocument(doc)}
                          className="btn-ghost px-3 py-2"
                          title="Quick Preview"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDownload(doc.id, doc.filename)}
                          className="btn-secondary px-3 py-2"
                        >
                          <Download className="w-4 h-4" />
                        </button>
                        
                        {/* Review buttons for supervisors/admins on pending documents */}
                        {canReview && doc.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleReview()}
                              className="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg transition-colors flex items-center"
                            >
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Approve
                            </button>
                            <button
                              onClick={() => handleReview()}
                              className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg transition-colors flex items-center"
                            >
                              <AlertCircle className="w-4 h-4 mr-1" />
                              Reject
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}            </div>
          )}
        </motion.div>
        )}

        {/* Pagination */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-12 flex justify-center"
        >
          <div className="glass px-6 py-3 rounded-2xl">
            <div className="flex items-center space-x-2">
              <button className="px-3 py-2 text-gray-500 hover:text-blue-600 transition-colors">
                Previous
              </button>
              <button className="px-3 py-2 bg-blue-600 text-white rounded-lg">1</button>
              <button className="px-3 py-2 text-gray-500 hover:text-blue-600 transition-colors">2</button>
              <button className="px-3 py-2 text-gray-500 hover:text-blue-600 transition-colors">3</button>
              <button className="px-3 py-2 text-gray-500 hover:text-blue-600 transition-colors">
                Next
              </button>
            </div>
          </div>        </motion.div>

        {/* Document Preview Modal */}
        <AnimatePresence>
          {previewDocument && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
              onClick={() => setPreviewDocument(null)}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="bg-white dark:bg-gray-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden shadow-2xl"
                onClick={(e) => e.stopPropagation()}
              >
                {/* Modal Header */}
                <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-600">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {previewDocument.title}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {previewDocument.filename} • {formatFileSize(previewDocument.file_size)}
                    </p>
                  </div>
                  <button
                    onClick={() => setPreviewDocument(null)}
                    className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-500" />
                  </button>
                </div>

                {/* Modal Content */}
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Document Info */}
                    <div className="md:col-span-1 space-y-4">
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-white mb-2">Document Details</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-500">Status:</span>
                            <span className={getStatusBadge(previewDocument.status)}>
                              {previewDocument.status.replace('_', ' ').toUpperCase()}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Category:</span>
                            <span className="text-gray-900 dark:text-white">
                              {previewDocument.category.charAt(0).toUpperCase() + previewDocument.category.slice(1)}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Uploader:</span>
                            <span className="text-gray-900 dark:text-white">{previewDocument.uploader}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Department:</span>
                            <span className="text-gray-900 dark:text-white">{previewDocument.department}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Uploaded:</span>
                            <span className="text-gray-900 dark:text-white">
                              {formatDistanceToNow(new Date(previewDocument.upload_date), { addSuffix: true })}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Downloads:</span>
                            <span className="text-gray-900 dark:text-white">{previewDocument.download_count}</span>
                          </div>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="space-y-2">
                        <Link
                          to={`/documents/${previewDocument.id}`}
                          className="btn-primary w-full py-2 text-center block"
                          onClick={() => setPreviewDocument(null)}
                        >
                          <Eye className="w-4 h-4 mr-2 inline" />
                          View Full Details
                        </Link>
                        <button
                          onClick={() => {
                            handleDownload(previewDocument.id, previewDocument.filename)
                            setPreviewDocument(null)
                          }}
                          className="btn-secondary w-full py-2"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </button>
                        
                        {/* Review buttons for supervisors/admins on pending documents */}
                        {canReview && previewDocument.status === 'pending' && (
                          <>
                            <button
                              onClick={() => {
                                handleReview()
                                setPreviewDocument(null)
                              }}
                              className="bg-green-600 hover:bg-green-700 text-white w-full py-2 rounded-lg transition-colors flex items-center justify-center"
                            >
                              <CheckCircle className="w-4 h-4 mr-2" />
                              Approve
                            </button>
                            <button
                              onClick={() => {
                                handleReview()
                                setPreviewDocument(null)
                              }}
                              className="bg-red-600 hover:bg-red-700 text-white w-full py-2 rounded-lg transition-colors flex items-center justify-center"
                            >
                              <AlertCircle className="w-4 h-4 mr-2" />
                              Reject
                            </button>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Document Preview */}
                    <div className="md:col-span-2">
                      <h4 className="font-medium text-gray-900 dark:text-white mb-4">Preview</h4>
                      <div className="border border-gray-200 dark:border-gray-600 rounded-lg p-8 bg-gray-50 dark:bg-gray-700 h-96 flex items-center justify-center">
                        <div className="text-center">
                          <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                          <p className="text-gray-500 mb-4">
                            Document preview is not available for this file type.
                          </p>
                          <p className="text-sm text-gray-400">
                            Click "View Full Details" to access the document or download it directly.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default Documents
