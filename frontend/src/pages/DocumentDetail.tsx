import React from 'react'
import { motion } from 'framer-motion'
import { FileText } from 'lucide-react'

const DocumentDetail: React.FC = () => {
  return (
    <div className="page-container">
      <div className="content-wrapper">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <FileText className="w-8 h-8 text-white" />
          </div>
          <h1 className="section-header">Document Details</h1>
          <div className="glass p-8 rounded-2xl">
            <p className="text-gray-600">
              Document detail view coming soon...
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default DocumentDetail
