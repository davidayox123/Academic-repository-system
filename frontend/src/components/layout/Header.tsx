import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Menu,
  X,
  FileText,
  Upload,
  BarChart3,
  Users,
  ChevronDown,
  Moon,
  Sun,
  Monitor,
  UserCheck
} from 'lucide-react'
import { useAuthStore } from '../../stores/useAuthStore'
import { useThemeStore } from '../../stores/useThemeStore'

const Header: React.FC = () => {
  const location = useLocation()
  const { currentRole, switchRole, hasSelectedRole } = useAuthStore()
  const { theme, resolvedTheme, setTheme } = useThemeStore()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isRoleMenuOpen, setIsRoleMenuOpen] = useState(false)
  const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false)
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { path: '/documents', label: 'Documents', icon: FileText },
    { path: '/upload', label: 'Upload', icon: Upload },
    { path: '/admin', label: 'Admin', icon: Users, role: 'admin' },
  ]

  const roles = [
    { value: 'student', label: 'Student', color: 'bg-blue-500' },
    { value: 'staff', label: 'Staff', color: 'bg-green-500' },
    { value: 'supervisor', label: 'Supervisor', color: 'bg-purple-500' },
    { value: 'admin', label: 'Admin', color: 'bg-red-500' },
  ]

  const themes = [
    { value: 'light', label: 'Light', icon: Sun },
    { value: 'dark', label: 'Dark', icon: Moon },
    { value: 'system', label: 'System', icon: Monitor },
  ]

  const filteredNavItems = navItems.filter(item => {
    if (item.role && currentRole !== item.role) return false
    return true
  })
  const isActive = (path: string) => location.pathname === path
  const isHomePage = location.pathname === '/'

  const currentRoleData = roles.find(role => role.value === currentRole)

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-700">
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
            <span className="font-bold text-xl bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Academic Repository
            </span>
          </Link>          {/* Desktop Navigation */}
          {hasSelectedRole && !isHomePage && (
            <nav className="hidden md:flex items-center space-x-8">
              {filteredNavItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                    isActive(item.path)
                      ? 'text-blue-600 bg-blue-50 dark:bg-blue-900/20'
                      : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-900/20'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              ))}
            </nav>
          )}

          {/* Home Link - Only show on non-home pages */}
          {!isHomePage && (
            <nav className="hidden md:flex items-center space-x-8">
              <Link
                to="/"
                className="flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-900/20"
              >
                <FileText className="w-4 h-4" />
                <span>Home</span>
              </Link>
            </nav>
          )}          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {/* Role Switcher */}
            <div className="relative">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsRoleMenuOpen(!isRoleMenuOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-200"
              >
                <div className={`w-3 h-3 rounded-full ${currentRoleData?.color || 'bg-gray-400'}`}></div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-200">
                  {currentRoleData?.label || 'Select Role'}
                </span>
                <ChevronDown className="w-4 h-4 text-gray-500" />
              </motion.button>

              <AnimatePresence>
                {isRoleMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700"
                  >
                    <div className="py-2">
                      {roles.map((role) => (
                        <button
                          key={role.value}
                          onClick={() => {
                            switchRole(role.value as any)
                            setIsRoleMenuOpen(false)
                          }}
                          className={`flex items-center space-x-3 w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${
                            currentRole === role.value ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                          }`}
                        >
                          <div className={`w-3 h-3 rounded-full ${role.color}`}></div>
                          <span className="text-gray-700 dark:text-gray-200">{role.label}</span>
                          {currentRole === role.value && (
                            <UserCheck className="w-4 h-4 text-blue-600 ml-auto" />
                          )}
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Theme Switcher */}
            <div className="relative">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsThemeMenuOpen(!isThemeMenuOpen)}
                className="p-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-900/20 rounded-lg transition-all duration-200"
              >
                {resolvedTheme === 'dark' ? (
                  <Moon className="w-5 h-5" />
                ) : (
                  <Sun className="w-5 h-5" />
                )}
              </motion.button>

              <AnimatePresence>
                {isThemeMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700"
                  >
                    <div className="py-2">
                      {themes.map((themeOption) => (
                        <button
                          key={themeOption.value}
                          onClick={() => {
                            setTheme(themeOption.value as any)
                            setIsThemeMenuOpen(false)
                          }}
                          className={`flex items-center space-x-3 w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${
                            theme === themeOption.value ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                          }`}
                        >
                          <themeOption.icon className="w-4 h-4 text-gray-600 dark:text-gray-300" />
                          <span className="text-gray-700 dark:text-gray-200">{themeOption.label}</span>
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Mobile Menu Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-900/20 rounded-lg transition-all duration-200"
            >
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </motion.button>
          </div>
        </div>        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && !isHomePage && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden py-4 border-t border-gray-200 dark:border-gray-700"
            >
              <nav className="space-y-2">
                <Link
                  to="/"
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-900/20"
                >
                  <FileText className="w-4 h-4" />
                  <span>Home</span>
                </Link>
                {filteredNavItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setIsMenuOpen(false)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                      isActive(item.path)
                        ? 'text-blue-600 bg-blue-50 dark:bg-blue-900/20'
                        : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-blue-50/50 dark:hover:bg-blue-900/20'
                    }`}
                  >
                    <item.icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </Link>
                ))}
              </nav>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  )
}

export default Header
