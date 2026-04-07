import axios from 'axios'

// Instancia base de Axios que apunta a nuestro backend de FastAPI
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor: añade automáticamente el JWT de localStorage a cada request
// Gracias a esto, no tenemos que pasar el token manualmente en cada llamada
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

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
