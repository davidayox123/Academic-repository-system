import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Download, 
  CheckCircle,
  Clock,
  AlertCircle,
  Plus,
  RefreshCw
} from 'lucide-react'
import { useAuthStore } from '../stores/useAuthStore'
import { useDashboardStore, startDashboardAutoRefresh, stopDashboardAutoRefresh } from '../stores/useDashboardStore'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatDistanceToNow } from 'date-fns'

const Dashboard: React.FC = () => {
  const { user } = useAuthStore()
  const { 
    stats, 
    recentDocuments, 
    isLoading, 
    error, 
    lastUpdated,
    fetchAllDashboardData,
    clearError  } = useDashboardStore()

  // Auto-refresh dashboard data every 30 seconds (replaces WebSocket)
  useEffect(() => {
    const interval = setInterval(() => {
      fetchAllDashboardData()
    }, 30000)

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    // Fetch initial data
    fetchAllDashboardData()
    
    // Start auto-refresh
    startDashboardAutoRefresh()

    // Cleanup on unmount
    return () => {
      stopDashboardAutoRefresh()
    }
  }, [fetchAllDashboardData])

  // Clear error when component mounts
  useEffect(() => {
    if (error) {
      clearError()
    }
  }, [error, clearError])

  const handleRefresh = () => {
    fetchAllDashboardData()
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

  const formatStatus = (status: string) => {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())  }

  // Loading state
  if (isLoading && !stats) {
    return (
      <div className="page-container">
        <div className="content-wrapper flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner size="lg" text="Loading dashboard..." />
        </div>
      </div>
    )
  }

  // Error state
  if (error && !stats) {
    return (
      <div className="page-container">
        <div className="content-wrapper">
          <div className="text-center py-12">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Error loading dashboard</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={handleRefresh}
              className="btn-primary"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }  // Map backend student stats to expected frontend keys
  let mappedStats = stats;
  if (user?.role === 'student' && stats) {
    mappedStats = {
      total_documents: stats.total_uploads,
      approved_documents: stats.approved_uploads,
      pending_reviews: stats.pending_reviews,
      total_downloads: stats.total_downloads,
      ...stats
    };
  }
  if (user?.role === 'staff' && stats) {
    mappedStats = {
      total_documents: stats.department_documents,
      approved_documents: stats.approved_documents,
      pending_reviews: stats.pending_reviews,
      total_downloads: stats.total_downloads,
      ...stats
    };
  }
  if (user?.role === 'supervisor' && stats) {
    mappedStats = {
      total_documents: stats.department_documents,
      approved_documents: stats.approved_documents,
      pending_reviews: stats.assigned_reviews,
      total_downloads: stats.completed_reviews,
      ...stats
    };
  }
  if (user?.role === 'admin' && stats) {
    mappedStats = {
      total_documents: stats.total_documents,
      approved_documents: stats.approved_documents,
      pending_reviews: stats.pending_reviews,
      total_downloads: stats.total_downloads,
      ...stats
    };
  }

  // Stats configuration
  const statsConfig = mappedStats ? [
    {
      title: 'Total Documents',
      value: mappedStats.total_documents?.toString() || '0',
      change: 0, // We don't have change tracking yet
      changeType: 'neutral' as 'neutral' | 'positive' | 'negative',
      icon: FileText,
      color: 'blue'
    },
    {
      title: 'Pending Reviews',
      value: mappedStats.pending_reviews?.toString() || '0',
      change: 0,
      changeType: 'neutral' as 'neutral' | 'positive' | 'negative',
      icon: Clock,
      color: 'yellow'
    },
    {
      title: 'Approved',
      value: mappedStats.approved_documents?.toString() || '0',
      change: 0,
      changeType: 'neutral' as 'neutral' | 'positive' | 'negative',
      icon: CheckCircle,
      color: 'green'
    },
    {
      title: 'Downloads',
      value: mappedStats.total_downloads?.toString() || '0',
      change: 0,
      changeType: 'neutral' as 'neutral' | 'positive' | 'negative',
      icon: Download,
      color: 'purple'
    }
  ] : []

  return (
    <div className="page-container">
      <div className="content-wrapper">        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Welcome back, {user?.email || 'User'}!
              </h1>
              <p className="text-gray-600">
                Here's what's happening with your documents today.
              </p>
            </div>
            <div className="flex items-center gap-4">
              {lastUpdated && (
                <p className="text-sm text-gray-500">
                  Last updated: {formatDistanceToNow(lastUpdated, { addSuffix: true })}
                </p>
              )}
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="btn-secondary flex items-center gap-2 disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <div className="flex flex-wrap gap-4">
            <Link to="/upload" className="btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Upload Document
            </Link>
            <Link to="/documents" className="btn-secondary">
              <FileText className="w-5 h-5 mr-2" />
              Browse Documents
            </Link>
          </div>
        </motion.div>        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {statsConfig.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 * index }}
              className="glass p-6 rounded-2xl hover-lift"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-${stat.color}-100 rounded-xl flex items-center justify-center`}>
                  <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
                </div>                <div className={`text-sm font-medium ${
                  stat.changeType === 'positive' ? 'text-green-600' : 
                  stat.changeType === 'negative' ? 'text-red-600' : 
                  'text-gray-600'
                }`}>
                  {stat.change !== 0 ? (stat.change > 0 ? '+' : '') + stat.change : ''}
                </div>
              </div>
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {stat.value}
              </div>
              <div className="text-gray-600 text-sm">
                {stat.title}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Documents */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="glass p-6 rounded-2xl"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Recent Documents</h3>
              <Link to="/documents" className="text-blue-600 hover:text-blue-500 text-sm font-medium">
                View All
              </Link>
            </div>
            
            <div className="space-y-4">
              {recentDocuments.map((doc) => (
                <div key={doc.id} className="flex items-center justify-between p-4 bg-gray-50/50 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">
                      {doc.title}
                    </h4>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span>Uploaded {doc.uploaded_at}</span>
                      <span>{doc.downloads} downloads</span>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(doc.status)}`}>
                    {formatStatus(doc.status)}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Quick Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8 glass p-6 rounded-2xl"
        >
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
              <AlertCircle className="w-5 h-5 text-yellow-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Quick Tips</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
            <div className="flex items-start space-x-2">
              <span className="text-blue-600 font-bold">•</span>
              <span>Upload documents in PDF format for better compatibility</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-blue-600 font-bold">•</span>
              <span>Add relevant tags to make your documents easier to find</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-blue-600 font-bold">•</span>
              <span>Check pending reviews regularly to stay updated</span>
            </div>
            <div className="flex items-start space-x-2">
              <span className="text-blue-600 font-bold">•</span>
              <span>Use descriptive titles and detailed descriptions</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard
