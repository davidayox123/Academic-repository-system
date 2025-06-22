import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  FileText,
  Download,
  Calendar,
  User,
  Building,
  ArrowLeft,
  Share2,
  Heart,
  MessageCircle,
  AlertCircle
} from 'lucide-react'
import { documentsApi, handleApiError } from '../services/api'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import toast from 'react-hot-toast'
import { formatDistanceToNow } from 'date-fns'

interface DocumentDetails {
  id: string
  title: string
  status: string
  upload_date: string
  file_size: number
  uploader: string
  department_id: string
  file_path: string
  rejection_reason?: string
  download_url?: string
}

const DocumentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
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
      const response = await documentsApi.getDocument(id!) // Remove user?.role argument
      const apiDoc = response.data.data
      setDoc({
        id: apiDoc.id,
        title: apiDoc.title,
        status: apiDoc.status,
        upload_date: apiDoc.upload_date,
        file_size: apiDoc.file_size || 0,
        uploader: typeof apiDoc.uploader === 'string' ? apiDoc.uploader : '',
        department_id: apiDoc.department_id,
        file_path: apiDoc.file_path || '',
        rejection_reason: apiDoc.rejection_reason,
        download_url: apiDoc.download_url
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
      link.download = doc.title
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
                      <span>{doc.uploader}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Building className="w-4 h-4" />
                      <span>{doc.department_id}</span>
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
                  {formatFileSize(doc.file_size || 0)}
                </div>
              </div>
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
              Filename: {doc.title}
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default DocumentDetail
