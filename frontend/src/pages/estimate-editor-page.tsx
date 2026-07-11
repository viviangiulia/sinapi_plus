import { useMemo, useState } from 'react'
import {
  ArrowLeft,
  ChevronDown,
  ChevronRight,
  Ellipsis,
  FolderPlus,
  Pencil,
  Plus,
  Trash2,
  Save
} from 'lucide-react'
import { Link, useLocation, useParams } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import {
  AddCompositionDialog,
  type Composition,
} from '@/features/estimates/components/add-composition-dialog'
import { CompositionDetailsDrawer } from '@/features/estimates/components/composition-details-drawer'

interface EstimateItem {
  id: string
  composition: Composition
  quantity: number
}

interface EstimateCategory {
  id: string
  name: string
  collapsed: boolean
  items: EstimateItem[]
}

const availableCompositions: Composition[] = [
  {
    code: '98546',
    description: 'Assentamento de tubo de PVC para rede de água, DN 100 mm.',
    unit: 'M',
    unitPrice: 130,
    group: 'Água Potável',
    source: 'SINAPI',
    components: [
      {
        code: '00009836',
        description: 'Tubo PVC para rede de água, DN 100 mm',
        type: 'material',
        unit: 'M',
        coefficient: 1.04,
        unitPrice: 48.2,
      },
      {
        code: '88246',
        description: 'Assentador de tubos com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.35,
        unitPrice: 24.8,
      },
      {
        code: '88316',
        description: 'Servente com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.35,
        unitPrice: 20.15,
      },
      {
        code: '90105',
        description: 'Escavação mecanizada de vala',
        type: 'auxiliary-composition',
        unit: 'M³',
        coefficient: 0.42,
        unitPrice: 76.5,
      },
    ],
  },
  {
    code: '89356',
    description:
      'Ligação predial de água com tubo de polietileno, incluindo conexões.',
    unit: 'UN',
    unitPrice: 619.37,
    group: 'Água Potável',
    source: 'SINAPI',
    components: [
      {
        code: '00009813',
        description: 'Tubo de polietileno PEAD para ligação predial',
        type: 'material',
        unit: 'M',
        coefficient: 8.5,
        unitPrice: 18.4,
      },
      {
        code: '00003148',
        description: 'Fita veda rosca em rolos de 18 mm x 50 m',
        type: 'material',
        unit: 'UN',
        coefficient: 0.02,
        unitPrice: 14.5,
      },
      {
        code: '88248',
        description: 'Auxiliar de encanador com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 1.5,
        unitPrice: 21.8,
      },
      {
        code: '88267',
        description: 'Encanador com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 1.5,
        unitPrice: 27.3,
      },
    ],
  },
  {
    code: '94796',
    description:
      'Hidrômetro DN 20 mm, incluindo instalação e acessórios.',
    unit: 'UN',
    unitPrice: 284.9,
    group: 'Água Potável',
    source: 'SINAPI',
    components: [
      {
        code: '00012773',
        description: 'Hidrômetro unijato, vazão máxima 3 m³/h, DN 20 mm',
        type: 'material',
        unit: 'UN',
        coefficient: 1,
        unitPrice: 198.5,
      },
      {
        code: '00003148',
        description: 'Fita veda rosca em rolos de 18 mm x 50 m',
        type: 'material',
        unit: 'UN',
        coefficient: 0.02,
        unitPrice: 14.5,
      },
      {
        code: '88248',
        description: 'Auxiliar de encanador com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.45,
        unitPrice: 21.8,
      },
      {
        code: '88267',
        description: 'Encanador com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.45,
        unitPrice: 27.3,
      },
    ],
  },
  {
    code: '90695',
    description:
      'Tubo de PVC para rede coletora de esgoto, DN 150 mm.',
    unit: 'M',
    unitPrice: 186.75,
    group: 'Esgoto Sanitário',
    source: 'SINAPI',
    components: [
      {
        code: '00009838',
        description: 'Tubo PVC para rede coletora de esgoto, DN 150 mm',
        type: 'material',
        unit: 'M',
        coefficient: 1.05,
        unitPrice: 92.4,
      },
      {
        code: '88246',
        description: 'Assentador de tubos com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.42,
        unitPrice: 24.8,
      },
      {
        code: '88316',
        description: 'Servente com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.42,
        unitPrice: 20.15,
      },
      {
        code: '90105',
        description: 'Escavação mecanizada de vala',
        type: 'auxiliary-composition',
        unit: 'M³',
        coefficient: 0.55,
        unitPrice: 76.5,
      },
    ],
  },
  {
    code: '97902',
    description:
      'Poço de visita circular para rede de esgoto, incluindo materiais.',
    unit: 'UN',
    unitPrice: 4850.6,
    group: 'Esgoto Sanitário',
    source: 'SINAPI',
    components: [
      {
        code: '00012568',
        description: 'Anel de concreto armado para poço de visita',
        type: 'material',
        unit: 'UN',
        coefficient: 3,
        unitPrice: 580,
      },
      {
        code: '00011386',
        description: 'Tampão circular em ferro fundido para poço de visita',
        type: 'material',
        unit: 'UN',
        coefficient: 1,
        unitPrice: 920,
      },
      {
        code: '88309',
        description: 'Pedreiro com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 8,
        unitPrice: 28.4,
      },
      {
        code: '88316',
        description: 'Servente com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 8,
        unitPrice: 20.15,
      },
      {
        code: '94970',
        description: 'Concreto FCK 20 MPa, preparo mecânico',
        type: 'auxiliary-composition',
        unit: 'M³',
        coefficient: 0.65,
        unitPrice: 520,
      },
    ],
  },
  {
    code: '94273',
    description: 'Assentamento de guia de concreto para urbanização.',
    unit: 'M',
    unitPrice: 58.42,
    group: 'Pavimentação',
    source: 'SINAPI',
    components: [
      {
        code: '00004059',
        description: 'Meio-fio ou guia de concreto pré-moldado',
        type: 'material',
        unit: 'M',
        coefficient: 1.005,
        unitPrice: 32.5,
      },
      {
        code: '88309',
        description: 'Pedreiro com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.25,
        unitPrice: 28.4,
      },
      {
        code: '88316',
        description: 'Servente com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.25,
        unitPrice: 20.15,
      },
    ],
  },
  {
    code: '95995',
    description:
      'Execução de pavimento com blocos intertravados de concreto.',
    unit: 'M²',
    unitPrice: 94.8,
    group: 'Pavimentação',
    source: 'SINAPI',
    components: [
      {
        code: '00036155',
        description: 'Bloco intertravado de concreto para pavimentação',
        type: 'material',
        unit: 'M²',
        coefficient: 1.004,
        unitPrice: 52.4,
      },
      {
        code: '00000370',
        description: 'Areia média para assentamento',
        type: 'material',
        unit: 'M³',
        coefficient: 0.0568,
        unitPrice: 145,
      },
      {
        code: '88260',
        description: 'Calceteiro com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 0.4,
        unitPrice: 27.8,
      },
      {
        code: '91277',
        description: 'Placa vibratória reversível com motor a gasolina',
        type: 'equipment',
        unit: 'CHP',
        coefficient: 0.08,
        unitPrice: 12.5,
      },
    ],
  },
  {
    code: '93358',
    description:
      'Escavação manual de vala com profundidade menor ou igual a 1,30 m.',
    unit: 'M³',
    unitPrice: 82.45,
    group: 'Terraplenagem',
    source: 'SINAPI',
    components: [
      {
        code: '88316',
        description: 'Servente com encargos complementares',
        type: 'labor',
        unit: 'H',
        coefficient: 3.956,
        unitPrice: 20.15,
      },
    ],
  },
]

