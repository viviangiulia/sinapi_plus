import { Monitor, Moon, Sun } from 'lucide-react'
import { useTheme } from '@/app/providers/use-theme'
import { cn } from '@/lib/utils'

const themeOptions = [
  { value: 'light', label: 'Claro', icon: Sun },
  { value: 'dark', label: 'Escuro', icon: Moon },
  { value: 'system', label: 'Sistema', icon: Monitor },
] as const

function ThemeSelector() {
  const { theme, setTheme } = useTheme()

  return (
    <section aria-labelledby="theme-selector-title">
      <p id="theme-selector-title" className="text-[11px] font-semibold tracking-[0.14em] text-sidebar-foreground/60 uppercase">
        Aparência
      </p>
      <div className="mt-3 grid grid-cols-3 gap-1" role="group" aria-label="Preferência de tema">
        {themeOptions.map(({ value, label, icon: Icon }) => (
          <button
            key={value}
            type="button"
            className={cn(
              'flex min-h-14 flex-col items-center justify-center gap-1 rounded-sm text-[11px] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',
              theme === value
                ? 'bg-sidebar-foreground/12 text-sidebar-foreground'
                : 'text-sidebar-foreground/60 hover:bg-sidebar-foreground/8 hover:text-sidebar-foreground',
            )}
            aria-pressed={theme === value}
            onClick={() => setTheme(value)}
          >
            <Icon aria-hidden="true" size={16} strokeWidth={1.75} />
            <span>{label}</span>
          </button>
        ))}
      </div>
    </section>
  )
}

export { ThemeSelector }
