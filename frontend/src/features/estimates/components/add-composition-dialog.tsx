import { useEffect, useMemo, useState } from 'react'
import { Check, Search, X } from 'lucide-react'

import { Button } from '@/components/ui/button'

export type CompositionComponentType =
  | 'material'
  | 'labor'
  | 'equipment'
  | 'auxiliary-composition'

export interface CompositionComponent {
  code: string
  description: string
  type: CompositionComponentType
  unit: string
  coefficient: number
  unitPrice: number
}

export interface Composition {
  code: string
  description: string
  unit: string
  unitPrice: number
  group: string
  source: string
  components: CompositionComponent[]
}

interface AddCompositionDialogProps {
  open: boolean
  categoryName: string
  existingCodes: string[]
  compositions: Composition[]
  onClose: () => void
  onAdd: (composition: Composition) => void
}

const brazilianCurrency = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

function AddCompositionDialog({
  open,
  categoryName,
  existingCodes,
  compositions,
  onClose,
  onAdd,
}: AddCompositionDialogProps) {
  const [search, setSearch] = useState('')

  useEffect(() => {
    if (!open) {
      setSearch('')
      return undefined
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onClose, open])

  const filteredCompositions = useMemo(() => {
    const normalizedSearch = search.trim().toLocaleLowerCase('pt-BR')

    if (!normalizedSearch) {
      return compositions
    }

    return compositions.filter((composition) => {
      return (
        composition.code.toLocaleLowerCase('pt-BR').includes(normalizedSearch) ||
        composition.description
          .toLocaleLowerCase('pt-BR')
          .includes(normalizedSearch)
      )
    })
  }, [compositions, search])

  if (!open) {
    return null
  }

  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-foreground/35 px-8"
      role="presentation"
      onMouseDown={onClose}
    >
      <section
        className="flex max-h-[80vh] w-full max-w-3xl flex-col border bg-surface text-surface-foreground"
        role="dialog"
        aria-modal="true"
        aria-labelledby="add-composition-title"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <header className="flex items-start justify-between gap-8 border-b px-8 py-6">
          <div>
            <p className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">
              Adicionar composição
            </p>

            <h2
              id="add-composition-title"
              className="mt-2 text-xl font-semibold tracking-tight"
            >
              Selecione uma composição.
            </h2>

            <p className="mt-2 text-sm text-muted-foreground">
              Categoria: {categoryName}
            </p>
          </div>

          <button
            type="button"
            aria-label="Fechar diálogo"
            onClick={onClose}
            className="flex size-9 items-center justify-center rounded-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
          >
            <X aria-hidden="true" size={18} strokeWidth={1.75} />
          </button>
        </header>

        <div className="border-b px-8 py-5">
          <label className="relative block">
            <span className="sr-only">
              Buscar composição por código ou descrição
            </span>

            <Search
              aria-hidden="true"
              size={17}
              strokeWidth={1.75}
              className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-muted-foreground"
            />

            <input
              autoFocus
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar por código ou descrição..."
              className="h-10 w-full rounded-sm border bg-background pr-4 pl-10 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:ring-2 focus:ring-ring/20"
            />
          </label>
        </div>

        <div className="min-h-0 flex-1 overflow-y-auto px-8">
          {filteredCompositions.length > 0 ? (
            <div>
              {filteredCompositions.map((composition) => {
                const alreadyAdded = existingCodes.includes(composition.code)

                return (
                  <article
                    key={composition.code}
                    className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-8 border-b py-5"
                  >
                    <div className="min-w-0">
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-semibold tracking-[0.08em] text-primary">
                          {composition.code}
                        </span>

                        <span className="text-xs text-muted-foreground">
                          {composition.group}
                        </span>
                      </div>

                      <p className="mt-2 text-sm font-medium leading-6">
                        {composition.description}
                      </p>

                      <div className="mt-2 flex items-center gap-3 text-xs text-muted-foreground">
                        <span>Unidade: {composition.unit}</span>
                        <span aria-hidden="true">·</span>
                        <span className="tabular-nums">
                          {brazilianCurrency.format(composition.unitPrice)}
                        </span>
                      </div>
                    </div>

                    {alreadyAdded ? (
                      <span className="inline-flex h-9 items-center gap-2 px-3 text-xs font-medium text-muted-foreground">
                        <Check
                          aria-hidden="true"
                          size={15}
                          strokeWidth={1.75}
                        />
                        Adicionada
                      </span>
                    ) : (
                      <Button onClick={() => onAdd(composition)}>
                        Adicionar
                      </Button>
                    )}
                  </article>
                )
              })}
            </div>
          ) : (
            <div className="flex min-h-64 flex-col items-center justify-center text-center">
              <Search
                aria-hidden="true"
                size={24}
                strokeWidth={1.5}
                className="text-muted-foreground"
              />

              <h3 className="mt-5 text-sm font-semibold">
                Nenhuma composição encontrada
              </h3>

              <p className="mt-2 text-sm text-muted-foreground">
                Tente buscar por outro código ou descrição.
              </p>
            </div>
          )}
        </div>

        <footer className="flex items-center justify-between border-t px-8 py-5">
          <p className="text-xs text-muted-foreground">
            {filteredCompositions.length}{' '}
            {filteredCompositions.length === 1
              ? 'composição encontrada'
              : 'composições encontradas'}
          </p>

          <Button variant="outline" onClick={onClose}>
            Concluir
          </Button>
        </footer>
      </section>
    </div>
  )
}

export { AddCompositionDialog }