const initialCategories: EstimateCategory[] = [
  {
    id: 'agua-potavel',
    name: 'Água Potável',
    collapsed: false,
    items: [
      {
        id: 'item-1',
        composition: availableCompositions[0],
        quantity: 250,
      },
      {
        id: 'item-2',
        composition: availableCompositions[1],
        quantity: 32,
      },
    ],
  },
  {
    id: 'esgoto-sanitario',
    name: 'Esgoto Sanitário',
    collapsed: false,
    items: [
      {
        id: 'item-3',
        composition: availableCompositions[3],
        quantity: 180,
      },
      {
        id: 'item-4',
        composition: availableCompositions[4],
        quantity: 4,
      },
    ],
  },
]

const brazilianCurrency = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

function EstimateEditorPage() {
  const { estimateId } = useParams()
  const location = useLocation()

  const [categories, setCategories] =
    useState<EstimateCategory[]>(initialCategories)

  const [activeCategoryId, setActiveCategoryId] = useState<string | null>(null)
  const [openMenuId, setOpenMenuId] = useState<string | null>(null)
  const [isCreatingCategory, setIsCreatingCategory] = useState(false)
  const [newCategoryName, setNewCategoryName] = useState('')
  const [selectedComposition, setSelectedComposition] =
  useState<Composition | null>(null)

  const estimateName =
    (location.state as { name?: string } | null)?.name ??
    getEstimateName(estimateId)

  const total = useMemo(() => {
    return categories.reduce((estimateTotal, category) => {
      return estimateTotal + getCategorySubtotal(category)
    }, 0)
  }, [categories])

  const activeCategory =
    categories.find((category) => category.id === activeCategoryId) ?? null

  function toggleCategory(categoryId: string) {
    setCategories((current) =>
      current.map((category) =>
        category.id === categoryId
          ? { ...category, collapsed: !category.collapsed }
          : category,
      ),
    )
  }

  function updateQuantity(
    categoryId: string,
    itemId: string,
    quantity: number,
  ) {
    const validQuantity = Math.max(0, quantity)

    setCategories((current) =>
      current.map((category) =>
        category.id === categoryId
          ? {
              ...category,
              items: category.items.map((item) =>
                item.id === itemId
                  ? { ...item, quantity: validQuantity }
                  : item,
              ),
            }
          : category,
      ),
    )
  }

  function removeItem(categoryId: string, itemId: string) {
    setCategories((current) =>
      current.map((category) =>
        category.id === categoryId
          ? {
              ...category,
              items: category.items.filter((item) => item.id !== itemId),
            }
          : category,
      ),
    )
  }

  function addComposition(composition: Composition) {
    if (!activeCategoryId) {
      return
    }

    setCategories((current) =>
      current.map((category) => {
        if (category.id !== activeCategoryId) {
          return category
        }

        const alreadyExists = category.items.some(
          (item) => item.composition.code === composition.code,
        )

        if (alreadyExists) {
          return category
        }

        return {
          ...category,
          items: [
            ...category.items,
            {
              id: `item-${Date.now()}`,
              composition,
              quantity: 1,
            },
          ],
        }
      }),
    )
  }

  function createCategory() {
    const name = newCategoryName.trim()

    if (!name) {
      return
    }

    setCategories((current) => [
      ...current,
      {
        id: `category-${Date.now()}`,
        name,
        collapsed: false,
        items: [],
      },
    ])

    setNewCategoryName('')
    setIsCreatingCategory(false)
  }

  function renameCategory(categoryId: string) {
    const category = categories.find((item) => item.id === categoryId)

    if (!category) {
      return
    }

    const nextName = window.prompt('Novo nome da categoria:', category.name)

    if (!nextName?.trim()) {
      return
    }

    setCategories((current) =>
      current.map((item) =>
        item.id === categoryId
          ? { ...item, name: nextName.trim() }
          : item,
      ),
    )

    setOpenMenuId(null)
  }

  function deleteCategory(categoryId: string) {
    const category = categories.find((item) => item.id === categoryId)

    if (!category) {
      return
    }

    const confirmed = window.confirm(
      `Excluir a categoria "${category.name}" e todos os seus itens?`,
    )

    if (!confirmed) {
      return
    }

    setCategories((current) =>
      current.filter((category) => category.id !== categoryId),
    )

    setOpenMenuId(null)
  }

  return (
    <>
      <main className="mx-auto w-full max-w-6xl px-12 py-12">
        <Link
          to="/orcamentos"
          className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
        >
          <ArrowLeft aria-hidden="true" size={16} strokeWidth={1.75} />
          Orçamentos
        </Link>

        <header className="mt-8 grid grid-cols-[minmax(0,1fr)_auto] items-end gap-12 border-b pb-8">
          <div className="min-w-0">
            <p className="text-xs font-semibold tracking-[0.16em] text-muted-foreground uppercase">
              Orçamento
            </p>

            <h1 className="mt-3 text-4xl font-semibold tracking-tight">
              {estimateName}
            </h1>

            <div className="mt-4 flex items-center gap-3 text-sm text-muted-foreground">
              <span className="font-medium text-foreground">MG</span>
              <span aria-hidden="true">·</span>
              <span>SINAPI</span>
              <span aria-hidden="true">·</span>
              <span>Agosto de 2025</span>
            </div>
          </div>

          <div className="flex items-end gap-8">
            <div className="min-w-56 border-l border-accent pl-6 text-right">
                <p className="text-[11px] font-semibold tracking-[0.14em] text-muted-foreground uppercase">
                Total estimado
                </p>

                <p className="mt-2 text-3xl font-semibold tracking-tight tabular-nums">
                {brazilianCurrency.format(total)}
                </p>

                <p className="mt-2 text-xs text-muted-foreground">
                {categories.length}{' '}
                {categories.length === 1 ? 'categoria' : 'categorias'}
                </p>
            </div>

            <Button>
                <Save aria-hidden="true" size={16} strokeWidth={1.75} />
                Salvar
            </Button>
            </div>
        </header>

        <section className="mt-10">
          <div className="flex items-center justify-between border-b pb-4">
            <div>
              <p className="text-xs font-semibold tracking-[0.14em] text-muted-foreground uppercase">
                Estrutura do orçamento
              </p>

              <p className="mt-2 text-sm text-muted-foreground">
                Organize as composições em categorias e defina suas quantidades.
              </p>
            </div>

            <Button
              variant="outline"
              onClick={() => setIsCreatingCategory(true)}
            >
              <FolderPlus aria-hidden="true" size={16} strokeWidth={1.75} />
              Nova categoria
            </Button>
          </div>

          {isCreatingCategory && (
            <div className="flex items-end gap-3 border-b bg-muted/35 px-5 py-5">
              <label className="grid flex-1 gap-2">
                <span className="text-xs font-medium text-muted-foreground">
                  Nome da categoria
                </span>

                <input
                  autoFocus
                  value={newCategoryName}
                  onChange={(event) => setNewCategoryName(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter') {
                      createCategory()
                    }

                    if (event.key === 'Escape') {
                      setIsCreatingCategory(false)
                      setNewCategoryName('')
                    }
                  }}
                  placeholder="Ex.: Drenagem"
                  className="h-10 rounded-sm border bg-background px-3 text-sm outline-none placeholder:text-muted-foreground focus:border-ring focus:ring-2 focus:ring-ring/20"
                />
              </label>

              <Button variant="outline" onClick={() => {
                setIsCreatingCategory(false)
                setNewCategoryName('')
              }}>
                Cancelar
              </Button>

              <Button onClick={createCategory}>Criar categoria</Button>
            </div>
          )}

          <div>
            {categories.map((category) => {
              const subtotal = getCategorySubtotal(category)

              return (
                <article key={category.id} className="border-b">
                  <header className="flex items-center justify-between gap-8 py-6">
                    <button
                      type="button"
                      onClick={() => toggleCategory(category.id)}
                      className="flex min-w-0 items-center gap-3 text-left focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
                    >
                      {category.collapsed ? (
                        <ChevronRight
                          aria-hidden="true"
                          size={18}
                          strokeWidth={1.75}
                          className="shrink-0 text-muted-foreground"
                        />
                      ) : (
                        <ChevronDown
                          aria-hidden="true"
                          size={18}
                          strokeWidth={1.75}
                          className="shrink-0 text-muted-foreground"
                        />
                      )}

                      <div className="min-w-0">
                        <h2 className="text-lg font-semibold tracking-tight">
                          {category.name}
                        </h2>

                        <p className="mt-1 text-xs text-muted-foreground">
                          {category.items.length}{' '}
                          {category.items.length === 1
                            ? 'composição'
                            : 'composições'}
                        </p>
                      </div>
                    </button>

                    <div className="flex items-center gap-6">
                      <div className="min-w-40 text-right">
                        <p className="text-[10px] font-semibold tracking-[0.12em] text-muted-foreground uppercase">
                          Subtotal
                        </p>

                        <p className="mt-1 text-base font-semibold tabular-nums">
                          {brazilianCurrency.format(subtotal)}
                        </p>
                      </div>

                      <div className="relative">
                        <button
                          type="button"
                          aria-label={`Ações para ${category.name}`}
                          aria-expanded={openMenuId === category.id}
                          onClick={() =>
                            setOpenMenuId((current) =>
                              current === category.id ? null : category.id,
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

                        {openMenuId === category.id && (
                          <div className="absolute top-11 right-0 z-20 w-48 rounded-sm border bg-elevated p-1 text-elevated-foreground shadow-lg">
                            <button
                              type="button"
                              onClick={() => renameCategory(category.id)}
                              className="flex h-9 w-full items-center gap-2 rounded-sm px-3 text-left text-sm transition-colors hover:bg-muted"
                            >
                              <Pencil
                                aria-hidden="true"
                                size={15}
                                strokeWidth={1.75}
                              />
                              Renomear
                            </button>

                            <button
                              type="button"
                              onClick={() => deleteCategory(category.id)}
                              className="flex h-9 w-full items-center gap-2 rounded-sm px-3 text-left text-sm transition-colors hover:bg-muted"
                            >
                              <Trash2
                                aria-hidden="true"
                                size={15}
                                strokeWidth={1.75}
                              />
                              Excluir categoria
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  </header>

                  {!category.collapsed && (
                    <div className="pb-6 pl-8">
                      {category.items.length > 0 ? (
                        <div>
                          <div className="grid grid-cols-[6rem_minmax(0,1fr)_5rem_8rem_9rem_3rem] items-center gap-4 border-y bg-muted/30 px-4 py-3 text-[10px] font-semibold tracking-[0.1em] text-muted-foreground uppercase">
                            <span>Código</span>
                            <span>Descrição</span>
                            <span>Un.</span>
                            <span className="text-right">Quantidade</span>
                            <span className="text-right">Total</span>
                            <span />
                          </div>

                          {category.items.map((item) => {
                            const itemTotal =
                              item.quantity * item.composition.unitPrice

                            return (
                              <div
                                key={item.id}
                                className="grid grid-cols-[6rem_minmax(0,1fr)_5rem_8rem_9rem_3rem] items-center gap-4 border-b px-4 py-4"
                              >
                                <button
                                type="button"
                                onClick={() => setSelectedComposition(item.composition)}
                                className="cursor-pointer text-left text-xs font-semibold text-primary underline-offset-4 transition-colors hover:text-primary/75 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
                                aria-label={`Ver detalhes da composição ${item.composition.code}`}
                                >
                                {item.composition.code}
                                </button>

                                <button
                                type="button"
                                onClick={() => setSelectedComposition(item.composition)}
                                className="min-w-0 cursor-pointer text-left focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
                                >
                                <p className="text-sm leading-5 transition-colors hover:text-primary">
                                    {item.composition.description}
                                </p>

                                <p className="mt-1 text-xs tabular-nums text-muted-foreground">
                                    {brazilianCurrency.format(item.composition.unitPrice)} /{' '}
                                    {item.composition.unit}
                                </p>
                                </button>

                                <span className="text-xs text-muted-foreground">
                                  {item.composition.unit}
                                </span>

                                <input
                                  type="number"
                                  min="0"
                                  step="any"
                                  value={item.quantity}
                                  onChange={(event) =>
                                    updateQuantity(
                                      category.id,
                                      item.id,
                                      Number(event.target.value),
                                    )
                                  }
                                  aria-label={`Quantidade de ${item.composition.description}`}
                                  className="h-9 w-full rounded-sm border bg-background px-2 text-right text-sm tabular-nums outline-none focus:border-ring focus:ring-2 focus:ring-ring/20"
                                />

                                <span className="text-right text-sm font-semibold tabular-nums">
                                  {brazilianCurrency.format(itemTotal)}
                                </span>

                                <button
                                  type="button"
                                  aria-label={`Remover ${item.composition.description}`}
                                  onClick={() =>
                                    removeItem(category.id, item.id)
                                  }
                                  className="flex size-9 items-center justify-center rounded-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                                >
                                  <Trash2
                                    aria-hidden="true"
                                    size={16}
                                    strokeWidth={1.75}
                                  />
                                </button>
                              </div>
                            )
                          })}
                        </div>
                      ) : (
                        <div className="border-y py-8 text-center">
                          <p className="text-sm font-medium">
                            Nenhuma composição nesta categoria.
                          </p>

                          <p className="mt-2 text-sm text-muted-foreground">
                            Adicione uma composição para começar a quantificar.
                          </p>
                        </div>
                      )}

                      <Button
                        variant="ghost"
                        className="mt-4"
                        onClick={() => setActiveCategoryId(category.id)}
                      >
                        <Plus
                          aria-hidden="true"
                          size={16}
                          strokeWidth={1.75}
                        />
                        Adicionar composição
                      </Button>
                    </div>
                  )}
                </article>
              )
            })}
          </div>

          {categories.length === 0 && (
            <div className="flex min-h-72 flex-col items-center justify-center border-b text-center">
              <FolderPlus
                aria-hidden="true"
                size={25}
                strokeWidth={1.5}
                className="text-muted-foreground"
              />

              <h2 className="mt-5 text-base font-semibold">
                Seu orçamento ainda não possui categorias.
              </h2>

              <p className="mt-2 max-w-md text-sm leading-6 text-muted-foreground">
                Crie uma categoria para organizar e adicionar suas composições.
              </p>

              <Button
                className="mt-6"
                onClick={() => setIsCreatingCategory(true)}
              >
                <Plus aria-hidden="true" size={16} strokeWidth={1.75} />
                Criar primeira categoria
              </Button>
            </div>
          )}
        </section>
      </main>

      {activeCategory && (
        <AddCompositionDialog
          open={Boolean(activeCategoryId)}
          categoryName={activeCategory.name}
          existingCodes={activeCategory.items.map(
            (item) => item.composition.code,
          )}
          compositions={availableCompositions}
          onClose={() => setActiveCategoryId(null)}
          onAdd={addComposition}
          
        />
      )}
      <CompositionDetailsDrawer
        composition={selectedComposition}
        state="MG"
        competence="Agosto de 2025"
        onClose={() => setSelectedComposition(null)}
        />
    </>
  )
}

function getCategorySubtotal(category: EstimateCategory) {
  return category.items.reduce((subtotal, item) => {
    return subtotal + item.quantity * item.composition.unitPrice
  }, 0)
}

function getEstimateName(estimateId?: string) {
  const names: Record<string, string> = {
    'residencial-horizonte': 'Residencial Horizonte',
    'infraestrutura-alameda': 'Infraestrutura Alameda',
    'loteamento-vale-verde': 'Loteamento Vale Verde',
    'sistema-viario-norte': 'Sistema Viário Norte',
  }

  return estimateId ? names[estimateId] ?? 'Novo orçamento' : 'Novo orçamento'
}

export { EstimateEditorPage }