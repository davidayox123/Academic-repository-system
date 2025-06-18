import React from 'react'
import { motion } from 'framer-motion'
import { User } from 'lucide-react'

const Profile: React.FC = () => {
  return (
    <div className="page-container">
      <div className="content-wrapper">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <User className="w-8 h-8 text-white" />
          </div>
          <h1 className="section-header">Profile</h1>
          <p className="text-xl text-gray-600 mb-8">
            Manage your account settings and preferences
          </p>
          <div className="glass p-8 rounded-2xl">
            <p className="text-gray-600">
              Profile management interface coming soon...
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Profile
