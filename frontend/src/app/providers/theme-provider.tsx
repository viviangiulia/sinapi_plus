import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { ThemeContext, type Theme } from './theme-context'

type ResolvedTheme = Exclude<Theme, 'system'>

const storageKey = 'sinapi-theme'

function resolveTheme(theme: Theme): ResolvedTheme {
  if (theme !== 'system') {
    return theme
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    const storedTheme = window.localStorage.getItem(storageKey)
    return storedTheme === 'light' || storedTheme === 'dark' || storedTheme === 'system'
      ? storedTheme
      : 'system'
  })

  useEffect(() => {
    const applyTheme = () => {
      const resolvedTheme = resolveTheme(theme)
      document.documentElement.classList.toggle('dark', resolvedTheme === 'dark')
      document.documentElement.dataset.theme = resolvedTheme
    }

    applyTheme()
    window.localStorage.setItem(storageKey, theme)

    if (theme !== 'system') {
      return undefined
    }

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', applyTheme)
    return () => mediaQuery.removeEventListener('change', applyTheme)
  }, [theme])

  const value = useMemo(() => ({ theme, setTheme }), [theme])
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export { ThemeProvider }
