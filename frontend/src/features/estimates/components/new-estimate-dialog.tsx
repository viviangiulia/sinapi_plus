import { useEffect, useState, type FormEvent } from 'react'
import { X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface NewEstimateDialogProps {
  open: boolean
  onClose: () => void
  onCreate: (name: string) => void
}

interface FormErrors {
  name?: string
  state?: string
  source?: string
  competence?: string
}

function NewEstimateDialog({ open, onClose, onCreate }: NewEstimateDialogProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [state, setState] = useState('MG')
  const [source, setSource] = useState('SINAPI')
  const [competence, setCompetence] = useState('2025-08')
  const [errors, setErrors] = useState<FormErrors>({})

  useEffect(() => {
    if (!open) {
      return undefined
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onClose, open])

  if (!open) {
    return null
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const nextErrors: FormErrors = {}
    if (!name.trim()) nextErrors.name = 'Informe o nome do orçamento.'
    if (!state) nextErrors.state = 'Selecione uma UF.'
    if (!source) nextErrors.source = 'Selecione uma fonte de preços.'
    if (!competence) nextErrors.competence = 'Selecione uma competência.'

    setErrors(nextErrors)
    if (Object.keys(nextErrors).length === 0) {
      onCreate(name.trim())
    }
  }

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-foreground/35 px-8" role="presentation" onMouseDown={onClose}>
      <section
        className="w-full max-w-2xl border bg-surface p-8 text-surface-foreground"
        role="dialog"
        aria-modal="true"
        aria-labelledby="new-estimate-title"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-8 border-b pb-5">
          <div>
            <p className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">Novo orçamento</p>
            <h2 id="new-estimate-title" className="mt-2 text-xl font-semibold tracking-tight">
              Defina o contexto inicial.
            </h2>
          </div>
          <button
            type="button"
            className="flex size-9 items-center justify-center rounded-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            aria-label="Fechar diálogo"
            onClick={onClose}
          >
            <X aria-hidden="true" size={18} />
          </button>
        </div>

        <form className="mt-6 grid grid-cols-2 gap-5" noValidate onSubmit={handleSubmit}>
          <div className="col-span-2 grid gap-2">
            <label className="text-sm font-medium" htmlFor="estimate-name">
              Nome do orçamento
            </label>
            <input
              id="estimate-name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              aria-invalid={Boolean(errors.name)}
              aria-describedby={errors.name ? 'estimate-name-error' : undefined}
              className={cn(
                'h-10 rounded-sm border bg-background px-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:ring-2 focus:ring-ring/20',
                errors.name && 'border-accent',
              )}
              placeholder="Ex.: Reforma da unidade administrativa"
            />
            {errors.name ? (
              <p id="estimate-name-error" className="text-xs text-muted-foreground" role="alert">
                {errors.name}
              </p>
            ) : null}
          </div>

          <div className="col-span-2 grid gap-2">
            <label className="text-sm font-medium" htmlFor="estimate-description">
              Descrição <span className="font-normal text-muted-foreground">(opcional)</span>
            </label>
            <textarea
              id="estimate-description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              className="min-h-20 resize-none rounded-sm border bg-background px-3 py-2 text-sm outline-none placeholder:text-muted-foreground focus:border-ring focus:ring-2 focus:ring-ring/20"
              placeholder="Contexto breve para identificação do orçamento"
            />
          </div>

          <Field label="UF" error={errors.state} id="estimate-state">
            <select id="estimate-state" value={state} onChange={(event) => setState(event.target.value)} className="h-10 rounded-sm border bg-background px-3 text-sm outline-none focus:border-ring focus:ring-2 focus:ring-ring/20">
              <option value="MG">Minas Gerais (MG)</option>
              <option value="SP">São Paulo (SP)</option>
              <option value="RJ">Rio de Janeiro (RJ)</option>
              <option value="BA">Bahia (BA)</option>
            </select>
          </Field>

          <Field label="Fonte de preços" error={errors.source} id="estimate-source">
            <select id="estimate-source" value={source} onChange={(event) => setSource(event.target.value)} className="h-10 rounded-sm border bg-background px-3 text-sm outline-none focus:border-ring focus:ring-2 focus:ring-ring/20">
              <option value="SINAPI">SINAPI</option>
            </select>
          </Field>

          <Field label="Competência" error={errors.competence} id="estimate-competence">
            <select id="estimate-competence" value={competence} onChange={(event) => setCompetence(event.target.value)} className="h-10 rounded-sm border bg-background px-3 text-sm outline-none focus:border-ring focus:ring-2 focus:ring-ring/20">
              <option value="2025-08">Agosto de 2025</option>
              <option value="2025-07">Julho de 2025</option>
            </select>
          </Field>

          <div className="flex items-end justify-end">
            <Button variant="outline" onClick={onClose}>
              Cancelar
            </Button>
          </div>

          <div className="col-span-2 mt-2 flex items-center justify-between border-t pt-5">
            <p className="text-xs text-muted-foreground">Dados simulados para o protótipo.</p>
            <Button type="submit">Criar orçamento</Button>
          </div>
        </form>
      </section>
    </div>
  )
}

interface FieldProps {
  label: string
  error?: string
  id: string
  children: React.ReactNode
}

function Field({ label, error, id, children }: FieldProps) {
  return (
    <div className="grid gap-2">
      <label className="text-sm font-medium" htmlFor={id}>
        {label}
      </label>
      {children}
      {error ? <p className="text-xs text-muted-foreground" role="alert">{error}</p> : null}
    </div>
  )
}

export { NewEstimateDialog }
