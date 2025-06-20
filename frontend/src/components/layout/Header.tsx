import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  User,
  LogOut,
  Settings,
  Bell,
  Search,
  Menu,
  X,
  Home,
  FileText,
  Upload,
  BarChart3,
  Users
} from 'lucide-react'
import { useAuthStore } from '../../stores/useAuthStore'
import { useThemeStore } from '../../stores/useThemeStore'

const Header: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, isAuthenticated, logout } = useAuthStore()
  const { theme, toggleTheme } = useThemeStore()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: BarChart3, auth: true },
    { path: '/documents', label: 'Documents', icon: FileText, auth: true },
    { path: '/upload', label: 'Upload', icon: Upload, auth: true },
    { path: '/admin', label: 'Admin', icon: Users, auth: true, role: 'admin' },
  ]

  const publicNavItems = [
    { path: '/', label: 'Home', icon: Home, public: true },
  ]

  const getNavItems = () => {
    if (isAuthenticated) {
      return navItems.filter(item => {
        if (item.role && user?.role !== item.role) return false
        return true
      })
    }
    return publicNavItems
  }

  const filteredNavItems = getNavItems()

  const isActive = (path: string) => location.pathname === path

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center"
            >
              <FileText className="w-5 h-5 text-white" />
            </motion.div>
            <span className="font-bold text-xl gradient-text">
              Academic Repository
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {filteredNavItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                  isActive(item.path)
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50/50'
                }`}
              >
                <item.icon className="w-4 h-4" />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {/* Search */}
            {isAuthenticated && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 rounded-lg transition-all duration-200"
              >
                <Search className="w-5 h-5" />
              </motion.button>
            )}

            {/* Notifications */}
            {isAuthenticated && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="relative p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 rounded-lg transition-all duration-200"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
              </motion.button>
            )}

            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleTheme}
              className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 rounded-lg transition-all duration-200"
            >
              {theme === 'dark' ? '🌙' : '☀️'}
            </motion.button>

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="relative">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsProfileOpen(!isProfileOpen)}
                  className="flex items-center space-x-2 p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 rounded-lg transition-all duration-200"
                >
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <span className="hidden md:block font-medium">
                    {user?.first_name}
                  </span>
                </motion.button>

                <AnimatePresence>
                  {isProfileOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="absolute right-0 mt-2 w-48 glass rounded-lg shadow-xl border border-white/20"
                    >
                      <div className="py-2">
                        <Link
                          to="/profile"
                          className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:bg-blue-50/50 transition-colors"
                          onClick={() => setIsProfileOpen(false)}
                        >
                          <Settings className="w-4 h-4" />
                          <span>Profile</span>
                        </Link>
                        <button
                          onClick={handleLogout}
                          className="flex items-center space-x-2 w-full px-4 py-2 text-gray-700 hover:bg-red-50/50 hover:text-red-600 transition-colors"
                        >
                          <LogOut className="w-4 h-4" />
                          <span>Logout</span>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  className="btn-secondary"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  Register
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 rounded-lg transition-all duration-200"
            >
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden glass border-t border-white/20"
          >
            <div className="px-4 py-4 space-y-2">
              {filteredNavItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMenuOpen(false)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                    isActive(item.path)
                      ? 'text-blue-600 bg-blue-50'
                      : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50/50'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}

export default Header
