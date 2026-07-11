import { useState, type FormEvent } from 'react'
import { ArrowRight, Eye, EyeOff } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface FormErrors {
  email?: string
  password?: string
}

function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState<FormErrors>({})

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const nextErrors: FormErrors = {}
    if (!email.trim()) {
      nextErrors.email = 'Informe seu e-mail.'
    }
    if (!password) {
      nextErrors.password = 'Informe sua senha.'
    }

    setErrors(nextErrors)
    if (Object.keys(nextErrors).length === 0) {
      navigate('/')
    }
  }

  return (
    <main className="grid min-h-screen grid-cols-[minmax(0,1.05fr)_minmax(32rem,0.95fr)] bg-background">
      <section className="flex min-h-screen flex-col justify-between bg-sidebar px-16 py-14 text-sidebar-foreground">
        <div>
          <div className="h-px w-10 bg-accent" />
          <p className="mt-6 text-base font-semibold tracking-[0.16em]">SINAPI+</p>
          <p className="mt-2 text-[11px] font-medium tracking-[0.16em] text-sidebar-foreground/60 uppercase">
            Custos de infraestrutura
          </p>
        </div>

        <div className="max-w-xl border-l-2 border-accent pl-7">
          <p className="font-editorial text-6xl leading-[0.96] tracking-tight">Precisão para construir decisões.</p>
          <p className="mt-7 max-w-md text-sm leading-7 text-sidebar-foreground/65">
            Uma base de trabalho clara para estimativas de infraestrutura com rigor técnico e visão de projeto.
          </p>
        </div>

        <p className="text-xs tracking-wide text-sidebar-foreground/50">SINAPI+ · Ambiente de demonstração</p>
      </section>

      <section className="flex items-center bg-surface px-20 py-14 text-surface-foreground">
        <div className="w-full max-w-md">
          <p className="text-xs font-semibold tracking-[0.16em] text-muted-foreground uppercase">Acesso ao workspace</p>
          <h1 className="mt-4 text-3xl font-semibold tracking-tight">Boas-vindas de volta.</h1>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">Use quaisquer credenciais para entrar no ambiente de demonstração.</p>

          <form className="mt-10 grid gap-5" noValidate onSubmit={handleSubmit}>
            <div className="grid gap-2">
              <label className="text-sm font-medium" htmlFor="email">
                E-mail
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                aria-invalid={Boolean(errors.email)}
                aria-describedby={errors.email ? 'email-error' : undefined}
                className={cn(
                  'h-11 rounded-sm border bg-background px-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:ring-2 focus:ring-ring/20',
                  errors.email && 'border-accent',
                )}
                placeholder="voce@empresa.com.br"
              />
              {errors.email ? (
                <p id="email-error" className="text-xs text-muted-foreground" role="alert">
                  {errors.email}
                </p>
              ) : null}
            </div>

            <div className="grid gap-2">
              <label className="text-sm font-medium" htmlFor="password">
                Senha
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  aria-invalid={Boolean(errors.password)}
                  aria-describedby={errors.password ? 'password-error' : undefined}
                  className={cn(
                    'h-11 w-full rounded-sm border bg-background px-3 pr-11 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:ring-2 focus:ring-ring/20',
                    errors.password && 'border-accent',
                  )}
                  placeholder="Informe sua senha"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 flex w-11 items-center justify-center text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-ring"
                  aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
                  onClick={() => setShowPassword((current) => !current)}
                >
                  {showPassword ? <EyeOff aria-hidden="true" size={18} /> : <Eye aria-hidden="true" size={18} />}
                </button>
              </div>
              {errors.password ? (
                <p id="password-error" className="text-xs text-muted-foreground" role="alert">
                  {errors.password}
                </p>
              ) : null}
            </div>

            <Button className="mt-2 h-11 w-full justify-center" type="submit">
              Entrar no workspace
              <ArrowRight aria-hidden="true" size={17} strokeWidth={1.75} />
            </Button>
          </form>

          <p className="mt-8 border-t pt-5 text-xs leading-5 text-muted-foreground">
            Acesso simulado para validação do protótipo. Nenhuma credencial é armazenada ou verificada.
          </p>
        </div>
      </section>
    </main>
  )
}

export { LoginPage }
