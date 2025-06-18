import React, { useState } from 'react'
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
  Star,
  Clock,
  CheckCircle,
  AlertCircle,
  Users
} from 'lucide-react'

const Documents: React.FC = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [filterOpen, setFilterOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  // Mock data
  const documents = [
    {
      id: '1',
      title: 'Advanced Machine Learning Algorithms',
      description: 'Comprehensive study on neural networks and deep learning architectures for academic research.',
      author: 'Dr. Sarah Johnson',
      department: 'Computer Science',
      uploadDate: '2024-01-15',
      status: 'approved',
      downloads: 234,
      views: 1205,
      tags: ['AI', 'Machine Learning', 'Neural Networks'],
      fileType: 'PDF',
      fileSize: '2.4 MB',
      rating: 4.8
    },
    {
      id: '2',
      title: 'Climate Change Impact Assessment',
      description: 'Analysis of environmental changes and their effects on global ecosystems.',
      author: 'Prof. Michael Chen',
      department: 'Environmental Science',
      uploadDate: '2024-01-14',
      status: 'under_review',
      downloads: 89,
      views: 456,
      tags: ['Climate', 'Environment', 'Research'],
      fileType: 'PDF',
      fileSize: '3.1 MB',
      rating: 4.6
    },
    {
      id: '3',
      title: 'Quantum Computing Fundamentals',
      description: 'Introduction to quantum mechanics principles applied in computational systems.',
      author: 'Dr. Emma Rodriguez',
      department: 'Physics',
      uploadDate: '2024-01-13',
      status: 'pending',
      downloads: 156,
      views: 892,
      tags: ['Quantum', 'Computing', 'Physics'],
      fileType: 'PDF',
      fileSize: '1.8 MB',
      rating: 4.9
    }
  ]

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
        </motion.div>

        {/* Documents Grid/List */}
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
                      </div>
                      <div className="text-xs text-gray-500">
                        {doc.fileType} • {doc.fileSize}
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
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
                    {doc.description}
                  </p>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {doc.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Meta Info */}
                  <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                    <div className="flex items-center space-x-2">
                      <Users className="w-4 h-4" />
                      <span>{doc.author}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4 text-yellow-400" />
                      <span>{doc.rating}</span>
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <Eye className="w-4 h-4" />
                        <span>{doc.views}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Download className="w-4 h-4" />
                        <span>{doc.downloads}</span>
                      </div>
                    </div>
                    <span>{doc.uploadDate}</span>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center space-x-2">
                    <button className="btn-primary flex-1 py-2 text-sm">
                      <Eye className="w-4 h-4 mr-1" />
                      View
                    </button>
                    <button className="btn-secondary px-3 py-2">
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
                        </h3>
                        <p className="text-gray-600 dark:text-gray-300 text-sm mb-2">
                          {doc.description}
                        </p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                          <span>{doc.author}</span>
                          <span>•</span>
                          <span>{doc.department}</span>
                          <span>•</span>
                          <span>{doc.uploadDate}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900 dark:text-white">{doc.views}</div>
                        <div className="text-xs text-gray-500">Views</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900 dark:text-white">{doc.downloads}</div>
                        <div className="text-xs text-gray-500">Downloads</div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button className="btn-primary py-2 px-4">
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </button>
                        <button className="btn-secondary px-3 py-2">
                          <Download className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

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
