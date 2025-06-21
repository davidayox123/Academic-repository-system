import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  FileText, 
  Search, 
  Filter, 
  Calendar,
  Grid,
  List,
  SortAsc,
  SortDesc,
  Download,
  Eye,
  Clock,
  CheckCircle,
  AlertCircle,
  Users
} from 'lucide-react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../stores/useAuthStore'
import { documentsApi, handleApiError } from '../services/api'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import toast from 'react-hot-toast'
import { formatDistanceToNow } from 'date-fns'

interface DocumentItem {
  id: string
  title: string
  filename: string
  category: string
  status: string
  upload_date: string
  file_size: number
  uploader_name: string
  department_name: string
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

  // Fetch documents from API
  const fetchDocuments = async () => {
    try {
      setIsLoading(true)
      setError(null)
      
      const filters = {
        role: user?.role,
        search: searchQuery || undefined
      }
      
      const response = await documentsApi.getDocuments(filters)
      // Map API response to our component interface
      const mappedDocs = (response.data.data?.items || []).map((doc: any) => ({
        id: doc.id,
        title: doc.title,
        filename: doc.filename || doc.file_name,
        category: doc.category,
        status: doc.status,
        upload_date: doc.upload_date,
        file_size: doc.file_size,
        uploader_name: doc.uploader_name || doc.author?.name || 'Unknown',
        department_name: doc.department_name || doc.department || 'Unknown',
        download_count: doc.download_count || 0,
        view_count: doc.view_count || 0
      }))
      setDocuments(mappedDocs)
    } catch (err: any) {
      const errorMessage = handleApiError(err)
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  // Fetch documents on mount and when filters change
  useEffect(() => {
    fetchDocuments()
  }, [user?.role, searchQuery])

  // Handle download
  const handleDownload = async (documentId: string, title: string) => {
    try {
      const response = await documentsApi.downloadDocument(documentId)
      
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
    } catch (err: any) {
      toast.error('Failed to download document')
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
            </div>

            {/* Filter Panel */}
            <AnimatePresence>
              {filterOpen && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-600"
                >
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <select className="form-input">
                      <option>All Departments</option>
                      <option>Computer Science</option>
                      <option>Physics</option>
                      <option>Environmental Science</option>
                    </select>
                    <select className="form-input">
                      <option>All Statuses</option>
                      <option>Approved</option>
                      <option>Pending</option>
                      <option>Under Review</option>
                    </select>
                    <select className="form-input">
                      <option>All Types</option>
                      <option>PDF</option>
                      <option>DOCX</option>
                      <option>PPTX</option>
                    </select>
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-4 h-4 text-gray-400" />
                      <input
                        type="date"
                        className="form-input"
                        placeholder="Date range"
                      />
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
                      <span>{doc.uploader_name}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <span>{doc.department_name}</span>
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
                  <div className="flex items-center space-x-2">
                    <Link
                      to={`/documents/${doc.id}`}
                      className="btn-primary flex-1 py-2 text-sm flex items-center justify-center"
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      View
                    </Link>
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
                        <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                          <span>{doc.uploader_name}</span>
                          <span>•</span>
                          <span>{doc.department_name}</span>
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
                      </div>                      <div className="flex items-center space-x-2">
                        <Link
                          to={`/documents/${doc.id}`}
                          className="btn-primary py-2 px-4 flex items-center"
                        >
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </Link>
                        <button
                          onClick={() => handleDownload(doc.id, doc.filename)}
                          className="btn-secondary px-3 py-2"
                        >
                          <Download className="w-4 h-4" />
                        </button>
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
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Documents
