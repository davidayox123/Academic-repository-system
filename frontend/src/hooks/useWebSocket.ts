import { useEffect, useRef, useState, useCallback } from 'react'
import { useAuthStore } from '../stores/useAuthStore'
import { useDashboardStore } from '../stores/useDashboardStore'

interface WebSocketMessage {
  type: string
  data?: any
  message?: string
  timestamp?: number
}

interface UseWebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void
  onError?: (error: Event) => void
  onConnect?: () => void
  onDisconnect?: () => void
  reconnectInterval?: number
  maxReconnectAttempts?: number
}

export const useWebSocket = (options: UseWebSocketOptions = {}) => {
  const {
    onMessage,
    onError,
    onConnect,
    onDisconnect,
    reconnectInterval = 3000,
    maxReconnectAttempts = 5
  } = options
  const { user, token } = useAuthStore()
  const { fetchStats, fetchRecentDocuments, fetchRecentActivity } = useDashboardStore()
  
  const [isConnected, setIsConnected] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected')
  
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectAttemptsRef = useRef(0)
  const reconnectTimeoutRef = useRef<number | null>(null)
  const connectionIdRef = useRef<string>('')

  const generateConnectionId = useCallback(() => {
    return `${user?.id || 'anonymous'}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }, [user?.id])

  const connect = useCallback(() => {
    if (!user || !token) return

    try {
      setConnectionStatus('connecting')
      connectionIdRef.current = generateConnectionId()
      
      const wsUrl = `ws://localhost:8000/api/v1/ws/ws/${connectionIdRef.current}?user_id=${user.id}&token=${token}`
      wsRef.current = new WebSocket(wsUrl)

      wsRef.current.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
        setConnectionStatus('connected')
        reconnectAttemptsRef.current = 0
        onConnect?.()
      }

      wsRef.current.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          console.log('WebSocket message received:', message)

          // Handle built-in message types
          switch (message.type) {
            case 'connected':
              console.log('WebSocket connection confirmed')
              break
                case 'document_uploaded':
              // Refresh dashboard data when a document is uploaded
              fetchStats()
              fetchRecentDocuments()
              fetchRecentActivity()
              break
              
            case 'document_reviewed':
              // Refresh dashboard data when a document is reviewed
              fetchStats()
              fetchRecentActivity()
              break
              
            case 'stats_update':
              // Update dashboard stats in real-time
              if (message.data) {
                // Update the dashboard store with new stats
                console.log('Stats updated:', message.data)
              }
              break
              
            case 'activity_update':
              // Refresh activity feed
              fetchRecentActivity()
              break
              
            case 'pong':
              // Handle ping/pong for connection health
              break
              
            case 'error':
              console.error('WebSocket error message:', message.message)
              setConnectionStatus('error')
              break
              
            default:
              console.log('Unknown message type:', message.type)
          }

          // Call custom message handler
          onMessage?.(message)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      wsRef.current.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason)
        setIsConnected(false)
        setConnectionStatus('disconnected')
        onDisconnect?.()

        // Attempt to reconnect if not a normal closure
        if (event.code !== 1000 && reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectAttemptsRef.current++
          console.log(`Attempting to reconnect... (${reconnectAttemptsRef.current}/${maxReconnectAttempts})`)
          
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, reconnectInterval)
        }
      }

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error)
        setConnectionStatus('error')
        onError?.(error)
      }

    } catch (error) {
      console.error('Error creating WebSocket connection:', error)
      setConnectionStatus('error')
    }
  }, [user, token, onConnect, onDisconnect, onMessage, onError, reconnectInterval, maxReconnectAttempts, generateConnectionId, fetchStats, fetchRecentDocuments, fetchRecentActivity])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }

    if (wsRef.current) {
      wsRef.current.close(1000, 'Manual disconnect')
      wsRef.current = null
    }

    setIsConnected(false)
    setConnectionStatus('disconnected')
  }, [])

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
      return true
    }
    return false
  }, [])

  const ping = useCallback(() => {
    return sendMessage({
      type: 'ping',
      timestamp: Date.now()
    })
  }, [sendMessage])

  const subscribe = useCallback((channel: string) => {
    return sendMessage({
      type: 'subscribe',
      data: { channel }
    })
  }, [sendMessage])

  // Auto-connect when user is available
  useEffect(() => {
    if (user && token) {
      connect()
    }

    return () => {
      disconnect()
    }
  }, [user, token, connect, disconnect])

  // Ping periodically to keep connection alive
  useEffect(() => {
    if (isConnected) {
      const pingInterval = setInterval(() => {
        ping()
      }, 30000) // Ping every 30 seconds

      return () => clearInterval(pingInterval)
    }
  }, [isConnected, ping])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [disconnect])

  return {
    isConnected,
    connectionStatus,
    connect,
    disconnect,
    sendMessage,
    ping,
    subscribe
  }
}

export default useWebSocket
