import React from 'react'
import { motion } from 'framer-motion'
import { Users, Shield, Settings, BarChart3 } from 'lucide-react'

const Admin: React.FC = () => {
  return (
    <div className="page-container">
      <div className="content-wrapper">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <div className="w-16 h-16 bg-gradient-to-r from-red-600 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <h1 className="section-header">Admin Panel</h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            System administration and user management
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {[
              { icon: Users, title: 'User Management', desc: 'Manage users and roles' },
              { icon: BarChart3, title: 'Analytics', desc: 'View system statistics' },
              { icon: Settings, title: 'System Settings', desc: 'Configure system options' }
            ].map((item, index) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="glass p-6 rounded-2xl card-hover"
              >
                <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <item.icon className="w-6 h-6 text-red-600 dark:text-red-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  {item.desc}
                </p>
              </motion.div>
            ))}
          </div>

          <div className="glass p-8 rounded-2xl">
            <p className="text-gray-600 dark:text-gray-300">
              Admin interface coming soon...
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Admin
