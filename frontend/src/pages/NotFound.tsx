import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  AlertTriangle, 
  Home, 
  ArrowLeft, 
  Search,
  FileText,
  Compass
} from 'lucide-react'

const NotFound: React.FC = () => {
  const navigate = useNavigate()

  const suggestions = [
    { icon: Home, label: 'Go Home', path: '/', color: 'blue' },
    { icon: Search, label: 'Browse Documents', path: '/documents', color: 'green' },
    { icon: FileText, label: 'Upload Document', path: '/upload', color: 'purple' },
    { icon: Compass, label: 'Dashboard', path: '/dashboard', color: 'orange' }
  ]

  return (
    <div className="min-h-screen flex items-center justify-center page-container">
      {/* Background Elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-red-300/20 dark:bg-red-800/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-orange-300/20 dark:bg-orange-800/20 rounded-full blur-3xl animate-pulse-slow"></div>
      </div>

      <div className="max-w-2xl w-full text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* 404 Animation */}
          <motion.div
            animate={{ 
              rotate: [0, 5, -5, 0],
              scale: [1, 1.1, 1]
            }}
            transition={{ 
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="mb-8"
          >
            <div className="text-9xl font-bold gradient-text mb-4">404</div>
            <div className="w-24 h-24 bg-gradient-to-r from-red-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6">
              <AlertTriangle className="w-12 h-12 text-white" />
            </div>
          </motion.div>

          {/* Content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="glass p-8 rounded-3xl mb-8"
          >
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Oops! Page Not Found
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
              The page you're looking for seems to have wandered off into the digital void. 
              Don't worry, even the best explorers sometimes take wrong turns!
            </p>
            
            {/* Quick Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-6">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate(-1)}
                className="btn-secondary flex items-center"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Go Back
              </motion.button>
              <Link to="/" className="btn-primary">
                <Home className="w-5 h-5 mr-2" />
                Go Home
              </Link>
            </div>
          </motion.div>

          {/* Suggestions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              Or try one of these popular destinations:
            </h3>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {suggestions.map((item, index) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: 0.1 * index }}
                  whileHover={{ scale: 1.05, y: -5 }}
                  className="group"
                >
                  <Link
                    to={item.path}
                    className="block glass p-6 rounded-2xl hover:shadow-xl transition-all duration-300"
                  >
                    <div className={`w-12 h-12 bg-${item.color}-100 dark:bg-${item.color}-900/30 rounded-xl flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform duration-200`}>
                      <item.icon className={`w-6 h-6 text-${item.color}-600 dark:text-${item.color}-400`} />
                    </div>
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white">
                      {item.label}
                    </span>
                  </Link>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Fun Message */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="mt-12 text-center"
          >
            <div className="glass p-4 rounded-xl inline-block">
              <p className="text-sm text-gray-500 dark:text-gray-400">
                🎯 <span className="font-medium">Pro tip:</span> Check the URL for typos, or use our search to find what you're looking for!
              </p>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default NotFound
