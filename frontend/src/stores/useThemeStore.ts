import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type Theme = 'light' | 'dark' | 'system'

interface ThemeState {
  theme: Theme
  resolvedTheme: 'light' | 'dark'
}

interface ThemeActions {
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
}

const getSystemTheme = (): 'light' | 'dark' => {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const resolveTheme = (theme: Theme): 'light' | 'dark' => {
  if (theme === 'system') {
    return getSystemTheme()
  }
  return theme
}

const applyTheme = (resolvedTheme: 'light' | 'dark') => {
  if (typeof document !== 'undefined') {
    const root = document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(resolvedTheme)
    
    // Also update the data attribute for better CSS targeting
    root.setAttribute('data-theme', resolvedTheme)
  }
}

export const useThemeStore = create<ThemeState & ThemeActions>()(
  persist(
    (set, get) => ({
      // State
      theme: 'light',
      resolvedTheme: 'light',

      // Actions
      setTheme: (theme: Theme) => {
        const resolved = resolveTheme(theme)
        
        set({
          theme,
          resolvedTheme: resolved,
        })

        applyTheme(resolved)
      },

      toggleTheme: () => {
        const { theme } = get()
        const newTheme = theme === 'dark' ? 'light' : 'dark'
        const resolved = resolveTheme(newTheme)
        
        set({
          theme: newTheme,
          resolvedTheme: resolved,
        })

        applyTheme(resolved)
      },
    }),
    {
      name: 'theme-storage',
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Apply theme on rehydration
          applyTheme(state.resolvedTheme)
        }
      },
    }
  )
)

// Listen for system theme changes
if (typeof window !== 'undefined') {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', () => {
    const { theme, setTheme } = useThemeStore.getState()
    if (theme === 'system') {
      setTheme('system') // This will trigger a re-resolution
    }
  })

  // Initialize theme on load
  const { theme } = useThemeStore.getState()
  const resolved = resolveTheme(theme)
  document.documentElement.classList.toggle('dark', resolved === 'dark')
}
