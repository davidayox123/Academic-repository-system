import React, { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { 
  Upload as UploadIcon, 
  File, 
  X, 
  CheckCircle, 
  AlertCircle,
  Loader2,
  FileText,
  Image,
  Music,
  Video,
  Archive,
  Plus,
  Tag
} from 'lucide-react'
import { useAuthStore } from '../stores/useAuthStore'
import { documentsApi } from '../services/api'
import toast from 'react-hot-toast'

interface UploadFile extends File {
  id: string
  progress: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  preview?: string
  error?: string
}

interface DocumentMetadata {
  title: string
  description: string
  tags: string[]
  department: string
  category: string
  course_code: string
}

const Upload: React.FC = () => {
  const { user } = useAuthStore()
  const [files, setFiles] = useState<UploadFile[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [metadata, setMetadata] = useState<DocumentMetadata>({
    title: '',
    description: '',
    tags: [],
    department: user?.department_name || '',
    category: 'research',
    course_code: ''
  })
  const [currentTag, setCurrentTag] = useState('')

  // File type configurations
  const acceptedFileTypes = {
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/vnd.ms-powerpoint': ['.ppt'],
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
    'text/plain': ['.txt'],
    'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp'],
    'video/*': ['.mp4', '.webm', '.mov'],
    'audio/*': ['.mp3', '.wav', '.ogg']
  }

  const maxFileSize = 50 * 1024 * 1024 // 50MB
  const maxFiles = 10

  const categories = [
    'research',
    'thesis',
    'assignment',
    'presentation',
    'paper',
    'report',
    'project',
    'other'
  ]

  const departments = [
    'Computer Science',
    'Engineering',
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'Psychology',
    'Economics',
    'Literature',
    'History',
    'Philosophy',
    'Art & Design',
    'Music',
    'Medicine',
    'Law',
    'Business',
    'Education',
    'Other'
  ]

  const getFileIcon = (file: File) => {
    const type = file.type
    if (type.startsWith('image/')) return Image
    if (type.startsWith('video/')) return Video
    if (type.startsWith('audio/')) return Music
    if (type.includes('pdf') || type.includes('document') || type.includes('text')) return FileText
    if (type.includes('zip') || type.includes('rar')) return Archive
    return File
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    // Handle rejected files
    rejectedFiles.forEach(rejection => {
      const { file, errors } = rejection
      errors.forEach((error: any) => {
        if (error.code === 'file-too-large') {
          toast.error(`${file.name} is too large. Maximum size is ${formatFileSize(maxFileSize)}`)
        } else if (error.code === 'file-invalid-type') {
          toast.error(`${file.name} is not a supported file type`)
        } else {
          toast.error(`Error with ${file.name}: ${error.message}`)
        }
      })
    })

    // Handle accepted files
    const newFiles: UploadFile[] = acceptedFiles.map(file => ({
      ...file,
      id: Math.random().toString(36).substring(7),
      progress: 0,
      status: 'pending',
      preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined
    }))

    setFiles(prev => [...prev, ...newFiles])
  }, [maxFileSize])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFileTypes,
    maxSize: maxFileSize,
    maxFiles: maxFiles - files.length,
    multiple: true
  })

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(file => file.id !== fileId))
  }

  const addTag = () => {
    if (currentTag.trim() && !metadata.tags.includes(currentTag.trim())) {
      setMetadata(prev => ({
        ...prev,
        tags: [...prev.tags, currentTag.trim()]
      }))
      setCurrentTag('')
    }
  }

  const removeTag = (tagToRemove: string) => {
    setMetadata(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }))
  }

  const validateForm = () => {
    if (!metadata.title.trim()) {
      toast.error('Please enter a title')
      return false
    }
    if (!metadata.description.trim()) {
      toast.error('Please enter a description')
      return false
    }
    if (files.length === 0) {
      toast.error('Please select at least one file')
      return false
    }
    return true
  }
  const uploadFiles = async () => {
    if (!validateForm()) return

    setIsUploading(true)
    
    try {
      const uploadPromises = files.map(async (file) => {
        // Update file status to uploading
        setFiles(prev => prev.map(f => 
          f.id === file.id ? { ...f, status: 'uploading' } : f
        ))

        const formData = new FormData()
        formData.append('file', file)
        formData.append('title', metadata.title)
        formData.append('description', metadata.description)
        formData.append('category', metadata.category)
        formData.append('department', metadata.department)
        formData.append('course_code', metadata.course_code)
        formData.append('tags', metadata.tags.join(','))

        try {
          const response = await documentsApi.uploadDocument(formData, (progressEvent) => {
            if (progressEvent.total) {
              const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
              setFiles(prev => prev.map(f => 
                f.id === file.id ? { ...f, progress } : f
              ))
            }
          })

          // Mark as successful
          setFiles(prev => prev.map(f => 
            f.id === file.id ? { ...f, status: 'success', progress: 100 } : f
          ))

          return response.data
        } catch (error: any) {
          // Mark as failed
          setFiles(prev => prev.map(f => 
            f.id === file.id ? { 
              ...f, 
              status: 'error', 
              error: error.response?.data?.detail || 'Upload failed' 
            } : f
          ))
          throw error
        }
      })

      await Promise.all(uploadPromises)
      toast.success('All files uploaded successfully!')
      
      // Reset form after successful upload
      setTimeout(() => {
        setFiles([])
        setMetadata({
          title: '',
          description: '',
          tags: [],
          department: user?.department_name || '',
          category: 'research',
          course_code: ''
        })
      }, 2000)    } catch (error: any) {
      const errorMessage = 'Upload failed. Please try again.'
      // Only show error toast for non-auth errors
      if (error.response?.status !== 401) {
        toast.error(errorMessage)
      }
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="content-wrapper max-w-4xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="w-16 h-16 bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <UploadIcon className="w-8 h-8 text-white" />
          </div>
          <h1 className="section-header">Upload Documents</h1>
          <p className="text-xl text-gray-600">
            Share your academic work with the community
          </p>
        </motion.div>

        {/* Upload Form */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Metadata Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-1 space-y-6"
          >
            <div className="glass p-6 rounded-2xl">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Document Information</h3>
              
              {/* Title */}
              <div className="form-group">
                <label htmlFor="title" className="form-label">Title</label>
                <input
                  id="title"
                  type="text"
                  value={metadata.title}
                  onChange={(e) => setMetadata(prev => ({ ...prev, title: e.target.value }))}
                  className="form-input"
                  placeholder="Enter document title"
                />
              </div>

              {/* Description */}
              <div className="form-group">
                <label htmlFor="description" className="form-label">Description</label>
                <textarea
                  id="description"
                  rows={4}
                  value={metadata.description}
                  onChange={(e) => setMetadata(prev => ({ ...prev, description: e.target.value }))}
                  className="form-input resize-none"
                  placeholder="Describe your document..."
                />
              </div>

              {/* Category */}
              <div className="form-group">
                <label htmlFor="category" className="form-label">Category</label>
                <select
                  id="category"
                  value={metadata.category}
                  onChange={(e) => setMetadata(prev => ({ ...prev, category: e.target.value }))}
                  className="form-input"
                >
                  {categories.map(category => (
                    <option key={category} value={category}>
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              {/* Department */}
              <div className="form-group">
                <label htmlFor="department" className="form-label">Department</label>
                <select
                  id="department"
                  value={metadata.department}
                  onChange={(e) => setMetadata(prev => ({ ...prev, department: e.target.value }))}
                  className="form-input"
                >
                  {departments.map(dept => (
                    <option key={dept} value={dept}>{dept}</option>
                  ))}
                </select>
              </div>

              {/* Tags */}
              <div className="form-group">
                <label className="form-label">Tags</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={currentTag}
                    onChange={(e) => setCurrentTag(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                    className="form-input flex-1"
                    placeholder="Add tag..."
                  />
                  <button
                    type="button"
                    onClick={addTag}
                    className="btn-secondary px-3"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {metadata.tags.map(tag => (
                    <span
                      key={tag}
                      className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded-lg"
                    >
                      <Tag className="w-3 h-3" />
                      {tag}
                      <button
                        type="button"
                        onClick={() => removeTag(tag)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}                </div>
              </div>

              {/* Course Code */}
              <div className="form-group">
                <label className="form-label">Course Code</label>
                <input
                  type="text"
                  value={metadata.course_code}
                  onChange={(e) => setMetadata(prev => ({ ...prev, course_code: e.target.value }))}
                  className="form-input"
                  placeholder="e.g., CS101, MATH201"
                />
              </div>
            </div>
          </motion.div>

          {/* File Upload Area */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2 space-y-6"
          >
            {/* Dropzone */}
            <div
              {...getRootProps()}
              className={`glass p-8 rounded-2xl border-2 border-dashed transition-all duration-300 cursor-pointer ${
                isDragActive 
                  ? 'border-blue-500 bg-blue-50/50' 
                  : 'border-gray-300 hover:border-blue-400'
              }`}
            >
              <input {...getInputProps()} />
              <div className="text-center">
                <motion.div
                  animate={isDragActive ? { scale: 1.05 } : { scale: 1 }}
                  className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4"
                >
                  <UploadIcon className="w-8 h-8 text-blue-600" />
                </motion.div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
                </h3>
                <p className="text-gray-600 mb-4">
                  or click to select files ({maxFiles - files.length} remaining)
                </p>
                <div className="text-sm text-gray-500">
                  <p>Supported formats: PDF, DOC, DOCX, PPT, PPTX, TXT, Images, Videos, Audio</p>
                  <p>Maximum file size: {formatFileSize(maxFileSize)}</p>
                </div>
              </div>
            </div>

            {/* File List */}
            <AnimatePresence>
              {files.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="glass p-6 rounded-2xl"
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Selected Files ({files.length})
                  </h3>
                  <div className="space-y-3">
                    {files.map(file => {
                      const FileIcon = getFileIcon(file)
                      return (
                        <motion.div
                          key={file.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: 20 }}
                          className="flex items-center gap-4 p-3 bg-white/50 rounded-xl"
                        >
                          <div className="flex-shrink-0">
                            <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                              <FileIcon className="w-5 h-5 text-gray-600" />
                            </div>
                          </div>
                          
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {file.name}
                            </p>
                            <p className="text-xs text-gray-500">
                              {formatFileSize(file.size)}
                            </p>
                            
                            {/* Progress Bar */}
                            {file.status === 'uploading' && (
                              <div className="mt-2">
                                <div className="w-full bg-gray-200 rounded-full h-1.5">
                                  <div 
                                    className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                                    style={{ width: `${file.progress}%` }}
                                  />
                                </div>
                                <p className="text-xs text-gray-500 mt-1">{file.progress}%</p>
                              </div>
                            )}
                          </div>

                          <div className="flex items-center gap-2">
                            {file.status === 'pending' && (
                              <div className="w-5 h-5 text-gray-400">
                                <AlertCircle className="w-5 h-5" />
                              </div>
                            )}
                            {file.status === 'uploading' && (
                              <div className="w-5 h-5 text-blue-600">
                                <Loader2 className="w-5 h-5 animate-spin" />
                              </div>
                            )}
                            {file.status === 'success' && (
                              <div className="w-5 h-5 text-green-600">
                                <CheckCircle className="w-5 h-5" />
                              </div>
                            )}
                            {file.status === 'error' && (
                              <div className="w-5 h-5 text-red-600">
                                <AlertCircle className="w-5 h-5" />
                              </div>
                            )}
                            
                            {!isUploading && (
                              <button
                                onClick={() => removeFile(file.id)}
                                className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                              >
                                <X className="w-4 h-4" />
                              </button>
                            )}
                          </div>
                        </motion.div>
                      )
                    })}
                  </div>

                  {/* Upload Button */}
                  <div className="mt-6 flex justify-end">
                    <button
                      onClick={uploadFiles}
                      disabled={isUploading || files.some(f => f.status === 'uploading')}
                      className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isUploading ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>
                          <UploadIcon className="w-5 h-5 mr-2" />
                          Upload Files
                        </>
                      )}
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default Upload
