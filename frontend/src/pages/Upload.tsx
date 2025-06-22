import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'react-hot-toast'
import { FileText, Image, Video, Music, Archive, File } from 'lucide-react'
import { useAuthStore } from '../stores/useAuthStore'
import { documentsApi } from '../services/api'

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
  const [currentTag, setCurrentTag] = useState('')
  const [metadata, setMetadata] = useState<DocumentMetadata>({
    title: '',
    description: '',
    tags: [],
    department: user?.department_name || '',
    category: 'research',
    course_code: ''
  })

  const maxFileSize = 50 * 1024 * 1024 // 50MB
  const maxFiles = 10

  const acceptedFileTypes = {
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'text/plain': ['.txt'],
    'text/markdown': ['.md'],
    'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'],
    'video/*': ['.mp4', '.webm', '.mov', '.avi'],
    'audio/*': ['.mp3', '.wav', '.ogg']
  }

  const formatFileSize = (bytes: number) => {
    if (!bytes || bytes === 0 || isNaN(bytes)) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (file: File) => {
    const type = file.type || ''
    if (type.startsWith('image/')) return Image
    if (type.startsWith('video/')) return Video
    if (type.startsWith('audio/')) return Music
    if (type.includes('pdf') || type.includes('document') || type.includes('text')) return FileText
    if (type.includes('zip') || type.includes('rar')) return Archive
    return File
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
    const newFiles: UploadFile[] = acceptedFiles.map((file, index) => {
      const uploadFile = Object.assign(file, {
        id: `${Date.now()}_${index}`,
        progress: 0,
        status: 'pending' as const,
        preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined
      })
      return uploadFile as UploadFile
    })

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
        formData.append('tags', metadata.tags.join(','))
        formData.append('course_code', metadata.course_code)
        formData.append('is_public', 'false')

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
      }, 2000)
    } catch (error: any) {
      console.error('Upload error:', error)
      toast.error('Upload failed. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Upload Documents</h1>
          
          {/* Upload Area */}
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
              isDragActive 
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-300 hover:border-blue-400'
            }`}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Drop files here or click to browse
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  Support for PDF, DOC, images, videos and more
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  Maximum file size: {formatFileSize(maxFileSize)}
                </p>
              </div>
            </div>
          </div>

          {/* File List */}
          {files.length > 0 && (
            <div className="mt-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Selected Files ({files.length})
              </h3>
              <div className="space-y-3">
                {files.map(file => {
                  const FileIcon = getFileIcon(file)
                  return (
                    <div
                      key={file.id}
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
                          <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${file.progress}%` }}
                            />
                          </div>
                        )}
                        
                        {/* Status */}
                        {file.status === 'success' && (
                          <p className="text-xs text-green-600 mt-1">Uploaded successfully</p>
                        )}
                        {file.status === 'error' && (
                          <p className="text-xs text-red-600 mt-1">{file.error}</p>
                        )}
                      </div>
                      
                      <button
                        onClick={() => removeFile(file.id)}
                        className="flex-shrink-0 w-8 h-8 bg-red-100 hover:bg-red-200 rounded-full flex items-center justify-center transition-colors"
                        disabled={file.status === 'uploading'}
                      >
                        <span className="text-red-600 text-sm">×</span>
                      </button>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {/* Metadata Form */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  value={metadata.title}
                  onChange={(e) => setMetadata(prev => ({ ...prev, title: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter document title"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description *
                </label>
                <textarea
                  value={metadata.description}
                  onChange={(e) => setMetadata(prev => ({ ...prev, description: e.target.value }))}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Describe your document"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  value={metadata.category}
                  onChange={(e) => setMetadata(prev => ({ ...prev, category: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="research">Research</option>
                  <option value="thesis">Thesis</option>
                  <option value="assignment">Assignment</option>
                  <option value="presentation">Presentation</option>
                  <option value="paper">Paper</option>
                  <option value="report">Report</option>
                  <option value="project">Project</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Course Code
                </label>
                <input
                  type="text"
                  value={metadata.course_code}
                  onChange={(e) => setMetadata(prev => ({ ...prev, course_code: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., CS101"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tags
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={currentTag}
                    onChange={(e) => setCurrentTag(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addTag()}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Add a tag"
                  />
                  <button
                    type="button"
                    onClick={addTag}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {metadata.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                    >
                      {tag}
                      <button
                        onClick={() => removeTag(tag)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Upload Button */}
          <div className="mt-8 flex justify-end">
            <button
              onClick={uploadFiles}
              disabled={isUploading || files.length === 0}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isUploading ? 'Uploading...' : 'Upload Files'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Upload
