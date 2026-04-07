# Día 12: React + TanStack Query (Data Fetching Profesional)

Cuando la mayoría de los desarrolladores necesitan cargar datos externos en React, el primer instinto es usar `useEffect` junto a `useState`. Ese patrón funciona, pero escala mal: hay que manejar a mano el estado de carga, errores, caché, reintentos y sincronización. **TanStack Query** (antes React Query) resuelve todo eso de forma declarativa.

## El Problema con `useEffect` para Fetching

```jsx
// ❌ Patrón frágil y verbose con useEffect
function ItemsList() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/items')
      .then(r => r.json())
      .then(data => { setItems(data); setLoading(false) })
      .catch(e => { setError(e); setLoading(false) })
  }, [])

  // Problemas: sin caché, sin reintentos, refetch manual, race conditions...
}
```

## La Solución: `useQuery`

```jsx
// ✅ Patrón declarativo con TanStack Query
import { useQuery } from '@tanstack/react-query'

function ItemsList() {
  const { data: items, isLoading, isError } = useQuery({
    queryKey: ['items'],    // Clave única de caché
    queryFn: fetchItems,    // La función que hace el fetch
    staleTime: 30_000,      // 30 seg de caché antes de refetch
  })
  // Aquí isLoading, isError y data son automáticos. Cero useState.
}
```

## Conceptos Clave

### `queryKey`
La clave de caché. Si dos componentes usan `queryKey: ['items']`, **comparten el mismo caché** sin hacer dos peticiones al servidor. También se puede usar con parámetros:
```js
queryKey: ['items', { status: 'active' }]
```

### `staleTime`
Tiempo en ms que los datos se consideran "frescos". Solo cuando expira, TanStack Query hace un refetch en segundo plano, sin bloquear la UI con el caché existente.

### `useMutation`
Para operaciones escritura. Su poder: el callback `onSuccess` permite invalidar queryKeys específicos forzando un refetch automático, manteniendo la UI sincronizada.

```js
const mutation = useMutation({
  mutationFn: createItem,
  onSuccess: () => {
    // Invalida el caché de 'items' → TanStack Query refetch automático
    queryClient.invalidateQueries({ queryKey: ['items'] })
  }
})
```

### Interceptor JWT en Axios
Configuramos un interceptor de solicitud en Axios que inserta el `Bearer token` en cada petición automáticamente, sin repetir el header en cada función de fetch.

## Estructura del Frontend

```
frontend/
├── src/
│   ├── services/
│   │   └── api.js          # Axios + interceptor JWT + funciones de fetch
│   ├── components/
│   │   ├── Login.jsx        # Formulario de login/registro
│   │   └── ItemsList.jsx    # useQuery + useMutation en acción
│   ├── App.jsx              # Orquesta Login ↔ ItemsList por estado de sesión
│   └── main.jsx             # QueryClientProvider + ReactQueryDevtools
```

## Cómo Ejecutar

1. Backend (en una terminal):
```bash
uvicorn main:app --reload
```

2. Frontend (en otra terminal):
```bash
cd frontend
npm run dev
```

3. Abre `http://localhost:5173` → Regístrate → Inicia sesión → ¡Crea y elimina Items!

> **ReactQueryDevtools**: En desarrollo verás un ícono flotante de TanStack en la esquina de la pantalla. Desde ahí puedes inspeccionar el estado del caché, ver qué queries están activas y forzar refetches manualmente.
