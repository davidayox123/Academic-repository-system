import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Users, 
  Shield, 
  Settings, 
  BarChart3, 
  FileText,
  Download,
  TrendingUp,
  UserPlus,
  Building,
  Search,
  MoreHorizontal
} from 'lucide-react'
import { adminApi, handleApiError, usersApi } from '../services/api'
import type { UserRole } from '../types'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import toast from 'react-hot-toast'
import { formatDistanceToNow } from 'date-fns'

declare interface UserStatsData {
  total_users: number
  active_users: number
  by_role: {
    students: number
    staff: number
    supervisors: number
    admins: number
  }
}

interface UserData {
  id: string
  first_name: string
  last_name: string
  email: string
  role: string
  department_id: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

const Admin: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'users' | 'analytics' | 'settings'>('dashboard')
  const [isLoading, setIsLoading] = useState(true)
  const [userStats, setUserStats] = useState<UserStatsData | null>(null)
  const [users, setUsers] = useState<UserData[]>([])
  const [usersLoading, setUsersLoading] = useState(false)
  const [userSearch, setUserSearch] = useState('')
  const [userRoleFilter, setUserRoleFilter] = useState('')
  const [showAddUser, setShowAddUser] = useState(false)
  const [addUserLoading, setAddUserLoading] = useState(false)
  const [addUserForm, setAddUserForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    role: 'student',
    department_id: '',
  })
  const [departments, setDepartments] = useState<{ id: string; name: string }[]>([])

  useEffect(() => {
    fetchInitialData()
  }, [])

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers()
    }
  }, [activeTab, userSearch, userRoleFilter])

  useEffect(() => {
    usersApi.getDepartments().then(res => setDepartments(res.data)).catch(() => setDepartments([]))
  }, [])

  const fetchInitialData = async () => {
    try {
      setIsLoading(true)
      const [userStatsRes] = await Promise.all([
        adminApi.getUserStats()
      ])
      
      setUserStats(userStatsRes.data)
    } catch (err: any) {
      const errorMessage = handleApiError(err)
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchUsers = async () => {
    try {
      setUsersLoading(true)
      const filters = {
        search: userSearch || undefined,
        role: userRoleFilter || undefined,
        limit: 50
      }
      const response = await adminApi.getUsers(filters)
      setUsers(
        response.data.items.map((user: any) => {
          // Split name into first_name and last_name (fallback if only one name)
          const [first_name, ...rest] = (user.name || '').split(' ')
          const last_name = rest.join(' ') || ''
          return {
            id: user.id,
            first_name: first_name || '',
            last_name: last_name,
            email: user.email,
            role: user.role,
            department_id: user.department_name || '',
            is_active: user.is_active,
            created_at: user.created_at,
            updated_at: user.updated_at
          }
        })
      )
    } catch (err: any) {
      const errorMessage = handleApiError(err)
      toast.error(errorMessage)
    } finally {
      setUsersLoading(false)
    }
  }

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault()
    setAddUserLoading(true)
    try {
      await usersApi.createUser({
        name: `${addUserForm.first_name} ${addUserForm.last_name}`.trim(),
        email: addUserForm.email,
        password: addUserForm.password,
        confirm_password: addUserForm.password,
        role: addUserForm.role as UserRole,
        department_id: addUserForm.department_id
      })
      toast.success('User added successfully')
      setShowAddUser(false)
      setAddUserForm({
        first_name: '', last_name: '', email: '', password: '', role: 'student', department_id: ''
      })
      fetchUsers()
    } catch (err: any) {
      toast.error(handleApiError(err))
    } finally {
      setAddUserLoading(false)
    }
  }

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'users', label: 'Users', icon: Users },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'settings', label: 'Settings', icon: Settings }
  ] as const

  const renderDashboard = () => (
    <div className="space-y-8">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          {
            title: 'Total Users',
            value: userStats?.total_users || 0,
            change: '',
            icon: Users,
            color: 'blue'
          },
          {
            title: 'Total Documents',
            value: 0,
            change: '',
            icon: FileText,
            color: 'green'
          },
          {
            title: 'Departments',
            value: 0,
            change: 'Active',
            icon: Building,
            color: 'purple'
          },
          {
            title: 'Total Downloads',
            value: 0,
            change: 'All time',
            icon: Download,
            color: 'orange'
          }
        ].map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass p-6 rounded-2xl"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 bg-${stat.color}-100 dark:bg-${stat.color}-900/30 rounded-xl flex items-center justify-center`}>
                <stat.icon className={`w-6 h-6 text-${stat.color}-600 dark:text-${stat.color}-400`} />
              </div>
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
              {stat.value.toLocaleString()}
            </div>
            <div className="text-sm text-gray-500">{stat.title}</div>
            <div className="text-xs text-green-600 mt-2">{stat.change}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )

  const renderUsers = () => (
    <div className="space-y-6">
      {/* User Management Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">User Management</h2>
        <button className="btn-primary flex items-center space-x-2" onClick={() => setShowAddUser(true)}>
          <UserPlus className="w-4 h-4" />
          <span>Add User</span>
        </button>
      </div>

      {/* Search and Filters */}
      <div className="glass p-4 rounded-xl">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search users..."
              value={userSearch}
              onChange={(e) => setUserSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500"
            />
          </div>
          <select
            value={userRoleFilter}
            onChange={(e) => setUserRoleFilter(e.target.value)}
            className="px-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500"
          >
            <option value="">All Roles</option>
            <option value="student">Students</option>
            <option value="staff">Staff</option>
            <option value="supervisor">Supervisors</option>
            <option value="admin">Admins</option>
          </select>
        </div>
      </div>

      {/* Users Table */}
      <div className="glass rounded-xl overflow-hidden">
        {usersLoading ? (
          <div className="p-8 text-center">
            <LoadingSpinner size="lg" text="Loading users..." />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700/50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Role
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Department
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Joined
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-600">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/30">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>                        <div className="text-sm font-medium text-gray-900 dark:text-white">
                          {user.first_name} {user.last_name}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {user.email}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        user.role === 'admin' ? 'bg-red-100 text-red-800' :
                        user.role === 'supervisor' ? 'bg-purple-100 text-purple-800' :
                        user.role === 'staff' ? 'bg-green-100 text-green-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {user.department_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {formatDistanceToNow(new Date(user.created_at), { addSuffix: true })}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                        <MoreHorizontal className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add User Modal */}
      <AnimatePresence>
        {showAddUser && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
            <motion.form initial={{ scale: 0.9 }} animate={{ scale: 1 }} exit={{ scale: 0.9 }} onSubmit={handleAddUser} className="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-xl w-full max-w-md">
              <h3 className="text-xl font-bold mb-4">Add New User</h3>
              <div className="space-y-3">
                <input type="text" required placeholder="First Name" className="input w-full" value={addUserForm.first_name} onChange={e => setAddUserForm(f => ({ ...f, first_name: e.target.value }))} />
                <input type="text" required placeholder="Last Name" className="input w-full" value={addUserForm.last_name} onChange={e => setAddUserForm(f => ({ ...f, last_name: e.target.value }))} />
                <input type="email" required placeholder="Email" className="input w-full" value={addUserForm.email} onChange={e => setAddUserForm(f => ({ ...f, email: e.target.value }))} />
                <input type="password" required placeholder="Password" className="input w-full" value={addUserForm.password} onChange={e => setAddUserForm(f => ({ ...f, password: e.target.value }))} />
                <select className="input w-full" value={addUserForm.role} onChange={e => setAddUserForm(f => ({ ...f, role: e.target.value }))}>
                  <option value="student">Student</option>
                  <option value="staff">Staff</option>
                  <option value="supervisor">Supervisor</option>
                  <option value="admin">Admin</option>
                </select>
                <select className="input w-full" value={addUserForm.department_id} onChange={e => setAddUserForm(f => ({ ...f, department_id: e.target.value }))} required>
                  <option value="">Select Department</option>
                  {departments.map(dep => (
                    <option key={dep.id} value={dep.id}>{dep.name}</option>
                  ))}
                </select>
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button type="button" className="btn-secondary" onClick={() => setShowAddUser(false)} disabled={addUserLoading}>Cancel</button>
                <button type="submit" className="btn-primary" disabled={addUserLoading}>{addUserLoading ? 'Adding...' : 'Add User'}</button>
              </div>
            </motion.form>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )

  const renderAnalytics = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Analytics</h2>
      <div className="glass p-8 rounded-2xl text-center">
        <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Advanced Analytics
        </h3>
        <p className="text-gray-600 dark:text-gray-300">
          Detailed analytics charts and reports will be implemented here.
        </p>
      </div>
    </div>
  )

  const renderSettings = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">System Settings</h2>
      <div className="glass p-8 rounded-2xl text-center">
        <Settings className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          System Configuration
        </h3>
        <p className="text-gray-600 dark:text-gray-300">
          System settings and configuration options will be implemented here.
        </p>
      </div>
    </div>
  )

  if (isLoading) {
    return (
      <div className="page-container">
        <div className="content-wrapper">
          <div className="flex items-center justify-center min-h-[400px]">
            <LoadingSpinner size="lg" text="Loading admin dashboard..." />
          </div>
        </div>
      </div>
    )
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
              className="w-16 h-16 bg-gradient-to-r from-red-600 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-6"
            >
              <Shield className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="section-header">Admin Panel</h1>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              System administration and user management
            </p>
          </div>

          {/* Navigation Tabs */}
          <div className="glass p-2 rounded-2xl mb-8">
            <div className="flex items-center space-x-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm'
                      : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === 'dashboard' && renderDashboard()}
            {activeTab === 'users' && renderUsers()}
            {activeTab === 'analytics' && renderAnalytics()}
            {activeTab === 'settings' && renderSettings()}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}

export default Admin
