import { useMemo, useState } from 'react'
import {
  ChevronDown,
  Ellipsis,
  FolderOpen,
  MapPin,
  Plus,
  Search,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { NewEstimateDialog } from '@/features/estimates/components/new-estimate-dialog'

type Estimate = {
  id: string
  name: string
  description?: string
  uf: string
  source: string
  competence: string
  updatedAt: string
  total: number
}

const estimates: Estimate[] = [
  {
    id: 'residencial-horizonte',
    name: 'Residencial Horizonte',
    description: 'Orçamento de infraestrutura para empreendimento residencial.',
    uf: 'MG',
    source: 'SINAPI',
    competence: 'Agosto de 2025',
    updatedAt: '10 de julho de 2026',
    total: 326480.52,
  },
  {
    id: 'infraestrutura-alameda',
    name: 'Infraestrutura Alameda',
    description: 'Redes de água, esgoto e infraestrutura urbana.',
    uf: 'SP',
    source: 'SINAPI',
    competence: 'Agosto de 2025',
    updatedAt: '8 de julho de 2026',
    total: 1280430.2,
  },
  {
    id: 'loteamento-vale-verde',
    name: 'Loteamento Vale Verde',
    description: 'Estimativa preliminar para obras de urbanização.',
    uf: 'PR',
    source: 'SINAPI',
    competence: 'Agosto de 2025',
    updatedAt: '3 de julho de 2026',
    total: 784920.85,
  },
  {
    id: 'sistema-viario-norte',
    name: 'Sistema Viário Norte',
    description: 'Orçamento para pavimentação e serviços complementares.',
    uf: 'BA',
    source: 'SINAPI',
    competence: 'Agosto de 2025',
    updatedAt: '28 de junho de 2026',
    total: 2450780,
  },
]

const brazilianCurrency = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

function EstimatesPage() {
  const navigate = useNavigate()

  const [search, setSearch] = useState('')
  const [selectedUf, setSelectedUf] = useState('TODAS')
  const [isNewEstimateOpen, setIsNewEstimateOpen] = useState(false)
  const [openMenuId, setOpenMenuId] = useState<string | null>(null)

  const availableUfs = useMemo(
    () => [...new Set(estimates.map((estimate) => estimate.uf))].sort(),
    [],
  )

  const filteredEstimates = useMemo(() => {
    const normalizedSearch = search.trim().toLocaleLowerCase('pt-BR')

    return estimates.filter((estimate) => {
      const matchesSearch =
        normalizedSearch.length === 0 ||
        estimate.name.toLocaleLowerCase('pt-BR').includes(normalizedSearch)

      const matchesUf =
        selectedUf === 'TODAS' || estimate.uf === selectedUf

      return matchesSearch && matchesUf
    })
  }, [search, selectedUf])

  function handleCreateEstimate(name: string) {
    const mockId = `mock-${Date.now()}`

    setIsNewEstimateOpen(false)

    navigate(`/orcamentos/${mockId}`, {
      state: { name },
    })
  }

  function handleOpenEstimate(id: string) {
    navigate(`/orcamentos/${id}`)
  }

  return (
    <>
      <main className="mx-auto w-full max-w-6xl px-12 py-16">
        <header className="flex items-end justify-between gap-12 border-b pb-10">
          <div className="max-w-2xl">
            <p className="text-xs font-semibold tracking-[0.16em] text-muted-foreground uppercase">
              Gestão de orçamentos
            </p>

            <h1 className="mt-4 text-4xl font-semibold tracking-tight">
              Orçamentos
            </h1>

            <p className="mt-4 max-w-xl text-sm leading-6 text-muted-foreground">
              Organize, consulte e continue seus orçamentos de construção civil
              e infraestrutura.
            </p>
          </div>

          <Button
            className="h-11 px-4"
            onClick={() => setIsNewEstimateOpen(true)}
          >
            <Plus aria-hidden="true" size={17} strokeWidth={1.75} />
            Novo orçamento
          </Button>
        </header>

        <section className="py-8" aria-label="Filtros de orçamentos">
          <div className="flex items-center gap-3">
            <label className="relative block max-w-md flex-1">
              <span className="sr-only">Buscar orçamento por nome</span>

              <Search
                aria-hidden="true"
                size={17}
                strokeWidth={1.75}
                className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-muted-foreground"
              />

              <input
                type="search"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Buscar por nome..."
                className="h-10 w-full rounded-sm border border-input bg-surface pr-4 pl-10 text-sm text-foreground outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:ring-1 focus:ring-ring"
              />
            </label>

            <label className="relative">
              <span className="sr-only">Filtrar por estado</span>

              <select
                value={selectedUf}
                onChange={(event) => setSelectedUf(event.target.value)}
                className="h-10 min-w-44 appearance-none rounded-sm border border-input bg-surface pr-10 pl-3 text-sm text-foreground outline-none transition-colors focus:border-ring focus:ring-1 focus:ring-ring"
              >
                <option value="TODAS">Todas as UFs</option>

                {availableUfs.map((uf) => (
                  <option key={uf} value={uf}>
                    {uf}
                  </option>
                ))}
              </select>

              <ChevronDown
                aria-hidden="true"
                size={16}
                strokeWidth={1.75}
                className="pointer-events-none absolute top-1/2 right-3 -translate-y-1/2 text-muted-foreground"
              />
            </label>
          </div>
        </section>

        <section aria-labelledby="estimates-list-title">
          <div className="flex items-center justify-between border-b pb-4">
            <h2
              id="estimates-list-title"
              className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase"
            >
              Seus orçamentos
            </h2>

            <p className="text-xs tabular-nums text-muted-foreground">
              {filteredEstimates.length}{' '}
              {filteredEstimates.length === 1
                ? 'orçamento encontrado'
                : 'orçamentos encontrados'}
            </p>
          </div>

          {filteredEstimates.length > 0 ? (
            <div>
              {filteredEstimates.map((estimate) => (
                <article
                  key={estimate.id}
                  className="group relative grid grid-cols-[minmax(0,1fr)_auto] gap-12 border-b py-7 transition-colors hover:bg-muted/45"
                >
                  <button
                    type="button"
                    onClick={() => handleOpenEstimate(estimate.id)}
                    className="min-w-0 cursor-pointer text-left focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-ring"
                  >
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold tracking-tight transition-colors group-hover:text-primary">
                        {estimate.name}
                      </h3>

                      <span className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
                        <MapPin
                          aria-hidden="true"
                          size={13}
                          strokeWidth={1.75}
                        />
                        {estimate.uf}
                      </span>
                    </div>

                    {estimate.description && (
                      <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
                        {estimate.description}
                      </p>
                    )}

                    <div className="mt-4 flex items-center gap-3 text-xs text-muted-foreground">
                      <span className="font-medium text-foreground">
                        {estimate.source}
                      </span>

                      <span aria-hidden="true">·</span>

                      <span>{estimate.competence}</span>

                      <span aria-hidden="true">·</span>

                      <span>Atualizado em {estimate.updatedAt}</span>
                    </div>
                  </button>

                  <div className="flex items-start gap-6">
                    <div className="min-w-40 text-right">
                      <p className="text-[11px] font-semibold tracking-[0.12em] text-muted-foreground uppercase">
                        Total estimado
                      </p>

                      <p className="mt-2 text-lg font-semibold tabular-nums">
                        {brazilianCurrency.format(estimate.total)}
                      </p>
                    </div>

                    <div className="relative">
                      <button
                        type="button"
                        aria-label={`Ações para ${estimate.name}`}
                        aria-expanded={openMenuId === estimate.id}
                        onClick={() =>
                          setOpenMenuId((current) =>
                            current === estimate.id ? null : estimate.id,
                          )
                        }
                        className="flex size-9 items-center justify-center rounded-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
                      >
                        <Ellipsis
                          aria-hidden="true"
                          size={18}
                          strokeWidth={1.75}
                        />
                      </button>

                      {openMenuId === estimate.id && (
                        <div className="absolute top-11 right-0 z-20 w-48 rounded-sm border bg-elevated p-1 text-elevated-foreground shadow-lg">
                          <button
                            type="button"
                            onClick={() => handleOpenEstimate(estimate.id)}
                            className="flex h-9 w-full items-center gap-2 rounded-sm px-3 text-left text-sm transition-colors hover:bg-muted focus-visible:outline-2 focus-visible:outline-ring"
                          >
                            <FolderOpen
                              aria-hidden="true"
                              size={16}
                              strokeWidth={1.75}
                            />
                            Abrir orçamento
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="flex min-h-72 flex-col items-center justify-center border-b text-center">
              <Search
                aria-hidden="true"
                size={24}
                strokeWidth={1.5}
                className="text-muted-foreground"
              />

              <h3 className="mt-5 text-base font-semibold">
                Nenhum orçamento encontrado
              </h3>

              <p className="mt-2 max-w-sm text-sm leading-6 text-muted-foreground">
                Ajuste os termos da busca ou altere o filtro de estado para
                visualizar outros resultados.
              </p>

              <Button
                variant="outline"
                className="mt-6"
                onClick={() => {
                  setSearch('')
                  setSelectedUf('TODAS')
                }}
              >
                Limpar filtros
              </Button>
            </div>
          )}
        </section>
      </main>

      <NewEstimateDialog
        open={isNewEstimateOpen}
        onClose={() => setIsNewEstimateOpen(false)}
        onCreate={handleCreateEstimate}
      />
    </>
  )
}

export { EstimatesPage }