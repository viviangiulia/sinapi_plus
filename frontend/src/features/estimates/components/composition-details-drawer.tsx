import { useEffect } from 'react'
import { X } from 'lucide-react'

import type {
  Composition,
  CompositionComponentType,
} from '@/features/estimates/components/add-composition-dialog'

interface CompositionDetailsDrawerProps {
  composition: Composition | null
  state: string
  competence: string
  onClose: () => void
}

const brazilianCurrency = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

const brazilianNumber = new Intl.NumberFormat('pt-BR', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 4,
})

const componentTypeLabels: Record<CompositionComponentType, string> = {
  material: 'Material',
  labor: 'Mão de obra',
  equipment: 'Equipamento',
  'auxiliary-composition': 'Composição auxiliar',
}

function CompositionDetailsDrawer({
  composition,
  state,
  competence,
  onClose,
}: CompositionDetailsDrawerProps) {
  useEffect(() => {
    if (!composition) {
      return undefined
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [composition, onClose])

  if (!composition) {
    return null
  }

  return (
    <div
      className="fixed inset-0 z-50 bg-foreground/25"
      role="presentation"
      onMouseDown={onClose}
    >
      <aside
        className="absolute top-0 right-0 flex h-full w-[min(46rem,60vw)] flex-col border-l bg-surface text-surface-foreground shadow-2xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="composition-details-title"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <header className="flex items-start justify-between gap-8 border-b px-8 py-7">
          <div className="min-w-0">
            <p className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">
              Detalhes da composição
            </p>

            <p className="mt-4 text-xs font-semibold tracking-[0.08em] text-primary">
              {composition.code}
            </p>

            <h2
              id="composition-details-title"
              className="mt-2 text-xl font-semibold leading-7 tracking-tight"
            >
              {composition.description}
            </h2>
          </div>

          <button
            type="button"
            aria-label="Fechar detalhes da composição"
            onClick={onClose}
            className="flex size-9 shrink-0 items-center justify-center rounded-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
          >
            <X aria-hidden="true" size={18} strokeWidth={1.75} />
          </button>
        </header>

        <div className="min-h-0 flex-1 overflow-y-auto">
          <section className="grid grid-cols-4 border-b px-8 py-6">
            <Detail label="Unidade" value={composition.unit} />

            <Detail
              label="Fonte"
              value={composition.source}
              withBorder
            />

            <Detail
              label="UF"
              value={state}
              withBorder
            />

            <Detail
              label="Competência"
              value={competence}
              withBorder
            />
          </section>

          <section className="border-b px-8 py-7">
            <p className="text-[11px] font-semibold tracking-[0.14em] text-muted-foreground uppercase">
              Preço unitário
            </p>

            <p className="mt-3 text-3xl font-semibold tracking-tight tabular-nums">
              {brazilianCurrency.format(composition.unitPrice)}
            </p>

            <p className="mt-2 text-xs text-muted-foreground">
              por {composition.unit}
            </p>
          </section>

          <section className="px-8 py-7">
            <div className="flex items-end justify-between gap-8">
              <div>
                <p className="text-[11px] font-semibold tracking-[0.14em] text-muted-foreground uppercase">
                  Componentes
                </p>

                <h3 className="mt-2 text-lg font-semibold tracking-tight">
                  Composição do custo
                </h3>
              </div>

              <p className="text-xs text-muted-foreground">
                {composition.components.length}{' '}
                {composition.components.length === 1
                  ? 'componente'
                  : 'componentes'}
              </p>
            </div>

            <div className="mt-6">
              <div className="grid grid-cols-[5.5rem_minmax(0,1fr)_6.5rem_5rem_7rem] gap-3 border-y bg-muted/30 px-3 py-3 text-[10px] font-semibold tracking-[0.08em] text-muted-foreground uppercase">
                <span>Código</span>
                <span>Descrição</span>
                <span>Tipo</span>
                <span className="text-right">Coef.</span>
                <span className="text-right">Custo</span>
              </div>

              {composition.components.map((component) => {
                const partialCost =
                  component.coefficient * component.unitPrice

                return (
                  <div
                    key={`${component.code}-${component.type}`}
                    className="grid grid-cols-[5.5rem_minmax(0,1fr)_6.5rem_5rem_7rem] items-start gap-3 border-b px-3 py-4"
                  >
                    <span className="text-xs font-semibold text-primary">
                      {component.code}
                    </span>

                    <div className="min-w-0">
                      <p className="text-sm leading-5">
                        {component.description}
                      </p>

                      <p className="mt-1 text-xs text-muted-foreground">
                        {brazilianCurrency.format(component.unitPrice)} /{' '}
                        {component.unit}
                      </p>
                    </div>

                    <span className="text-xs leading-5 text-muted-foreground">
                      {componentTypeLabels[component.type]}
                    </span>

                    <span className="text-right text-xs leading-5 tabular-nums">
                      {brazilianNumber.format(component.coefficient)}
                    </span>

                    <span className="text-right text-xs font-semibold leading-5 tabular-nums">
                      {brazilianCurrency.format(partialCost)}
                    </span>
                  </div>
                )
              })}
            </div>
          </section>
        </div>

        <footer className="border-t px-8 py-5">
          <p className="text-xs leading-5 text-muted-foreground">
            Valores exibidos conforme a fonte, competência e UF do contexto de
            precificação do orçamento.
          </p>
        </footer>
      </aside>
    </div>
  )
}

interface DetailProps {
  label: string
  value: string
  withBorder?: boolean
}

function Detail({ label, value, withBorder = false }: DetailProps) {
  return (
    <div className={withBorder ? 'border-l pl-5' : 'pr-5'}>
      <dt className="text-[10px] font-semibold tracking-[0.1em] text-muted-foreground uppercase">
        {label}
      </dt>

      <dd className="mt-2 text-sm font-semibold">
        {value}
      </dd>
    </div>
  )
}

export { CompositionDetailsDrawer }