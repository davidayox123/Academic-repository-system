import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { LogIn, User, Building, Shield, GraduationCap } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/useAuthStore'
import toast from 'react-hot-toast'

// Demo accounts from the database
const demoAccounts = {
  student: [
    { id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef', name: 'John Doe', email: 'john.doe@student.edu', department: 'Computer Science' },
    { id: 'auto-generated-uuid', name: 'Alice Smith', email: 'alice.smith@student.edu', department: 'Physics' },
    { id: 'auto-generated-uuid', name: 'Bob Johnson', email: 'bob.johnson@student.edu', department: 'Mathematics' }
  ],
  staff: [
    { id: 'b2c3d4e5-f6a7-8901-2345-67890abcdef0', name: 'Jennifer Anderson', email: 'jennifer.anderson@staff.edu', department: 'Computer Science' }
  ],
  supervisor: [
    { id: 'c3d4e5f6-a7b8-9012-3456-7890abcdef01', name: 'Dr. Rachel White', email: 'rachel.white@supervisor.edu', department: 'Computer Science' }
  ],
  admin: [
    { id: 'd4e5f6a7-b8c9-0123-4567-890abcdef012', name: 'Super Administrator', email: 'super.admin@admin.edu', department: 'Computer Science' }
  ]
}

const Login: React.FC = () => {  
  const [selectedRole, setSelectedRole] = useState<'student' | 'staff' | 'supervisor' | 'admin'>('student')
  const [selectedAccount, setSelectedAccount] = useState<string>('')
  const navigate = useNavigate()
  const { selectRole } = useAuthStore()

  const handleLogin = () => {
    if (!selectedAccount) {
      toast.error('Please select a demo account')
      return
    }

    const account = demoAccounts[selectedRole].find(acc => acc.id === selectedAccount)
    if (!account) {
      toast.error('Account not found')
      return
    }

    // Set user role and ID in store
    selectRole(selectedRole, account.id)

    toast.success(`Logged in as ${account.name}`)
    navigate('/dashboard')
  }

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'student': return <GraduationCap className="w-5 h-5" />
      case 'staff': return <User className="w-5 h-5" />
      case 'supervisor': return <Building className="w-5 h-5" />
      case 'admin': return <Shield className="w-5 h-5" />
      default: return <User className="w-5 h-5" />
    }
  }

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'student': return 'from-blue-600 to-indigo-600'
      case 'staff': return 'from-green-600 to-emerald-600'
      case 'supervisor': return 'from-purple-600 to-violet-600'
      case 'admin': return 'from-red-600 to-orange-600'
      default: return 'from-gray-600 to-gray-700'
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center py-8">
      {/* Back Button */}
      <button
        onClick={() => navigate('/')}
        className="mb-6 px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-all"
        aria-label="Back to Home"
      >
        ← Back
      </button>

      <div className="w-full max-w-md">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass p-8 rounded-3xl shadow-2xl"
        >
          {/* Header */}
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className={`w-16 h-16 bg-gradient-to-r ${getRoleColor(selectedRole)} rounded-2xl flex items-center justify-center mx-auto mb-6`}
            >
              <LogIn className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Academic Repository
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Login with Demo Account
            </p>
          </div>

          {/* Role Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Select Role
            </label>
            <div className="grid grid-cols-2 gap-2">
              {(['student', 'staff', 'supervisor', 'admin'] as const).map((role) => (
                <button
                  key={role}
                  onClick={() => {
                    setSelectedRole(role)
                    setSelectedAccount('')
                  }}
                  className={`p-3 rounded-xl border-2 transition-all duration-200 flex items-center justify-center space-x-2 ${
                    selectedRole === role
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 text-gray-700 dark:text-gray-300'
                  }`}
                >
                  {getRoleIcon(role)}
                  <span className="capitalize text-sm font-medium">{role}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Account Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Choose Demo Account
            </label>
            <div className="space-y-2">
              {demoAccounts[selectedRole].map((account) => (
                <button
                  key={account.id}
                  onClick={() => setSelectedAccount(account.id)}
                  className={`w-full p-4 rounded-xl border-2 transition-all duration-200 text-left ${
                    selectedAccount === account.id
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-10 h-10 bg-gradient-to-r ${getRoleColor(selectedRole)} rounded-lg flex items-center justify-center`}>
                      {getRoleIcon(selectedRole)}
                    </div>
                    <div>
                      <div className="font-medium text-gray-900 dark:text-white">
                        {account.name}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {account.department}
                      </div>
                      <div className="text-xs text-gray-400 dark:text-gray-500">
                        {account.email}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Login Button */}
          <button
            onClick={handleLogin}
            disabled={!selectedAccount}
            className="w-full btn-primary py-3 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LogIn className="w-5 h-5" />
            <span>Login to Dashboard</span>
          </button>

          {/* Info */}
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/30 rounded-xl">
            <p className="text-sm text-blue-700 dark:text-blue-300 text-center">
              🎓 Demo accounts are pre-loaded with sample data for testing all features
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Login
