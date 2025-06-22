import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Users,
  Shield,
  Search,
  Upload,
  Download,
  Star,
  ArrowRight,
  CheckCircle,
  Zap,
  Globe,
  Award,
  GraduationCap,
  UserCheck,
  Crown,
  UserCog
} from 'lucide-react'
import { useAuthStore } from '../stores/useAuthStore'

const Home: React.FC = () => {  const navigate = useNavigate()
  const { selectRole } = useAuthStore()
  const [selectedRole, setSelectedRole] = useState<string>('')

  const roles = [
    {
      value: 'student',
      label: 'Student',
      icon: GraduationCap,
      color: 'bg-blue-500',
      description: 'Upload and manage your academic documents'
    },
    {
      value: 'staff',
      label: 'Staff',
      icon: UserCheck,
      color: 'bg-green-500',
      description: 'Access departmental documents and resources'
    },
    {
      value: 'supervisor',
      label: 'Supervisor',
      icon: UserCog,
      color: 'bg-purple-500',
      description: 'Review and approve student submissions'
    },
    {
      value: 'admin',
      label: 'Admin',
      icon: Crown,
      color: 'bg-red-500',
      description: 'Full system access and user management'
    }
  ]

  const handleGetStarted = () => {
    if (selectedRole) {
      // TODO: Replace 'user-id-placeholder' with the actual user ID from your auth state/store
      selectRole(selectedRole as any, 'user-id-placeholder')
      navigate('/dashboard')
    }
  }

  const features = [
    {
      icon: Upload,
      title: 'Easy Upload',
      description: 'Upload documents with drag-and-drop simplicity. Support for multiple file formats.',
      color: 'blue'
    },
    {
      icon: Search,
      title: 'Smart Search',
      description: 'Find documents quickly with advanced search and filtering capabilities.',
      color: 'green'
    },
    {
      icon: Shield,
      title: 'Secure Storage',
      description: 'Your documents are protected with enterprise-grade security and encryption.',
      color: 'purple'
    },
    {
      icon: Users,
      title: 'Collaboration',
      description: 'Work together with role-based access control and review workflows.',
      color: 'orange'
    },
    {
      icon: Download,
      title: 'Easy Access',
      description: 'Download and share documents with proper version control and tracking.',
      color: 'indigo'
    },
    {
      icon: Award,
      title: 'Quality Control',
      description: 'Maintain high standards with peer review and approval processes.',
      color: 'red'
    }
  ]

  const stats = [
    { number: '10,000+', label: 'Documents Stored' },
    { number: '500+', label: 'Active Users' },
    { number: '50+', label: 'Departments' },
    { number: '99.9%', label: 'Uptime' }
  ]

  const benefits = [
    'Streamlined document management',
    'Collaborative review workflows',
    'Advanced search and filtering',
    'Role-based access control',
    'Audit trails and analytics',
    'Mobile-responsive interface'
  ]

  return (
    <div className="page-container">
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-300/20 rounded-full blur-3xl animate-pulse-slow"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-indigo-300/20 rounded-full blur-3xl animate-pulse-slow"></div>
        </div>

        <div className="content-wrapper text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <motion.div
              className="inline-flex items-center space-x-2 glass px-4 py-2 rounded-full mb-8"
              whileHover={{ scale: 1.05 }}
            >
              <Zap className="w-4 h-4 text-yellow-500" />
              <span className="text-sm font-medium">Modern Academic Repository</span>
            </motion.div>

            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="gradient-text">Academic</span>
              <br />
              <span className="text-gray-900">Repository System</span>
            </h1>            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              A comprehensive platform for managing academic documents, research papers, 
              and scholarly resources with advanced collaboration and review workflows.
            </p>            {/* Role Selection */}
            <div className="mb-8" id="role-selector">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Choose your role to get started:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl mx-auto">
                {roles.map((role) => (
                  <motion.div
                    key={role.value}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setSelectedRole(role.value)}
                    className={`p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                      selectedRole === role.value
                        ? 'border-blue-500 bg-blue-50 shadow-lg'
                        : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                    }`}
                  >
                    <div className={`w-12 h-12 ${role.color} rounded-xl flex items-center justify-center mb-3 mx-auto`}>
                      <role.icon className="w-6 h-6 text-white" />
                    </div>
                    <h4 className="font-semibold text-gray-900 mb-2">{role.label}</h4>
                    <p className="text-sm text-gray-600 text-center">{role.description}</p>
                  </motion.div>
                ))}
              </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <motion.button
                whileHover={{ scale: selectedRole ? 1.05 : 1 }}
                whileTap={{ scale: selectedRole ? 0.95 : 1 }}
                onClick={handleGetStarted}
                disabled={!selectedRole}
                className={`px-8 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 ${
                  selectedRole
                    ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                <span>Get Started</span>
                <ArrowRight className="w-5 h-5" />
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16">
        <div className="content-wrapper">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center glass p-6 rounded-2xl hover-lift"
              >
                <div className="text-3xl md:text-4xl font-bold gradient-text mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600 font-medium">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="content-wrapper">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="section-header">Powerful Features</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need to manage academic documents efficiently and securely
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="glass p-8 rounded-2xl card-hover"
              >
                <div className={`w-12 h-12 bg-${feature.color}-100 rounded-xl flex items-center justify-center mb-6`}>
                  <feature.icon className={`w-6 h-6 text-${feature.color}-600`} />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-3xl mx-4"></div>
        <div className="content-wrapper relative">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Why Choose Our Platform?
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Built specifically for academic institutions with modern technology 
                and user-centric design principles.
              </p>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={benefit}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="flex items-center space-x-3"
                  >
                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700 font-medium">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="glass p-8 rounded-2xl">
                <div className="flex items-center space-x-4 mb-6">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                    <Globe className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Global Accessibility
                    </h3>
                    <p className="text-gray-600">Available anywhere, anytime</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Uptime</span>
                    <span className="font-semibold text-green-600">99.9%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Response Time</span>
                    <span className="font-semibold text-blue-600">&lt; 200ms</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Security Score</span>
                    <div className="flex items-center space-x-1">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <Star key={star} className="w-4 h-4 text-yellow-400 fill-current" />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="content-wrapper">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center glass p-12 rounded-3xl"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Join thousands of academics and researchers who trust our platform 
              for their document management needs.
            </p>
              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  document.getElementById('role-selector')?.scrollIntoView({ behavior: 'smooth' })
                }}
                className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl"
              >
                <span>Get Started Now</span>
                <ArrowRight className="w-5 h-5" />
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home
