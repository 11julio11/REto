import axios from 'axios'

// Instancia base de Axios que apunta a nuestro backend de FastAPI
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor REQUEST: añade automáticamente el JWT de localStorage a cada request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Interceptor RESPONSE: manejo global de errores ────────────────────────
// Este interceptor es el corazón del Día 13.
// En lugar de manejar errores en cada componente, los centralizamos aquí.
// onGlobalError es una función que se registra desde el App para disparar Toasts.
let onGlobalError = null

export function setGlobalErrorHandler(handler) {
  onGlobalError = handler
}

apiClient.interceptors.response.use(
  // Respuesta exitosa: pasarla sin tocar
  (response) => response,
  // Error: clasificarlo y emitir un Toast coherente
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail

    // Ignoramos errores de auth en rutas de login/register
    // para que esos componentes los manejen localmente
    const url = error.config?.url || ''
    const isAuthRoute = url.includes('/auth/login') || url.includes('/auth/register')

    if (!isAuthRoute && onGlobalError) {
      if (!error.response) {
        // Sin respuesta del servidor (red caída, backend apagado)
        onGlobalError('❌ No se puede conectar al servidor. ¿El backend está corriendo?', 'error')
      } else if (status === 401) {
        onGlobalError('🔒 Sesión expirada. Por favor inicia sesión de nuevo.', 'warning')
        localStorage.removeItem('access_token')
        window.location.reload()
      } else if (status === 403) {
        onGlobalError('⛔ No tienes permisos para esta acción.', 'warning')
      } else if (status === 404) {
        onGlobalError(`🔍 Recurso no encontrado: ${detail || ''}`, 'info')
      } else if (status === 422) {
        onGlobalError('📝 Datos inválidos en la solicitud.', 'warning')
      } else if (status >= 500) {
        onGlobalError(`💥 Error interno del servidor (${status}). Intenta de nuevo.`, 'error')
      } else {
        onGlobalError(detail || `Error inesperado (${status})`, 'error')
      }
    }

    // Re-lanzamos el error para que los componentes lo intercepten si necesitan
    return Promise.reject(error)
  }
)

// ── Funciones de petición ──────────────────────────────────────────────────

export const loginUser = async ({ username, password }) => {
  const form = new URLSearchParams()
  form.append('username', username)
  form.append('password', password)
  const { data } = await apiClient.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data
}

export const registerUser = async ({ username, password }) => {
  const { data } = await apiClient.post('/auth/register', { username, password })
  return data
}

export const fetchItems = async () => {
  const { data } = await apiClient.get('/items')
  return data
}

export const createItem = async (item) => {
  const { data } = await apiClient.post('/items', item)
  return data
}

export const deleteItem = async (itemId) => {
  await apiClient.delete(`/items/${itemId}`)
}

export default apiClient
