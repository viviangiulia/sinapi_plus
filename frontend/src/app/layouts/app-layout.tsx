import { Database, House, ReceiptText, Settings, UserRound } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import { ThemeSelector } from '@/components/shared/theme-selector'
import { cn } from '@/lib/utils'

const navigation = [
  { to: '/', label: 'Início', icon: House, end: true },
  { to: '/orcamentos', label: 'Orçamentos', icon: ReceiptText, end: false },
  { to: '/base-precos', label: 'Base de preços', icon: Database, end: false },
  { to: '/configuracoes', label: 'Configurações', icon: Settings, end: false },
] as const

function AppLayout() {
  return (
    <div className="grid min-h-screen grid-cols-[17rem_minmax(0,1fr)] bg-background text-foreground">
      <aside className="sticky top-0 flex h-screen flex-col border-r border-sidebar-foreground/15 bg-sidebar px-4 py-5 text-sidebar-foreground">
        <div className="border-b border-sidebar-foreground/15 px-3 pb-6">
          <div className="h-px w-8 bg-accent" />
          <p className="mt-4 text-base font-semibold tracking-[0.14em]">SINAPI+</p>
          <p className="mt-1 text-[10px] font-medium tracking-[0.13em] text-sidebar-foreground/60 uppercase">
            Custos de infraestrutura
          </p>
        </div>

        <nav className="mt-6" aria-label="Navegação principal">
          <p className="px-3 text-[11px] font-semibold tracking-[0.14em] text-sidebar-foreground/60 uppercase">Workspace</p>
          <ul className="mt-3 grid gap-1">
            {navigation.map(({ to, label, icon: Icon, end }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  end={end}
                  className={({ isActive }) =>
                    cn(
                      'flex h-10 items-center gap-3 rounded-sm px-3 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',
                      isActive
                        ? 'bg-sidebar-foreground/12 text-sidebar-foreground'
                        : 'text-sidebar-foreground/65 hover:bg-sidebar-foreground/8 hover:text-sidebar-foreground',
                    )
                  }
                >
                  <Icon aria-hidden="true" size={18} strokeWidth={1.75} />
                  <span>{label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        <div className="mt-auto border-t border-sidebar-foreground/15 pt-5">
          <ThemeSelector />
          <div className="mt-6 flex items-center gap-3 border-t border-sidebar-foreground/15 pt-5">
            <span className="flex size-9 items-center justify-center rounded-full bg-sidebar-foreground/12 text-sidebar-foreground" aria-hidden="true">
              <UserRound size={17} strokeWidth={1.75} />
            </span>
            <div className="min-w-0">
              <p className="truncate text-sm font-medium">Ana Martins</p>
              <p className="mt-0.5 truncate text-xs text-sidebar-foreground/60">Orçamentista · Demonstração</p>
            </div>
          </div>
        </div>
      </aside>

      <main className="min-w-0">
        <Outlet />
      </main>
    </div>
  )
}

export { AppLayout }
