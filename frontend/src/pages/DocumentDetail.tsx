import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  FileText,
  Download,
  Calendar,
  User,
  Building,
  Tag,
  ArrowLeft,
  Share2,
  Heart,
  MessageCircle,
  AlertCircle
} from 'lucide-react'
import { useAuthStore } from '../stores/useAuthStore'
import { documentsApi, handleApiError } from '../services/api'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import toast from 'react-hot-toast'
import { formatDistanceToNow } from 'date-fns'

interface DocumentDetails {
  id: string
  title: string
  description: string
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

const DocumentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [doc, setDoc] = useState<DocumentDetails | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      fetchDocument()
    }
  }, [id])

  const fetchDocument = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const response = await documentsApi.getDocument(id!, user?.role)      // Map API response to our interface
      const apiDoc = response.data.data
      setDoc({
        id: apiDoc.id,
        title: apiDoc.title,
        description: apiDoc.description || '',
        filename: apiDoc.file_name || 'document.pdf',
        category: 'general', // Mock category since not in API
        status: apiDoc.status,
        upload_date: apiDoc.upload_date,
        file_size: apiDoc.file_size,
        uploader_name: apiDoc.author?.name || 'Unknown',
        department_name: apiDoc.department || 'Unknown',
        download_count: apiDoc.download_count || 0,
        view_count: 0 // Mock view count since not in API
      })
    } catch (err: any) {
      const errorMessage = handleApiError(err)
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!doc) return
    
    try {
      const response = await documentsApi.downloadDocument(doc.id)
      
      // Create blob URL and trigger download
      const blob = new Blob([response.data])
      const url = window.URL.createObjectURL(blob)
      const link = window.document.createElement('a')
      link.href = url
      link.download = doc.filename
      window.document.body.appendChild(link)
      link.click()
      window.document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      toast.success('Download started')
    } catch (err: any) {
      toast.error('Failed to download document')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'under_review':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'rejected':
        return 'bg-red-100 text-red-800 border-red-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  if (isLoading) {
    return (
      <div className="page-container">
        <div className="content-wrapper flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner size="lg" text="Loading document..." />
        </div>
      </div>
    )
  }
  if (error || !doc) {
    return (
      <div className="page-container">
        <div className="content-wrapper text-center py-12">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {error || 'Document not found'}
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            The document you're looking for doesn't exist or you don't have permission to view it.
          </p>
          <button
            onClick={() => navigate('/documents')}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Documents</span>
          </button>
        </div>
      </div>
    )
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
          <button
            onClick={() => navigate('/documents')}
            className="btn-ghost mb-6 inline-flex items-center space-x-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Documents</span>
          </button>

          <div className="glass p-8 rounded-2xl">
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-start space-x-4">
                <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center">
                  <FileText className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="flex-1">                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {doc.title}
                  </h1>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                    <div className="flex items-center space-x-1">
                      <User className="w-4 h-4" />
                      <span>{doc.uploader_name}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Building className="w-4 h-4" />
                      <span>{doc.department_name}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-4 h-4" />
                      <span>{formatDistanceToNow(new Date(doc.upload_date), { addSuffix: true })}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(doc.status)}`}>
                  {doc.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>            {/* Document Info */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="bg-white/50 dark:bg-gray-800/50 p-4 rounded-xl">
                <div className="text-sm text-gray-500 mb-1">File Size</div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white">
                  {formatFileSize(doc.file_size)}
                </div>
              </div>
              <div className="bg-white/50 dark:bg-gray-800/50 p-4 rounded-xl">
                <div className="text-sm text-gray-500 mb-1">Downloads</div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white">
                  {doc.download_count}
                </div>
              </div>
              <div className="bg-white/50 dark:bg-gray-800/50 p-4 rounded-xl">
                <div className="text-sm text-gray-500 mb-1">Views</div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white">
                  {doc.view_count}
                </div>
              </div>
            </div>

            {/* Category */}
            <div className="mb-6">
              <div className="flex items-center space-x-2 mb-2">
                <Tag className="w-4 h-4 text-gray-500" />
                <span className="text-sm text-gray-500">Category</span>
              </div>
              <span className="px-3 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm rounded-full">
                {doc.category}
              </span>
            </div>

            {/* Description */}
            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Description</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {doc.description || 'No description available for this document.'}
              </p>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-4">
              <button
                onClick={handleDownload}
                className="btn-primary inline-flex items-center space-x-2"
              >
                <Download className="w-4 h-4" />
                <span>Download</span>
              </button>
              <button className="btn-secondary inline-flex items-center space-x-2">
                <Share2 className="w-4 h-4" />
                <span>Share</span>
              </button>
              <button className="btn-ghost inline-flex items-center space-x-2">
                <Heart className="w-4 h-4" />
                <span>Save</span>
              </button>
              <button className="btn-ghost inline-flex items-center space-x-2">
                <MessageCircle className="w-4 h-4" />
                <span>Comment</span>
              </button>
            </div>
          </div>
        </motion.div>

        {/* Preview Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass p-8 rounded-2xl"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Document Preview</h3>
          <div className="bg-gray-100 dark:bg-gray-700 rounded-xl p-8 text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">
              Preview functionality will be available in the next update
            </p>            <p className="text-sm text-gray-500 mt-2">
              Filename: {doc.filename}
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default DocumentDetail
