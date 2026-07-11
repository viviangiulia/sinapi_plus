import { Calculator, Database, FolderTree, Plus, ShieldCheck } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { NewEstimateDialog } from '@/features/estimates/components/new-estimate-dialog'
import { Button } from '@/components/ui/button'

const referenceDetails = [
  { label: 'Fonte', value: 'SINAPI' },
  { label: 'Competência', value: 'Agosto de 2025' },
  { label: 'Abrangência', value: '27 UFs' },
  { label: 'Preços', value: 'Regionalizados' },
]

const capabilities = [
  {
    icon: FolderTree,
    title: 'Organize seu orçamento',
    description: 'Crie categorias personalizadas e estruture os custos conforme as necessidades de cada projeto.',
  },
  {
    icon: ShieldCheck,
    title: 'Trabalhe com referências confiáveis',
    description: 'Consulte composições e preços regionalizados com rastreabilidade da fonte e competência.',
  },
  {
    icon: Calculator,
    title: 'Quantifique com clareza',
    description: 'Adicione composições, informe quantidades e acompanhe subtotais e o custo total do orçamento.',
  },
]

function HomePage() {
  const navigate = useNavigate()
  const [isNewEstimateOpen, setIsNewEstimateOpen] = useState(false)

  function handleCreateEstimate(name: string) {
    const mockId = `mock-${Date.now()}`
    setIsNewEstimateOpen(false)
    navigate(`/orcamentos/${mockId}`, { state: { name } })
  }

  return (
    <>
      <main className="mx-auto w-full max-w-6xl px-12 py-16">
        <section className="max-w-3xl border-l-2 border-accent pl-7">
          <p className="text-xs font-semibold tracking-[0.16em] text-muted-foreground uppercase">Orçamentos de construção civil</p>
          <h1 className="mt-5 font-editorial text-6xl leading-[0.96] tracking-tight">Custos confiáveis para decisões bem construídas.</h1>
          <p className="mt-7 max-w-2xl text-base leading-7 text-muted-foreground">
            Crie e organize orçamentos de construção civil e infraestrutura com composições de custos, preços
            regionalizados e referências reconhecidas de mercado.
          </p>
          <Button className="mt-8 h-11 px-4" onClick={() => setIsNewEstimateOpen(true)}>
            <Plus aria-hidden="true" size={17} strokeWidth={1.75} />
            Novo orçamento
          </Button>
        </section>

        <section className="mt-18 border-y py-6" aria-labelledby="reference-title">
          <div className="flex items-center justify-between gap-8">
            <div>
              <p id="reference-title" className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">
                Referência de preços atual
              </p>
              <p className="mt-2 text-sm text-muted-foreground">Contexto usado para os novos orçamentos simulados.</p>
            </div>
            <Link
              to="/base-precos"
              className="inline-flex h-9 items-center gap-2 rounded-sm border border-border bg-surface px-3 text-sm font-medium text-foreground transition-colors hover:bg-muted focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            >
              <Database aria-hidden="true" size={16} strokeWidth={1.75} />
              Explorar base de preços
            </Link>
          </div>
          <dl className="mt-6 grid grid-cols-4 border-t pt-5">
            {referenceDetails.map(({ label, value }, index) => (
              <div key={label} className={index === 0 ? 'pr-6' : 'border-l pl-6'}>
                <dt className="text-xs font-medium text-muted-foreground">{label}</dt>
                <dd className="mt-2 text-sm font-semibold tabular-nums">{value}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className="mt-18" aria-labelledby="capabilities-title">
          <div className="max-w-xl">
            <p className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">O que você pode fazer</p>
            <h2 id="capabilities-title" className="mt-3 text-2xl font-semibold tracking-tight">
              Um fluxo de trabalho claro, do contexto ao custo.
            </h2>
          </div>
          <div className="mt-8 grid grid-cols-3 border-t">
            {capabilities.map(({ icon: Icon, title, description }, index) => (
              <article key={title} className={index === 0 ? 'py-6 pr-8' : 'border-l px-8 py-6'}>
                <Icon aria-hidden="true" size={20} strokeWidth={1.5} className="text-primary" />
                <h3 className="mt-6 text-base font-semibold">{title}</h3>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">{description}</p>
              </article>
            ))}
          </div>
        </section>
      </main>

      <NewEstimateDialog open={isNewEstimateOpen} onClose={() => setIsNewEstimateOpen(false)} onCreate={handleCreateEstimate} />
    </>
  )
}

export { HomePage }
