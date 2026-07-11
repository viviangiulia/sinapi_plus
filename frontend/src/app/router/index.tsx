import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '@/app/layouts/app-layout'
import { FoundationPage } from '@/pages/foundation-page'
import { HomePage } from '@/pages/home-page'
import { LoginPage } from '@/pages/login-page'
import { EstimatesPage } from '@/pages/estimates-page'
import { EstimateEditorPage } from '@/pages/estimate-editor-page'

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'orcamentos', element: <EstimatesPage /> },
      { path: 'orcamentos/:estimateId', element: <EstimateEditorPage /> },
      { path: 'base-precos', element: <FoundationPage /> },
      { path: 'configuracoes', element: <FoundationPage /> },
    ],
  },
])

export { router }