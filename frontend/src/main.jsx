import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import './index.css'
import App from './App.jsx'

// QueryClient: El núcleo del sistema de caché de TanStack Query.
// staleTime: cuánto tiempo (ms) considera los datos "frescos" antes de refetch.
// retry: cuántos reintentos hace si un request falla.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 30, // 30 segundos en caché antes de considerarlos obsoletos
      retry: 2,             // Reintenta 2 veces en caso de error de red
    },
  },
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      {/* DevTools: Panel visual de caché — solo visible en desarrollo */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </StrictMode>,
)
